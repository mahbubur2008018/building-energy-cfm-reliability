#!/usr/bin/env python3
"""Checkpointable standard conditional flow matching on validated building pEUI data.
Train with torch.distributed.run from the accompanying master notebook.
For scientific correctness: selects checkpoints on VALIDATION ONLY, NEVER test.
"""
import os, sys, csv, json, time, random, hashlib, zipfile, argparse
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import torch
from torch import nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, TensorDataset, DistributedSampler

def now(): return datetime.now(timezone.utc).isoformat()
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for p in iter(lambda:f.read(1048576),b''): h.update(p)
    return h.hexdigest()
def write_json_atomic(path,obj):
    path=Path(path); tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8')
    os.replace(tmp,path)
def archive_state(root,path):
    if path is None: return
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
        for f in sorted(root.rglob('*')):
            if f.is_file():z.write(f,(Path('BUILDING_CFM_STATE')/f.relative_to(root)).as_posix())
    os.replace(tmp,path)
def record_epoch(root,archive,fp,last,best,history,epoch,best_epoch,archive_now,details):
    mf=root/'manifest.json'
    m=json.loads(mf.read_text(encoding='utf-8'))
    outputs={}
    for p in (last,best,history):
        if p.exists():outputs[p.relative_to(root).as_posix()]=digest(p)
    m.setdefault('stages',{})['phase4_standard_cfm_training']={
        'fingerprint':fp,'completed_at':now(),'outputs':outputs,
        'details':dict(details,last_completed_epoch=epoch,best_epoch=best_epoch)
    }
    m['updated_at']=now()
    write_json_atomic(mf,m)
    if archive_now:archive_state(root,archive)

class VelocityNet(nn.Module):
    def __init__(self,xdim,hidden):
        super().__init__()
        self.layers=nn.Sequential(nn.Linear(xdim+2,hidden),nn.SiLU(),
            nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,1))
    def forward(self,x,z,t):
        return self.layers(torch.cat((x,z,t),dim=1))

def rng_save():
    return dict(py=random.getstate(),np=np.random.get_state(),torch=torch.get_rng_state(),
                cuda=torch.cuda.get_rng_state() if torch.cuda.is_available() else None)
def rng_load(s):
    random.setstate(s['py']);np.random.set_state(s['np']);torch.set_rng_state(s['torch'])
    if s['cuda'] is not None and torch.cuda.is_available():torch.cuda.set_rng_state(s['cuda'])

def inverse_y(z,mean,sd):
    z=np.clip(np.asarray(z,dtype=np.float64),-4.,4.)
    return np.maximum(np.expm1(z*sd+mean),0.)

@torch.no_grad()
def sample_conditional(model,x,device,draws,steps,seed,batch=128):
    """Euler integration of straight-line CFM ODE; returns [n, draws] scaled y samples."""
    model.eval(); n=len(x); answer=np.empty((n,draws),dtype=np.float32)
    gen=torch.Generator(device=device).manual_seed(seed)
    for start in range(0,n,batch):
        xb=torch.from_numpy(x[start:start+batch]).to(device)
        b=len(xb); xf=xb.repeat_interleave(draws,dim=0)
        z=torch.randn((b*draws,1),device=device,generator=gen)
        for i in range(steps):
            t=torch.full_like(z,(i+.5)/steps)
            z=z+model(xf,z,t)/steps
        answer[start:start+b]=z.reshape(b,draws).cpu().numpy()
    return answer

