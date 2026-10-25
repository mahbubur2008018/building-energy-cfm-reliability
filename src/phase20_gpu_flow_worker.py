#!/usr/bin/env python3
import os,sys,json,time,random,hashlib
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
torch.set_num_threads(2)
from scipy.special import logsumexp
kind=sys.argv[1]; infile=Path(sys.argv[2]);dest=Path(sys.argv[3]);conf=json.loads(Path(sys.argv[4]).read_text());dest.mkdir(parents=True,exist_ok=True)
assert kind in ('direct','residual','residual_nobase')
smoke=os.environ.get('P20_LOCAL_SMOKE','0')=='1'
if not smoke:assert torch.cuda.is_available() and torch.cuda.device_count()==1,'Worker must see exactly one assigned physical GPU'
device=torch.device('cpu' if smoke else 'cuda:0')
seeds=conf['flow_seeds'] if len(sys.argv)<6 else [int(z) for z in sys.argv[5].split(',')]
assert seeds and set(seeds).issubset(set(conf['flow_seeds']))
epochs=conf['flow_epochs'];batch=conf['flow_batch']
with np.load(infile,allow_pickle=False) as d:
    xt=d['x_train'].astype('float32');zt=d['z_train'].astype('float32').reshape(-1,1)
    bt=d['b_train'].astype('float32').reshape(-1,1)
    xs=d['x_stop'].astype('float32');zs=d['z_stop'].astype('float32').reshape(-1,1)
    bs=d['b_stop'].astype('float32').reshape(-1,1)
    xv=d['x_validation'].astype('float32');bv=d['anchor_validation'].astype('float32').reshape(-1)
    yv=d['y_validation_kWh'].astype('float64').reshape(-1)
    gv=d['group_validation'].astype(str)
assert np.isfinite(xt).all() and np.isfinite(xv).all()
if kind in ('residual','residual_nobase'):zt=zt-bt;zs=zs-bs
class Flow(nn.Module):
    def __init__(self,dim,hidden,residual):
        super().__init__()
        d=dim+2+int(residual)
        self.net=nn.Sequential(nn.Linear(d,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,1))
    def forward(self,x,s,t,base):
        z=[x,s,t]
        if kind=='residual':z.append(base)
        return self.net(torch.cat(z,dim=1))

def t_save(path,content):
    tmp=path.with_name(path.name+'.p20writing')
    torch.save(content,tmp);os.replace(tmp,path)
def j_save(path,content):
    tmp=path.with_name(path.name+'.p20writing')
    tmp.write_text(json.dumps(content,indent=2,sort_keys=True,allow_nan=False));os.replace(tmp,path)
def n_save(path,**entries):
    tmp=path.with_name(path.name+'.p20writing')
    with open(tmp,'wb') as f:np.savez_compressed(f,**entries)
    os.replace(tmp,path)

