# R_b (as pre-registered): drop cases with Cook's distance > 4/N from the final model, refit, HC3 inference.
# Usage: Rscript robust_Rb_cooks.R <session.RData> <outdir>
args <- commandArgs(trailingOnly = TRUE); sess <- args[1]; outdir <- args[2]
suppressMessages({library(sandwich); library(lmtest)})
e <- new.env(); load(sess, envir = e)
# data object glm() received at fit time (the script redefines ds_analysis_paper2_CTBs_Ant later, line 3207)
stopifnot(identical(e$model_CTB$data, e$model_misinfo$data))
base <- as.data.frame(e$model_CTB$data)
one <- function(m, label) {
  mf <- model.frame(m); d <- base[rownames(mf), ]; N <- nobs(m)  # index by row NAME
  stopifnot(nrow(d) == N, identical(names(cooks.distance(m)), rownames(d)))
  cd <- cooks.distance(m); keep <- cd <= 4 / N
  m2 <- glm(formula(m), data = d[keep, ], family = binomial)
  ct <- lmtest::coeftest(m2, vcov = sandwich::vcovHC(m2, type = "HC3"))
  pb <- p.adjust(ct[, 4], "bonferroni")
  r <- function(term) data.frame(model = label, term = term, N_original = N, n_dropped = sum(!keep), N_refit = nobs(m2),
       converged = m2$converged, log_odds = ct[term, 1], OR = exp(ct[term, 1]), se_hc3 = ct[term, 2],
       ci_low_OR = exp(ct[term,1] - qnorm(.975) * ct[term,2]), ci_high_OR = exp(ct[term,1] + qnorm(.975) * ct[term,2]),
       p_raw = ct[term, 4], p_bonf = pb[term])
  rbind(r("ConspMent_index"), r("EpistBel_Truth_index"))
}
out <- rbind(one(e$model_CTB, "model_CTB"), one(e$model_misinfo, "model_misinfo"))
out$same_direction_and_significance <- out$OR > 1 & out$p_bonf < .001
write.csv(out, file.path(outdir, "Rb_cooks_summary.csv"), row.names = FALSE)
print(out)
