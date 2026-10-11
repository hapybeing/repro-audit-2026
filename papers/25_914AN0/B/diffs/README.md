# Diffs (agent B, 25_914AN0)

- functions_R_mc_cores.diff: code/functions.R line 306. `mc.cores=min(length(yvarz),parallel::detectCores()/4)` is 0.5 on this 2-CPU machine and `parallel::mclapply` rejects it ("'mc.cores' must be >= 1"). Changed to `max(1, min(...))` (= 1, sequential). Pre-registered allowed env fix (PREREG section 2; batch5_class_decisions #3). No RNG in ensemble_modz.

No other authors' file was changed. The target blocks were run by my stage scripts (scripts/s1a_prep.R, s1b_models.R, s4_war.R) which evaluate the authors' run2_main.R line ranges verbatim in fresh sessions (batch5_class_decisions #2). s1b_models.R calls `data.table::setalloccol(X_s)` after loading the saved X_s, because readRDS returns a data.table without column over-allocation and the authors' by-reference weight assignment then behaves differently from the one-session route (LOG.md 07:58-08:02).
