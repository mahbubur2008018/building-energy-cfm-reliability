from pathlib import Path
from catboost import CatBoostRegressor
import json, os, sys, hashlib, numpy as np
p=Path(sys.argv[1]);kind=sys.argv[2]
cfg=json.loads((p/'P18_FIT_ONLY_BASELINE_POLICY.json').read_text());fp=cfg['fingerprint'];c=cfg['protocol']
model_dir=Path(sys.argv[3]);model_dir.mkdir(parents=True,exist_ok=True)
samples=Path(sys.argv[4]);oof=Path(sys.argv[5])
with np.load(samples,allow_pickle=False) as d:
    x=np.asarray(d['x_fit'],dtype=np.float32)
    y=np.asarray(d['y_fit'],dtype=np.float64).reshape(-1)
mu=float(sys.argv[6]);sd=float(sys.argv[7]);target=mu+sd*y
if kind=='oof_log_abs_error':
    with np.load(oof,allow_pickle=False) as f:
        assert str(f['fingerprint'].item())==fp
        error=np.asarray(f['oof_abs_log_error'],dtype=np.float64)
    target=np.log(error+0.02)
params=dict(c['catboost'])
if kind!='oof_log_abs_error':
    params['loss_function']='Quantile:alpha='+str({'q05':0.05,'q50':0.50,'q95':0.95}[kind])
else:
    params['loss_function']='RMSE'
if os.environ.get('P18_LOCAL_CPU_TEST')=='1':
    params['iterations']=8;params['depth']=3;params['task_type']='CPU'
else:
    params['task_type']='GPU';params['devices']='0'
mdl=CatBoostRegressor(**params)
mdl.fit(x,target)
final=model_dir/('P18_'+kind+'.cbm');tmp=model_dir/('P18_'+kind+'.incomplete.cbm')
mdl.save_model(str(tmp));os.replace(tmp,final)
meta={'fingerprint':fp,'model':kind,'fits_only':True,'training_rows':len(x),
      'gpu_assignment_visible':os.environ.get('CUDA_VISIBLE_DEVICES',''),
      'parameters':params}
mfile=model_dir/('P18_'+kind+'.json');mtemp=mfile.with_name(mfile.name+'.tmp')
mtemp.write_text(json.dumps(meta,sort_keys=True,indent=2));os.replace(mtemp,mfile)
print('TRAINED',kind,'rows',len(x),'file',final,'gpu',os.environ.get('CUDA_VISIBLE_DEVICES'),flush=True)
