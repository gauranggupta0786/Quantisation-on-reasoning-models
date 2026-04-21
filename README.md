# 03_code: Reproducible Package for DL23.ipynb

This folder packages the main notebook workflow from `DL23.ipynb` into a clean handoff structure with:

- Source assets (`src/`) copied from the project.
- Runnable entry points (`scripts/`) for train/eval/infer/demo workflows.
- Main hyperparameter/config snapshots (`configs/`) extracted from `DL23.ipynb`.

## 1) Folder Layout

```
03_code/
  README.md
  src/
    DL23.ipynb
    outputs_math/
    outputs_science/
    Quantization_Reasoning_Project/
  scripts/
    README.md
    train.sh
    eval.sh
    infer.sh
    demo.sh
    setup_demo_venv.sh
    requirements.txt
    demo_requirements.txt
    demo_instructions.md
    sample_inputs.txt
  configs/
    phase7_qlora.yaml
    phase8_grpo.yaml
    runtime_environment.yaml
```

## 2) What `DL23.ipynb` Does

`src/DL23.ipynb` is the canonical end-to-end notebook for the quantization-on-reasoning study.

High-level phase map:

1. Phase 1 baseline: 8-bit baseline reference on GSM8K/GPQA.
2. Phase 2 degradation: aggressive 4-bit quantization and quality drop measurement.
3. Phase 4 recovery: QLoRA-based adapter recovery.
4. Phase 5 decoding ablations: decoding-time mitigations.
5. Phase 7: structured QLoRA training/evaluation pipeline and result exports.
6. Phase 8: GRPO pilot, reward shaping, comparison to Phase 7, report plots.
7. Demo section: side-by-side inference behavior and interpretation.

All notebook outputs are preserved in `src/DL23.ipynb` exactly as copied.

## 3) Environment Setup

### Option A: Main notebook environment (recommended)

Run from `03_code/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  torch pandas transformers peft bitsandbytes accelerate datasets trl \
  sentence-transformers matplotlib seaborn scikit-learn jupyter ipykernel
```

If you use Unsloth-specific paths in Phase 7, install Unsloth in this environment as needed.

### Option B: Demo-only environment

```bash
bash scripts/setup_demo_venv.sh
```

This creates `scripts/.venv_demo` and registers a Jupyter kernel for demo execution.

## 4) Dependency Versions Observed in `DL23.ipynb`

Observed runtime versions printed in notebook output:

- Python: 3.13.2
- CUDA: 12.8
- transformers: 5.5.0
- trl: 0.24.0
- peft: 0.19.1
- accelerate: 1.13.0
- datasets: 4.3.0
- bitsandbytes: 0.49.2

## 5) Hardware Used

Observed hardware output in notebook:

- GPU: NVIDIA H100 NVL
- GPU VRAM: 93.09 GB

Study framing in notebook text also discusses constrained settings (for example T4-class VRAM) as a target motivation for quantization.

## 6) Train Commands

### Interactive (recommended for research iteration)

```bash
jupyter lab src/DL23.ipynb
```

### Batch-style execution wrapper

```bash
bash scripts/train.sh
```

This executes the full notebook via `nbconvert` and writes an executed copy under `scripts/artifacts/`.

## 7) Evaluation Commands

### Summarize existing CSV outputs

```bash
bash scripts/eval.sh
```

### Re-run full notebook first, then summarize

```bash
bash scripts/eval.sh --run-notebook
```

## 8) Demo and Inference Commands

### Launch demo environment and open demo notebook

```bash
bash scripts/demo.sh
```

### Execute demo notebook headlessly (inference-style run)

```bash
bash scripts/infer.sh
```

## 9) Main Output Locations

- Phase 7 outputs:
  - `src/Quantization_Reasoning_Project/phase7_qlora_experiment/`
- Phase 8 outputs:
  - `src/Quantization_Reasoning_Project/phase8_grpo_experiment/`
- Aggregated results and plots from original workspace:
  - `../05_results/`

## 10) Reproducibility Notes

- Keep GPU/CUDA/toolchain close to notebook runtime for stable behavior.
- GRPO and generation workloads can be compute heavy; expect long runtimes.
- If kernels or dependencies change, re-run from clean environment to reduce drift.
