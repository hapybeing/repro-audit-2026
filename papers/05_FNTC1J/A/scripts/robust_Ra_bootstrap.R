# R_a (pre-registered): nonparametric case bootstrap, 1000 resamples, set.seed(20261009) once.
# Data = rows model_CTB was fit on. Same resample indices also used to refit model_misinfo (secondary).
# Usage: Rscript robust_Ra_bootstrap.R <session.RData> <out_summary.csv> <out_draws.csv>
args <- commandArgs(trailingOnly = TRUE)
load(args[1])
# model_CTB$data is the data frame the model was fit on (ds_analysis_paper2_CTBs_Ant after the row "1400" removal);
# the global object of that name is overwritten later in the script (original line 3207).
d <- model_CTB$data[rownames(model.frame(model_CTB)), ]
stopifnot(identical(model_CTB$data, model_misinfo$data))
stopifnot(nrow(d) == nobs(model_CTB), nrow(model.frame(model_misinfo)) == nrow(d))
fC <- formula(model_CTB); fM <- formula(model_misinfo)
n <- nrow(d); B <- 1000
set.seed(20261009)
terms <- c("ConspMent_index", "EpistBel_Truth_index")
draws <- data.frame(b = 1:B)
for (nm in c(paste0("CTB_", terms), paste0("misinfo_", terms), "CTB_converged", "misinfo_converged")) draws[[nm]] <- NA
for (b in 1:B) {
  idx <- sample(n, n, replace = TRUE)
  db <- d[idx, ]
  mC <- suppressWarnings(glm(fC, data = db, family = binomial))
  mM <- suppressWarnings(glm(fM, data = db, family = binomial))
  draws[b, paste0("CTB_", terms)] <- coef(mC)[terms]
  draws[b, paste0("misinfo_", terms)] <- coef(mM)[terms]
  draws$CTB_converged[b] <- mC$converged; draws$misinfo_converged[b] <- mM$converged
}
write.csv(draws, args[3], row.names = FALSE)
summ <- do.call(rbind, lapply(list(c("CTB", terms[1]), c("CTB", terms[2]), c("misinfo", terms[1]), c("misinfo", terms[2])), function(x) {
  m <- if (x[1] == "CTB") model_CTB else model_misinfo
  lo <- draws[[paste0(x[1], "_", x[2])]]
  conv <- draws[[paste0(x[1], "_converged")]]
  data.frame(model = x[1], term = x[2], B = B, n = n, n_not_converged = sum(!conv),
             or_original = exp(coef(m)[x[2]]),
             or_pct_ci_low = exp(quantile(lo, 0.025, names = FALSE)),
             or_pct_ci_high = exp(quantile(lo, 0.975, names = FALSE)),
             boot_se_logodds = sd(lo),
             p_boot = min(2 * mean(lo <= 0), 1),
             or_pct_ci_low_converged_only = exp(quantile(lo[conv], 0.025, names = FALSE)),
             or_pct_ci_high_converged_only = exp(quantile(lo[conv], 0.975, names = FALSE)))
}))
write.csv(summ, args[2], row.names = FALSE)
print(summ, digits = 6)
