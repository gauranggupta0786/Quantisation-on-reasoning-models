#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROOT_DIR="$(cd "$CODE_DIR/.." && pwd)"

RUN_NOTEBOOK=false
if [[ "${1:-}" == "--run-notebook" ]]; then
  RUN_NOTEBOOK=true
fi

if [[ "$RUN_NOTEBOOK" == "true" ]]; then
  "$SCRIPT_DIR/train.sh"
fi

python3 - "$CODE_DIR" "$ROOT_DIR" <<'PY'
import csv
import os
import sys

code_dir = sys.argv[1]
root_dir = sys.argv[2]

targets = [
    (
        "Phase 7 final results",
        os.path.join(
            code_dir,
            "src",
            "Quantization_Reasoning_Project",
            "phase7_qlora_experiment",
            "phase7_step6_final_results.csv",
        ),
    ),
    (
        "Phase 8 metrics",
        os.path.join(
            code_dir,
            "src",
            "Quantization_Reasoning_Project",
            "phase8_grpo_experiment",
            "reports",
            "phase8_metrics.csv",
        ),
    ),
    (
        "Cross-phase summary",
        os.path.join(root_dir, "05_results", "main_results.csv"),
    ),
]


def read_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def clean(value):
    if value is None:
        return "NA"
    text = str(value).strip()
    return text if text else "NA"


for label, path in targets:
    print(f"\n[{label}]")
    print(f"path: {path}")

    if not os.path.exists(path):
        print("status: missing")
        continue

    rows = read_rows(path)
    print(f"status: found ({len(rows)} rows)")
    if not rows:
        continue

    columns = list(rows[0].keys())
    interesting = [
        c
        for c in (
            "phase",
            "dataset",
            "setting",
            "run_name",
            "method",
            "accuracy_pct",
            "loop_failure_pct",
            "truncation_failure_pct",
            "samples",
        )
        if c in columns
    ]
    if not interesting:
        interesting = columns[:5]

    print("columns:", ", ".join(columns))
    print("preview:")
    for row in rows[:5]:
        values = [f"{k}={clean(row.get(k))}" for k in interesting]
        print("  - " + ", ".join(values))
PY
