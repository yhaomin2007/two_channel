# Three-dataset validation of the two-channel Ni–Cr corrosion model

Release prepared 2026-11-24. This package is **additive** to the existing
[yhaomin2007/two_channel](https://github.com/yhaomin2007/two_channel)
repository. It preserves the model and separates observations from illustrative assumptions.

## Directory map

- `validation/UW_ATH/`: pointers to the original UW–Madison ATH benchmark and Ni–5Cr / Ni–20Cr archives in the existing repository.
- `validation/ORNL2021/`: reproducible standalone solver, 36 comparison rows, all time histories / profiles, and model-to-figure comparison plots.
- `validation/NCSU_INL2026/`: 2026 exploratory code, original / 300-s / 60-s time-step output cases, EDS attack-depth comparisons, and GB profiles.
- `reports/`: complete technical report (DOCX, PDF), presentation (PPTX), and supporting figures.
- `references/`: provenance, source links, and publication details.

## Model

Two Cr-transport channels (bulk and GB), connected by exchange:
`a_bg=4/G`, `f_gb=2 delta/G`,
`k_bg^eff(t)=max(sqrt(D_b/(pi t)),2 D_b/G)`.
A **perfect-sink surface** is imposed on both channels; there is no surface recession,
grain-boundary migration, evolving porosity, or explicit redox reaction.

ATH transferred Arrhenius inputs:
- `D_b=4.28e-4 exp(-285200/(R T))` m²/s
- `D_gb=4.85e-2 exp(-196200/(R T))` m²/s
- `R=8.314462618 J/(mol K)`

## Scientific comparison status

- **UW–Madison ATH:** primary original baseline; see the previously committed case archives and paper.
- **ORNL 2021:** `Ni–7Cr`, `Ni–16Cr`, `Ni–24Cr` at 800 °C and 522/1625/2614 h. Figure 4 Cr-specific experimental losses were **visually estimated**, not source CSV measurements. Grain sizes 3,30,240 µm and GB widths 0.5/1 nm are assumed sensitivities. The 240 µm comparison is NOT an independently measured grain size.
- **NCSU/INL 2026:** Ni–19Cr–5Fe plus minor Cu/Si/Ti is **not binary Ni–Cr**. EDS attack depths 22.0±3.4 / 28.0±10.1 / 83.8±26.2 µm at 30/240/500 h are compared to a model-defined GB depletion threshold. These are **non-equivalent depth metrics**, and the solver had time-step sensitivity. NCSU cases are exploratory rather than independent, numerically converged validation.

All model transport coefficients are transferred from ATH; none were fitted to
these experiments. The differences cannot be attributed solely to transport
without independently measured grain size/GB mobility and a consistent EDS metric.

## Reproduction

```
python -m pip install numpy scipy matplotlib
cd validation/ORNL2021 && python run_ornl2021.py
cd ../NCSU_INL2026 && python scripts/run_ncsu_inl_dt60.py
```

NCSU scripts were corrected to write within this package using paths relative to their own script locations. Check the `inputs.json` and README before interpreting the output.

## Repository integration

Unzip this package at the root of `two_channel`, then copy or merge its
`validation/`, `reports/`, and `references/` subfolders. Paths are organized
so that pre-existing original cases are **not** overwritten.

No third-party publisher full-text PDFs are bundled here.
