#!/usr/bin/env python3
"""Exploratory no-fit two-channel simulation for Gentile et al., JOM 2026.
Derived from the ORNL2021 solver; paper contains no calibrated bulk/GB coefficients or mean grain size.
Measured EDS 'depth of attack' is a morphology/line-scan endpoint, NOT equal to an integral mass deficit.
"""
import numpy as np, math, csv, json
from pathlib import Path
from scipy.sparse import diags
from scipy.sparse.linalg import factorized
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent.parent/'NCSU_INL_2026_two_channel_dt60';OUT.mkdir(parents=True,exist_ok=True)
R=8.314462618; T=973.15
DB=4.28e-4*np.exp(-285200/(R*T));DGB=4.85e-2*np.exp(-196200/(R*T))
T_H=[30,240,500];OBS=[22.,28.,83.8];ERR=[3.4,10.1,26.2]
G_LIST=[100.];DELTA_NM=.5
DT=60.0;L=.003;C0=.19;RHO=8500

def mesh():
 e=[0.];h=1e-8
 while e[-1]<L:
  e.append(min(L,e[-1]+h));h=min(5e-6,h*1.05)
 e=np.array(e);return np.diff(e),(e[1:]+e[:-1])/2

def fac(w,x,D):
 q=D/np.diff(x)
 below=-DT*q/w[1:];above=-DT*q/w[:-1]
 diag=np.ones(len(w));diag[1:]-=below;diag[:-1]-=above
 diag[0]+=DT*D/(w[0]*x[0])
 return factorized(diags([below,diag,above],[-1,0,1],format='csc'))

def exchange(cb,cg,t,h,G,fg):
 fb=1-fg
 tc=(G/2)**2/(math.pi*DB)
 def integral(z):
  if z<=tc:return 2*math.sqrt(DB/math.pi)*math.sqrt(z)
  return 2*math.sqrt(DB/math.pi)*math.sqrt(tc)+(2*DB/G)*(z-tc)
 expnt=(4/G)*(integral(t+h)-integral(t))/(fb*fg)
 residual=(cb-cg)*np.exp(-min(expnt,700.))
 mean=fb*cb+fg*cg
 return mean+fg*residual,mean-fb*residual

def depth_criterion(x,c,threshold):
 # farthest depth where Cr deficiency exceeds threshold of virgin concentration
 idx=np.where(c<1-threshold)[0]
 return float(x[idx[-1]]*1e6) if len(idx) else 0.

rows=[]; profiles=[]
for G_um in G_LIST:
 G=G_um*1e-6; fg=2*DELTA_NM*1e-9/G;fb=1-fg
 w,x=mesh();nb=w.size
 b=fac(w,x,DB);g=fac(w,x,DGB)
 cb=np.ones(nb);cg=np.ones(nb);initial=L
 checkpoints={int(h*3600/DT):h for h in T_H}
 for i in range(int(T_H[-1]*3600/DT)+1):
  if i in checkpoints:
   h=checkpoints[i]
   # volume weighted c = fraction of solid Cr; GB profile is extremely narrow spatially but relevant to corrosion penetration
   avg=fb*cb+fg*cg
   mass=(initial-np.dot(w,avg))*RHO*C0*0.1 # kg/m2 to mg/cm2 conversion: kg/m2 -> 100mg/cm2
   # correct kg/m2 * 100 mg/cm2
   mass=(initial-np.dot(w,avg))*RHO*C0*100
   row={'G_um_assumed':G_um,'GB_width_nm_assumed':DELTA_NM,'time_h':h,'experimental_depth_um':OBS[T_H.index(h)],'experimental_depth_unc_um':ERR[T_H.index(h)],
        'GB_depletion_depth_10percent_um':depth_criterion(x,cg,.1),
        'GB_depletion_depth_50percent_um':depth_criterion(x,cg,.5),
        'avg_depletion_depth_10percent_um':depth_criterion(x,avg,.1),
        'model_Cr_loss_mg_cm2_not_measured_experimentally':mass}
   rows.append(row)
   if G_um in (30.,100.,240.): profiles.append((G_um,h,x.copy(),cb.copy(),cg.copy(),avg.copy()))
  if i==int(T_H[-1]*3600/DT):break
  t=i*DT
  cb,cg=exchange(cb,cg,t,DT/2,G,fg)
  cb=b(cb);cg=g(cg)
  cb,cg=exchange(cb,cg,t+DT/2,DT/2,G,fg)
 print('finished',G_um,[(r['time_h'],round(r['GB_depletion_depth_50percent_um'],1),round(r['model_Cr_loss_mg_cm2_not_measured_experimentally'],4)) for r in rows if r['G_um_assumed']==G_um],flush=True)
