# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3). Loads the as-is session objects.
.libPaths(c("/workspace/audit_runs/08_SQRZR8/A/rlib", .libPaths()))
suppressMessages(library(estimatr))
OUT <- Sys.getenv("OUTDIR"); load(file.path(OUT, "session_models.RData"))
term <- "surveillance_facPersonalized"
covs <- trimws(strsplit(covariates_str, "\\+")[[1]])
fml <- function(y) as.formula(paste0(y, " ~ surveillance_fac + censorship_fac + ", covariates_str))
est_sample <- function(y) data[complete.cases(data[, c(y, "surveillance_fac", "censorship_fac", covs)]), ]
res <- list()
add <- function(...) res[[length(res)+1]] <<- data.frame(...)
for (y in c("positive_emo_rv", "general_attitude_fic")) {
  role <- if (y == "positive_emo_rv") "primary_T1" else "secondary_T3"
  d <- est_sample(y); n <- nrow(d)
  # R_a: case bootstrap
  orig <- coef(lm(fml(y), data = d))[term]
  set.seed(20261009)
  B <- 1000; bs <- rep(NA_real_, B); bad <- 0
  for (b in 1:B) { i <- sample(n, n, replace = TRUE); db <- d[i, ]
    if (length(unique(db$surveillance_fac)) < 3 || length(unique(db$censorship_fac)) < 3) { bad <- bad + 1; next }
    cf <- coef(lm(fml(y), data = db)); if (any(is.na(cf))) { bad <- bad + 1; next }; bs[b] <- cf[term] }
  ok <- bs[!is.na(bs)]
  write.csv(data.frame(draw = 1:B, estimate = bs), file.path(OUT, paste0("R_a_bootstrap_draws_", y, ".csv")), row.names = FALSE)
  add(check="R_a", role=role, outcome=y, n=n, estimate=unname(orig), se=sd(ok), ci_low=unname(quantile(ok,.025)),
      ci_high=unname(quantile(ok,.975)), p_value=min(2*mean(ok >= 0), 1), dropped_or_bad=bad, n_valid_draws=length(ok))
  # R_b: |z|>3 on outcome
  z <- (d[[y]] - mean(d[[y]])) / sd(d[[y]]); keep <- abs(z) <= 3
  m <- lm_robust(fml(y), data = d[keep, ]); s <- summary(m)$coefficients
  add(check="R_b", role=role, outcome=y, n=sum(keep), estimate=s[term,"Estimate"], se=s[term,"Std. Error"],
      ci_low=s[term,"CI Lower"], ci_high=s[term,"CI Upper"], p_value=s[term,"Pr(>|t|)"], dropped_or_bad=sum(!keep), n_valid_draws=NA)
}
# R_c: pos_mean_z
d <- est_sample("positive_emo_rv")
d$pos_mean <- (d$Secured + d$Happiness) / 2
d$pos_mean_z <- (d$pos_mean - mean(d$pos_mean)) / sd(d$pos_mean)
m <- lm_robust(fml("pos_mean_z"), data = d); s <- summary(m)$coefficients
add(check="R_c", role="primary_T1", outcome="pos_mean_z", n=nobs(m), estimate=s[term,"Estimate"], se=s[term,"Std. Error"],
    ci_low=s[term,"CI Lower"], ci_high=s[term,"CI Upper"], p_value=s[term,"Pr(>|t|)"], dropped_or_bad=0, n_valid_draws=NA)
out <- do.call(rbind, res)
write.csv(out, file.path(OUT, "robustness.csv"), row.names = FALSE)
print(out, digits = 6)
