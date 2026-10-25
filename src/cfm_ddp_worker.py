
#!/usr/bin/env python3
"""Single-node PyTorch DDP conditional flow matching trainer.
Source generated from the master notebook. Dataset must be independently audited.
"""
import argparse, csv, hashlib, json, os, random, sys, time, zipfile
from datetime import datetime, timezone
from pathlib import Path
from contextlib import nullcontext
import numpy as np
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, TensorDataset, DistributedSampler

def utc(): return datetime.now(timezone.utc).isoformat()
def digest_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
def atomic_write_json(p, data):
    t=p.with_suffix(p.suffix+'.tmp')
    t.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    os.replace(t,p)
def archive_all(state, archive):
    if archive is None: return
    archive.parent.mkdir(parents=True,exist_ok=True)
    tmp=archive.with_suffix(archive.suffix+'.tmp')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
        for f in sorted(state.rglob('*')):
            if f.is_file(): z.write(f,arcname=(Path('BUILDING_CFM_STATE')/f.relative_to(state)).as_posix())
    os.replace(tmp,archive)
def record_training(state,archive,run,epoch,ckpt,history_path,archive_this):
    manifest_path=state/'manifest.json'
    if manifest_path.exists(): m=json.loads(manifest_path.read_text())
    else: m={'format':'BUILDING_CFM_STATE_V1','created_at':utc(),'record':'13622940','stages':{}}
    m.setdefault('stages',{})['training_'+run]={
        'fingerprint':'standard-cfm-ddp-v1-epoch-'+str(epoch),
        'completed_at':utc(),
        'outputs':{str(f.relative_to(state)):digest_file(f) for f in (ckpt,history_path)},
        'details':{'last_completed_epoch':epoch,'training_backend':'torchrun-DDP'},
    }
    m['updated_at']=utc()
    atomic_write_json(manifest_path,m)
    if archive_this: archive_all(state,archive)
class VelocityNet(nn.Module):
    def __init__(self, x_dim, y_dim, hidden=256):
        super().__init__()
        self.layers=nn.Sequential(nn.Linear(x_dim+y_dim+1,hidden),nn.SiLU(),
            nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),
            nn.Linear(hidden,y_dim))
    def forward(self,features,z_t,t):
        return self.layers(torch.cat((features,z_t,t),dim=1))
def rng_capture():
    return {'python':random.getstate(),'numpy':np.random.get_state(),
            'torch':torch.get_rng_state(),
            'cuda':torch.cuda.get_rng_state() if torch.cuda.is_available() else None}
def rng_restore(o):
    random.setstate(o['python']); np.random.set_state(o['numpy']); torch.set_rng_state(o['torch'])
    if torch.cuda.is_available() and o.get('cuda') is not None: torch.cuda.set_rng_state(o['cuda'])
