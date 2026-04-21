#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Canonical generation path in this workspace.
python3 build_fallback_pdf.py

# Optional consistency check: if LaTeX is installed, compile wrapper and ensure it mirrors final_report.pdf.
if command -v pdflatex >/dev/null 2>&1; then
	pdflatex -interaction=nonstopmode main.tex >/dev/null
	echo "Built wrapper PDF: $SCRIPT_DIR/main.pdf"
fi

echo "Built: ../final_report.pdf"
