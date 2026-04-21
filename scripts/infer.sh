#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$CODE_DIR/.." && pwd)"

DEMO_NOTEBOOK="$REPO_ROOT/06_demo/Demo.ipynb"
ARTIFACT_DIR="$SCRIPT_DIR/artifacts"
OUT_NOTEBOOK="$ARTIFACT_DIR/Demo_infer_executed.ipynb"

mkdir -p "$ARTIFACT_DIR"

if ! command -v jupyter >/dev/null 2>&1; then
  echo "Error: jupyter command not found."
  echo "Install it with: python -m pip install jupyter nbconvert"
  exit 1
fi

if [[ ! -f "$DEMO_NOTEBOOK" ]]; then
  echo "Error: demo notebook not found at $DEMO_NOTEBOOK"
  exit 1
fi

echo "Executing demo notebook for inference-style run."
echo "Input:  $DEMO_NOTEBOOK"
echo "Output: $OUT_NOTEBOOK"

jupyter nbconvert \
  --to notebook \
  --execute "$DEMO_NOTEBOOK" \
  --output "$(basename "$OUT_NOTEBOOK")" \
  --output-dir "$ARTIFACT_DIR" \
  --ExecutePreprocessor.timeout=-1

echo "Done."
