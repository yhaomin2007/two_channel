#!/usr/bin/env python3
"""Independent, conservative implementation of Yuan & Hoyt's two-channel model.
Wang et al., Corrosion Science 109 (2016) 43-49, DOI 10.1016/j.corsci.2016.03.027.
Six cases (CG/FG x Ni-{5,10,15} at.%Cr). Reference figure values have NOT been
available; comparisons are explicitly to reported qualitative/factor 2-4 result.
Run: python run_wang2016.py
Requires: numpy scipy matplotlib.
"""
from __future__ import annotations
import csv, json
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import factorized
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
M_CR = 51.9961  # g/mol
M_NI = 58.6934  # g/mol
R = 8.31446

@dataclass
class Parameters:
    T_K: float = 973.15             # 700 degC (Wang 2016)
    hours: float = 100.0           # from Guo et al. review of Wang 2016
    grain_CG_um: float = 1150.0    # illustrative midpoint of observed range 800-1500 um
    grain_FG_um: float = 3.0       # approximate from Guo et al. review
    grain_boundary_width_m: float = 5.0e-10  # from Yuan & Hoyt baseline
    density_kg_m3: float = 8700.0  # assumed, from Yuan & Hoyt Ni-5Cr baseline
    length_m: float = 3.0e-3      # model domain sufficiently deep for 100 h
    min_dx_m: float = 2.0e-8      # fine surface resolution for bulk diffusion
    max_dx_m: float = 4.0e-6
    growth: float = 1.025
    dt_s: float = 15.0
    history_step_h: float = 1.0
    k_t0_s: float = 1.0


def geometry(p: Parameters):
    # cell edges: geometric grading, near-surface dx=20 nm, far-field max 4 microns
    edges = [0.0]
    dx = p.min_dx_m
    while edges[-1] < p.length_m:
        edges.append(min(p.length_m, edges[-1] + dx))
        dx = min(p.max_dx_m, dx*p.growth)
    edges = np.asarray(edges)
    return edges, np.diff(edges), 0.5*(edges[1:]+edges[:-1])


def diffusivities(T):
    # Bhave (2023) correlations as used in Yuan & Hoyt ATH 2026 paper
    return 4.28e-4*np.exp(-285200/(R*T)), 4.85e-2*np.exp(-196200/(R*T))


def diffusion_solver(edges, widths, centers, D, dt):
    """FV concentration per cell; c(0)=0, dc/dx(L)=0.
    Conservative implicit Euler for diffusion on graded mesh.
    """
    n = len(widths)
    transmiss = D / np.diff(centers)
    a = np.zeros(n)
    b = np.ones(n)
    c = np.zeros(n)
    # fluxes between neighboring cell centers
    l = dt*transmiss / widths[1:]
    r = dt*transmiss / widths[:-1]
    a[1:] = -l; c[:-1] = -r
    b[1:] += l; b[:-1] += r
    # left Dirichlet at 0, gradient over center distance
    b[0] += dt*D/(widths[0]*centers[0])
    mat = diags([a[1:], b, c[:-1]], [-1,0,1], format='csc')
    return factorized(mat)


def exchange(cb, cg, t, duration, Db, grain, fg, width, t0):
    # Gamma=a*k*(cb-cg); transfer is exactly conservative in f-weighted inventory
    # k(t) uses paper's max(sqrt(Db/(pi*t)), Db/(G/2)) closure.
    fb = 1.0-fg
    abg = 4.0/grain
    tm = max(t + 0.5*duration, t0)
    k = max(np.sqrt(Db/(np.pi*tm)), Db/(0.5*grain))
    lam = abg*k/(fb*fg)
    delta_old = cb-cg
    delta_new = delta_old*np.exp(-np.clip(lam*duration, 0, 700))
    avg = fb*cb+fg*cg
    return avg+fg*delta_new, avg-fb*delta_new