def evaluate(model,x,y_raw,device,mean,sd,draws,steps,seed):
    samples_z=sample_conditional(model,x,device,draws,steps,seed)
    ys=inverse_y(samples_z,mean,sd)
    y_true=np.asarray(y_raw,dtype=np.float64).reshape(-1)
    pred=ys.mean(axis=1)
    rmse=float(np.sqrt(np.mean((pred-y_true)**2)))
    mae=float(np.mean(np.abs(pred-y_true)))
    lo,hi=np.quantile(ys,[.05,.95],axis=1)
    coverage=float(np.mean((y_true>=lo)&(y_true<=hi)))
    width=float(np.mean(hi-lo))
    # Ensemble empirical CRPS. The 2nd term is the mean pairwise sample distance.
    # O(M^2), so validation uses a controlled modest sample count.
    crps=np.mean(np.abs(ys-y_true[:,None]),axis=1)-.5*np.mean(np.abs(ys[:,:,None]-ys[:,None,:]),axis=(1,2))
    return dict(rmse=rmse,mae=mae,crps=float(np.mean(crps)),coverage90=coverage,
                width90=width,draws=draws,ode_steps=steps)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--npz',required=True,type=Path)
    p.add_argument('--state-root',required=True,type=Path)
    p.add_argument('--archive',type=Path)
    p.add_argument('--epochs',type=int,default=80)
    p.add_argument('--batch-per-gpu',type=int,default=256)
    p.add_argument('--hidden',type=int,default=128)
    p.add_argument('--lr',type=float,default=.001)
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--validation-every',type=int,default=5)
    p.add_argument('--val-draws',type=int,default=32)
    p.add_argument('--ode-steps',type=int,default=32)
    p.add_argument('--archive-every',type=int,default=1)
    p.add_argument('--target-mean',required=True,type=float)
    p.add_argument('--target-std',required=True,type=float)
    a=p.parse_args()
    for v in (a.epochs,a.batch_per_gpu,a.hidden,a.validation_every,a.val_draws,a.ode_steps,a.archive_every):
        if v<=0:raise ValueError('All positive-integer training parameters must be positive')
    world=int(os.environ.get('WORLD_SIZE','1'))
    rank=int(os.environ.get('RANK','0'))
    local=int(os.environ.get('LOCAL_RANK','0'))
    gpu=torch.cuda.is_available()
    if gpu:torch.cuda.set_device(local)
    device=torch.device('cuda',local) if gpu else torch.device('cpu')
    if world>1:dist.init_process_group('nccl' if gpu else 'gloo')
    torch.set_num_threads(1 if world>1 else min(4,os.cpu_count() or 1))
    random.seed(a.seed+rank);np.random.seed(a.seed+rank);torch.manual_seed(a.seed+rank)
    if gpu:torch.cuda.manual_seed_all(a.seed+rank)
    with np.load(a.npz,allow_pickle=False) as dat:
        x=np.asarray(dat['x_train'],dtype=np.float32)
        y=np.asarray(dat['y_train'],dtype=np.float32).reshape(-1,1)
        xv=np.asarray(dat['x_val'],dtype=np.float32)
        yv=np.asarray(dat['raw_y_val'],dtype=np.float64)
    assert x.ndim==2 and y.shape==(len(x),1) and len(xv)==len(yv) and xv.shape[1]==x.shape[1]
    assert all(np.isfinite(d).all() for d in (x,y,xv,yv))
    assert len(x)>20 and len(xv)>5 and a.target_std>0
    root=a.state_root
    d=root/'model_checkpoints'/'phase4_standard_cfm';d.mkdir(parents=True,exist_ok=True)
    out=root/'outputs'/'phase4_standard_cfm';out.mkdir(parents=True,exist_ok=True)
    latest=d/'latest.pt';best=d/'best.pt';hist=out/'training_history.csv'
    config=dict(npz_sha256=digest(a.npz),train_rows=len(x),val_rows=len(xv),
                input_dim=x.shape[1],world_size=world,batch_per_gpu=a.batch_per_gpu,hidden=a.hidden,
                learning_rate=a.lr,seed=a.seed,validation_every=a.validation_every,
                val_draws=a.val_draws,ode_steps=a.ode_steps,
                target_mean=a.target_mean,target_std=a.target_std,
                worker_version='standard-cfm-ddp-pEUI-v2')
    fp=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    sampler=DistributedSampler(TensorDataset(torch.from_numpy(x),torch.from_numpy(y)),
               num_replicas=world,rank=rank,shuffle=True,seed=a.seed) if world>1 else None
    data=TensorDataset(torch.from_numpy(x),torch.from_numpy(y))
    loader=DataLoader(data,batch_size=a.batch_per_gpu,sampler=sampler,
                     shuffle=(sampler is None),num_workers=0,pin_memory=gpu)
    net=VelocityNet(x.shape[1],a.hidden).to(device)
    wrapped=DDP(net,device_ids=[local]) if world>1 and gpu else (DDP(net) if world>1 else net)
    opt=torch.optim.AdamW(wrapped.parameters(),lr=a.lr,weight_decay=1e-5)
    scaler=torch.amp.GradScaler('cuda',enabled=gpu)
    epoch0=0;history=[]; best_rmse=float('inf');best_epoch=-1
    if latest.exists():
        ck=torch.load(latest,map_location='cpu',weights_only=False) # OWN generated checkpoint only
        if ck['config']!=config:raise RuntimeError('Resume config/data mismatch; change run name or restore original settings')
        epoch0=int(ck['epoch'])+1
        net.load_state_dict(ck['model']); opt.load_state_dict(ck['optimizer']);scaler.load_state_dict(ck['scaler'])
        history=ck['history'];best_rmse=float(ck['best_rmse']);best_epoch=int(ck['best_epoch'])
        rng_load(ck['rng_by_rank'][rank])
        if rank==0:print('RESUME CFM from finished epoch',epoch0,'of',a.epochs,flush=True)
    if rank==0:
        print('CFM source: TOTAL SITE ENERGY pEUI, kWh/year; NOT heating-only.',flush=True)
        print('DDP ranks',world,'CUDA',gpu,'Train',len(x),'Validation',len(xv), 'Features',x.shape[1],flush=True)
        print('Selection is exclusively on validation RMSE; no test set loaded.',flush=True)
    t0=time.perf_counter()
    try:
        for epoch in range(epoch0,a.epochs):
            if sampler:sampler.set_epoch(epoch)
            wrapped.train();sum_loss=0.;count=0
            for xb,yb in loader:
                xb=xb.to(device,non_blocking=True);yb=yb.to(device,non_blocking=True)
                t=torch.rand((len(xb),1),device=device)
                noise=torch.randn_like(yb)
                z=(1-t)*noise+t*yb
                target=yb-noise
                opt.zero_grad(set_to_none=True)
                with torch.autocast(device_type='cuda',dtype=torch.float16,enabled=gpu):
                    loss=(wrapped(xb,z,t)-target).square().mean()
                scaler.scale(loss).backward()
                scaler.unscale_(opt);torch.nn.utils.clip_grad_norm_(wrapped.parameters(),1.)
                scaler.step(opt);scaler.update()
                sum_loss+=float(loss.detach())*len(xb);count+=len(xb)
            stats=torch.tensor([sum_loss,count],dtype=torch.float64,device=device)
            if world>1:dist.all_reduce(stats,op=dist.ReduceOp.SUM)
            train_loss=float((stats[0]/stats[1]).item())
            metrics=None
            if rank==0:
                needs_eval=(epoch==0 or (epoch+1)%a.validation_every==0 or epoch+1==a.epochs)
                if needs_eval:
                    metrics=evaluate(net,xv,yv,device,a.target_mean,a.target_std,
                              a.val_draws,a.ode_steps,seed=314159)
                    if not np.isfinite(metrics['rmse']):raise RuntimeError('Nonfinite validation metrics')
                    if metrics['rmse']<best_rmse:
                        best_rmse=metrics['rmse'];best_epoch=epoch
                        payload=dict(model=net.state_dict(),config=config,epoch=epoch,
                                     metrics=metrics,saved_at=now())
                        tmp=best.with_suffix('.pt.tmp');torch.save(payload,tmp);os.replace(tmp,best)
                history.append(dict(epoch=epoch+1,train_loss=train_loss,
                                    **({k:v for k,v in metrics.items()} if metrics else {})))
            state=rng_save()
            rank_rng=[None]*world
            if world>1:dist.all_gather_object(rank_rng,state)
            else:rank_rng=[state]
            if rank==0:
                ck=dict(config=config,epoch=epoch,model=net.state_dict(),optimizer=opt.state_dict(),
                        scaler=scaler.state_dict(),history=history,best_rmse=best_rmse,
                        best_epoch=best_epoch,rng_by_rank=rank_rng,saved_at=now())
                tmp=latest.with_suffix('.pt.tmp');torch.save(ck,tmp);os.replace(tmp,latest)
                with hist.open('w',encoding='utf-8',newline='') as f:
                    keys=['epoch','train_loss','rmse','mae','crps','coverage90','width90','draws','ode_steps']
                    writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(history)
                record_epoch(root,a.archive,fp,latest,best,hist,epoch,best_epoch,
                             archive_now=((epoch+1)%a.archive_every==0 or epoch+1==a.epochs),
                             details={'target':'pEUI kWh/year','world_size':world,'best_validation_rmse':best_rmse,
                                      'target_epochs':a.epochs,'train_rows':len(x),'val_rows':len(xv)})
                if needs_eval or (epoch+1)%10==0:
                    print(f'CFM epoch {epoch+1}/{a.epochs}: flow loss={train_loss:.5f} '
                          + (f'val_RMSE={metrics["rmse"]:.2f}, val_CRPS={metrics["crps"]:.2f}, coverage90={metrics["coverage90"]:.3f}' if metrics else '')
                          +f' | best_RMSE={best_rmse:.2f} | elapsed={time.perf_counter()-t0:.1f}s',flush=True)
            if world>1:dist.barrier()
    finally:
        if world>1:dist.destroy_process_group()
    if rank==0:print(f'CFM TRAINING COMPLETE: best validation RMSE={best_rmse:.3f} at epoch {best_epoch+1}; last epoch={max(epoch0,a.epochs)}',flush=True)

if __name__=='__main__':main()
