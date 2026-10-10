# Agent B: extract target quantities from a saved session of the authors' script.
# Usage: Rscript extract_targets.R <session.RData> <out_prefix>
args <- commandArgs(trailingOnly = TRUE)
sess <- args[1]; pre <- args[2]
suppressMessages({library(sandwich); library(lmtest)})
e <- new.env(); load(sess, envir = e)
one <- function(m, name) {
  V <- sandwich::vcovHC(m, type = "HC3"); ct <- lmtest::coeftest(m, vcov = V)
  data.frame(model = name, term = rownames(ct), log_odds = ct[,1], se_hc3 = ct[,2], z = ct[,3],
             p_raw = ct[,4], p_bonf = p.adjust(ct[,4], "bonferroni"), odds_ratio = exp(ct[,1]),
             nobs = nobs(m), chisq = m$null.deviance - m$deviance, chisq_df = m$df.null - m$df.residual,
             row.names = NULL)
}
res <- rbind(one(e$model_CTB, "model_CTB"), one(e$model_misinfo, "model_misinfo"))
write.csv(res, paste0(pre, "_all_terms.csv"), row.names = FALSE)
key <- res[res$term %in% c("ConspMent_index", "EpistBel_Truth_index"), ]
write.csv(key, paste0(pre, "_targets.csv"), row.names = FALSE)
# Nagelkerke R2 as secondary context
nk <- function(m) { n <- nobs(m); l0 <- -m$null.deviance/2; l1 <- -m$deviance/2
  (1 - exp(2*(l0 - l1)/n)) / (1 - exp(2*l0/n)) }
fit <- data.frame(model = c("model_CTB","model_misinfo"), nobs = c(nobs(e$model_CTB), nobs(e$model_misinfo)),
  chisq = c(e$model_CTB$null.deviance - e$model_CTB$deviance, e$model_misinfo$null.deviance - e$model_misinfo$deviance),
  nagelkerke = c(nk(e$model_CTB), nk(e$model_misinfo)))
write.csv(fit, paste0(pre, "_fit.csv"), row.names = FALSE)
print(key); print(fit)
