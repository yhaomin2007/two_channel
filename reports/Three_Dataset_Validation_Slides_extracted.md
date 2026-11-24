# Three-dataset validation presentation — slide text

> This is searchable extracted slide text, not the editable PowerPoint. The PPTX is in the companion release archive.

<PARSED TEXT FOR PAGE: 1 / 12>
[Presentation metadata from ppt/presentation.xml]
Canvas width: 12192000 EMU; canvas height: 6858000 EMU; 914400 EMU per inch.

MOSCATO  |  TECHNICAL ASSESSMENT
Two-Channel Chromium
Depletion Model
Three experimental programs • UW–Madison • ORNL • NCSU/INL
Ni–Cr-focused diffusion-controlled corrosion screening
24 November 2026  |  Based on ATH 2026 and published independent experiments

Speaker notes:
1
<PARSED TEXT FOR PAGE: 2 / 12>
MODEL VALIDATION
Three complementary datasets — one transport framework
UW–Madison
Original binary Ni–5Cr / Ni–20Cr benchmark
ORNL 2021
Independent binary Ni–7/16/24Cr long-time dataset
NCSU / INL 2026
Fe-containing Ni–Cr model alloy; GB penetration
•
Diffusion parameters transferred from ATH; no fit to each corrosion experiment.
•
UW and ORNL: Cr-loss trends and magnitude.  NCSU/INL: spatial penetration and GB character.
•
Conclusion: useful Ni–Cr screening model, not a universal salt-corrosion predictor.
Sources: Yuan & Hoyt (ATH 2026); Pillai et al. (JNM 2021); Gentile et al. (JOM 2026)
02

Speaker notes:
2
<PARSED TEXT FOR PAGE: 3 / 12>
MODEL VALIDATION
Two-channel physics and closure
Bulk:   fb ∂cb/∂t = ∂x(fb Db ∂x cb) − Γbg
GB:    fgb ∂cgb/∂t = ∂x(fgb Dgb ∂x cgb) + Γbg
Γbg = (4/G) kbg(t) (cb − cgb)     |     fgb = 2δgb/G
Perfect Cr sink at the exposed surface; finite-grain cutoff in exchange coefficient.
Source: ATH 2026 two-channel model, Sections 2.1–2.3
03

Speaker notes:
3
<PARSED TEXT FOR PAGE: 4 / 12>
MODEL VALIDATION
One diffusion parameterization across programs
Db = 4.28 × 10⁻⁴ exp[−285200/(RT)]  m²/s
Dgb = 4.85 × 10⁻² exp[−196200/(RT)]  m²/s
700 °C
Db = 2.18 × 10⁻¹⁹   |   Dgb = 1.41 × 10⁻¹² m²/s
800 °C
Db = 5.62 × 10⁻¹⁸   |   Dgb = 1.37 × 10⁻¹¹ m²/s
Unknown specimen grain size is an explicit assumption, not a fitted material measurement.
Source: diffusion correlations reported in ATH 2026, based on Bhave et al.
04

Speaker notes:
4
<PARSED TEXT FOR PAGE: 5 / 12>
MODEL VALIDATION
UW–Madison baseline | Ni–5Cr and Ni–20Cr
Ni–5Cr: G = 16.22 μm
Ni–20Cr: G = 4.64 μm
ATH figures compare Cr-loss histories and 1000-h bulk/GB Cr profiles against experiments and other models.
Source: user-provided ATH 2026 paper, Figs. 3–4 (reproduced)
05

Speaker notes:
5
<PARSED TEXT FOR PAGE: 6 / 12>
MODEL VALIDATION
ORNL 2021 | measured Cr-specific loss
At 1625 h: predicted / measured ≈ 0.81 (Ni–7Cr), 1.49 (Ni–16Cr), 1.22 (Ni–24Cr).
Conditions: 800°C · purified KCl–MgCl₂ · Mo capsule · 522–2614 h.
Important: G = 240 μm and δgb = 0.5 nm are assumed. Experimental points are estimated from published Figure 4.
Source: Pillai, Raiman & Pint, JNM 546 (2021) 152755, Figs. 2–4
06

