#!/usr/bin/env bash
set -euo pipefail

# Create a fully isolated venv for Demo.ipynb and register it as a Jupyter kernel.
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$DEMO_DIR/.venv_demo"
REQ_FILE="$DEMO_DIR/requirements.txt"
KERNEL_NAME="demo_venv"
KERNEL_DISPLAY="Demo Venv (06_demo)"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "$REQ_FILE"
python -m ipykernel install --user --name "$KERNEL_NAME" --display-name "$KERNEL_DISPLAY"

echo ""
echo "Setup complete."
echo "1) Open 06_demo/Demo.ipynb"
echo "2) Select kernel: $KERNEL_DISPLAY"
echo "3) Run all cells in order"
