import csv, math, json, pathlib
from artifact_tool import Workbook, SpreadsheetFile
P=pathlib.Path('/mnt/data/Cr_Diffusion_Database'); R=8.314462618; T=973.15
S={
'S01':('Monma, Suto & Oikawa (1964)','Cr-51 tracer diffusion in FCC Ni-Cr alloys','https://doi.org/10.2320/jinstmet1952.28.4_188','1313-1573 K; extrapolation to 973 K'),
'S02':('Cr tracer SIMS (2018)','Tracer diffusion of Cr in Ni and Ni-22Cr','https://doi.org/10.1016/j.mtla.2018.08.004','815-1116 K; near target temperature'),
'S03':('Chen et al. (2003)','Volume and Grain Boundary Diffusion of Chromium in Ni-Base Ni-Cr-Fe Alloys','https://doi.org/10.2320/matertrans.44.40','858-1424 K; includes measurements at 973 K'),
'S04':('Sevlikar et al. (2024)','Cr GB diffusion and segregation in Ni Sigma11 bicrystal','https://doi.org/10.1016/j.actamat.2024.120229','503-1203 K; boundary-specific'),
'S05':('Cr GB SIMS (2019)','Grain boundary diffusion of chromium in polycrystalline nickel studied by SIMS','https://www.sciencedirect.com/science/article/pii/S2589152919300791','GB data; parameters not yet extracted'),
'S06':('NIST mobility assessments','Published diffusion mobility assessments, FCC Cr-Ni and Cr-Fe','https://www.nist.gov/mml/materials-science-and-engineering-division/thermodynamics-and-kinetics-group/published-diffusion','database availability; no numerical inputs imported'),
'S07':('Bhave et al. (2023) / ATH model','Previous two-channel benchmark coefficients','https://www.sciencedirect.com/science/article/pii/S0022311522005215','legacy benchmark only; not independent validation'),
'S08':('Wang et al. (2016)','Effect of grain refinement on corrosion of Ni-Cr alloys in FLiNaK','https://doi.org/10.1016/j.corsci.2016.03.027','experimental corrosion test; no measured D_b or D_gb'),
'S09':('Doniger et al. (2023)','Corrosion of 316L and 316H stainless steel in FLiNaK','https://doi.org/10.1016/j.jnucmat.2023.154383','experimental corrosion test; no measured D_b or D_gb'),
}
rows=[]
def add(id,alloy,phase,cr,crbasis,c,fe,kind,d0,q,tmin,tmax,source,method,note,quality='Measured correlation', gb=None):
 val=(d0*math.exp(-q*1000/(R*T))) if d0 is not None else None
 rows.append(dict(ID=id,Alloy=alloy,Phase=phase,Cr=cr,Cr_basis=crbasis,C_wt_pct=c,Fe_wt_pct=fe,Quantity=kind,D0_SI=d0,Q_kJ_mol=q,T_min_K=tmin,T_max_K=tmax,D_at_973K_SI=val,Source=source,Method=method,Quality=quality,GB_structure=gb or '',Notes=note,URL=S[source][2]))
# 1964 values Cr radioactive tracer in Ni Cr alloys (D0 in cm2/s converted to m2/s)
for cr,d0,q in [(0,1.1e-4,65.1*4.184),(10,1.4e-4,66.5*4.184),(19.9,1.9e-4,67.7*4.184),(29.7,3.2e-4,69.4*4.184)]:
 add('M64-'+str(cr),'Ni-'+str(cr)+'atCr' if cr else 'Ni (Cr tracer)','FCC',cr,'at.%',None,0,'Cr_tracer_bulk_D_m2_s',d0,q,1313,1573,'S01','radiotracer + lathe sectioning','High-temperature extrapolation to 973.15 K; do not use unqualified')
# SIMS 2018 ln D0 in cm2/s, converted to SI
for cr,lnd0,q in [(0,-1.6,260),(22,-0.3,279)]:
 add('SIMS18-'+str(cr),'Ni-'+str(cr)+'atCr' if cr else 'Ni (Cr tracer)','FCC',cr,'at.%',None,0,'Cr_tracer_bulk_D_m2_s',math.exp(lnd0)*1e-4,q,815,1116,'S02','SIMS isotopic tracer','2018 study reports ln(D0) in cm2/s; converted by exp(lnD0)*1e-4; Q uncertainty 2/10 kJ/mol')
