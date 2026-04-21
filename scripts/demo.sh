#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$CODE_DIR/.." && pwd)"
DEMO_NOTEBOOK="$REPO_ROOT/06_demo/Demo.ipynb"

SETUP_ONLY=false
if [[ "${1:-}" == "--setup-only" ]]; then
  SETUP_ONLY=true
fi

"$SCRIPT_DIR/setup_demo_venv.sh"

if [[ "$SETUP_ONLY" == "true" ]]; then
  echo "Demo environment setup complete."
  exit 0
fi

if ! command -v jupyter >/dev/null 2>&1; then
  echo "Error: jupyter command not found."
  exit 1
fi

echo "Launching demo notebook: $DEMO_NOTEBOOK"
jupyter notebook "$DEMO_NOTEBOOK"
