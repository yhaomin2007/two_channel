#!/usr/bin/env python3
"""Select and calculate source-traceable chromium diffusion quantities.

Usage:
  python select_diffusion.py --list
  python select_diffusion.py --id M64-10 --temperature 973.15
  python select_diffusion.py --id CH03-B-P --temperature 973.15 --gb-width-nm 0.5

This script does NOT assert that a measured tracer D is a chemical diffusivity,
that an inferred Dgb transfers between alloys, or that GB segregation equals 1.
"""
import argparse, csv, json, math
from pathlib import Path
R=8.314462618
p=argparse.ArgumentParser()
p.add_argument('--id');p.add_argument('--temperature',type=float,default=973.15)
p.add_argument('--gb-width-nm',type=float,help='Only for delta_Dgb records: explicit width assumption')
p.add_argument('--list',action='store_true')
a=p.parse_args()
records={r['ID']:r for r in csv.DictReader((Path(__file__).parent/'literature_coefficients.csv').open())}
if a.list:
 for r in records.values(): print(f"{r['ID']:16} {r['Alloy']:23} {r['Quantity']}")
 raise SystemExit
if a.id not in records: p.error('Select a valid --id; use --list')
r=records[a.id]
if not r['D0_SI'] or not r['Q_kJ_mol']:
 p.error('This record has no extracted numerical correlation, and cannot be evaluated')
D=float(r['D0_SI'])*math.exp(-float(r['Q_kJ_mol'])*1000/(R*a.temperature))
report={'id':a.id,'alloy':r['Alloy'],'quantity':r['Quantity'],'value_SI':D,'temperature_K':a.temperature,'source':r['URL'],'quality':r['Quality'],'measured_range_K':[r['T_min_K'],r['T_max_K']]}
if r['T_min_K'] and not(float(r['T_min_K'])<=a.temperature<=float(r['T_max_K'])):
 report['WARNING']='Outside measured temperature range: extrapolation'
if r['Quantity']=='delta_Dgb_m3_s' and a.gb_width_nm:
 report['inferred_Dgb_m2_s']=D/(a.gb_width_nm*1e-9)
 report['inference']='Assumes effective GB width; inspect original source for segregation-factor convention'
elif r['Quantity']=='delta_Dgb_m3_s':
 report['WARNING_GB']='Not Dgb; provide --gb-width-nm to infer a conditional Dgb'
if r['Quantity']=='Cr_tracer_bulk_D_m2_s':
 report['WARNING_bulk']='Tracer D*, not automatically the chemical interdiffusion coefficient needed in corrosion PDE'
print(json.dumps(report,indent=2))
