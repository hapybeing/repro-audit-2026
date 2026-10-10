# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3). Loads saved session objects.
R <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B/outputs"
load(file.path(R, "session_models.RData"))
suppressMessages(library(estimatr))
term <- "surveillance_facPersonalized"
fml <- function(y) as.formula(paste0(y, " ~ surveillance_fac + censorship_fac + ", covariates_str))
covs <- strsplit(covariates_str, " \\+ ")[[1]]
est_sample <- function(y) { v <- c(y, "surveillance_fac", "censorship_fac", covs); data[complete.cases(data[, v]), ] }
out <- list()
for (y in c("positive_emo_rv", "general_attitude_fic")) {
  role <- if (y == "positive_emo_rv") "primary (T1)" else "secondary (T3)"
  d <- est_sample(y); n <- nrow(d)
  orig <- lm_robust(fml(y), data = d)
  # R_a bootstrap
  set.seed(20261009)
  b <- rep(NA_real_, 1000); nbad <- 0
  for (i in 1:1000) { idx <- sample(n, n, replace = TRUE); db <- d[idx, ]
    if (any(table(db$surveillance_fac) == 0) || any(table(db$censorship_fac) == 0)) { nbad <- nbad + 1; next }
    cf <- coef(lm(fml(y), data = db))[term]; if (is.na(cf)) { nbad <- nbad + 1; next }; b[i] <- cf }
  bb <- b[!is.na(b)]; ci <- quantile(bb, c(0.025, 0.975)); p <- min(2 * mean(bb >= 0), 1)
  out[[length(out)+1]] <- data.frame(check="R_a", outcome=y, role=role, estimate=unname(orig$coefficients[term]),
    se=sd(bb), ci_low=unname(ci[1]), ci_high=unname(ci[2]), p_value=p, n_used=n, n_dropped=NA, n_bad_resamples=nbad,
    same_dir_sig=(orig$coefficients[term] < 0 & ci[2] < 0))
  write.csv(data.frame(draw=1:1000, coef=b), file.path(R, paste0("R_a_bootstrap_draws_", y, ".csv")), row.names=FALSE)
  # R_b outlier exclusion
  z <- (d[[y]] - mean(d[[y]])) / sd(d[[y]]); keep <- abs(z) <= 3
  mb <- lm_robust(fml(y), data = d[keep, ])
  out[[length(out)+1]] <- data.frame(check="R_b", outcome=y, role=role, estimate=unname(mb$coefficients[term]),
    se=unname(mb$std.error[term]), ci_low=unname(mb$conf.low[term]), ci_high=unname(mb$conf.high[term]),
    p_value=unname(mb$p.value[term]), n_used=sum(keep), n_dropped=sum(!keep), n_bad_resamples=NA,
    same_dir_sig=(mb$coefficients[term] < 0 & mb$p.value[term] < 0.001))
}
# R_c alternative positive outcome
d <- est_sample("positive_emo_rv")
pm <- (d$Secured + d$Happiness) / 2; d$pos_mean_z <- (pm - mean(pm)) / sd(pm)
mc <- lm_robust(fml("pos_mean_z"), data = d)
out[[length(out)+1]] <- data.frame(check="R_c", outcome="pos_mean_z", role="primary (T1)", estimate=unname(mc$coefficients[term]),
  se=unname(mc$std.error[term]), ci_low=unname(mc$conf.low[term]), ci_high=unname(mc$conf.high[term]),
  p_value=unname(mc$p.value[term]), n_used=nrow(d), n_dropped=0, n_bad_resamples=NA,
  same_dir_sig=(mc$coefficients[term] < 0 & mc$p.value[term] < 0.001))
res <- do.call(rbind, out); rownames(res) <- NULL
write.csv(res, file.path(R, "robustness.csv"), row.names=FALSE); print(res, digits=5)
