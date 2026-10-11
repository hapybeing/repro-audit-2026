# diffs for 23_FXRNBA agent B

No file of the authors was edited, so there is no .diff file.

Environment handling without edits:
- Deposit files were placed in the sub-folders the code reads ("Data Analysis/", "Beats/", "Crime Data/") under /workspace/audit_runs/23_FXRNBA/B/run/, and R was started with that folder as working directory (path-only layout fix named in PREREG.md).
- The five CSVs were downloaded with `?format=original` (PREREG.md and batch5 brief).
- R was run with LC_ALL=C.UTF-8 (locale fix named in PREREG.md).
- Packages without a Debian binary (fixest, ivtools, weathermetrics and their dependencies) were installed from current CRAN into a per-run library.
- scripts/run_part.R sources the authors' lines 1-668 unchanged (a subset run, PREREG plan step 3); scripts/run_full.R sources the whole script unchanged. scripts/robustness.R sources lines 1-405 unchanged to rebuild seattle_main and the helper functions.
