#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
NOTEBOOK="$CODE_DIR/src/DL23.ipynb"
ARTIFACT_DIR="$SCRIPT_DIR/artifacts"
OUT_NOTEBOOK="$ARTIFACT_DIR/DL23_train_executed.ipynb"

mkdir -p "$ARTIFACT_DIR"

if ! command -v jupyter >/dev/null 2>&1; then
  echo "Error: jupyter command not found."
  echo "Install it with: python -m pip install jupyter nbconvert"
  exit 1
fi

echo "Executing full DL23 notebook (train/eval/demo cells included)."
echo "Input:  $NOTEBOOK"
echo "Output: $OUT_NOTEBOOK"

jupyter nbconvert \
  --to notebook \
  --execute "$NOTEBOOK" \
  --output "$(basename "$OUT_NOTEBOOK")" \
  --output-dir "$ARTIFACT_DIR" \
  --ExecutePreprocessor.timeout=-1

echo "Done."
echo "Phase 7 outputs: $CODE_DIR/src/Quantization_Reasoning_Project/phase7_qlora_experiment"
echo "Phase 8 outputs: $CODE_DIR/src/Quantization_Reasoning_Project/phase8_grpo_experiment"