with open(OUT/'results.csv','w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
for G,h,x,cb,cg,avg in profiles:
 np.savetxt(OUT/f'profile_G{G:g}um_{h}h.csv',np.c_[x*1e6,cb,cg,avg],delimiter=',',header='depth_um,Cbulk_over_C0,Cgb_over_C0,Cweighted_over_C0',comments='')
fig,ax=plt.subplots(figsize=(8.2,5.3))
ax.errorbar(T_H,OBS,yerr=ERR,fmt='ko',capsize=4,label='Experiment: EDS-defined corrosion depth')
for G in G_LIST:
 sel=[r for r in rows if r['G_um_assumed']==G]
 ax.plot(T_H,[r['GB_depletion_depth_50percent_um'] for r in sel],'-o',label=f'Model GB 50% depletion, G={G:g} μm')
ax.set_xlabel('Exposure time (h)');ax.set_ylabel('Depth (μm)');ax.set_title('Different depth definitions: comparison is exploratory')
ax.grid(alpha=.3);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'depth_comparison.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.2,5.2))
for G,h,x,cb,cg,avg in profiles:
 if h==500:ax.plot(x*1e6,cg,label=f'G={G:g} μm')
ax.set_xlim(0,500);ax.set_ylim(-.02,1.03);ax.set_xlabel('Depth from original surface (μm)');ax.set_ylabel('GB Cr concentration / initial');ax.set_title('500 h grain-boundary Cr profiles (perfect sink)');ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/'gb_profiles_500h.png',dpi=180);plt.close(fig)
(OUT/'README.md').write_text('''# Gentile et al., JOM 78 (2026), two-channel exploratory assessment\n\nSource: https://doi.org/10.1007/s11837-025-08019-1\n\nExperimental alloy is NOT binary: Ni-19Cr-5Fe-0.5Cu-0.5Si-0.4Ti, nominal wt%. Grain size not numerically specified.\n\nSimulation uses the existing ATH 2026 binary Ni-Cr Cr diffusivity correlations at 973.15 K, NOT independently validated for the Fe-bearing alloy. Same perfect-sink surface boundary on both channels.\n\nGrain sizes 10/30/100/240 microns are illustrative, GB width 0.5 nm assumed, alloy density 8500 kg/m3 assumed. Domain length 3 mm, no-flux end.\n\nIMPORTANT: paper Table II provides EDS-defined corrosion/attack depth, NOT Cr mass loss. Model 50% GB-depletion depth is a proxy only; the metrics are not equivalent. Model Cr-specific mass loss has NO direct experimental counterpart in the article. No fitting was performed.\n\nSource experimental depths: 30h 22.0±3.4 µm; 240h 28.0±10.1 µm; 500h 83.8±26.2 µm.\n''')
(OUT/'inputs.json').write_text(json.dumps(dict(T_K=T,Db_m2s=DB,Dgb_m2s=DGB,density_kg_m3_assumed=RHO,Cr_weight_fraction=.19,grain_sizes_um_assumed=G_LIST,GB_width_nm_assumed=DELTA_NM,dt_s=DT,domain_m=L,BC='perfect Cr sink at 0; no flux at L',experimental_metric='EDS depth of attack; differs from model grain-boundary diffusion length'),indent=2))
