# Scripts in 03_code/scripts

This folder contains runnable wrappers around the notebook-based workflow, plus copied demo resources.

## Runnable Entry Points

- `train.sh`
  - Executes `../src/DL23.ipynb` headlessly via `jupyter nbconvert`.
  - Produces `scripts/artifacts/DL23_train_executed.ipynb`.

- `eval.sh`
  - Reads and summarizes key evaluation CSV files.
  - Optional `--run-notebook` executes training/eval notebook first.

- `infer.sh`
  - Executes `../../06_demo/Demo.ipynb` headlessly via `jupyter nbconvert`.
  - Produces `scripts/artifacts/Demo_infer_executed.ipynb`.

- `demo.sh`
  - Runs `setup_demo_venv.sh`.
  - Launches `../../06_demo/Demo.ipynb` in Jupyter.
  - Use `--setup-only` to only prepare the environment.

## Copied Supporting Files

- `setup_demo_venv.sh` (copied from `06_demo/`)
- `requirements.txt` (copied from `06_demo/`)
- `demo_requirements.txt` (same dependency list, alternate name)
- `demo_instructions.md` (copied from `06_demo/`)
- `sample_inputs.txt` (copied from `06_demo/`)

These copied files are included to keep demo launch scripts self-contained inside `03_code/scripts`.
