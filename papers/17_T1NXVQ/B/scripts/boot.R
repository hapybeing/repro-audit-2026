# Agent B: reduced parametric bootstrap, serial copy of the body of pspm's par_bootstrap_composite_log_likelihood worker
# (pspm_R6.R lines 786-795): set.seed(i); py_set_seed(i); bootstrap_composite_log_likelihood(n_boot_iter = 1, ...).
# Args (env): AUDIT_MODEL, BOOT_FROM, BOOT_TO, BOOT_TAG (authorseeds|seeds1001), BOOT_CAP_MIN, BOOT_STOP_AFTER (optional, minutes since start; stop starting new draws)
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B"
S <- "/workspace/audit_runs/17_T1NXVQ/B"
setwd(file.path(S, "replication"))
model <- Sys.getenv("AUDIT_MODEL"); from <- as.integer(Sys.getenv("BOOT_FROM")); to <- as.integer(Sys.getenv("BOOT_TO"))
tag <- Sys.getenv("BOOT_TAG"); cap <- as.numeric(Sys.getenv("BOOT_CAP_MIN", "35"))
source("scripts/analysis/analysis_globals.R")
m <- readRDS(file.path(S, "models", "main", paste0("pool_", model, "_model.rds")))
learn_obj <- reset_pspmlearn(m$learn_obj)
f <- file.path(P, "outputs", paste0("boot_", tag, "_", model, ".csv"))
done <- if (file.exists(f)) read.csv(f)$seed else integer(0)
prev_min <- if (file.exists(f)) sum(read.csv(f)$minutes) else 0
t0 <- Sys.time()
for (i in from:to) {
  if (i %in% done) next
  el <- prev_min + as.numeric(difftime(Sys.time(), t0, units = "mins"))
  if (el > cap) { cat("CAP reached before seed", i, "elapsed", el, "\n"); break }
  ti <- Sys.time()
  set.seed(i)
  reticulate::py_set_seed(i, disable_hash_randomization = TRUE)
  bse <- learn_obj$bootstrap_composite_log_likelihood(n_boot_iter = 1, burnin = burnin, ci_level = 0.95,
                                                     return_sims = T, report_every = 5, cache_samples = T)
  b <- bse$beta_boot
  row <- data.frame(seed = i, minutes = as.numeric(difftime(Sys.time(), ti, units = "mins")), t(b[1, ]), check.names = FALSE)
  write.table(row, f, sep = ",", row.names = FALSE, col.names = !file.exists(f), append = file.exists(f))
  cat("DRAW", model, tag, "seed", i, "min", round(row$minutes, 2), grep("VmHWM", readLines("/proc/self/status"), value = TRUE), "\n"); flush.console()
}
