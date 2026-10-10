# Diffs (agent A, 16_QZNVZ0)

- `regression_verbatim_extraction.diff`: `scripts/regression_verbatim_orig.py` (the 13 code cells of the deposited Regression.ipynb, version 2.0, concatenated verbatim with `# ---- cell N ----` comment markers) vs `scripts/regression_verbatim.py`, which appends an extraction block after the authors' last line. The block only reads the fitted `results_*` objects and writes outputs/regression_estimates.csv, outputs/regression_summaries.txt and the Model 1 / Model 4 estimation row labels. This is route 2 of PREREG section 2 step 3. No author line was changed.
- Working directory: the script is run from /workspace/audit_runs/16_QZNVZ0/A/data, where `regression_table_anonymous_final.csv` sits, so the authors' bare-filename `read_csv` works unchanged. No file edit was needed for this.
- No package-version fix was needed: current releases (pandas 3.0.6, numpy 2.5.3, statsmodels 0.15.0) ran all cells; `fit(maxiter=100)` was accepted.
