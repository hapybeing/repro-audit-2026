# R_b: drop rows with |z| > 3 on viol_mean (unweighted mean of Q25B,Q25C,Q25D), refit, as pre-registered.
# R_c: identical call without sampling.weights (all 1203 rows), as pre-registered.
.libPaths(c("/workspace/audit_runs/04_PSHE5L/A/rlib", .libPaths()))
suppressMessages(library(lavaan))
inp <- readRDS("/workspace/audit_runs/04_PSHE5L/A/checks_input.rds")
rural <- inp$rural; model <- inp$model
od <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/outputs"
grab <- function(fit, tag, extra) {
  ss <- standardizedSolution(fit); pe <- parameterEstimates(fit)
  pick <- function(df, lhs, op, rhs = NULL) { k <- df$lhs == lhs & df$op == op; if (!is.null(rhs)) k <- k & df$rhs == rhs; df[k, ] }
  s1 <- pick(ss, "violence", "~", "polgriev"); s2 <- pick(ss, "indirect1_econgriev", ":=")
  p1 <- pick(pe, "violence", "~", "polgriev"); p2 <- pick(pe, "indirect1_econgriev", ":=")
  data.frame(check = tag, quantity = c("b1_violence_on_polgriev", "indirect1_econgriev"),
             est_std = c(s1$est.std, s2$est.std), se_std = c(s1$se, s2$se),
             ci_lower_std = c(s1$ci.lower, s2$ci.lower), ci_upper_std = c(s1$ci.upper, s2$ci.upper),
             p_std = c(s1$pvalue, s2$pvalue), est_unstd = c(p1$est, p2$est), p_unstd = c(p1$pvalue, p2$pvalue),
             nobs = lavInspect(fit, "nobs"), converged = lavInspect(fit, "converged"), extra)
}
viol_mean <- rowMeans(rural[, c("Q25B", "Q25C", "Q25D")], na.rm = TRUE)
z <- (viol_mean - mean(viol_mean)) / sd(viol_mean)
drop <- abs(z) > 3
cat("R_b rows dropped:", sum(drop), " max |z|:", max(abs(z)), "\n")
fit_b <- cfa(model, data = rural[!drop, ], sampling.weights = "WTS", missing = "ML", estimator = "MLR")
rb <- grab(fit_b, "R_b", data.frame(rows_dropped = sum(drop), max_abs_z = max(abs(z))))
write.csv(rb, file.path(od, "R_b_outliers.csv"), row.names = FALSE)
fit_c <- cfa(model, data = rural, missing = "ML", estimator = "MLR")
rc <- grab(fit_c, "R_c", data.frame(rows_dropped = 0, max_abs_z = NA))
write.csv(rc, file.path(od, "R_c_unweighted.csv"), row.names = FALSE)
print(rb); print(rc)
