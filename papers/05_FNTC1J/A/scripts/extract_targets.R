# Extract coefficient tables from model_CTB and model_misinfo saved by run_authors.R.
# Mirrors the authors' table code (lines 2011-2060): HC3 vcov, lmtest::coeftest, OR = exp(coef),
# Bonferroni via p.adjust over all model terms (19 incl. intercept).
# Usage: Rscript extract_targets.R <in.RData> <out_coefs.csv> <out_fit.csv>
args <- commandArgs(trailingOnly = TRUE)
suppressMessages({library(sandwich); library(lmtest)})
load(args[1])
one <- function(m, label) {
  V <- sandwich::vcovHC(m, type = "HC3")
  ct <- lmtest::coeftest(m, vcov = V)
  ci <- lmtest::coefci(m, vcov = V)
  data.frame(model = label, term = rownames(ct), log_odds = ct[, 1], se_hc3 = ct[, 2], z = ct[, 3],
             p_raw = ct[, 4], p_bonf = p.adjust(ct[, 4], method = "bonferroni"),
             odds_ratio = exp(coef(m)), or_ci_low = exp(ci[, 1]), or_ci_high = exp(ci[, 2]),
             se_model = sqrt(diag(vcov(m))), n_terms = nrow(ct), nobs = nobs(m), row.names = NULL)
}
fit <- function(m, label) {
  chi <- m$null.deviance - m$deviance; df <- m$df.null - m$df.residual
  n <- nobs(m); ll0 <- -m$null.deviance / 2; ll1 <- -m$deviance / 2
  cs <- 1 - exp((2 / n) * (ll0 - ll1)); nk <- cs / (1 - exp((2 / n) * ll0))
  data.frame(model = label, nobs = n, chi2 = chi, chi2_df = df, p_model = pchisq(chi, df, lower.tail = FALSE),
             nagelkerke_r2 = nk, aic = AIC(m), loglik = as.numeric(logLik(m)), converged = m$converged,
             n_outcome_1 = sum(m$y == 1), n_outcome_0 = sum(m$y == 0))
}
co <- rbind(one(model_CTB, "CTB"), one(model_misinfo, "misinfo"))
fi <- rbind(fit(model_CTB, "CTB"), fit(model_misinfo, "misinfo"))
write.csv(co, args[2], row.names = FALSE)
write.csv(fi, args[3], row.names = FALSE)
print(co[co$term %in% c("ConspMent_index", "EpistBel_Truth_index"), ], digits = 6)
print(fi, digits = 6)
