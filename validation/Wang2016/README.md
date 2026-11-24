# Wang et al. (2016) / Ni–Cr grain refinement — preliminary independent validation

## Sources
- Y. L. Wang et al., *Effect of grain refinement on the corrosion of Ni-Cr alloys in molten (Li,Na,K)F*, Corrosion Science 109 (2016) 43–49. DOI: 10.1016/j.corsci.2016.03.027.
- S. Guo et al., *Corrosion in the molten fluoride and chloride salts and materials development for nuclear applications*, Progress in Materials Science 97 (2018) 448–487. Reports ~3 μm laser-refined grains and a 2–4-fold increase in measured weight loss following 100 h exposure, compared with 800–1500 μm coarse-grained material.
- H. Yuan and N. Hoyt, ATH 2026 two-channel conference manuscript (user-supplied): Eqs. 1–25.

## Important disclosure
The accessible primary study abstract/section snippets support 5, 10, and 15 **atomic %** chromium, 700 °C FLiNaK in Ar, cast vs laser-remelted material, and greater mass loss in FG material. The primary paper's full figures and per-composition numerical weight-loss values were unavailable. **This is a preliminary sensitivity / partial validation study; it does not contain a quantitative per-specimen experiment-versus-simulation comparison.** The approximate ~2–4× observation is a SECONDARY review summary, not individual exact datapoints.

## Cases
Six: 5/10/15 at.% Cr x CG/FG.

| Input | Value | Provenance |
|---|---|---|
| Cr composition | 5/10/15 at.% | Wang paper |
| Salt, environment | FLiNaK, Ar, 700 °C | Wang paper |
| Exposure | 100 h | Guo review |
| Grain coarse | 800–1500 μm (baseline midpoint 1150 μm) | Wang paper / midpoint assumption |
| Grain fine | ~3 μm (all compositions assumed) | Guo review; individual values unverified |
| Cr GB width | 0.5 nm | ATH 2026 baseline |
| Ni–Cr density | 8700 kg/m3 (common estimate) | ATH 2026 Ni-5Cr baseline; not Wang measured |
| D_bulk | 4.28e-4 exp(-285200/(RT)) m2/s | Bhave/Yuan ATH paper |
| D_GB | 4.85e-2 exp(-196200/(RT)) m2/s | Bhave/Yuan ATH paper |
| BC salt interface | Cr=0 in bulk & GB | ATH model idealization; not established for experiment |
| Thickness | 3 mm model depth | computational assumption, large vs penetration |

The stand-alone simulation uses a conservative nonuniform finite-volume approximation for both transport channels, implicit diffusion and exact analytical channel-exchange substeps (Strang splitting). It implements the same equations, but is NOT a reproduction of the user's original Python code's finite-difference discretization. The output is predicted *Cr-specific release*, not necessarily experimental total alloy weight loss.

## Results (dt=15 s)

| Cr (at.%) | CG predicted Cr loss (mg/cm2) | FG predicted Cr loss (mg/cm2) | FG/CG |
|---|---:|---:|---:|
| 5 | 0.01281 | 0.28541 | 22.28 |
| 10 | 0.02577 | 0.57412 | 22.28 |
| 15 | 0.03888 | 0.86619 | 22.28 |

Reported (secondary review, not per-alloy measurements): ~2–4x FG/CG **total weight loss**.

### Interpretation
Predicted grain-size sensitivity is much stronger than the reported total weight-loss effect. These are not like-for-like observables, and independently measured parameters are missing; this is not a definitive model falsification. The use of 0.5 nm as the GB transport channel width, perfect sink for every specimen, and phase-field-derived diffusivities could all matter. The response ratio is nearly composition-independent because both equations are linear when diffusivities and geometric parameters are kept constant, so all Cr concentrations scale linearly; this is a model implication rather than experimental evidence.

### Sensitivities (10 at.% Cr, dt=120s screening)
- CG=800 μm, FG=3 μm: ratio ~20.25.
- CG=1500 μm, FG=3 μm: ratio ~21.02.
- CG=1150 μm, FG=2 μm: ratio ~29.67.
- CG=1150 μm, FG=4 μm: ratio ~16.05.
These ratios are not quantitatively converged in time; they establish the substantial scale of the discrepancy across the estimated grain-size range.

### Numerical checks (10 at.% Cr; dt in seconds)
| dt (s) | CG Cr loss | FG Cr loss | FG/CG |
|---:|---:|---:|---:|
| 120 | 0.02563 | 0.53163 | 20.75 |
| 60 | 0.02570 | 0.55446 | 21.57 |
| 30 | 0.02575 | 0.56724 | 22.03 |
| 15 | 0.02577 | 0.57412 | 22.28 |

The time step remains a source of uncertainty (FG loss changes ~1.2% from dt=30 to dt=15s). Spatial convergence check at dt=120s with near-surface dx 10nm versus 20nm changes mass losses by far less than 1%, but no exhaustive V&V study has been performed. Cumulative loss is computed from a conservative chromium inventory deficit; model source steps conserve the volume-weighted Cr exactly to floating-point tolerance.

## Reproduce
`python run_wang2016.py` (Python 3.10+, numpy, scipy, matplotlib). Program writes the six time-series CSVs, six concentration profile CSVs, parameter and summary JSON, summary.csv and comparison.png.

## Needed before claiming quantitative validation
1. Obtain primary Wang et al. full-text figure(s) and accurately digitize per-composition CG/FG weight losses, uncertainty, test time and grain-size distributions.
2. Establish how weight loss was measured (TGA/cleaning) and how much reflects Cr versus Ni removal.
3. Get alloy-specific density and independently measured Cr lattice/GB diffusivities at 700 °C if possible; check laser-remelted dislocations and residual stresses.
4. Investigate boundary-condition validity (salt redox/impurity and Cr build-up), compare depth profiles and depletion zone definitions.
5. Complete grid/time-convergence tests prior to making quantitative error claims.
