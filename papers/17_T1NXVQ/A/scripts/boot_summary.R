# Agent A, 17_T1NXVQ: summarise step-6 draws (seeds 1..K) and R_a draws (seeds 1001..1000+K);
# compare step-6 draws with the deposited pool_se.ls.rds rows for the same seeds (informative only).
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/A/outputs"
dep <- readRDS("/workspace/audit_runs/17_T1NXVQ/A/deposited_models/pool_se.ls.rds")
dep_idx <- c(pool_ldv = 1, pool_xsec = 2)   # order of form.ls in analysis_pool.R
key <- c(pool_xsec = "cuteth", pool_ldv = "cuteth_lag")
summ <- list(); cmp <- list()
for (nm in c("pool_xsec", "pool_ldv")) {
  fit <- file.path(OUT, paste0("fit_", nm, "_main.csv"))
  if (!file.exists(fit)) next
  est <- read.csv(fit, check.names = FALSE)
  for (set in c("authorseeds", "ra_seeds")) {
    f <- file.path(OUT, paste0("boot_", set, "_", nm, ".csv"))
    if (!file.exists(f)) next
    b <- read.csv(f, check.names = FALSE)
    ok <- b[!b$failed, , drop = FALSE]
    for (term in est$term) {
      if (!term %in% names(ok)) next
      x <- ok[[term]]; p <- est$estimate[est$term == term]
      sdv <- if (length(x) >= 2) sd(x) else NA
      summ[[length(summ) + 1]] <- data.frame(model = nm, seed_set = set, term = term, point_estimate = p,
        n_draws_ok = length(x), n_draws_failed = sum(b$failed), seeds = paste(b$seed, collapse = ";"),
        boot_mean = mean(x), boot_sd = sdv, ci_lo_1.96sd = p - 1.96 * sdv, ci_hi_1.96sd = p + 1.96 * sdv,
        perc_2.5 = if (length(x)) unname(quantile(x, .025)) else NA, perc_97.5 = if (length(x)) unname(quantile(x, .975)) else NA,
        excludes_zero = if (is.na(sdv)) NA else (p - 1.96 * sdv > 0 | p + 1.96 * sdv < 0),
        mean_draw_seconds = mean(b$seconds))
    }
    if (set == "authorseeds") {
      D <- dep[[dep_idx[nm]]]$beta_boot
      for (r in seq_len(nrow(ok))) {
        s <- ok$seed[r]
        for (term in colnames(D)) cmp[[length(cmp) + 1]] <- data.frame(model = nm, seed = s, term = term,
          reproduced_draw = ok[[term]][r], deposited_draw_row_seed = D[s, term], abs_diff = abs(ok[[term]][r] - D[s, term]))
      }
    }
  }
}
S <- do.call(rbind, summ)
write.csv(S, file.path(OUT, "boot_summary.csv"), row.names = FALSE)
if (length(cmp)) write.csv(do.call(rbind, cmp), file.path(OUT, "boot_vs_deposited.csv"), row.names = FALSE)
# SD ratio R_a vs step 6 (descriptive, factor 1.5 rule)
if (!is.null(S)) {
  r <- merge(S[S$seed_set == "authorseeds", c("model", "term", "boot_sd")], S[S$seed_set == "ra_seeds", c("model", "term", "boot_sd")],
             by = c("model", "term"), suffixes = c("_authorseeds", "_ra"))
  r$sd_ratio_ra_over_authorseeds <- r$boot_sd_ra / r$boot_sd_authorseeds
  r$differs_more_than_1.5x <- r$sd_ratio_ra_over_authorseeds > 1.5 | r$sd_ratio_ra_over_authorseeds < 1 / 1.5
  write.csv(r, file.path(OUT, "boot_sd_ratio.csv"), row.names = FALSE)
  print(S[S$term %in% key, ], digits = 5)
}

# Added at finish (agent A): pre-registered significance rule for R_b and R_c (PREREG section 3):
# same direction and significance = estimate > 0 AND estimate - 1.96 x SD_boot > 0, SD_boot = SD of the step-6 draws
# (authors' seeds 1..K) for the same coefficient in the same model. Only variants whose fit file exists are written.
sig <- list()
for (nm in names(key)) {
  term <- key[[nm]]
  sb <- if (!is.null(S)) S[S$model == nm & S$seed_set == "authorseeds" & S$term == term, ] else NULL
  sd_boot <- if (!is.null(sb) && nrow(sb) == 1) sb$boot_sd else NA
  for (v in c("rb", "rc")) {
    f <- file.path(OUT, paste0("fit_", nm, "_", v, ".csv"))
    if (!file.exists(f)) { sig[[length(sig) + 1]] <- data.frame(model = nm, variant = v, term = term, ran = FALSE,
      estimate = NA, maxlik_se = NA, sd_boot_step6 = sd_boot, ci_lo_1.96sd = NA, ci_hi_1.96sd = NA, same_dir_and_sig = NA); next }
    fv <- read.csv(f, check.names = FALSE); e <- fv$estimate[fv$term == term]; se <- fv$maxlik_se[fv$term == term]
    sig[[length(sig) + 1]] <- data.frame(model = nm, variant = v, term = term, ran = TRUE, estimate = e, maxlik_se = se,
      sd_boot_step6 = sd_boot, ci_lo_1.96sd = e - 1.96 * sd_boot, ci_hi_1.96sd = e + 1.96 * sd_boot,
      same_dir_and_sig = if (is.na(sd_boot)) NA else (e > 0 & e - 1.96 * sd_boot > 0))
  }
}
G <- do.call(rbind, sig)
write.csv(G, file.path(OUT, "robustness_significance.csv"), row.names = FALSE)
print(G, digits = 5)
