# Agent B: reproduced bootstrap draw for seed i vs row i of deposited pool_se.ls.rds beta_boot (element 2 = pool_xsec, 1 = pool_ldv). Reported, not a target.
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B"
se <- readRDS("/workspace/audit_runs/17_T1NXVQ/B/deposited_models/pool_se.ls.rds")
out <- list()
for (mm in list(c("pool_xsec", 2), c("pool_ldv", 1))) {
  f <- file.path(P, "outputs", paste0("boot_authorseeds_", mm[1], ".csv")); if (!file.exists(f)) next
  b <- read.csv(f, check.names = FALSE); dep <- se[[as.integer(mm[2])]]$beta_boot
  for (k in seq_len(nrow(b))) for (term in colnames(dep)) {
    out[[length(out) + 1]] <- data.frame(model = mm[1], seed = b$seed[k], term = term, reproduced = b[[term]][k], deposited_row = dep[b$seed[k], term])
  }
  # deposited 120-draw percentile CI and SD for context
  ci <- se[[as.integer(mm[2])]]$ci_mat
  write.csv(data.frame(term = colnames(dep), dep_sd_120 = apply(dep, 2, sd), dep_LB_Perc = ci[3, ], dep_UB_Perc = ci[4, ]), file.path(P, "outputs", paste0("deposited_boot_context_", mm[1], ".csv")), row.names = FALSE)
}
o <- do.call(rbind, out); o$abs_diff <- o$reproduced - o$deposited_row
write.csv(o, file.path(P, "outputs", "compare_boot_vs_deposited.csv"), row.names = FALSE); print(o)
