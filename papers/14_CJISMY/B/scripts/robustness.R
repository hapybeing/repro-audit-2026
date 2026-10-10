# Agent B, 14_CJISMY. Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3).
# Usage: Rscript robustness.R <session.RData> <outdir>
args <- commandArgs(trailingOnly = TRUE)
sess <- args[1]; outdir <- args[2]
suppressPackageStartupMessages(library(fixest))
load(sess)
rhs <- "resource_and_agriculture + n_orgs + regaut + groupsize + incidence_flag + status_pwrrank + any_multiethnic + nightlight_total_pc_log + n_tek_groups"
outcomes <- c(T1_model1 = "disagreement", T2_model3 = "share_disagreement")
d_all <- as.data.frame(mean_h1)
idx <- setdiff(seq_len(nrow(d_all)), full_model_h1$obs_selection$obsRemoved * -1)
if (length(full_model_h1$obs_selection$obsRemoved) == 0) idx <- seq_len(nrow(d_all))
idx2 <- tryCatch(obs(full_model_h1), error = function(e) NULL)
if (!is.null(idx2)) stopifnot(identical(as.integer(idx2), as.integer(idx)))
est <- d_all[idx, ]
cat("Estimation sample rows:", nrow(est), " countries:", length(unique(est$countries_gwid)), "\n")
res <- list()
add <- function(...) res[[length(res) + 1]] <<- data.frame(..., stringsAsFactors = FALSE)
getc <- function(m) { ct <- coeftable(m); if ("resource_and_agriculture" %in% rownames(ct)) ct["resource_and_agriculture", ] else rep(NA_real_, 4) }

for (k in names(outcomes)) {
  y <- outcomes[[k]]
  f_fe <- as.formula(paste(y, "~", rhs, "| countries_gwid"))
  f_po <- as.formula(paste(y, "~", rhs))
  base <- feols(f_fe, cluster = ~countries_gwid, data = est)
  b0 <- getc(base)
  add(check = "baseline_on_est_sample", target = k, estimate = b0[1], se = b0[2], p = b0[4], ci_low = NA, ci_high = NA,
      n = nobs(base), n_dropped = NA, n_failed = NA, note = "")

  # R_a country-cluster bootstrap
  set.seed(20261010)
  countries <- unique(est$countries_gwid)
  B <- 1000; draws <- rep(NA_real_, B); fails <- 0
  for (b in seq_len(B)) {
    pick <- sample(countries, length(countries), replace = TRUE)
    bd <- do.call(rbind, lapply(seq_along(pick), function(j) { x <- est[est$countries_gwid == pick[j], , drop = FALSE]; x$boot_id <- j; x }))
    fb <- tryCatch(feols(as.formula(paste(y, "~", rhs, "| boot_id")), cluster = ~boot_id, data = bd, warn = FALSE, notes = FALSE),
                   error = function(e) NULL)
    cf <- if (is.null(fb)) NA_real_ else unname(coef(fb)["resource_and_agriculture"])
    if (is.na(cf)) fails <- fails + 1 else draws[b] <- cf
  }
  write.csv(data.frame(draw = seq_len(B), coef = draws), file.path(outdir, paste0("R_a_draws_", y, ".csv")), row.names = FALSE)
  ok <- draws[!is.na(draws)]
  q <- quantile(ok, c(0.025, 0.975), names = FALSE)
  pb <- min(1, 2 * min(mean(ok <= 0), mean(ok >= 0)))
  add(check = "R_a", target = k, estimate = b0[1], se = sd(ok), p = pb, ci_low = q[1], ci_high = q[2],
      n = nobs(base), n_dropped = NA, n_failed = fails,
      note = paste0("bootstrap SD as se; percentile 95% CI; ", length(ok), " successful draws of ", B, "; seed 20261010"))

  # R_b Cook's distance > 4/N
  lmf <- lm(as.formula(paste(y, "~", rhs, "+ factor(countries_gwid)")), data = est)
  eq <- abs(unname(coef(lmf)["resource_and_agriculture"]) - b0[1]) < 1e-8
  cd <- cooks.distance(lmf)
  N <- nrow(est)
  nonfinite <- sum(!is.finite(cd))
  drop <- is.finite(cd) & cd > 4 / N
  fb <- feols(f_fe, cluster = ~countries_gwid, data = est[!drop, ])
  bb <- getc(fb)
  z <- (est[[y]] - mean(est[[y]])) / sd(est[[y]])
  add(check = "R_b", target = k, estimate = bb[1], se = bb[2], p = bb[4], ci_low = NA, ci_high = NA,
      n = nobs(fb), n_dropped = sum(drop), n_failed = NA,
      note = paste0("lm coef equals feols coef to 1e-8: ", eq, "; Cook's threshold 4/N = ", signif(4 / N, 4),
                    "; non-finite Cook's distances kept: ", nonfinite, "; |z|>3 rule on outcome would remove: ", sum(abs(z) > 3)))

  # R_c no country fixed effects
  fp <- feols(f_po, cluster = ~countries_gwid, data = est)
  bp <- getc(fp)
  add(check = "R_c", target = k, estimate = bp[1], se = bp[2], p = bp[4], ci_low = NA, ci_high = NA,
      n = nobs(fp), n_dropped = NA, n_failed = NA, note = "pooled OLS with intercept, SE clustered by country")
}
out <- do.call(rbind, res)
out$fixest_version <- as.character(packageVersion("fixest"))
write.csv(out, file.path(outdir, "robustness.csv"), row.names = FALSE)
print(out)