def load_data(path):
    with np.load(path, allow_pickle=False) as d:
        req=['x_train','y_train','x_val','y_val']
        if not all(k in d for k in req): raise ValueError('NPZ must have '+', '.join(req))
        a=[np.asarray(d[k],dtype=np.float32) for k in req]
    x,y,xv,yv=a
    for v in a:
        if v.ndim==1: v.shape=(v.shape[0],1)
        if v.ndim!=2 or len(v)==0 or not np.isfinite(v).all():
            raise ValueError('All NPZ arrays must be finite, nonempty, 2D numerical arrays')
    if len(x)!=len(y) or len(xv)!=len(yv): raise ValueError('X/Y size mismatch')
    if x.shape[1]!=xv.shape[1] or y.shape[1]!=yv.shape[1]: raise ValueError('Train/validation dimensions do not match')
    return x,y,xv,yv

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--npz',type=Path)
    ap.add_argument('--state-root',type=Path,required=True)
    ap.add_argument('--archive',type=Path)
    ap.add_argument('--run-name',default='standard_cfm_ddp')
    ap.add_argument('--epochs',type=int,default=80)
    ap.add_argument('--batch-size',type=int,default=256,help='BATCH SIZE PER GPU/process')
    ap.add_argument('--hidden',type=int,default=256)
    ap.add_argument('--lr',type=float,default=0.001)
    ap.add_argument('--workers',type=int,default=0)
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--archive-every',type=int,default=1)
    ap.add_argument('--smoke-test',action='store_true')
    args=ap.parse_args()
    if args.epochs<1 or args.batch_size<1 or args.archive_every<1: raise ValueError('epoch, batch-size and archive-every must be >=1')
    world=int(os.environ.get('WORLD_SIZE','1'))
    rank=int(os.environ.get('RANK','0'))
    local_rank=int(os.environ.get('LOCAL_RANK','0'))
    gpu=torch.cuda.is_available()
    device=torch.device('cuda',local_rank) if gpu else torch.device('cpu')
    if gpu: torch.cuda.set_device(local_rank)
    if world>1: dist.init_process_group('nccl' if gpu else 'gloo')
    torch.set_num_threads(1 if world>1 else min(4,max(1,os.cpu_count() or 1)))
    random.seed(args.seed+rank); np.random.seed(args.seed+rank); torch.manual_seed(args.seed+rank)
    if gpu: torch.cuda.manual_seed(args.seed+rank)
    if args.smoke_test:
        # NO research output, NO checkpoint: verifies distinct processes/devices can train together.
        x=np.random.default_rng(0).normal(size=(512,8)).astype('float32')
        y=np.random.default_rng(1).normal(size=(512,2)).astype('float32')
        xv=x[:64].copy(); yv=y[:64].copy()
        epochs=2
        batch_size=64
        run='__smoke_not_saved__'
    else:
        if args.npz is None or not args.npz.is_file(): raise FileNotFoundError('Validated Phase-2 train/validation .npz is required')
        x,y,xv,yv=load_data(args.npz)
        epochs=args.epochs; batch_size=args.batch_size; run=args.run_name
        if not run.replace('_','').replace('-','').isalnum(): raise ValueError('Use a simple alphanumeric run-name')
    train_ds=TensorDataset(torch.from_numpy(x),torch.from_numpy(y))
    sampler=DistributedSampler(train_ds,num_replicas=world,rank=rank,shuffle=True,seed=args.seed) if world>1 else None
    loader=DataLoader(train_ds,batch_size=batch_size,sampler=sampler,shuffle=sampler is None,
                      num_workers=args.workers,pin_memory=gpu,drop_last=False)
    net=VelocityNet(x.shape[1],y.shape[1],args.hidden).to(device)
    ddp=DDP(net,device_ids=[local_rank]) if world>1 and gpu else (DDP(net) if world>1 else net)
    optimizer=torch.optim.AdamW(ddp.parameters(),lr=args.lr)
    use_amp=gpu
    scaler=torch.amp.GradScaler('cuda',enabled=use_amp)
    state=args.state_root
    ckpt=state/'model_checkpoints'/f'{run}_latest.pt'
    hist=state/'outputs'/f'{run}_history.csv'
    start_epoch=0; history=[]; best_val=float('inf')
    if not args.smoke_test:
        ckpt.parent.mkdir(parents=True,exist_ok=True);hist.parent.mkdir(parents=True,exist_ok=True)
        if ckpt.exists():
            saved=torch.load(ckpt,map_location='cpu',weights_only=False) # trusted self-created training state only
            expected={'x_dim':x.shape[1],'y_dim':y.shape[1],'hidden':args.hidden,
                      'world_size':world,'batch_size':batch_size,
                      'npz_hash':digest_file(args.npz),'seed':args.seed,'lr':args.lr}
            if saved['config'] != expected: raise ValueError('Resume configuration/data/world-size differ; choose a new run-name or original config')
            net.load_state_dict(saved['model'])
            optimizer.load_state_dict(saved['optimizer'])
            scaler.load_state_dict(saved['scaler'])
            history=saved['history'];best_val=saved['best_val']; start_epoch=saved['epoch']+1
            rng_restore(saved['rng_by_rank'][rank])
            if rank==0: print(f'RESUME {run}: last completed epoch {start_epoch-1}, next {start_epoch}; world size={world}',flush=True)
    if rank==0:
        print(f'Device={device}, ranks={world}, train={len(x)}, val={len(xv)}, input={x.shape[1]}, outputs={y.shape[1]}, batch/GPU={batch_size}, fp16={use_amp}',flush=True)
    t_start=time.perf_counter()
    try:
        for epoch in range(start_epoch,epochs):
            if sampler is not None: sampler.set_epoch(epoch)
            ddp.train()
            epoch_loss=0.0; count=0
            for bx,by in loader:
                bx=bx.to(device,non_blocking=True); by=by.to(device,non_blocking=True)
                t=torch.rand((by.shape[0],1),device=device)
                z0=torch.randn_like(by)
                zt=(1-t)*z0+t*by
                target=by-z0
                optimizer.zero_grad(set_to_none=True)
                with torch.autocast('cuda',dtype=torch.float16) if use_amp else nullcontext():
                    pred=ddp(bx,zt,t)
                    loss=((pred-target)**2).mean()
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(ddp.parameters(),max_norm=1.)
                scaler.step(optimizer);scaler.update()
                epoch_loss+=float(loss.detach())*by.shape[0];count+=by.shape[0]
            losses=torch.tensor([epoch_loss,count],device=device,dtype=torch.float64)
            if world>1:dist.all_reduce(losses,op=dist.ReduceOp.SUM)
            tr_loss=float(losses[0]/losses[1])
            val_loss=0.0
            if rank==0:
                net.eval()
                with torch.no_grad():
                    vx=torch.from_numpy(xv).to(device)
                    vy=torch.from_numpy(yv).to(device)
                    # Fixed draw per epoch; validation does not touch training RNG state.
                    g=torch.Generator(device=device).manual_seed(123456)
                    error,count_v=0.,0
                    for offset in range(0,len(vx),batch_size):
                        bx=vx[offset:offset+batch_size];by=vy[offset:offset+batch_size]
                        t=torch.rand((len(by),1),device=device,generator=g)
                        z0=torch.randn(by.shape,device=device,generator=g)
                        zt=(1-t)*z0+t*by
                        with torch.autocast('cuda',dtype=torch.float16) if use_amp else nullcontext():
                            pred=net(bx,zt,t)
                            diff=(pred-(by-z0))**2
                        error+=float(diff.float().sum());count_v+=diff.numel()
                    val_loss=error/max(1,count_v)
                history.append({'epoch':epoch,'train_loss':tr_loss,'val_loss':val_loss})
                best_val=min(best_val,val_loss)
            # Record independent RNG states for both GPU workers for strict epoch-boundary resume.
            state_here=rng_capture()
            all_rng=[None]*world
            if world>1: dist.all_gather_object(all_rng,state_here)
            else: all_rng=[state_here]
            if rank==0:
                print(f'Epoch {epoch+1}/{epochs} | train={tr_loss:.6f} | val={val_loss:.6f} | elapsed={time.perf_counter()-t_start:.1f}s',flush=True)
                if not args.smoke_test:
                    config={'x_dim':x.shape[1],'y_dim':y.shape[1],'hidden':args.hidden,
                            'world_size':world,'batch_size':batch_size,
                            'npz_hash':digest_file(args.npz),'seed':args.seed,'lr':args.lr}
                    payload={'epoch':epoch,'model':net.state_dict(),'optimizer':optimizer.state_dict(),
                             'scaler':scaler.state_dict(),'history':history,'best_val':best_val,
                             'config':config,'rng_by_rank':all_rng,'saved_at':utc()}
                    tmp=ckpt.with_suffix('.pt.tmp')
                    torch.save(payload,tmp);os.replace(tmp,ckpt)
                    with hist.open('w',newline='',encoding='utf-8') as f:
                        w=csv.DictWriter(f,fieldnames=['epoch','train_loss','val_loss']);w.writeheader();w.writerows(history)
                    record_training(state,args.archive,run,epoch,ckpt,hist,
                                    archive_this=((epoch+1)%args.archive_every==0 or epoch==epochs-1))
            if world>1:dist.barrier()
    finally:
        if world>1:dist.destroy_process_group()
    if rank==0:print('DONE | distributed training smoke test' if args.smoke_test else f'DONE | {run} complete at epoch {epochs}',flush=True)
if __name__=='__main__': main()

