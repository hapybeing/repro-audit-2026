# Diffs (agent B, 09_4U8CTG)

One changed file: `replication_scripts/02_supplementary_materials.R` -> `02_supplementary_materials.R.diff` (`diff -u deposit run`). Only `if (FALSE) {` / `}` wrapper lines were inserted (16 lines added, 0 removed); no author line was edited. Line numbers below are those of the deposited file.

| deposited lines | what is skipped | why |
|---|---|---|
| 114-117 | `if (tinytex::tinytex_root() != "") tinytex::tlmgr_install(...)` | Environment fix. With Debian system TeX Live, `tinytex::tinytex_root()` stops with "/usr/share/texlive does not seem to be the root directory of TeX Live (no "bin/" dir under it)" (outputs/run_02_attempt1_log.txt). The block only installs LaTeX packages; 02 never compiles LaTeX. PREREG plan item 2 allows skipping it. Lines 108-112 (the pdflatex check) are kept and pass because pdflatex is present. |
| 146-149 | `read_csv` of `study1_fes_panel.csv`, `study1_fes_panel_long.csv` | Missing-input skip (PREREG plan item 1): Study 1 FES files are not in the deposit and are registration-only at ELIPSS. |
| 162-192 | FES panel preparation (`panel`, `Z_voters`, `panel_short`) | same |
| 253-286 | FES models (`baseline_model_panel` ... `full_affect`) | same |
| 1218-1262 | Figure F1 | same |
| 1455-1468 | Table B4 | same |
| 1789-1815 | Table F1 | same |
| 1819-1861 | Tables F2 / F3 | same |

Study 2 code is untouched. Execution note (not a code change): `scripts/extract_targets.R` sources the script with `print.eval = TRUE` so that `texreg()` calls inside `sink()` write their tables, as they do when the file is run top level with Rscript or in the console; with plain `source(echo = FALSE)` the texreg .tex files come out empty (observed in attempt 3, outputs/run_02_attempt3_log.txt; target numbers identical, outputs/targets_extracted_attempt3_echoFALSE.csv).
Packages: texreg 1.40, stargazer 5.2.3, vtable 1.4.8, binom, jtools 2.3.1 installed from CRAN source into the per-run library (no Debian binary candidates found by apt-cache); no versions pinned by the authors.
