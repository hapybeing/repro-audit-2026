# Agent B: pre-registered robustness checks R_a, R_b, R_c on teste_2 (PREREG.md section 3),
# plus one clearly labelled exploratory (not pre-registered) output on party 45.
# Usage: Rscript robustness.R SESSION.RData OUTDIR
suppressPackageStartupMessages({library(dplyr); library(jsonlite)})
a <- commandArgs(trailingOnly = TRUE); load(a[1]); od <- a[2]
d <- as.data.frame(teste_2); yrs <- sort(unique(d$ano))
r_by <- function(dd) sapply(yrs, function(y) { s <- dd[dd$ano == y, ]; cor(s$HGPE_total, s$VR_RECEITA_total) })
orig <- setNames(r_by(d), yrs)
# R_a stratified bootstrap
set.seed(20261010); B <- 2000
idx <- split(seq_len(nrow(d)), d$ano)
bs <- t(replicate(B, { ii <- unlist(lapply(idx, function(v) v[sample.int(length(v), length(v), replace = TRUE)])); r_by(d[ii, ]) }))
colnames(bs) <- yrs
write.csv(bs, file.path(od, "R_a_bootstrap_draws.csv"), row.names = FALSE)
r18 <- bs[, "2018"]
Ra <- list(estimate = unname(orig["2018"]), ci_low = unname(quantile(r18, 0.025)), ci_high = unname(quantile(r18, 0.975)),
  boot_se = sd(r18), p_value = min(2 * mean(r18 <= 0), 1), share_r2018_gt_r2002 = mean(bs[, "2018"] > bs[, "2002"]),
  orig_r_by_year = as.list(orig), boot_ci_by_year = lapply(as.character(yrs), function(y) unname(quantile(bs[, y], c(.025, .975)))),
  diff_2018_2002 = unname(orig["2018"] - orig["2002"]), seed = 20261010, B = B)
names(Ra$boot_ci_by_year) <- yrs
# R_b outlier exclusion |z|>3 on VR_RECEITA_total within year
Rb <- list(by_year = list())
for (y in yrs) { s <- d[d$ano == y, ]; z <- (s$VR_RECEITA_total - mean(s$VR_RECEITA_total)) / sd(s$VR_RECEITA_total)
  k <- s[abs(z) <= 3, ]; ct <- cor.test(k$HGPE_total, k$VR_RECEITA_total)
  Rb$by_year[[as.character(y)]] <- list(n_before = nrow(s), n_dropped = sum(abs(z) > 3), r = unname(ct$estimate), ci = unname(ct$conf.int[1:2]), p = ct$p.value) }
Rb$estimate <- Rb$by_year[["2018"]]$r; Rb$ci <- Rb$by_year[["2018"]]$ci; Rb$p_value <- Rb$by_year[["2018"]]$p
Rb$diff_2018_2002 <- Rb$by_year[["2018"]]$r - Rb$by_year[["2002"]]$r
# R_c Spearman
Rc <- list(by_year = list())
for (y in yrs) { s <- d[d$ano == y, ]; ct <- cor.test(s$HGPE_total, s$VR_RECEITA_total, method = "spearman", exact = FALSE)
  Rc$by_year[[as.character(y)]] <- list(rho = unname(ct$estimate), p = ct$p.value) }
Rc$estimate <- Rc$by_year[["2018"]]$rho; Rc$p_value <- Rc$by_year[["2018"]]$p
Rc$diff_2018_2002 <- Rc$by_year[["2018"]]$rho - Rc$by_year[["2002"]]$rho
# Exploratory, NOT pre-registered: Figura 5 table if the "´45" entry matched party 45
ps45 <- bd_doxa_programas |> filter(numpartido %in% c("15", "13", "50", "22", "25", "45", "12", "11"))
t45 <- chisq.test(table(ps45$numpartido, ps45$APE3))
Ex <- list(note = "Exploratory, not pre-registered: line 177 filter with '45' instead of the deposited U+00B4 + '45' entry",
  n_rows_added = nrow(ps45) - nrow(partidos_sel), obs_13_Sim = unname(table(ps45$numpartido, ps45$APE3)["13", "Sim"]),
  expected_13_Sim = t45$expected["13", "Sim"], expected_15_Sim = t45$expected["15", "Sim"], chisq_p = t45$p.value)
res <- list(R_a = Ra, R_b = Rb, R_c = Rc, exploratory_party45 = Ex)
write_json(res, file.path(od, "robustness.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 6, pretty = TRUE))
