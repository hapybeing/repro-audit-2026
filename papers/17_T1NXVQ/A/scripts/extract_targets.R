# Agent A, 17_T1NXVQ, PREREG step 5: read the two saved fitted models (one at a time, memory) and write every
# coefficient, maxLik stdEr, and the counts to outputs/targets_extracted.csv
suppressMessages({library(maxLik); library(pspm)})
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/A/outputs"
rows <- list()
for (nm in c("pool_xsec", "pool_ldv")) {
  f <- file.path(OUT, paste0("pool_", nm, "_model.rds"))
  if (!file.exists(f)) { cat("missing", f, "\n"); next }
  ml <- readRDS(f); m <- ml[[nm]]
  rows[[nm]] <- data.frame(model = nm, term = names(m$estimate), estimate = unname(m$estimate),
                           maxlik_se = unname(miscTools::stdEr(m)), N_sum = sum(m$N), N_edges_sum = sum(m$N_edges),
                           N_groups_sum = sum(m$N_groups), N_instances = m$N_instances,
                           maxlik_code = m$code, maxlik_message = m$message, iterations = unname(m$iterations[1]))
  rm(ml, m); invisible(gc())
}
out <- do.call(rbind, rows)
write.csv(out, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
print(out[, 1:8], digits = 6)
