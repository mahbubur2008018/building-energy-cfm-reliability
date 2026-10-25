from pathlib import Path
import sys,os,json,time,math,random
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
seed=int(sys.argv[5]);torch.manual_seed(seed);random.seed(seed);np.random.seed(seed)
kind=sys.argv[1];data=Path(sys.argv[2]);out=Path(sys.argv[3]);config=json.loads(Path(sys.argv[4]).read_text())['config']
device=torch.device('cuda:0' if torch.cuda.is_available() and os.environ.get('P19_LOCAL_SMOKE')!='1' else 'cpu')
with np.load(data,allow_pickle=False) as d:
    xf=d['x_train'].astype('float32');yf=d['y_train'].astype('float32').reshape(-1,1)
    xv=d['x_stop'].astype('float32');yv=d['y_stop'].astype('float32').reshape(-1,1)
class Net(nn.Module):
    def __init__(self,dim,kind,hidden):
        super().__init__();self.kind=kind
        self.shared=nn.Sequential(nn.Linear(dim,hidden),nn.SiLU(),nn.Linear(hidden,hidden),nn.SiLU())
        self.head=nn.Linear(hidden,2 if kind=='GaussianMLP' else 6)
    def forward(self,x):return self.head(self.shared(x))
def nll(raw,y,kind):
    if kind=='GaussianMLP':
        mu=raw[:,0:1];scale=.04+2.46*torch.sigmoid(raw[:,1:2])
        return (torch.log(scale)+.5*((y-mu)/scale).square()).mean()
    means=raw[:,:2];scales=.04+2.46*torch.sigmoid(raw[:,2:4]);lw=torch.log_softmax(raw[:,4:6],dim=-1)
    logp=lw-torch.log(scales)-.5*((y-means)/scales).square()
    return -torch.logsumexp(logp,dim=-1).mean()
net=Net(xf.shape[1],kind,config['hidden']).to(device)
opt=torch.optim.AdamW(net.parameters(),lr=config['learning_rate'],weight_decay=1e-4)
ckpt=out/(kind+'_LATEST.pt');bestfile=out/(kind+'_BEST.pt');meta=out/(kind+'_METADATA.json')
start=0;best=float('inf');bad=0;hist=[]
if ckpt.exists():
    st=torch.load(ckpt,map_location='cpu',weights_only=False)
    assert st['kind']==kind and st['config']==config
    net.load_state_dict(st['net']);opt.load_state_dict(st['optimizer'])
    start=st['epoch']+1;best=st['best'];bad=st['bad'];hist=st['history']
loader=DataLoader(TensorDataset(torch.from_numpy(xf),torch.from_numpy(yf)),batch_size=config['batch_size'],shuffle=True,num_workers=0,pin_memory=(device.type=='cuda'))
batch=int(config['batch_size'])
for ep in range(start,config['epochs']):
    net.train();total=0.;seen=0
    for xx,yy in loader:
        xx=xx.to(device,non_blocking=True);yy=yy.to(device,non_blocking=True)
        loss=nll(net(xx),yy,kind);opt.zero_grad(set_to_none=True);loss.backward()
        nn.utils.clip_grad_norm_(net.parameters(),1.0);opt.step()
        total+=float(loss.detach())*len(xx);seen+=len(xx)
    net.eval();vs=0.;vn=0
    with torch.inference_mode():
        for j in range(0,len(xv),batch):
            a=torch.from_numpy(xv[j:j+batch]).to(device);b=torch.from_numpy(yv[j:j+batch]).to(device)
            l=nll(net(a),b,kind);vs+=float(l)*len(a);vn+=len(a)
    val=vs/vn;imp=val<best-0.0001
    if imp:
        best=val;bad=0
        state={'kind':kind,'config':config,'epoch':ep,'net':{k:v.detach().cpu() for k,v in net.state_dict().items()},'best':best}
        tmp=bestfile.with_name(bestfile.name+'.tmp');torch.save(state,tmp);os.replace(tmp,bestfile)
    else:bad+=1
    hist.append({'epoch':ep+1,'train_nll':total/seen,'fit_site_holdout_nll':val})
    state={'kind':kind,'config':config,'epoch':ep,'net':{k:v.detach().cpu() for k,v in net.state_dict().items()},
           'optimizer':opt.state_dict(),'best':best,'bad':bad,'history':hist}
    tmp=ckpt.with_name(ckpt.name+'.tmp');torch.save(state,tmp);os.replace(tmp,ckpt)
    if (ep+1)%10==0:print(kind,'epoch',ep+1,'inner FIT-site NLL',round(val,5),flush=True)
    if bad>=config['patience'] and ep+1>=config['min_epochs']:break
rec={'kind':kind,'config':config,'completed':True,'epochs_run':len(hist),'best_inner_fit_nll':best,
     'gpu_visible':os.environ.get('CUDA_VISIBLE_DEVICES',''),'inner_fit_site_only':True}
tmp=meta.with_name(meta.name+'.tmp');tmp.write_text(json.dumps(rec,sort_keys=True,indent=2));os.replace(tmp,meta)
print(kind,'DONE epochs',len(hist),'best_inner_nll',best,flush=True)
