# Three-dataset validation report — extracted text

> For formatting, plots, and equations, use the original DOCX/PDF in the companion release archive. This is a text extraction, not the original report.

<PARSED TEXT FOR PAGE: 1 / 6>
Two-Channel Cr Depletion Model
Model formulation, three-program validation and engineering screening scope
Technical assessment | 24 November 2026 | MOSCATO / Ni–Cr-focused model

Prepared from the ATH 2026 model paper, Pillai et al. (2021), Gentile et al. (2026), and archived two-channel
calculation outputs. This is a technical synthesis, not a new experimental study.



Executive summary
The two-channel model explicitly represents axial chromium transport in grain interiors and in a fast grain-
boundary (GB) network, with a time-dependent bulk-to-GB exchange closure. Its principal intended use is rapid,
standardized screening of diffusion-controlled Cr depletion in Ni–Cr alloys under an idealized perfect-sink surface
condition.

Three research programs supply complementary evidence: (1) UW–Madison Ni–5Cr/Ni–20Cr experiments and
companion phase-field benchmarks reported in the ATH paper; (2) ORNL 2021 binary Ni–7Cr/Ni–16Cr/Ni–24Cr
long-duration KCl–MgCl₂ immersions with Cr-specific loss inferred from EDS profiles; and (3) NCSU/INL 2026 Ni–
19Cr–5Fe-based passive immersions with measured EDS attack depths and GB-character observations. The third
alloy contains Fe and minor solutes and is an applicability check, not strict binary validation.

Overall, the calculations reproduce important trends and generally plausible magnitudes without fitting diffusion
coefficients to each corrosion dataset. The evidence supports the transport framework as a screening model; it
does not establish salt-independent prediction of physical recession, void growth, or arbitrary multicomponent
corrosion.



1. Model scope and equations




Figure 1. Schematic of the two-channel approximation: parallel axial paths and exchange from the bulk
reservoir toward fast grain boundaries. Conceptual diagram created for this report.
Let cb(x,t) and cgb(x,t) denote chromium molar concentrations in the bulk and GB channels, and fbV and fgbV
their volume fractions. The governing conservation laws are:

fbV ∂cb/∂t = ∂x(fbV Db ∂x cb) − Γbg

fgbV ∂cgb/∂t = ∂x(fgbV Dgb ∂x cgb) + Γbg

Γbg = abg kbg,eff(t) (cb − cgb);   abg = 4/G;   fgbV = 2δgb/G;   fbV = 1 − fgbV.

kbg,eff(t) = max[ √(Db/(π t)), Db/(0.5 G) ].



                            MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 1
<PARSED TEXT FOR PAGE: 2 / 6>
At the exposed alloy surface x = 0, cb = cgb = 0 (perfect Cr sink). At the far boundary x = L, both normal gradients
vanish. Both channels initially contain the same homogeneous Cr concentration. Surface fluxes are added with
volume-fraction weighting to obtain Cr-specific cumulative loss; physical coupon recession is not modeled.

Diffusion parameters carried over from the ATH model
Db = 4.28 × 10⁻⁴ exp[−285,200/(RT)] m²/s; Dgb = 4.85 × 10⁻² exp[ −196,200/(RT)] m²/s; R = 8.314 J mol⁻¹ K⁻¹.

 Temperature                  Db (m²/s)                     Dgb (m²/s)                    Use

 700°C (973 K)                2.18 × 10⁻¹⁹                  1.41 × 10⁻¹²                  UW; NCSU/INL transfer
 800°C (1073 K)               5.62 × 10⁻¹⁸                  1.37 × 10⁻¹¹                  ORNL transfer

These correlations were reported in the ATH paper based on Bhave et al. They are not measured for every alloy
and microstructure represented here. Transferability of especially Dgb is a major uncertainty. For screening,
grain size and GB character should be independently documented whenever possible.



2. Three experimental programs and comparison status
 Program                      Material / environment        Metric                        Evidence status

                              Ni–5Cr, Ni–20Cr; 700°C;
                                                            Cr mass-loss histories;       Original benchmark in
                              FLiBe-related
 UW–Madison / ATH                                           bulk/GB Cr profiles at        ATH paper; quantitative
                              benchmark; grain sizes
                                                            1000 h                        figures
                              16.22 and 4.64 μm
                              Ni–7Cr, Ni–16Cr, Ni–24Cr                                    Independent immersion;
                                                            Cr-specific mass loss from
 ORNL 2021                    (wt.%); 800°C; purified                                     assumed grain size in
                                                            EDS profile integration
                              KCl–MgCl₂; 522–2614 h                                       model
                                                                                          Independent
                              Nominal Ni–19Cr–5Fe
                                                            EDS-defined attack depth;     qualitative/mechanistic
 NCSU/INL 2026                with Cu/Si/Ti; 700°C;
                                                            EBSD-GB character             and provisional depth
                              NaCl–MgCl₂; 30–500 h
                                                                                          comparison




