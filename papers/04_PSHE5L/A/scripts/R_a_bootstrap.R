# R_a: nonparametric case bootstrap, 1000 replicates, set.seed(20261009) once.
# Resumable: all 1000 resample index vectors are drawn up front, in replicate order, right after the
# single set.seed call (identical to drawing them inside a loop, since only sample() is used for them);
# each run fits the replicates not yet in outputs/R_a_boot.csv, up to a time budget, appending rows.
.libPaths(c("/workspace/audit_runs/04_PSHE5L/A/rlib", .libPaths()))
suppressMessages(library(lavaan))
args <- commandArgs(trailingOnly = TRUE)
budget_s <- if (length(args)) as.numeric(args[1]) else 500
inp <- readRDS("/workspace/audit_runs/04_PSHE5L/A/checks_input.rds")
rural <- inp$rural; model <- inp$model
B <- 1000; n <- nrow(rural)
idx_file <- "/workspace/audit_runs/04_PSHE5L/A/R_a_indices.rds"
if (!file.exists(idx_file)) {
  set.seed(20261009)
  idx <- vector("list", B)
  for (i in seq_len(B)) idx[[i]] <- sample(n, n, replace = TRUE)
  saveRDS(idx, idx_file)
}
idx <- readRDS(idx_file)
out <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/outputs/R_a_boot.csv"
done <- if (file.exists(out)) read.csv(out)$rep else integer(0)
todo <- setdiff(seq_len(B), done)
t0 <- Sys.time()
for (i in todo) {
  if (as.numeric(difftime(Sys.time(), t0, units = "secs")) > budget_s) break
  d <- rural[idx[[i]], , drop = FALSE]
  row <- tryCatch({
    fit <- cfa(model, data = d, sampling.weights = "WTS", missing = "ML", estimator = "MLR")
    conv <- lavInspect(fit, "converged")
    ss <- standardizedSolution(fit)
    b1 <- ss$est.std[ss$lhs == "violence" & ss$op == "~" & ss$rhs == "polgriev"]
    ind <- ss$est.std[ss$lhs == "indirect1_econgriev" & ss$op == ":="]
    data.frame(rep = i, converged = conv, error = "", b1_std = b1, indirect_std = ind)
  }, error = function(e) data.frame(rep = i, converged = FALSE, error = gsub("[\r\n,]", " ", conditionMessage(e)), b1_std = NA, indirect_std = NA))
  write.table(row, out, sep = ",", append = file.exists(out), col.names = !file.exists(out), row.names = FALSE)
}
cat("rows now:", nrow(read.csv(out)), "\n")
