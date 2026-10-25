import os,sys,json,math
from pathlib import Path
import numpy as np
import torch
from torch import nn
from catboost import CatBoostRegressor
import joblib
kind=sys.argv[1];inputfile=Path(sys.argv[2]);outdir=Path(sys.argv[3]);checkpointdir=Path(sys.argv[4]);config=json.loads(Path(sys.argv[5]).read_text())
assert kind in ('direct','residual','residual_nobase')
assert torch.cuda.is_available() and torch.cuda.device_count()==1
# Each GPU worker owns only its assigned device; parent owns all ZIP operations.
torch.set_num_threads(2);device=torch.device('cuda:0')
class Flow(nn.Module):
 def __init__(self,dim,hidden,base_feature):
  super().__init__();d=dim+2+int(base_feature)
  self.net=nn.Sequential(nn.Linear(d,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU(),nn.Linear(hidden,1))
 def forward(self,x,s,t,base):
  parts=[x,s,t]
  if kind=='residual':parts.append(base)
  return self.net(torch.cat(parts,1))
with np.load(inputfile,allow_pickle=False) as data:
 x=data['x'].astype('float32');base=data['base'].astype('float32').reshape(-1)
assert np.isfinite(x).all() and np.isfinite(base).all()
step=config['flow_ode_steps'];mc=config['flow_mc_draws'];chunk=config['flow_eval_batch']
for seed in config['all_flow_seeds']:
 dest=outdir/f'{kind}_{seed}.npz';outdir.mkdir(parents=True,exist_ok=True)
 if dest.exists():continue
 cp=checkpointdir/f'{kind}_{seed}'/'BEST.pt';c=torch.load(cp,map_location='cpu',weights_only=False)
 assert c['kind']==kind and c['seed']==seed
 net=Flow(x.shape[1],config['hidden'],kind=='residual').to(device)
 net.load_state_dict(c['model']);net.eval()
 rng=np.random.default_rng(seed+config['mc_rng_offset']);results=[];clip_events=0
 with torch.inference_mode():
  for start in range(0,len(x),chunk):
   xx=x[start:start+chunk];bb=base[start:start+len(xx)];n=len(xx)
   xt=torch.from_numpy(np.repeat(xx,mc,0)).to(device)
   bt=torch.from_numpy(np.repeat(bb,mc).reshape(-1,1)).to(device)
   z=torch.from_numpy(rng.standard_normal((n*mc,1)).astype('float32')).to(device)
   for j in range(step):
    t=torch.full_like(z,float(j)/step);z=z+net(xt,z,t,bt)/step
   vals=z.detach().cpu().numpy().reshape(n,mc).astype('float64')
   if kind!='direct':vals=vals+bb[:,None]
   logs=config['mu']+config['std']*vals
   clip_events+=int(np.sum((logs<config['inverse_log_min'])|(logs>config['inverse_log_max'])))
   v=np.expm1(np.clip(logs,config['inverse_log_min'],config['inverse_log_max']))
   assert np.isfinite(v).all()
   results.append(v.astype('float32'))
 all_draws=np.concatenate(results)
 tmp=dest.with_name(dest.name+'.p21writing')
 with open(tmp,'wb') as f:np.savez_compressed(f,draws=all_draws,clip_event_count=clip_events)
 os.replace(tmp,dest)
 print(kind,seed,'inferred',len(all_draws),'rows; clipped MC draws',clip_events,flush=True)
print('INFERENCE COMPLETE',kind,flush=True)