def estimate(draws, obs):
    pred=draws.mean(axis=1);lower=np.quantile(draws,.05,axis=1);upper=np.quantile(draws,.95,axis=1)
    err=pred-obs
    crps=(np.mean(np.abs(draws-obs[:,None]),axis=1)
          -0.5*np.mean(np.abs(draws[:,:draws.shape[1]//2]-draws[:,draws.shape[1]//2:]),axis=1))
    score=(upper-lower)+(2/.10)*np.maximum(lower-obs,0)+(2/.10)*np.maximum(obs-upper,0)
    result={'RMSE_kWh':float(np.sqrt(np.mean(err**2))),'MAE_kWh':float(np.mean(np.abs(err))),
      'CRPS_kWh_paired_MC':float(np.mean(crps)),'Coverage90':float(np.mean((obs>=lower)&(obs<=upper))),
      'Width90_kWh':float(np.mean(upper-lower)),'IntervalScore90_kWh':float(np.mean(score)),
      'PredAbove1M':int(np.sum(pred>1e6)),'MaxPredKWh':float(np.max(pred))}
    sub=[]
    for site in np.unique(gv):
        m=gv==site
        covered=float(np.mean(np.logical_and(obs[m]>=lower[m],obs[m]<=upper[m])))
        sub.append({'building_id':site,'RMSE_kWh':float(np.sqrt(np.mean(err[m]**2))),
           'CRPS_kWh_paired_MC':float(np.mean(crps[m])), 'Coverage90':covered,
           'Rows':int(m.sum())})
    result['equal_building_mean_CRPS_kWh']=float(np.mean([p['CRPS_kWh_paired_MC'] for p in sub]))
    return result,sub,pred,lower,upper,crps

def sample_cfm(net,seed):
    net.eval();N=len(xv);draws=conf['flow_mc_draws'];steps=conf['flow_ode_steps']
    rng=np.random.default_rng(seed+89123)
    pieces=[];before_clip=0
    with torch.inference_mode():
        for start in range(0,N,conf['flow_eval_batch']):
            x0=xv[start:start+conf['flow_eval_batch']];b0=bv[start:start+len(x0)]
            bsz=len(x0)
            xx=torch.from_numpy(np.repeat(x0,draws,axis=0)).to(device)
            bb=torch.from_numpy(np.repeat(b0,draws).reshape(-1,1)).to(device)
            zz=torch.from_numpy(rng.standard_normal((bsz*draws,1)).astype('float32')).to(device)
            for s in range(steps):
                tt=torch.full_like(zz,float(s)/steps)
                zz=zz+net(xx,zz,tt,bb)/steps
            z=zz.detach().cpu().numpy().reshape(bsz,draws).astype('float64')
            if kind in ('residual','residual_nobase'):z=z+b0[:,None]
            logp=conf['mu']+conf['target_std']*z
            before_clip+=int(((logp<conf['physical_inverse_min_log'])|(logp>conf['physical_inverse_max_log'])).sum())
            ph=np.expm1(np.clip(logp,conf['physical_inverse_min_log'],conf['physical_inverse_max_log']))
            assert np.isfinite(ph).all()
            pieces.append(ph)
    return np.concatenate(pieces),before_clip

for seed in seeds:
    folder=dest/(kind+'_'+str(seed));folder.mkdir(exist_ok=True)
    latest=folder/'LATEST.pt';bestfile=folder/'BEST.pt';completed=folder/'EVALUATED.json';samplesfile=folder/'VALIDATION_MC_SAMPLES.npz'
    if completed.exists() and samplesfile.exists():
        rec=json.loads(completed.read_text());assert rec['data_sha256']==conf['data_sha256']
        print(kind,seed,'ALREADY COMPLETED; skip',flush=True);continue
    torch.manual_seed(seed);np.random.seed(seed);random.seed(seed)
    net=Flow(xt.shape[1],conf['flow_hidden'],kind=='residual').to(device)
    opt=torch.optim.AdamW(net.parameters(),lr=conf['flow_lr'],weight_decay=1e-4)
    best=float('inf');bad=0;start=0;history=[]
    if latest.exists():
        ck=torch.load(latest,map_location='cpu',weights_only=False)
        assert ck['data_sha256']==conf['data_sha256'] and ck['kind']==kind and ck['seed']==seed
        net.load_state_dict(ck['model']);opt.load_state_dict(ck['optimizer'])
        for state in opt.state.values():
            for k,v in state.items():
                if torch.is_tensor(v):state[k]=v.to(device)
        best=ck['best'];bad=ck['bad'];start=ck['epoch']+1;history=ck['history']
        torch.set_rng_state(ck['torch_rng'])
        if device.type=='cuda' and ck['cuda_rng'] is not None:torch.cuda.set_rng_state(ck['cuda_rng'],device=device)
        np.random.set_state(ck['numpy_rng']);random.setstate(ck['python_rng'])
    train=DataLoader(TensorDataset(torch.from_numpy(xt),torch.from_numpy(zt),torch.from_numpy(bt)),
         batch_size=batch,shuffle=True,pin_memory=(device.type=='cuda'),num_workers=0)
    # Deterministic inner-site stopping noise/t, drawn from FIT-only samples.
    sg=np.random.default_rng(seed+7300)
    ss=sg.standard_normal((len(zs),1)).astype('float32');st=sg.uniform(0,1,(len(zs),1)).astype('float32')
    def inner_loss():
        net.eval();loss_sum=0.;n=0
        with torch.inference_mode():
            for j in range(0,len(xs),batch):
                xx=torch.from_numpy(xs[j:j+batch]).to(device)
                z1=torch.from_numpy(zs[j:j+batch]).to(device)
                base=torch.from_numpy(bs[j:j+batch]).to(device)
                epsilon=torch.from_numpy(ss[j:j+batch]).to(device)
                t=torch.from_numpy(st[j:j+batch]).to(device)
                z=(1-t)*epsilon+t*z1
                pred=net(xx,z,t,base);v=z1-epsilon
                loss_sum+=float((pred-v).square().sum());n+=len(xx)
        return loss_sum/n
    for epoch in range(start,epochs):
        net.train();sse=0.;n=0
        for xx,z1,base in train:
            xx=xx.to(device,non_blocking=True);z1=z1.to(device,non_blocking=True)
            base=base.to(device,non_blocking=True)
            eps=torch.randn_like(z1);t=torch.rand_like(z1)
            z=(1-t)*eps+t*z1
            pred=net(xx,z,t,base)
            loss=(pred-(z1-eps)).square().mean()
            opt.zero_grad(set_to_none=True);loss.backward()
            nn.utils.clip_grad_norm_(net.parameters(),1.0);opt.step()
            sse+=float(loss.detach())*len(xx);n+=len(xx)
        val=inner_loss();improved=val<best-0.0001
        if improved:
            best=val;bad=0
            t_save(bestfile,{'kind':kind,'seed':seed,'epoch':epoch,
                'model':{k:v.detach().cpu() for k,v in net.state_dict().items()},
                'data_sha256':conf['data_sha256'],'inner_fit_loss':best})
        else:bad+=1
        history.append({'epoch':epoch+1,'train_flow_mse':sse/n,'fit_inner_building_mse':val})
        ck={'kind':kind,'seed':seed,'epoch':epoch,'model':{k:v.detach().cpu() for k,v in net.state_dict().items()},
            'optimizer':opt.state_dict(),'best':best,'bad':bad,'history':history,
            'data_sha256':conf['data_sha256'],'torch_rng':torch.get_rng_state(),
            'cuda_rng':torch.cuda.get_rng_state(device=device) if device.type=='cuda' else None,
            'numpy_rng':np.random.get_state(),'python_rng':random.getstate()}
        t_save(latest,ck) # EXACT optimizer + RNG resume; one checkpoint PER EPOCH.
        if (epoch+1)%10==0:print(kind,seed,'epoch',epoch+1,'FIT inner-site loss',round(val,5),flush=True)
        if bad>=conf['flow_patience'] and epoch+1>=conf['flow_min_epochs']:break
    assert bestfile.exists()
    best_checkpoint=torch.load(bestfile,map_location='cpu',weights_only=False)
    net.load_state_dict(best_checkpoint['model']);net.to(device)
    samples,clipped=sample_cfm(net,seed)
    metrics,site,pred,lo,hi,crps=estimate(samples,yv)
    n_save(samplesfile,draws_kWh=samples.astype('float32'),observed_kWh=yv.astype('float32'),
        building_id=gv,point_kWh=pred.astype('float32'),lower_kWh=lo.astype('float32'),
        upper_kWh=hi.astype('float32'),crps_per_row_kWh=crps.astype('float32'))
    j_save(folder/'PER_BUILDING_VALIDATION.json',site)
    j_save(completed,{'kind':kind,'seed':seed,'metrics':metrics,
      'fit_site_only_earlystop':True,'validation_used_for_earlystop':False,
      'total_epochs_run':len(history),'inner_best_loss':best,
      'MC_raw_logvalues_clipped_before_expm1':clipped,
      'data_sha256':conf['data_sha256'],'GPU_visible':os.environ.get('CUDA_VISIBLE_DEVICES',''),
      'model_params':sum(p.numel() for p in net.parameters()),'evaluated_at':time.time()})
    print('EVALUATED',kind,seed,metrics,flush=True)
print('WORKER FINISHED:',kind,flush=True)
