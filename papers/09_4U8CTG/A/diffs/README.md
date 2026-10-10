# Diffs, agent A, 09_4U8CTG

## 02_supplementary_materials.R.diff
Copy of `replication_scripts/02_supplementary_materials.R` with lines commented out (prefix `#SKIP_LATEX# ` or `#SKIP_MISSING_STUDY1# `). No line was edited otherwise; Study 2 code is untouched. Allowed by PREREG section 2, items 1 and 2.

| lines (original numbering) | tag | why |
|---|---|---|
| 108 to 117 | SKIP_LATEX | pdflatex is present (system TeX Live), so the install-and-stop branch is not taken, but `tinytex::tinytex_root()` then errors: "/usr/share/texlive does not seem to be the root directory of TeX Live (no "bin/" dir under it)", which would stop the script. 02 writes .tex text and PNG files only; it does not compile LaTeX. |
| 146 to 149 | SKIP_MISSING_STUDY1 | read `data/study1_fes_panel.csv` and `data/study1_fes_panel_long.csv`, not in the deposit (registration-only FES data at ELIPSS). |
| 162 to 192 | SKIP_MISSING_STUDY1 | FES panel preparation (`panel`, `Z_voters`, `panel_short`). |
| 253 to 286 | SKIP_MISSING_STUDY1 | FES models `baseline_model_panel`, `soc_model_panel`, `full_model_panel`, `baseline_affect`, `soc_affect`, `full_affect`. |
| 1218 to 1262 | SKIP_MISSING_STUDY1 | Figure F1 (uses `panel_short`). |
| 1454 to 1468 | SKIP_MISSING_STUDY1 | Table B4 (uses `Z_voters`). |
| 1789 to 1815 | SKIP_MISSING_STUDY1 | Table F1 (uses `panel`). |
| 1818 to 1861 | SKIP_MISSING_STUDY1 | Tables F2 and F3 (FES models), to end of file. |

After the edit, a grep for `panel`, `panel_long`, `Z_voters`, `panel_short` and the FES model names over uncommented lines finds only `panel.grid` theme arguments and comments.

No other file was changed. 01_manuscript.R and 00_fes_data_preprocessing.R were not run (01 fits the same Study 2 baseline models as 02; 00 needs the ELIPSS raw files).