3. UW–Madison / ATH baseline
The ATH benchmark evaluated Ni–5Cr (G = 16.22 μm; ρ = 8700 kg/m³) and Ni–20Cr (G = 4.64 μm; ρ = 8570 kg/m³),
using δgb = 0.5 nm and the same diffusion correlations at 700°C. Cr transport data and comparison with a
previous phase-field model and experimental data were adopted from the referenced Bhave/Zheng investigations.

The ATH paper reports reasonable mass-loss agreement and substantially improved GB-depletion representation
relative to a one-dimensional effective-diffusivity treatment. The present report reproduces the original figures
rather than inventing numerical points not explicitly tabulated in the source.




                          MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 2
<PARSED TEXT FOR PAGE: 3 / 6>
Figure 2. Ni–5Cr mass-loss history and 1000-h Cr profiles; reproduced from the user-supplied ATH 2026
paper, Figure 3.




Figure 3. Ni–20Cr mass-loss history and 1000-h Cr profiles; reproduced from the user-supplied ATH 2026
paper, Figure 4.
Interpretation: the two-channel model resolves distinct GB and grain-interior depletion. For Ni–20Cr the original
paper notes a potentially anomalous experimental mass-loss point; agreement should be characterized as trend-
level rather than exact pointwise reproduction.



4. ORNL 2021 independent binary Ni–Cr benchmark
Pillai et al. tested binary Ni–7Cr, Ni–16Cr and Ni–24Cr (measured 7.0, 16.1 and 23.2 wt.% Cr) in purified KCl–MgCl₂
(68:32 mol.%) at 800°C, with Mo capsules, 28 g salt and 6 × 12 × 1.5 mm coupons. Cr-specific loss was computed by
the authors from integrated EDS-depletion profiles. The three times compared are 522, 1625 and 2614 h (published
Figures 2–4).

For the independent transport-parameter calculation, the ATH correlations were evaluated at 800°C, with GB
width δgb = 0.5 nm and illustrative G = 240 μm. Crucially, ORNL did NOT report a measured numerical grain size
for these binary specimens, so 240 μm must not be described as their actual grain size.

 Alloy                  h                      ORNL Cr loss*           Model Cr loss          Pred./obs.

 Ni-7Cr                 522                    0.59                    0.33                   0.56
 Ni-7Cr                 1625                   0.82                    0.66                   0.81
 Ni-7Cr                 2614                   0.64                    0.88                   1.38
 Ni-16Cr                522                    0.65                    0.76                   1.17


                            MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 3
<PARSED TEXT FOR PAGE: 4 / 6>
 Ni-16Cr                1625                    1.02                   1.52                     1.49
 Ni-16Cr                2614                    0.93                   2.03                     2.18
 Ni-24Cr                522                     0.71                   1.10                     1.55
 Ni-24Cr                1625                    1.79                   2.19                     1.22
 Ni-24Cr                2614                    2.04                   2.93                     1.44

* ORNL loss approximate reading of Figure 4; both losses in mg/cm². These points are not an author-
supplied digitized dataset. Model: G = 240 μm, δgb = 0.5 nm (assumed).




Figure 4. Comparison of model Cr-specific loss with approximate ORNL Figure 4 estimates. Curves serve as
illustrative parameter-transfer comparison, not fully independent validation of the unreported G.
At 1625 h, the predicted/observed ratios are approximately 0.81, 1.49 and 1.22 for Ni–7Cr, Ni–16Cr and Ni–24Cr.
The trend of greater Cr loss at higher nominal Cr content is reproduced. At 2614 h, the model overpredicts Ni–16Cr
and Ni–24Cr; the experiment also shows apparent leveling or a decrease for Ni–7Cr and Ni–16Cr that a cumulative
perfect-sink model cannot reproduce.

Grain-size sensitivity is substantial: at 2614 h, the modeled Ni–16Cr Cr loss is approximately 2.03 mg/cm² (G = 240
μm), 7.30 mg/cm² (G = 30 μm), and 32.37 mg/cm² (G = 3 μm). Actual specimen microstructure is therefore the key
missing input.



5. NCSU/INL 2026 independent GB-attack benchmark
Gentile et al. exposed Goodfellow Ni–19Cr–5Fe–0.5Cu–0.5Si–0.4Ti (nominal wt.%) coupons, 10 × 5 × 1 mm, in
purified NaCl–MgCl₂ at 700°C for 30, 240 and 500 h using glassy-carbon crucibles. EBSD/EDS indicates preferential
Cr depletion at high-angle GBs; lower-angle and Σ3 boundaries are generally less susceptible.

The published quantitative metric is EDS-defined corrosion/attack penetration. It is NOT integrated Cr-specific
mass loss and does not share a unique threshold with the model. For an illustrative assumed G = 100 μm, δgb = 0.5
nm, the model-derived GB depths are shown at two depletion thresholds: 50% and 10% below initial GB Cr. All
numbers are exploratory, with no parameter fitting.

                               Measured EDS attack
 Time (h)                                                  Model GB 50% (μm)             Model GB 10% (μm)
                               (μm)

 30                            22.0 ± 3.4                  12.8                          48.2
 240                           28.0 ± 10.1                 23.1                          82.6
 500                           83.8 ± 26.2                 28.1                          95.7




                          MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 4