# 2003 original profiles H/A/B composition and Arrhenius for volume and delta Dgb
for name,cr,fe,c,bd0,bq,pd0,pq in [('H',15.18,7.76,0.070,1.8e-2,340,8.2e-8,335),('A',16.49,7.40,0.015,1.0e-3,300,1.9e-9,227),('B',16.24,6.78,0.004,5.1e-4,286,4.8e-12,203)]:
 add('CH03-'+name+'-B','Ni-Cr-Fe '+name,'FCC',cr,'wt.%',c,fe,'Cr_tracer_bulk_D_m2_s',bd0,bq,858,1424,'S03','51Cr radioactive tracer','Actual ternary and microalloyed composition; NOT 316 steel')
 add('CH03-'+name+'-P','Ni-Cr-Fe '+name,'FCC',cr,'wt.%',c,fe,'delta_Dgb_m3_s',pd0,pq,858,1424,'S03','51Cr tracer + Whipple/LeClaire GB analysis','Reported as δ D_gb by authors; conversion to D_gb needs δ and validity of segregation treatment','Measured GB product')
# legacy not eligible
add('LEGACY-B','ATH legacy Ni-Cr', 'FCC',None,'unspecified',None,None,'Cr_bulk_effective_D_m2_s',4.28e-4,285.2,None,None,'S07','Bhave/ATH correlation','Reference baseline ONLY; not independently established for Wang compositions','Legacy benchmark')
add('LEGACY-GB','ATH legacy Ni-Cr','FCC',None,'unspecified',None,None,'Cr_GB_effective_D_m2_s',4.85e-2,196.2,None,None,'S07','Bhave/ATH correlation','Reference baseline ONLY; not independently established for Wang compositions','Legacy benchmark')
# bibliographic unquantified records
for id,alloy,q,source,note in [('S24-GB','Ni Sigma11','GB: Cr transport, fast and slow','S04','Need primary-article parameter extraction and GB segregation assessment before numeric use'),('SIMS19-GB','Polycrystalline Ni','GB: Cr diffusion','S05','Need original paper tables and evaluated GB triple product'),('CALPHAD-NICR','FCC Ni-Cr','bulk: composition-dependent mobility','S06','Obtain thermodynamic and mobility DB to calculate chemical interdiffusion')]:
 add(id,alloy,'FCC',None,'unspecified',None,None,q,None,None,None,None,source,'literature pointer',note,'Pending extraction')
