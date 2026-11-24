# ORNL 2021 Pillai/Raiman/Pint: two-channel Ni–Cr calculation

Reference: *First steps toward predicting corrosion behavior of structural materials in molten salts*, Journal of Nuclear Materials **546** (2021) 152755; DOI 10.1016/j.jnucmat.2020.152755.

## Experimental basis (source paper)

- Binary Ni–7Cr (7.0 wt.% Cr), Ni–16Cr (16.1 wt.% Cr), Ni–24Cr (23.2 wt.% Cr), Table 1.
- 800°C, purified KCl–MgCl₂ 68:32 mol.%, sealed Mo capsules, 28 g salt, 6×12×1.5 mm samples, 600-grit preparation.
- The corrosion-exposure durations used for comparisons are 522, 1625, and 2614 hours, Fig. 4.
- **Experimental quantity:** Cr-specific loss derived by the authors by integrating post-exposure EDS Cr concentration profiles and multiplying by alloy density (NOT total sample mass loss). Figs. 2–4.
- Experimental numbers in `experimental_fig4_estimates.csv` were *visually estimated from the paper figure*. They are approximate, not raw measurements or precise digitization.
- Original paper does **not** give a measured numeric grain size or grain boundary width for the three binary NiCr coupons. Do not label any model results fully predictive.

## Independent model inputs (not fitted)

- Two-channel equations with perfect-sink surface `c_b(0)=c_gb(0)=0` and no-flux far boundary.
- `a_bg=4/G`, `f_gb=2 delta/G`, `k_bg=max(sqrt(D_b/(pi*t)),D_b/(G/2))`, fully conservative exact local exchange + implicit FV diffusion.
- Cr diffusivities from the user's ATH 2026 conference paper, evaluated at 1073.15 K, **transferred** to ORNL alloys without independent Ni-7/16/24Cr mobility measurement:
  - `D_b = 4.28e-4 exp(-285200/(RT)) = 5.62e-18 m2/s`
  - `D_gb = 4.85e-2 exp(-196200/(RT)) = 1.37e-11 m2/s`
- Grain size **assumed**: 3, 30, 240 µm. GB width **assumed**: 0.5 nm (plus 1 nm at G=30 µm). These are sensitivity cases only; 240 µm is not ORNL-measured.
- `rho = 8700 kg/m3` assumed constant, not measured in ORNL paper.
- Numerical domain 600 µm (for one-face, no-recession, semi-infinite approximation); graded finite-volume mesh, no-flux far side, dt=120 s. At Ni–16Cr, G=240 µm, delta=0.5 nm, 2614 h, dt=60 s gave 2.071 vs 2.032 mg/cm² for dt=120 s (1.9% difference), dt=30 s gave 2.092 (about 1% over dt=60 s). Domain length 600 vs 1200 µm gave negligible change at dt=1200 s. Time-step errors on the most demanding G=3 µm case may differ, so those runs should be treated as sensitivity estimates.

## Key limitations

1. Grain size and GB width not measured on ORNL samples; result is **sensitivity analysis**, not fully parameter-independent validation.
2. Model assumes a permanent zero-Cr concentration at the exterior surface, but EDS near-surface Cr values are nonzero in Figure 2.
3. Experiments show Ni–7Cr and Ni–16Cr *lower* inferred Cr loss at 2614 h than at 1625 h; this might reflect heterogeneity or measurement variability. The model, as formulated, cannot reverse the cumulative Cr release.
4. The paper's own computational model *fits a surface Cr flux law from measured EDS profiles* (section 3.2); do not confuse that boundary-calibrated result with an independent prediction.
5. Literature diffusivity correlations are not necessarily the true transport parameters for each composition; 800°C may also involve chemical-potential gradients and evolving salt chemistry.
6. No attempted fit of grain size or diffusivity to measured Cr loss.

## Run

`python run_ornl2021.py` (requires numpy/scipy/matplotlib)

## Outputs

- `results.csv`: 36 comparison rows across all compositions/time points/geometry assumptions.
- `experimental_fig4_estimates.csv`: approximate values manually read from published Figure 4.
- `parameters.json`: provenance, equations and assumptions.
- `*_history.csv`, `*_profile.csv`: model time histories and concentration profiles (individual channels and GB-volume-weighted average).
- `comparison_mass_loss.png`: complete sensitivity figure.
- `coarse_grain_comparison.png`: visually focused G=240 µm comparison.
- `comparison_profiles.png`: model profiles; no digitized EDS overlay.