# Diffs, agent B, 17_T1NXVQ

Applied by scripts/apply_env_fixes.py to fresh copies of the deposited files (originals sha256-checked against the deposit).

- analysis_globals.R.diff
  - E1 (pre-registered): RETICULATE_PYTHON '/usr/bin/python3' -> the run's venv python (lines 58 and 120). System python has no numpy/scipy/networkx.
  - E2 (pre-registered): ncore 40 -> 1 (README allows adapting ncore). No cluster is created in this run anyway.
  - E3 (pre-registered, conditional): library(rgeos), library(rgdal) removed (lines 69-70, 125-126). The last archived versions (rgeos 0.6-4, rgdal 1.6-7) failed to compile twice with "fatal error: sp.h: No such file or directory" (current sp ships no C headers). PREREG checked that no rgeos/rgdal function is on the Table 1 path.
- analysis_pool.R.diff (the run uses a copy, scripts/analysis/pspm/analysis_pool_B.R; the deposited file is untouched)
  - F1 (pre-registered): form.ls restricted to one model per R process (AUDIT_MODEL = pool_xsec or pool_ldv); the formula text is unchanged.
  - F2 (pre-registered): parLapply(cl, ...) -> lapply(...); no cluster and no clusterExport_fast. The estimation function body (set.seed(1), fit_pspm_model arguments) is unchanged.
  - F3 (pre-registered): the fitted model is saved to the audit scratch folder instead of over data/models/pool_model.ls.rds; the 120-draw bootstrap (lines 91-118) is not run and is replaced by the pre-registered reduced bootstrap (scripts/boot.R, a serial copy of the pspm worker body).

Not code changes, recorded here for completeness: R_c (sigma2 = 1000) is applied at run time by scripts/fit_main.R with a one-token substitution in memory of the analysis_pool_B.R text; R_b sets outlier edges to NA on the in-memory graph before the same code runs.
