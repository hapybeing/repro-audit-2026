# Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3). Usage: Rscript robustness.R <outdir>
args <- commandArgs(TRUE); outdir <- if (length(args)) args[1] else "outputs"
suppressPackageStartupMessages({library(fixest); library(dplyr)})
load(file.path(outdir, "session.RData"))
rhs <- "resource_and_agriculture + n_orgs + regaut + groupsize + incidence_flag + status_pwrrank + any_multiethnic + nightlight_total_pc_log + n_tek_groups"
est <- as.data.frame(mean_h1)[obs(full_model_h1), ]
N <- nrow(est); cat("estimation sample N =", N, " countries =", length(unique(est$countries_gwid)), "\n")
res <- list(); key <- "resource_and_agriculture"
for (y in c("disagreement", "share_disagreement")) {
  f_fe <- as.formula(paste(y, "~", rhs, "| countries_gwid")); f_ols <- as.formula(paste(y, "~", rhs))
  m0 <- feols(f_fe, cluster = ~countries_gwid, data = est); b0 <- coef(m0)[key]
  # R_a country cluster bootstrap
  set.seed(20261010)
  ctry <- unique(est$countries_gwid); B <- 1000; draws <- rep(NA_real_, B); nfail <- 0
  for (b in 1:B) {
    s <- sample(ctry, length(ctry), replace = TRUE)
    bd <- do.call(rbind, lapply(seq_along(s), function(i) { x <- est[est$countries_gwid == s[i], ]; x$boot_id <- i; x }))
    fit <- tryCatch(feols(as.formula(paste(y, "~", rhs, "| boot_id")), cluster = ~boot_id, data = bd, notes = FALSE, warn = FALSE), error = function(e) NULL)
    if (is.null(fit) || !(key %in% names(coef(fit)))) { nfail <- nfail + 1 } else draws[b] <- coef(fit)[key]
  }
  ok <- draws[!is.na(draws)]
  q <- quantile(ok, c(.025, .975), names = FALSE)
  pb <- min(1, 2 * min(mean(ok <= 0), mean(ok >= 0)))
  write.csv(data.frame(draw = 1:B, coef = draws), file.path(outdir, paste0("R_a_bootstrap_draws_", y, ".csv")), row.names = FALSE)
  res[[length(res)+1]] <- data.frame(check = "R_a", outcome = y, estimate = b0, se = sd(ok), ci_lo = q[1], ci_hi = q[2], p = pb,
                                     n_used = N, n_dropped = NA, n_boot_ok = length(ok), n_boot_failed = nfail, note = "")
  # R_b Cook's distance > 4/N
  ml <- lm(as.formula(paste(y, "~", rhs, "+ factor(countries_gwid)")), data = est)
  eqdiff <- abs(coef(ml)[key] - b0)
  cd <- cooks.distance(ml); nonfin <- sum(!is.finite(cd))
  drop <- is.finite(cd) & cd > 4 / N
  mb <- feols(f_fe, cluster = ~countries_gwid, data = est[!drop, ]); cb <- coeftable(mb)
  z <- (est[[y]] - mean(est[[y]])) / sd(est[[y]])
  res[[length(res)+1]] <- data.frame(check = "R_b", outcome = y, estimate = cb[key,1], se = cb[key,2], ci_lo = NA, ci_hi = NA, p = cb[key,4],
                                     n_used = nobs(mb), n_dropped = sum(drop), n_boot_ok = NA, n_boot_failed = NA,
                                     note = sprintf("lm vs feols coef abs diff %.3g; nonfinite Cook's kept %d; |z|>3 on outcome would drop %d", eqdiff, nonfin, sum(abs(z) > 3)))
  # R_c no country FE
  mc <- feols(f_ols, cluster = ~countries_gwid, data = est); cc <- coeftable(mc)
  res[[length(res)+1]] <- data.frame(check = "R_c", outcome = y, estimate = cc[key,1], se = cc[key,2], ci_lo = NA, ci_hi = NA, p = cc[key,4],
                                     n_used = nobs(mc), n_dropped = NA, n_boot_ok = NA, n_boot_failed = NA, note = "")
}
out <- do.call(rbind, res); rownames(out) <- NULL
write.csv(out, file.path(outdir, "robustness.csv"), row.names = FALSE); print(out, digits = 6)