# save rows
cols=list(rows[0]);
with open(P/'literature_coefficients.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
with open(P/'sources.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['Source ID','Citation','Title','URL','Notes']);w.writerows([[k,*v] for k,v in S.items()])
# recommended candidate mapping NOT pretend 316 data known
mapping=[
['Wang Ni-5Cr CG/FG',5,'at.%','Ni-5atCr','M64-0 / M64-10 (interpolate exploratory ONLY)','S24-GB or SIMS19-GB; no binary-alloy-specific value yet','Bulk interpolation not independent at 973 K; GB missing','NO'],
['Wang Ni-10Cr CG/FG',10,'at.%','Ni-10atCr','M64-10','S24-GB or SIMS19-GB; no binary-alloy-specific value yet','1964 bulk extrapolates 340 K below measurement range; GB missing','NO'],
['Wang Ni-15Cr CG/FG',15,'at.%','Ni-15atCr','M64-10 / M64-19.9 (interpolate exploratory ONLY)','S24-GB or SIMS19-GB; no binary-alloy-specific value yet','Bulk extrapolation; GB missing','NO'],
['Doniger 316L',16.77,'wt.%','Fe-base 316L','CALPHAD Fe-Cr-Ni mobility, pending','Cr GB transport in Fe-base austenite, pending','Ni-base Ni-Cr-Fe alloys CH03 are NOT representative of Fe-balance 316L','NO'],
['Doniger 316H',16.77,'wt.%','Fe-base 316H','CALPHAD Fe-Cr-Ni mobility, pending','Cr GB transport with sensitization/carbides, pending','Ni-base CH03 carbon trends are mechanistic context, not direct 316H parameters','NO']]
with open(P/'validation_mapping.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['Experiment','Cr','Cr basis','Alloy matrix','Bulk candidate','GB candidate','Limitations','Ready for predictive run']);w.writerows(mapping)
# workbook
wb=Workbook.create()
def sheet_write(name, matrix, widths=None):
 s=wb.worksheets.add(name)
 s.get_range_by_indexes(0,0,len(matrix),len(matrix[0])).values=matrix
 head=s.get_range_by_indexes(0,0,1,len(matrix[0]));head.format={'fill':'#17324A','font':{'bold':True,'color':'#FFFFFF'},'row_height':32,'wrap_text':True}
 s.freeze_panes.freeze_rows(1)
 for j in range(len(matrix[0])):
  s.get_range_by_indexes(0,j,len(matrix),1).format.column_width=(widths[j] if widths and j<len(widths) else 20)
 s.get_range_by_indexes(1,0,len(matrix)-1,len(matrix[0])).format.row_height=25
 return s
intro=[['DATABASE GUIDE','Description'],['Purpose','Independent chromium bulk/GB transport data for two-channel structural corrosion validation'],['Reference temperature','973.15 K'],['Numerical convention','D(T) = D0 exp[-Q*1000/(R*T)]; Q in kJ/mol; D0 SI units'],['Bulk tracer vs chemical','Measured Cr tracer D* is not automatically binary chemical interdiffusion coefficient'],['Grain-boundary product','delta*Dgb in m3/s must not be inserted directly as Dgb in m2/s'],['Segregation','Some sources report s*delta*Dgb; check convention before inversion'],['Measured composition','Atomic percent and mass percent kept separate'],['No invented matches','Ni-base Fe-Cr-Ni coefficients are not assigned to Fe-base 316 steels'],['GB model width','GB width is an assumed conversion input; default 0.5 nm for demonstration ONLY'],['Predictive-ready','NO until material-specific chemical bulk D and suitable GB D are independently supported'],['Scope','Version 0.1, Cr only, FCC Ni-Cr and Ni-Cr-Fe foundation; extend to commercial alloys']]
sheet_write('Guide',intro,[24,95])
record_header=['ID','Alloy','Phase','Cr','Cr basis','C (wt.%)','Fe (wt.%)','Quantity','D0 SI','Q kJ/mol','Tmin K','Tmax K','D(973K) SI','Source','Method','Quality','GB structure','Notes','Source URL']
mat=[record_header]+[[r[k] for k in cols] for r in rows]
s=sheet_write('Coefficients',mat,[18,24,10,10,12,12,12,28,18,16,14,14,22,10,25,24,24,62,53]);s.get_range('I2:I20').set_number_format('0.000E+00');s.get_range('M2:M20').set_number_format('0.000E+00')
sheet_write('Sources',[['ID','Citation','Title','URL','Notes']]+[[k,*v] for k,v in S.items()],[12,40,66,75,52])
sheet_write('Case Mapping',[['Experiment','Cr','Basis','Matrix','Bulk candidate','GB candidate','Limitations','Predictive-ready']]+mapping,[30,12,12,25,60,60,80,18])
# Demonstration conversion explicit calculations from Chen 2003, 0.5nm and s=1 assumption, not approved to validate
G=['Demonstration - GB product conversion','Value','Unit','Note'];demo=[G,['Temperature',973.15,'K','Change reference temperature manually to calculate in external script'],['GB width assumption',5e-10,'m','Not measured for these alloys'],['Segregation assumption',1.0,'-','Not independently verified; source reports delta D_gb'],['Chen B: delta D_gb at 973 K',next(r['D_at_973K_SI'] for r in rows if r['ID']=='CH03-B-P'),'m3/s','Ni-rich ternary; not 316'],['Chen B: inferred Dgb',None,'m2/s','EXAMPLE only; not applicable to Wang or Doniger']]
s=sheet_write('GB Conversion',demo,[38,24,16,72]);s.get_range('B6').formulas=[['=B5/(B3*B4)']];s.get_range('B3:B6').set_number_format('0.000E+00')
SpreadsheetFile.export_xlsx(wb).save(str(P/'Cr_Diffusion_Database_v0_1.xlsx'))
print('rows',len(rows),'xlsx',P/'Cr_Diffusion_Database_v0_1.xlsx')
print(wb.inspect({'kind':'table','range':'GB Conversion!A1:D6','include':'values,formulas','table_max_rows':6,'table_max_cols':4}).ndjson[:1800])
