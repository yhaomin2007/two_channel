# Three-dataset Ni–Cr corrosion validation (2026-11-24)

This note indexes the three experimental programs assessed with the existing two-channel diffusion model. The original ATH conference paper and Ni–5Cr / Ni–20Cr case archives are already in the repository. The complete additional case outputs, scripts, report (DOCX/PDF), and slides (PPTX) are distributed in the companion release archive `two_channel_three_dataset_release.zip`.

## Governing assumptions

Two Cr channels: grain interior and grain boundary. Volumetric grain-boundary fraction `f_gb=2δ/G`, exchange area `a_bg=4/G`, effective exchange coefficient `k_bg=max(sqrt(D_b/(πt)),2D_b/G)`. Both channels have a zero-Cr surface condition (perfect sink); far-field zero flux. No surface recession, explicit salt electrochemistry, porosity, or grain-boundary migration.

Transferred ATH diffusivity correlations in SI units:

- `D_b = 4.28e-4 * exp(-285200/(R*T))`
- `D_gb = 4.85e-2 * exp(-196200/(R*T))`
- `R=8.314462618 J/(mol*K)`, temperature `T` in kelvin.

## Cases and quantitative comparisons

### UW–Madison ATH 2026

Original primary baseline: Ni–5Cr and Ni–20Cr at 700 °C with documented grain-size inputs. See existing `original_cases/Ni-5Cr.rar`, `original_cases/Ni-20Cr.rar`, and the ATH PDF in `references/`. Original benchmark results are not altered here.

### ORNL 2021 — Pillai, Raiman, Pint

*Journal of Nuclear Materials* 546 (2021) 152755; DOI [10.1016/j.jnucmat.2020.152755](https://doi.org/10.1016/j.jnucmat.2020.152755).
Ni–7Cr (7.0 wt.% Cr), Ni–16Cr (16.1 wt.%), Ni–24Cr (23.2 wt.%); 800 °C, purified KCl–MgCl₂, sealed Mo capsules, 522/1625/2614 h.

Reported Cr loss was calculated by integrating experimental EDS concentration profiles, **not** measured as total specimen mass loss. Values read approximately from Figure 4 (mg/cm²):

| Alloy | h | Approx experiment | Model (G=240 µm, δ=0.5 nm) |
|---|---:|---:|---:|
| Ni–7Cr | 522 | 0.59 | 0.33 |
| Ni–7Cr | 1625 | 0.82 | 0.66 |
| Ni–7Cr | 2614 | 0.64 | 0.88 |
| Ni–16Cr | 522 | 0.65 | 0.76 |
| Ni–16Cr | 1625 | 1.02 | 1.52 |
| Ni–16Cr | 2614 | 0.93 | 2.03 |
| Ni–24Cr | 522 | 0.71 | 1.10 |
| Ni–24Cr | 1625 | 1.79 | 2.19 |
| Ni–24Cr | 2614 | 2.04 | 2.93 |

**Critical:** G=240 µm and δ=0.5 nm are assumptions, not measurements on the ORNL specimens. No fit was carried out. Sensitivities include G=3, 30, 240 µm, δ=0.5/1 nm. `D_b=5.62e-18 m²/s`, `D_gb=1.37e-11 m²/s` at 800 °C. Earlier numerical time-step testing did not establish full convergence for all fine-grain cases.

### NCSU/INL 2026 — Gentile et al.

*JOM* 2026; DOI [10.1007/s11837-025-08019-1](https://doi.org/10.1007/s11837-025-08019-1).
Nominal Ni–19Cr–5Fe plus minor Cu, Si and Ti: **not binary Ni–Cr**. Goodfellow material, 700 °C NaCl–MgCl₂, conventional passive immersion.

| Time (h) | Experimental EDS attack depth (µm) | Exploratory model GB 50%-depletion depth (µm), G=100 µm |
|---:|---:|---:|
| 30 | 22.0 ± 3.4 | 12.8 |
| 240 | 28.0 ± 10.1 | 23.1 |
| 500 | 83.8 ± 26.2 | 28.1 |

**Critical:** Experimental EDS attack depth is not mathematically equivalent to the modeled 50%-GB-Cr-depletion depth. Mean grain size and effective GB width are not measured; model G=100 µm and δ=0.5 nm are illustrative assumptions. The operator-split code showed time-step dependence; results are **exploratory**, not fully numerically converged quantitative validation. Diffusion correlations are transferred from binary Ni–Cr to an Fe-containing alloy.

## Reproducibility and model scope

The companion release archive contains:
- `validation/ORNL2021/run_ornl2021.py`, parameters, results and histories;
- `validation/NCSU_INL2026/scripts/run_ncsu_inl*.py`, three time-step datasets, profiles, and plots;
- `reports/Two_Channel_NiCr_Three_Dataset_Validation_Report.docx/.pdf`;
- `reports/Two_Channel_NiCr_Three_Dataset_Validation_Slides.pptx`;
- README, source links and SHA-256 file manifest.

Only Cr-specific transport and depletion are predicted. The standardized perfect-sink framework is intended for comparative Ni–Cr alloy screening, **not** unconditional prediction of total corrosion mass loss under arbitrary salt chemistry.

Source publisher PDFs are not redistributed in the new release archive.