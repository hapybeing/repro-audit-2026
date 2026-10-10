# R_b (pre-registered): drop cases with Cook's distance > 4/N (N = nobs of the model), refit identical glm,
# HC3 SE, Bonferroni over all 19 terms. CTB model primary; misinfo model with its own Cook's distances (secondary).
# Usage: Rscript robust_Rb_cooks.R <session.RData> <out.csv>
args <- commandArgs(trailingOnly = TRUE)
suppressMessages({library(sandwich); library(lmtest)})
load(args[1])
# model_CTB$data = data the models were fit on (global ds_analysis_paper2_CTBs_Ant is overwritten at original line 3207)
d <- model_CTB$data
stopifnot(identical(model_CTB$data, model_misinfo$data))
res <- list()
for (lab in c("CTB", "misinfo")) {
  m <- if (lab == "CTB") model_CTB else model_misinfo
  N <- nobs(m); cd <- cooks.distance(m); thr <- 4 / N
  keep <- names(cd)[cd <= thr]
  dd <- d[keep, ]
  m2 <- glm(formula(m), data = dd, family = binomial)
  V <- sandwich::vcovHC(m2, type = "HC3"); ct <- lmtest::coeftest(m2, vcov = V)
  padj <- p.adjust(ct[, 4], method = "bonferroni")
  for (t in c("ConspMent_index", "EpistBel_Truth_index")) {
    res[[length(res) + 1]] <- data.frame(model = lab, term = t, N_original = N, threshold = thr,
      n_dropped = sum(cd > thr), n_refit = nobs(m2), converged = m2$converged,
      log_odds = ct[t, 1], odds_ratio = exp(ct[t, 1]), se_hc3 = ct[t, 2],
      or_ci_low = exp(ct[t, 1] - qnorm(.975) * ct[t, 2]), or_ci_high = exp(ct[t, 1] + qnorm(.975) * ct[t, 2]),
      p_raw = ct[t, 4], p_bonf = padj[t], n_terms = nrow(ct),
      n_outcome1_dropped = sum(m$y[cd > thr] == 1))
  }
}
out <- do.call(rbind, res); write.csv(out, args[2], row.names = FALSE); print(out, digits = 6)
