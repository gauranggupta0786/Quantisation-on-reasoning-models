# 05_results

This folder packages the final quantitative outputs, ablations, figures, and verification logs for the project.

## Files

- `main_results.csv`
  - Compact summary of the main quantitative results used in the report/presentation.
  - Includes phase-level headline metrics from the notebook's final comparison section and Phase 8 report tables.

- `ablations.csv`
  - Consolidated ablation studies from:
    - Phase 5 decoding-parameter sweeps (GSM8K + GPQA)
    - Phase 7 quantization configuration comparison (NF4 vs NF4+KV)
    - Phase 7 vs Phase 8 method comparison (QLoRA SFT vs GRPO)

- `figures/`
  - Exact plot files, result tables, and qualitative/raw-eval CSVs used for reporting and presentation.

- `logs/`
  - Training/evaluation summary logs and trainer state useful for verification.

## Data Provenance

- Notebook-derived headline values were taken from `DL23.ipynb` (Phase 6 comparison arrays/summary text).
- Experiment tables and logs were pulled from `Quantization_Reasoning_Project/...` CSV/PNG/JSON artifacts.

## Notes

- Percentage fields are stored in percent units (for example, `76.67` means 76.67%).
- `samples` reflects the evaluation subset size for each reported row.