<PARSED TEXT FOR PAGE: 5 / 6>
Figure 5. Experimental EDS attack depth vs model-defined GB depletion depths. The different definitions
prevent direct error-score interpretation. Model values use the archived 60 s integration output.
At 240 h, the 50%-GB threshold result (23.1 μm) lies within the reported experimental 28.0 ± 10.1 μm interval; at
500 h the 50%-threshold prediction (28.1 μm) falls below the experimental 83.8 ± 26.2 μm interval, while the 10%-
threshold depth is 95.7 μm. This large threshold sensitivity underlines the need for a common EDS-to-model
detection criterion before claiming quantitative penetration accuracy.

The archived exploratory implementation also showed material time-step dependence, especially at early times. A
stiff, fully coupled or otherwise converged time integration and spatial-grid check remain necessary. Moreover, Fe
and trace solutes change both thermodynamics and diffusion relative to binary Ni–Cr.



6. Cross-program synthesis and interpretation
 Aspect                                                    Assessment

                                                           GBs act as fast axial pathways supplied by slower
 Transport mechanism                                       grain-interior diffusion; consistent with
                                                           microstructure observations.
                                                           UW and ORNL support encouraging magnitude/trend
 Quantitative Cr loss
                                                           comparisons, with qualifications noted above.
                                                           NCSU/INL supports mechanism and provisional
 Penetration depth
                                                           magnitude; metrics are not directly identical.
                                                           Transferred diffusion correlations and geometric
 No case-specific fitting                                  sensitivity inputs; apparent agreement alone does not
                                                           establish independent grain-size knowledge.
                                                           cb = cgb = 0 is a standardized perfect sink, not a
 Idealized boundary                                        representation of changing salt redox or product
                                                           films.

The datasets span two nominally binary Ni–Cr experimental programs and a third Fe-containing model alloy.
Their independence at the institutional/program level strengthens confidence in the underlying GB-transport



                            MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 5
<PARSED TEXT FOR PAGE: 6 / 6>
mechanism, but uncertainty in material pedigree, GB character, initial grain sizes, surface chemistry and
measurement metrics prevents a universal accuracy claim.

Uncertainty and applicability boundary
Primary uncertainties: (i) Db/Dgb versus alloy composition and processing; (ii) grain-size distributions, GB width
and topology; (iii) distinction between weight loss, Cr-specific dissolved mass, EDS integrated depletion and
deepest attack; (iv) finite salt redox and chemical activity; (v) porosity, surface recession, DIGM and local GB
penetration; (vi) mesh/time-step convergence for the exploratory model outputs.

Accordingly, the recommended near-term scope is diffusion-controlled Cr depletion in Ni–Cr alloys using known
microstructure and independently sourced diffusivities. Use the current results for standardized, comparative
screening under a common perfect-sink condition—not direct lifetime certification in arbitrary salts. NCSU/INL is
retained as a mechanistic cross-check of this Ni–Cr core model rather than justification for general
multicomponent capability.



7. Recommended closure of the present development phase
Freeze the two-channel governing equations, exchange closure and perfect-sink boundary for the current Ni–Cr
screening version. Archive the three datasets and provenance separately. Resolve numerical convergence, obtain
independent grain sizes for ORNL and NCSU/INL if possible, and standardize the definition of GB penetration
depth. Future versions may incorporate GB-character weighting, surface recession, porous evolution and finite
salt chemistry only when corresponding measurements are available.



References and data provenance
[1] Yuan, H., and Hoyt, N., “Development of a Two-channel Structural Corrosion Model in MOSCATO,” ATH 2026
conference manuscript (user-provided PDF), Figs. 3–4 and Table II.

[2] Pillai, R., Raiman, S.S., and Pint, B.A., “First steps toward predicting corrosion behavior of structural materials
in molten salts,” Journal of Nuclear Materials 546 (2021) 152755. https://doi.org/10.1016/j.jnucmat.2020.152755

[3] Gentile, R., Hawkins, L., Woods, M., Gakhar, R., Murray, D., and He, L., “Corrosion Response of Ni-19Cr-5Fe in
Molten NaCl-MgCl₂ Salt,” JOM 78 (2026), 2410–2420. https://doi.org/10.1007/s11837-025-08019-1

[4] Bhave, C.V., Zheng, G., Sridharan, K., Schwen, D., and Tonks, M.R., electrochemical mesoscale corrosion
modeling study; diffusion correlations as quoted by [1].

[5] Archived project calculation exports: ORNL2021_two_channel/results.csv and experimental_fig4_estimates.csv;
NCSU_INL_2026_two_channel_dt60/results.csv. Assumed G and δgb are model inputs; do not represent measured
specimen microstructure.




                           MOSCATO | Two-channel Ni–Cr assessment • 24 Nov 2026 • 6