# R_a (as pre-registered): nonparametric case bootstrap, 1000 resamples, set.seed(20261009) once.
# Usage: Rscript robust_Ra_bootstrap.R <session.RData> <outdir>
args <- commandArgs(trailingOnly = TRUE); sess <- args[1]; outdir <- args[2]
e <- new.env(); load(sess, envir = e)
m <- e$model_CTB; mm <- e$model_misinfo
mf <- model.frame(m)                         # exact rows model_CTB was fit on
# m$data is the data object glm() received at fit time (ds_analysis_paper2_CTBs_Ant as of line 1814; the script
# redefines that name later at line 3207, so the session copy must not be used)
stopifnot(identical(m$data, mm$data))
d  <- as.data.frame(m$data)[rownames(mf), ]   # rownames are the original raw-data row names, index by name
stopifnot(nrow(d) == nobs(m))
f_ctb <- formula(m); f_mis <- formula(mm)
# sanity: refit on d reproduces the original coefficients
stopifnot(isTRUE(all.equal(coef(glm(f_ctb, data = d, family = binomial)), coef(m))))
n <- nrow(d); B <- 1000
set.seed(20261009)
res <- data.frame(b = 1:B, lo_cm_ctb = NA, lo_truth_ctb = NA, conv_ctb = NA,
                  lo_cm_mis = NA, lo_truth_mis = NA, conv_mis = NA)
for (b in 1:B) {
  idx <- sample(n, n, replace = TRUE); db <- d[idx, ]
  f1 <- suppressWarnings(glm(f_ctb, data = db, family = binomial))
  f2 <- suppressWarnings(glm(f_mis, data = db, family = binomial))
  res[b, 2:7] <- c(coef(f1)["ConspMent_index"], coef(f1)["EpistBel_Truth_index"], f1$converged,
                   coef(f2)["ConspMent_index"], coef(f2)["EpistBel_Truth_index"], f2$converged)
}
write.csv(res, file.path(outdir, "Ra_bootstrap_draws.csv"), row.names = FALSE)
summ <- function(lo, est, conv, label) {
  ok <- conv == 1   # all draws kept (not replaced); non-converged counted
  data.frame(quantity = label, estimate_OR = exp(est), boot_n = length(lo), n_not_converged = sum(!ok),
             ci_low_OR = exp(quantile(lo, .025, names = FALSE)), ci_high_OR = exp(quantile(lo, .975, names = FALSE)),
             boot_se_logodds = sd(lo), p_boot = min(2 * mean(lo <= 0), 1))
}
out <- rbind(summ(res$lo_cm_ctb, coef(m)["ConspMent_index"], res$conv_ctb, "T1_ConspMent_CTB"),
             summ(res$lo_truth_ctb, coef(m)["EpistBel_Truth_index"], res$conv_ctb, "T3_Truth_CTB"),
             summ(res$lo_cm_mis, coef(mm)["ConspMent_index"], res$conv_mis, "T2_ConspMent_misinfo"),
             summ(res$lo_truth_mis, coef(mm)["EpistBel_Truth_index"], res$conv_mis, "T4_Truth_misinfo"))
out$same_direction_and_significance <- out$estimate_OR > 1 & out$ci_low_OR > 1
write.csv(out, file.path(outdir, "Ra_bootstrap_summary.csv"), row.names = FALSE)
print(out)
