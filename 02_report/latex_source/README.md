# latex_source

Contents:
- `main.tex`: synchronized TeX wrapper that mirrors `../final_report.pdf` exactly.
- `references.bib`: bibliography with verified citations from attached papers.
- `figures/`: local figures used by the report.
- `build.sh`: canonical build entry that generates `../final_report.pdf` from `build_fallback_pdf.py`.
- `build_fallback_pdf.py`: canonical report-content generator in this environment.

Synchronization note:
- `build_fallback_pdf.py` is the source of truth for report content.
- `main.tex` is intentionally a wrapper around `../final_report.pdf` so TeX source and shipped PDF stay in sync.

## Regenerate using LaTeX (preferred)

```bash
cd 02_report/latex_source
./build.sh
```

This always regenerates `../final_report.pdf`.
If `pdflatex` is available, it also compiles `main.tex` as a wrapper consistency check.

## Regenerate without LaTeX (fallback)

```bash
cd 02_report/latex_source
python3 build_fallback_pdf.py
```
