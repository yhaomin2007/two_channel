# Chromium structural-diffusion database — version 0.1

Focus: FCC Ni–Cr and Ni-rich Ni–Cr–Fe, for Wang (2016) and preliminary screening of Doniger (2023). This is a *source-data foundation*, not yet a qualified universal alloy diffusion database.

## Files
- `Cr_Diffusion_Database_v0_1.xlsx`: formatted workbook with Guide, Coefficients, Sources, Case Mapping, and GB Conversion sheets.
- `literature_coefficients.csv`: machine-readable record-level source parameters and calculated values at 973.15 K.
- `sources.csv`: citation/URL registry.
- `validation_mapping.csv`: experiment-to-reference mapping with explicit readiness flags.
- `select_diffusion.py`: evaluate a chosen Arrhenius parameter set at a temperature.

## Key constraints
1. The 1964 Ni–Cr tracer experiments span 1313–1573 K. Results at 973 K are extrapolations.
2. The 2018 SIMS tracer measurements (815–1116 K) are better anchored to 973 K but only Ni and Ni–22 at.% Cr were measured.
3. Chen et al. (2003) is **Ni-rich Ni–Cr–Fe**, not Fe-balance 316 stainless steel. The compositions contain Ti or Nb. It supplies Cr tracer bulk coefficients and GB product delta*Dgb, not a universal Dgb.
4. `GB Conversion` is a clearly labeled illustrative calculation only. GB width and segregation require independent evidence.
5. For 316L and 316H, the database intentionally flags insufficient source-specific diffusivity inputs; a Fe–Cr–Ni CALPHAD mobility/thermodynamic assessment and grain boundary data are needed.
6. Published tracer diffusivity is not automatically the chemical/interdiffusion coefficient in a concentration-gradient PDE.
7. The legacy Bhave/ATH coefficients are present only for comparison and excluded from independent parameter selection.

## Run
```
python select_diffusion.py --list
python select_diffusion.py --id SIMS18-22 --temperature 973.15
python select_diffusion.py --id CH03-B-P --temperature 973.15 --gb-width-nm 0.5
```
