#!/usr/bin/env python3
"""Pillai, Raiman & Pint JNM 546 (2021) 152755; binary Ni-Cr comparison.
Conservative two-channel diffusion with finite-volume implicit diffusion,
exact weighted bulk/GB exchange split in half steps. No fitting to experiment.
G/delta not measured in reference and are sensitivity inputs only.
Run: python run_ornl2021.py
"""
from pathlib import Path
import numpy as np, math, csv, json
from scipy.sparse import diags
from scipy.sparse.linalg import factorized
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).parent
R=8.314462618; T=1073.15; MCR=51.9961; MNI=58.6934
RHO=8700.0 # assumed constant for all model alloy compositions, not measured in paper
BULK_D0=4.28e-4; BULK_Q=285200.0; GB_D0=4.85e-2; GB_Q=196200.0
DB=BULK_D0*np.exp(-BULK_Q/(R*T)); DGB=GB_D0*np.exp(-GB_Q/(R*T))
TIMES_H=[522,1625,2614]; MAX_H=max(TIMES_H)
# Manual visual estimates from Figure 4 (not raw data; +/- ~0.05-0.1 mg/cm2 digitization error).
EXPERIMENT={'Ni-7Cr':{522:0.59,1625:0.82,2614:0.64},'Ni-16Cr':{522:0.65,1625:1.02,2614:0.93},'Ni-24Cr':{522:0.71,1625:1.79,2614:2.04}}
ALLOYS={'Ni-7Cr':7.0,'Ni-16Cr':16.1,'Ni-24Cr':23.2} # wt % from table 1

def mesh(L=600e-6,dx0=2e-8,dxmax=2e-6,grow=1.036):
    edges=[0.]; dx=dx0
    while edges[-1]<L:
        edges.append(min(L,edges[-1]+dx)); dx=min(dxmax,dx*grow)
    e=np.array(edges); return np.diff(e),(e[1:]+e[:-1])/2

def fac(width,x,D,dt):
    trans=D/np.diff(x)
    below=-dt*trans/width[1:]; above=-dt*trans/width[:-1]
    diag=np.ones(len(width));diag[1:]-=below;diag[:-1]-=above
    diag[0]+=dt*D/(width[0]*x[0])
    return factorized(diags([below,diag,above],[-1,0,1],format='csc'))

def exchange(cb,cg,t,duration,G,fg):
    fb=1-fg
    # EXACT time integral of k_eff = max(sqrt(Db/(pi*t)), 2*Db/G).
    # Avoid treating the t=0 singularity with a step-size-dependent midpoint.
    tc=(G/2)**2/(math.pi*DB)
    def primitive(x):
        if x<=tc:
            return 2*math.sqrt(DB/math.pi)*math.sqrt(x)
        return 2*math.sqrt(DB/math.pi)*math.sqrt(tc)+(2*DB/G)*(x-tc)
    int_k=primitive(t+duration)-primitive(t)
    exponent=(4/G)*int_k/(fb*fg)
    diff=(cb-cg)*np.exp(-min(exponent,700.0))
    mean=fb*cb+fg*cg
    return mean+fg*diff,mean-fb*diff

def sim(name,wt_cr,G_um,delta_nm,dt=120.,L=600e-6,store=True):
    G=G_um*1e-6; d=delta_nm*1e-9; fg=2*d/G;fb=1-fg
    w,x=mesh(L); a=fac(w,x,DB,dt); b=fac(w,x,DGB,dt)
    # conversion:  mass fraction -> Cr molar concentration
    c0=RHO*(wt_cr/100)/(MCR*1e-3)
    cb=np.full(w.size,c0);cg=cb.copy();inv0=c0*L
    n=int(round(MAX_H*3600/dt)); times={int(round(h*3600/dt)):h for h in TIMES_H}
    hist=[]; records=[]
    for i in range(n+1):
        t=i*dt
        if i in times or i==0 or i%int(round(24*3600/dt))==0:
            remain=float(np.dot(w,fb*cb+fg*cg));lost=inv0-remain
            mloss=lost*MCR*0.1
            hist.append([t/3600,mloss])
            if i in times:
                h=times[i]
                records.append({'alloy':name,'Cr_wt_pct':wt_cr,'G_um':G_um,'delta_nm':delta_nm,
                 'exposure_h':h,'D_bulk_m2s':DB,'D_gb_m2s':DGB,'gb_volume_fraction':fg,
                 'model_Cr_loss_mg_cm2':mloss,'observed_Cr_loss_mg_cm2_approx_fig4':EXPERIMENT[name][h],
                 'ratio_model_observed':mloss/EXPERIMENT[name][h], 'mass_balance_mol_m2':lost-mloss/(MCR*.1)})
        if i==n:break
        cb,cg=exchange(cb,cg,t,dt/2,G,fg)
        cb=a(cb);cg=b(cg)
        cb,cg=exchange(cb,cg,t+dt/2,dt/2,G,fg)
    if store:
        tag=f'{name}_G{G_um:g}um_delta{delta_nm:g}nm'
        np.savetxt(OUT/f'{tag}_history.csv',np.array(hist),delimiter=',',header='time_h,Cr_loss_mg_cm2',comments='')
        np.savetxt(OUT/f'{tag}_profile.csv',np.column_stack((x*1e6,cb/c0,cg/c0,(fb*cb+fg*cg)/c0)),delimiter=',',header='depth_um,Cb_over_C0,Cgb_over_C0,Cweighted_over_C0',comments='')
    return records

