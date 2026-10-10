# Agent A, 09_4U8CTG. Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3).
# Builds the `zemmour` analysis sample exactly as 02 lines 196-213 do, from the deposited CSV.
suppressPackageStartupMessages(library(tidyverse))
OUT <- Sys.getenv("OUTDIR")
fr_exp <- read_csv("data/study2_experiment_data.csv", show_col_types = FALSE) |>
  mutate(across(where(is.character), as.factor)) |>
  mutate(opened_quest = as.character(opened_quest)) |>
  filter(!is.na(treatment), !is.na(swd_ch))
zemmour <- fr_exp |> filter(block == "EZ")
stopifnot(levels(zemmour$treatment)[1] == "control")
TERM <- "treatmentwin_mainstream"
res <- list(); add <- function(...) res[[length(res) + 1]] <<- data.frame(...)

ols <- function(f, d) { s <- summary(lm(f, data = d))$coefficients; s[TERM, ] }

# ---- R_a stratified case bootstrap ----
set.seed(20261010)
boot_one <- function(dv, d) {
  d <- d[!is.na(d[[dv]]), ]
  f <- as.formula(paste(dv, "~ treatment"))
  est0 <- ols(f, d)[1]
  idx_by_arm <- split(seq_len(nrow(d)), d$treatment, drop = TRUE)
  b <- replicate(2000, {
    ii <- unlist(lapply(idx_by_arm, function(ix) ix[sample.int(length(ix), length(ix), replace = TRUE)]))
    coef(lm(f, data = d[ii, ]))[TERM]
  })
  q <- quantile(b, c(0.025, 0.975), names = FALSE)
  p <- min(1, 2 * min(mean(b >= 0), mean(b <= 0)))
  add(check = "R_a", dv = dv, n = nrow(d), estimate = est0, se = sd(b), ci_low = q[1], ci_high = q[2],
      p = p, dropped = NA, dropped_arms = NA, extra = paste0("B=2000; n_NA_boot=", sum(is.na(b))))
}
boot_one("swd_ch", zemmour)
boot_one("affect_LREM_ch", zemmour)   # continues same RNG stream

# ---- R_b |z| > 3 exclusion ----
outl <- function(dv, d) {
  d <- d[!is.na(d[[dv]]), ]
  z <- (d[[dv]] - mean(d[[dv]])) / sd(d[[dv]])
  drop <- abs(z) > 3
  arms <- if (any(drop)) paste(names(table(droplevels(d$treatment[drop]))), table(droplevels(d$treatment[drop])), sep = ":", collapse = ";") else ""
  dk <- d[!drop, ]
  s <- ols(as.formula(paste(dv, "~ treatment")), dk)
  add(check = "R_b", dv = dv, n = nrow(dk), estimate = s[1], se = s[2],
      ci_low = s[1] - qt(0.975, df = nrow(dk) - 5) * s[2], ci_high = s[1] + qt(0.975, df = nrow(dk) - 5) * s[2],
      p = s[4], dropped = sum(drop), dropped_arms = arms,
      extra = paste0("range_z=", round(min(z), 3), "..", round(max(z), 3)))
}
outl("swd_ch", zemmour)
outl("affect_LREM_ch", zemmour)

# ---- R_c ANCOVA ----
diag_swd  <- sum(zemmour$swd_ch != zemmour$swd_w2 - zemmour$swd_w1, na.rm = TRUE)
diag_swd_na <- sum(is.na(zemmour$swd_ch != zemmour$swd_w2 - zemmour$swd_w1))
diag_lrem <- sum(zemmour$affect_LREM_ch != zemmour$affect_LREM_w2 - zemmour$affect_LREM_w1, na.rm = TRUE)
writeLines(c(paste0("rows_swd_ch_ne_w2_minus_w1=", diag_swd), paste0("rows_swd_comparison_NA=", diag_swd_na),
             paste0("rows_lrem_ch_ne_w2_minus_w1=", diag_lrem)), file.path(OUT, "R_c_diagnostic.txt"))
anc <- function(f, label) {
  m <- lm(f, data = zemmour); s <- summary(m)$coefficients[TERM, ]; ci <- confint(m)[TERM, ]
  add(check = "R_c", dv = label, n = nobs(m), estimate = s[1], se = s[2], ci_low = ci[1], ci_high = ci[2],
      p = s[4], dropped = NA, dropped_arms = NA, extra = deparse(f))
}
anc(swd_w2 ~ treatment + swd_w1, "swd_w2")
anc(affect_LREM_w2 ~ treatment + affect_LREM_w1, "affect_LREM_w2")

out <- do.call(rbind, res)
write.csv(out, file.path(OUT, "robustness.csv"), row.names = FALSE)
print(out)