def run_case(p, at_cr, state):
    grain = (p.grain_CG_um if state=='CG' else p.grain_FG_um)*1e-6
    fg = 2*p.grain_boundary_width_m/grain
    fb = 1-fg
    edges, w, x = geometry(p)
    Db,Dgb = diffusivities(p.T_K)
    sol_b=diffusion_solver(edges,w,x,Db,p.dt_s)
    sol_g=diffusion_solver(edges,w,x,Dgb,p.dt_s)
    # at.% -> mol/m3, based on binary alloy and estimated bulk mass density
    xcr = at_cr/100.0
    mean_molar_mass_kg=(xcr*M_CR+(1-xcr)*M_NI)*1e-3
    c0=p.density_kg_m3/mean_molar_mass_kg*xcr
    cb=np.full(len(w),c0)
    cg=np.full(len(w),c0)
    mass0=np.sum(w*(fb*cb+fg*cg))
    hist=[]
    nsteps=int(round(p.hours*3600/p.dt_s))
    next_h=0
    for step in range(nsteps+1):
        t=step*p.dt_s
        if step==next_h or step==nsteps:
            inventory=np.sum(w*(fb*cb+fg*cg))
            lost=mass0-inventory
            loss=lost*M_CR*0.1
            # surface release flux in mol/m2/s (first cell to c=0)
            flux=fb*Db*cb[0]/x[0]+fg*Dgb*cg[0]/x[0]
            hist.append((t/3600,loss,flux))
            next_h += int(round(p.history_step_h*3600/p.dt_s))
        if step==nsteps: break
        cb,cg=exchange(cb,cg,t,p.dt_s/2,Db,grain,fg,p.grain_boundary_width_m,p.k_t0_s)
        cb=sol_b(cb);cg=sol_g(cg)
        cb,cg=exchange(cb,cg,t+p.dt_s/2,p.dt_s/2,Db,grain,fg,p.grain_boundary_width_m,p.k_t0_s)
    a=np.asarray(hist)
    np.savetxt(OUT/f'profile_{at_cr}atCr_{state}.csv', np.column_stack([x*1e6,cb,cg,fb*cb+fg*cg]), delimiter=',',header='depth_um,Cr_bulk_mol_m3,Cr_GB_mol_m3,Cr_volume_averaged_mol_m3', comments='')
    np.savetxt(OUT/f'history_{at_cr}atCr_{state}.csv',a, delimiter=',',header='time_h,Cr_mass_loss_mg_cm2,Cr_flux_mol_m2_s',comments='')
    return {'composition_at_pct':at_cr,'grain_condition':state,'grain_size_um':grain*1e6,
            'cr_mass_loss_100h_mg_cm2':float(a[-1,1]),'initial_Cr_mol_m3':float(c0),
            'D_bulk_m2_s':Db,'D_gb_m2_s':Dgb,'f_GB_volume':fg,
            'time_h':a[:,0].tolist(),'loss_mg_cm2':a[:,1].tolist()}


def main():
    p=Parameters()
    rows=[run_case(p,at,s) for at in (5,10,15) for s in ('CG','FG')]
    short=[]
    for at in (5,10,15):
        cg=next(q for q in rows if q['composition_at_pct']==at and q['grain_condition']=='CG')
        fg=next(q for q in rows if q['composition_at_pct']==at and q['grain_condition']=='FG')
        short.append({'Cr_at_pct':at,'CG_loss_mg_cm2':cg['cr_mass_loss_100h_mg_cm2'],
             'FG_loss_mg_cm2':fg['cr_mass_loss_100h_mg_cm2'],
             'FG_to_CG_predicted':fg['cr_mass_loss_100h_mg_cm2']/cg['cr_mass_loss_100h_mg_cm2'],
             'reported_range_review_only':'roughly 2-4 across selected alloys, not individual values'})
    with open(OUT/'summary.csv','w',newline='') as f:
        wr=csv.DictWriter(f,short[0].keys());wr.writeheader();wr.writerows(short)
    (OUT/'parameters.json').write_text(json.dumps(asdict(p),indent=2))
    (OUT/'results.json').write_text(json.dumps(short,indent=2))
    fig,axs=plt.subplots(1,2,figsize=(12,4.6))
    for at in (5,10,15):
        for state,ls in [('CG','--'),('FG','-')]:
            d=next(q for q in rows if q['composition_at_pct']==at and q['grain_condition']==state)
            axs[0].plot(d['time_h'],d['loss_mg_cm2'],ls,label=f'Ni-{at}at.%Cr {state}')
    axs[0].set(xlabel='Exposure time (h)',ylabel='Predicted Cr loss (mg/cm²)',title='Two-channel perfect-sink predictions')
    axs[0].grid(alpha=.25);axs[0].legend(fontsize=8)
    xs=[r['Cr_at_pct'] for r in short];ys=[r['FG_to_CG_predicted'] for r in short]
    axs[1].axhspan(2,4,alpha=.17,label='Literature review: ~2–4× overall (not per alloy)')
    axs[1].plot(xs,ys,'o-',label='Model prediction')
    axs[1].set(xlabel='Cr composition (at.%)',ylabel='FG/CG Cr-loss ratio at 100 h',title='Grain-refinement response')
    axs[1].set_xticks(xs);axs[1].set_ylim(bottom=0);axs[1].grid(alpha=.25);axs[1].legend(fontsize=8)
    fig.tight_layout();fig.savefig(OUT/'comparison.png',dpi=180);plt.close(fig)
    print('Model T, Db, Dgb',p.T_K,*diffusivities(p.T_K))
    for row in short:print(row)

if __name__=='__main__':main()