def main():
    rows=[]
    for name,c in ALLOYS.items():
        for G,d in [(3.,.5),(30.,.5),(240.,.5),(30.,1.)]:
            rr=sim(name,c,G,d)
            rows+=rr
            print(name,G,d,[(r['exposure_h'],round(r['model_Cr_loss_mg_cm2'],5)) for r in rr],flush=True)
    with open(OUT/'results.csv','w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
    with open(OUT/'experimental_fig4_estimates.csv','w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['alloy','exposure_h','approx_Cr_loss_mg_cm2','note'])
        for a,ds in EXPERIMENT.items():
            for t,v in ds.items(): wr.writerow([a,t,v,'Visually estimated from published Figure 4; NOT exact digitized data'])
    fig,axes=plt.subplots(1,3,figsize=(14,4.6),sharey=True)
    for ax,(name,c) in zip(axes,ALLOYS.items()):
        xs=np.array(TIMES_H);ax.plot(xs,[EXPERIMENT[name][x] for x in TIMES_H],'o-',lw=2.2,label='Experiment (Fig. 4 approx)')
        for G,d in [(3.,.5),(30.,.5),(240.,.5),(30.,1.)]:
            h=np.genfromtxt(OUT/f'{name}_G{G:g}um_delta{d:g}nm_history.csv',delimiter=',',names=True)
            ax.plot(h['time_h'],h['Cr_loss_mg_cm2'],label=f'G={G:g} μm, δ={d:g} nm',ls='--' if d==1 else '-')
        ax.set_title(f'{name} ({c:g} wt.% Cr)');ax.set_xlabel('Exposure (h)');ax.grid(alpha=.25)
    axes[0].set_ylabel('Cr depletion-equivalent loss (mg/cm²)')
    axes[0].legend(fontsize=7.7)
    fig.suptitle('ORNL Pillai et al. (2021): no-fit two-channel prediction vs Fig. 4')
    fig.tight_layout();fig.savefig(OUT/'comparison_mass_loss.png',dpi=190);plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(14,4.4),sharey=True)
    for ax,(name,c) in zip(axes,ALLOYS.items()):
        for G,d in [(3.,.5),(30.,.5),(240.,.5),(30.,1.)]:
            dat=np.genfromtxt(OUT/f'{name}_G{G:g}um_delta{d:g}nm_profile.csv',delimiter=',',names=True)
            ax.plot(dat['depth_um'],dat['Cweighted_over_C0']*c,label=f'G={G:g} μm δ={d:g} nm')
        ax.axhline(c,color='gray',alpha=.3,ls=':');ax.set_xlim(0,120);ax.set_title(name);ax.set_xlabel('Depth (μm)');ax.grid(alpha=.2)
    axes[0].set_ylabel('Volume-weighted Cr concentration (wt.%)')
    axes[0].legend(fontsize=7.5)
    fig.suptitle('Predicted 2614 h Cr profiles; compare to paper Figure 2 (no raw EDS values)')
    fig.tight_layout();fig.savefig(OUT/'comparison_profiles.png',dpi=190);plt.close(fig)
    (OUT/'parameters.json').write_text(json.dumps({'reference':'Pillai, Raiman, Pint, JNM 546 (2021) 152755','T_C':800,'salt':'purified KCl-MgCl2 68:32 mol%','exposure_h':TIMES_H,'alloy_Cr_wt_pct':ALLOYS,'D_bulk_D0_m2s':BULK_D0,'D_bulk_Q_Jmol':BULK_Q,'D_gb_D0_m2s':GB_D0,'D_gb_Q_Jmol':GB_Q,'D_bulk_m2s':DB,'D_gb_m2s':DGB,'grain_size_um_options_assumed':[3,30,240],'gb_width_nm_assumed':[.5,1.0],'density_kg_m3_assumed':RHO,'dt_s':120,'length_um':600,'surface':'perfect Cr sink on both channels','grain_exchange':'a_bg=4/G; k_eff=max(sqrt(D_bulk/(pi*t)),D_bulk/(G/2))','experimental_Cr_loss':'manually estimated from Figure 4; NOT exact raw data','constraint':'paper reports no actual grain sizes or GB widths for binary Ni-Cr specimens; coefficients taken from ATH 2026 paper, not independently measured for these three ORNL alloys'},indent=2))
if __name__=='__main__':main()
