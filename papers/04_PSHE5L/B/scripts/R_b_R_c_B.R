# R_b (outlier exclusion on violence indicators, |z| > 3 on unweighted z of row mean of Q25B-D)
# R_c (unweighted: same call without sampling.weights). Both on the primary-run data preparation.
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/B/scripts/prep_B.R")
outdir <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/B/outputs"
grab <- function(fit, check, extra) {
  ss <- standardizedSolution(fit); pe <- parameterEstimates(fit)
  rows <- list(b1 = c("violence", "~", "polgriev"), indirect1_econgriev = c("indirect1_econgriev", ":=", "a1*b1"))
  do.call(rbind, lapply(names(rows), function(k) {
    r <- rows[[k]]
    s <- ss[ss$lhs == r[1] & ss$op == r[2] & ss$rhs == r[3], ]
    p <- pe[pe$lhs == r[1] & pe$op == r[2] & pe$rhs == r[3], ]
    data.frame(check = check, param = k, est_std = s$est.std, se_std = s$se, ci_lower_std = s$ci.lower,
               ci_upper_std = s$ci.upper, p_std = s$pvalue, est_unstd = p$est, p_unstd = p$pvalue,
               nobs = lavInspect(fit, "nobs"), converged = lavInspect(fit, "converged"), extra)
  }))
}
viol_mean <- rowMeans(rural[, c("Q25B", "Q25C", "Q25D")], na.rm = TRUE)
z <- (viol_mean - mean(viol_mean)) / sd(viol_mean)
drop <- abs(z) > 3
cat("R_b rows meeting |z|>3:", sum(drop), "\n"); print(table(round(viol_mean[drop], 3)))
fb <- fit_model(rural[!drop, ])
rb <- grab(fb, "R_b", data.frame(rows_dropped = sum(drop), note = ""))
write.csv(rb, file.path(outdir, "R_b_outliers.csv"), row.names = FALSE)
fc <- fit_model(rural, weighted = FALSE)
rc <- grab(fc, "R_c", data.frame(rows_dropped = 0, note = "unweighted, all 1203 rows incl. 11 with WTS = 0"))
write.csv(rc, file.path(outdir, "R_c_unweighted.csv"), row.names = FALSE)
print(rb); print(rc)
