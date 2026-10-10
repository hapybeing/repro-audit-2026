# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3) on teste_2 as built by the
# authors' code (session saved after the deposited script ran on the v1 file mapping), plus one
# clearly labelled EXPLORATORY check (not pre-registered, CHANGELOG #4e): Figura 5 chi-square with
# party 45 matched as "45". Args: RUNDIR OUTDIR
suppressPackageStartupMessages({library(dplyr); library(jsonlite)})
args <- commandArgs(trailingOnly = TRUE)
rundir <- args[1]; outdir <- args[2]
load(file.path(rundir, "session_after_script.RData"))
d <- as.data.frame(teste_2)
years <- sort(unique(d$ano))
pear <- function(x) if (nrow(x) > 2) cor(x$HGPE_total, x$VR_RECEITA_total) else NA_real_

# R_a: stratified bootstrap
set.seed(20261010)
B <- 2000
idx_by_year <- split(seq_len(nrow(d)), d$ano)
boot <- matrix(NA_real_, B, length(years), dimnames = list(NULL, as.character(years)))
for (b in seq_len(B)) {
  for (y in as.character(years)) {
    ii <- idx_by_year[[y]]
    s <- d[sample(ii, length(ii), replace = TRUE), ]
    boot[b, y] <- pear(s)
  }
}
write.csv(boot, file.path(outdir, "R_a_bootstrap_draws.csv"), row.names = FALSE)
orig <- sapply(as.character(years), function(y) pear(d[d$ano == as.numeric(y), ]))
r18 <- boot[, "2018"]
R_a <- list(
  id = "R_a", seed = 20261010, B = B,
  estimate_r2018 = unname(orig["2018"]),
  ci_low = unname(quantile(r18, 0.025)), ci_high = unname(quantile(r18, 0.975)),
  boot_se = sd(r18),
  p_boot = min(2 * mean(r18 <= 0), 1),
  share_r2018_gt_r2002 = mean(boot[, "2018"] > boot[, "2002"]),
  orig_r_by_year = as.list(orig),
  ci_by_year = lapply(as.character(years), function(y) unname(quantile(boot[, y], c(0.025, 0.975)))),
  diff_2018_2002 = unname(orig["2018"] - orig["2002"]),
  diff_ci = unname(quantile(boot[, "2018"] - boot[, "2002"], c(0.025, 0.975)))
)
names(R_a$ci_by_year) <- as.character(years)

# R_b: drop |z| > 3 on VR_RECEITA_total within year
R_b_rows <- list(); dropped <- list()
for (y in years) {
  x <- d[d$ano == y, ]
  z <- (x$VR_RECEITA_total - mean(x$VR_RECEITA_total)) / sd(x$VR_RECEITA_total)
  keep <- abs(z) <= 3
  x2 <- x[keep, ]
  ct <- cor.test(x2$HGPE_total, x2$VR_RECEITA_total)
  dropped[[as.character(y)]] <- sum(!keep)
  R_b_rows[[as.character(y)]] <- list(r = unname(ct$estimate), ci = unname(ct$conf.int[1:2]),
                                      p = ct$p.value, n = nrow(x2), dropped = sum(!keep))
}
R_b <- list(id = "R_b", by_year = R_b_rows,
            diff_2018_2002 = R_b_rows[["2018"]]$r - R_b_rows[["2002"]]$r)

# R_c: Spearman
R_c_rows <- list()
for (y in years) {
  x <- d[d$ano == y, ]
  ct <- suppressWarnings(cor.test(x$HGPE_total, x$VR_RECEITA_total, method = "spearman", exact = FALSE))
  R_c_rows[[as.character(y)]] <- list(rho = unname(ct$estimate), p = ct$p.value, n = nrow(x))
}
R_c <- list(id = "R_c", by_year = R_c_rows,
            diff_2018_2002 = R_c_rows[["2018"]]$rho - R_c_rows[["2002"]]$rho)

# EXPLORATORY (not pre-registered): Figura 5 filter with "45" instead of the deposited "\u00b445"
ps45 <- bd_doxa_programas |>
  filter(numpartido %in% c("15", "13", "50", "22", "25", "45", "12", "11"))
t45 <- chisq.test(table(ps45$numpartido, ps45$APE3))
tab45 <- table(ps45$numpartido, ps45$APE3)
EXP <- list(id = "EXPLORATORY_party45",
            note = "Not pre-registered. Deposited line 177 has '\u00b445', which matches no row; here '45' is used.",
            rows_party45 = sum(ps45$numpartido == 45, na.rm = TRUE),
            obs_13_Sim = tab45["13", "Sim"], exp_13_Sim = t45$expected["13", "Sim"],
            obs_15_Sim = tab45["15", "Sim"], exp_15_Sim = t45$expected["15", "Sim"],
            obs_45_Sim = tab45["45", "Sim"], exp_45_Sim = t45$expected["45", "Sim"],
            chisq = unname(t45$statistic), df = unname(t45$parameter), p = t45$p.value,
            deposited_filter_rows = nrow(partidos_sel), filter45_rows = nrow(ps45))

out <- list(R_a = R_a, R_b = R_b, R_c = R_c, exploratory_party45 = EXP)
write_json(out, file.path(outdir, "robustness.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat(toJSON(out, auto_unbox = TRUE, digits = 6, pretty = TRUE))
