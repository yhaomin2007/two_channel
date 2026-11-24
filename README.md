# Two-channel structural corrosion model — validation archive

This project collects the ATH 2026 two-channel structural corrosion model, original Ni–Cr test cases, standardized corrosion-screening proposal, independent validation experiments, and a source-traceable Cr diffusion-coefficient database.

## Repository layout

- `references/` — conference paper; Wang (2016) and Doniger (2023) experimental papers.
- `original_cases/` — Ni–5Cr and Ni–20Cr original archives.
- `proposal/` — standardized alloy-screening assessment proposal.
- `validation/Wang2016/` — six standalone simulations and comparison outputs.
- `validation/Two_Paper_Validation/` — experimental comparison and Doniger table.
- `diffusion_database/` — diffusion coefficient records, provenance, and Python scripts.
- `review_figures/` — original review figures.

## Important caveats

The initial Wang cases used the Bhave/Yuan diffusion correlations across alloy compositions and **must not be described as independently validated**. Cr diffusion in bulk and grain boundaries is alloy-dependent; the database records coefficient type and source so future cases can use defensible alloy-specific values. Doniger's observed total mass loss includes mechanisms beyond Cr-only perfect-sink depletion.

## Reproduction

```bash
pip install numpy scipy matplotlib
python validation/Wang2016/run_wang2016.py
```

**Status:** Initial repository setup. A complete file bundle is being prepared separately; do not assume that all binary references or case outputs have been pushed until they appear in the repository.