Speaker notes:
6
<PARSED TEXT FOR PAGE: 7 / 12>
MODEL VALIDATION
ORNL sensitivity | parameter transfer, not parameter fitting
2.03
mg/cm²   Ni–16Cr, 2614 h, G=240 μm
7.30
mg/cm²   Ni–16Cr, 2614 h, G=30 μm
32.37
mg/cm²   Ni–16Cr, 2614 h, G=3 μm
•
The unreported ORNL grain sizes dominate uncertainty in absolute predictions.
•
Model reproduces the composition ranking in Cr release; experiment levels off at long times.
•
Never identify assumed G as a measured property of the ORNL coupons.
Source: archived ORNL two-channel calculation outputs; Figure 4 experimental estimates
07

Speaker notes:
7
<PARSED TEXT FOR PAGE: 8 / 12>
MODEL VALIDATION
NCSU / INL 2026 | GB corrosion penetration
Measured EDS depth
30 h   22.0 ± 3.4 μm
240 h  28.0 ± 10.1 μm
500 h  83.8 ± 26.2 μm
Threshold mismatch
50%-GB and 10%-GB depths are model-defined, not identical to EDS attack depth.
Goodfellow Ni–19Cr–5Fe + minor solutes; 700°C; NaCl–MgCl₂.
Source: Gentile et al., JOM 78 (2026) 2410–2420, Table II
08

Speaker notes:
8
<PARSED TEXT FOR PAGE: 9 / 12>
MODEL VALIDATION
Evidence is promising, but validation quantities differ
UW–Madison
Measured Cr loss / profiles
Original benchmark; grain sizes documented
ORNL 2021
Integrated EDS-derived Cr loss
Good order-of-magnitude; G assumed
NCSU/INL 2026
EDS attack depth + EBSD
GB pathway evidence; depth thresholds differ
Key distinctions: total weight loss ≠ Cr-specific loss ≠ deepest attack depth
09

Speaker notes:
9
<PARSED TEXT FOR PAGE: 10 / 12>
MODEL VALIDATION
What the model does — and does not — claim
•
Models: Cr diffusion in grains and fast GB pathways, plus time-dependent transfer.
•
Uses: inexpensive, standardized relative Ni–Cr alloy screening under a perfect-sink surface.
•
Does not resolve: voids, surface recession, DIGM, finite salt redox, or protective films.
•
Primary unknowns: GB character, grain size, effective Dgb, measurement definitions.
NCSU/INL is an applicability check outside strictly binary Ni–Cr.
Scope conclusion of this three-program assessment
10

Speaker notes:
10
<PARSED TEXT FOR PAGE: 11 / 12>
MODEL VALIDATION
Development phase: close the Ni–Cr-focused model
Freeze
Keep current governing equations and perfect sink
Document
Trace material pedigree and assumptions explicitly
Verify
Finish numerical convergence and common depth criteria
Apply
Use as comparative screening, not universal lifetime forecast
Three distinct programs provide complementary evidence for GB-mediated Cr depletion.
Recommended closure of current research phase
11

Speaker notes:
11
<PARSED TEXT FOR PAGE: 12 / 12>
REFERENCES
Sources and quantitative provenance
•
Yuan & Hoyt, “Development of a Two-channel Structural Corrosion Model in MOSCATO,” ATH 2026 manuscript.
•
Pillai, Raiman & Pint, Journal of Nuclear Materials 546 (2021) 152755. DOI: 10.1016/j.jnucmat.2020.152755.
•
Gentile et al., JOM 78 (2026), 2410–2420. DOI: 10.1007/s11837-025-08019-1.
•
Numerical comparison data: archived ORNL2021_two_channel/results.csv and NCSU_INL_2026_two_channel_dt60/results.csv.
•
ORNL experimental Cr loss = approximate readings from Fig. 4; NCSU measured depth = reported Table II; model depth thresholds are not the same metric.
Technical report includes detailed tables, uncertainty discussion and equations
12

Speaker notes:
12