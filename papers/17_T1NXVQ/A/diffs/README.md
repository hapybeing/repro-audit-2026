# diffs/ (agent A, 17_T1NXVQ)

## Environment fixes (allowed by PREREG section 2)
- `analysis_globals_E1_E2_E3.diff` (file `scripts/analysis/analysis_globals.R` in the run copy of the deposit):
  - E1, lines 58 and 120: `RETICULATE_PYTHON` from `/usr/bin/python3` to the run venv python (`RUNDIR/venv/bin/python`, numpy/scipy/networkx installed there). Path fix; /usr/bin/python3 has no numpy.
  - E2, line 46: `ncore <- 40` to `ncore <- 1` (README allows adapting ncore; no cluster is created on the pre-registered path anyway).
  - E3, lines 69-70 and 125-126: `library(rgeos)` and `library(rgdal)` deleted, because neither archived package could be installed (both fail with `fatal error: sp.h: No such file or directory`; sp 2.x ships no headers). PREREG checked that no rgeos/rgdal function is called on the Table 1 path.

## Pre-registered run-structure changes (PREREG section 2, F1 to F3; not analysis changes)
- `analysis_pool_A.diff` (`scripts/analysis/pspm/analysis_pool.R` -> `scripts/analysis_pool_A.R`):
  - F1: `form.ls <- form.ls[MODEL_NAME]` after the unchanged `form.ls` definition: one Table 1 model per R process (memory).
  - F2: cluster creation and `clusterExport_fast` commented out; `parLapply(cl, form.ls, ...)` replaced by `lapply(form.ls, ...)`. The estimation function body (set.seed(1), fit_pspm_model arguments) is unchanged.
  - F3: the fitted model is saved to `outputs/pool_<model>_model.rds` instead of `data/models/pool_model.ls.rds`; lines 96-111 (120-draw parallel bootstrap and saves) are removed and replaced by PREREG step 6 in `scripts/run_model.R` (the authors' foreach worker body, run serially with seeds i: `set.seed(i); py_set_seed(i, disable_hash_randomization = TRUE); bootstrap_composite_log_likelihood(n_boot_iter = 1, burnin = 100, ...)`).

## Pre-registered robustness variants (applied in memory by scripts/run_model.R, not env fixes)
- `R_c_sigma2.diff`: `sigma2 = 10` -> `sigma2 = 1000` in the estimation call (R_c only).
- R_b changes data, not code: edges with |z| > 3 on `length.norm` or `elevmean.norm` set to NA in `graph` before estimation (run_model.R, VARIANT == "rb").
- Robustness/R_a fits save their model to `outputs/pool_<model>_<variant>_model.rds` so the main fit files are not overwritten.
