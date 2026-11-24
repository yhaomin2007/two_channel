# Two-channel structural corrosion model — validation archive

This repository organizes the ATH 2026 two-channel structural corrosion model, original Ni–Cr benchmark archives, standardized screening proposal, external experimental papers, preliminary Wang (2016) validation simulations, two-paper comparisons, and the Cr diffusion coefficient database.

## Organization

- `references/`: ATH 2026 conference paper; Wang et al. (2016) and Doniger et al. (2023) uploaded PDFs. Publisher copyright applies; review redistribution permissions before making repository public.
- `original_cases/`: Original Ni–5Cr and Ni–20Cr `.rar` test archives.
- `proposal/`: Standardized Cr-depletion assessment research proposal.
- `validation/Wang2016/`: Standalone FV two-channel solver and six-case calculation outputs, including mass-loss histories and profiles.
- `validation/Two_Paper_Validation/`: Wang experimental comparison and Doniger Table 3 digitized measurements.
- `diffusion_database/`: Source traceability, Arrhenius parameters, input mapping and Python selectors.
- `review_figures/`: Review figures extracted from the project conference paper.

## Scientific caution

The Wang simulations use the **Bhave/Yuan reference Arrhenius values** across all compositions and *have not* been re-run with independently established alloy-specific diffusion coefficients. They are preliminary predictions, not validated results. Additional chemical-interdiffusion/GB triple-product research is required before claiming predictive validation. The Doniger mass loss includes phenomena not captured by Cr-only perfect-sink modeling (including surface recession and other elements).

## Run the Wang cases

```bash
pip install numpy scipy matplotlib
python validation/Wang2016/run_wang2016.py
```

These cases originally had only literature-review-based measurements available. The experimental-comparison CSV was later created from the full Wang PDF and should supersede the early comparison annotations in the solver.

## Data provenance

`FILE_MANIFEST_SHA256.csv` records SHA-256 hashes and sizes for auditability. This archive preserves originally uploaded materials rather than silently changing their content.
