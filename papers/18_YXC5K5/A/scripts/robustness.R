# Usage: Rscript robustness.R <session.RData> <check: R_a|R_b|R_c> <out_prefix>
# Pre-registered checks (PREREG.md section 3). Bootstrap: set.seed(20261010) once, 1000 resamples of row indices,
# same idx applied to every matrix (authors' row pairing kept). Hamming loss = mean over labels of mean(bench != model).
args <- commandArgs(TRUE)
suppressMessages(library(tidyverse))
e <- new.env(); load(args[1], envir = e); check <- args[2]; pref <- args[3]
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
m8 <- list("Claude Sonnet 3.5 (Zero Shot)" = e$claude10matx, "Claude Sonnet 3.5 (One Shot)" = e$claude10mat_onex,
  "Claude Sonnet 3.5 (Few Shot)" = e$claude10mat_fewx, "GPT 4 Turbo (Zero Shot)" = e$gpt10matx,
  "GPT 4 Turbo (One Shot)" = e$gpt10mat_onex, "GPT 4 Turbo (Few Shot)" = e$gpt10mat_fewx,
  "GPT 4o (Zero Shot)" = e$gpt4o10matx, "GPT 4o (One Shot)" = e$gpt4o10mat_onex, "GPT 4o (Few Shot)" = e$gpt4o10mat_fewx)
m4 <- list("Claude Sonnet 3.5 (Zero Shot)" = e$claude4matx, "Claude Sonnet 3.5 (One Shot)" = e$claude4mat_onex,
  "Claude Sonnet 3.5 (Few Shot)" = e$claude4mat_fewx, "GPT 4 Turbo (Zero Shot)" = e$gpt4matx,
  "GPT 4 Turbo (One Shot)" = e$gpt4mat_onex, "GPT 4 Turbo (Few Shot)" = e$gpt4mat_fewx,
  "GPT 4o (Zero Shot)" = e$gpt4o4matx, "GPT 4o (One Shot)" = e$gpt4o4mat_onex, "GPT 4o (Few Shot)" = e$gpt4o4mat_fewx)
pi10 <- e$pi10mat; pi4 <- e$pi4mat; h10 <- e$hum10matx; h4 <- e$hum4matx
hl <- function(b, m, idx) mean(sapply(1:ncol(b), function(j) mean(b[idx, j] != m[idx, j])))
stats <- function(idx) {
  l8 <- sapply(m8, function(m) hl(pi10, m, idx)); l4 <- sapply(m4, function(m) hl(pi4, m, idx))
  names(l8) <- paste("8", names(l8)); names(l4) <- paste("4", names(l4))
  u8 <- hl(pi10, h10, idx); u4 <- hl(pi4, h4, idx)
  all18 <- c(l8, l4); t1 <- all18[["8 GPT 4o (Few Shot)"]]
  c(all18, U8 = u8, U4 = u4, T1 = t1, D = t1 - u8, T3minusT1 = all18[["4 GPT 4o (Few Shot)"]] - t1,
    rank_T1 = rank(all18, ties.method = "min")[["8 GPT 4o (Few Shot)"]], lowest = as.numeric(t1 <= min(all18)))
}
n <- nrow(pi10)
keep <- 1:n; ndrop <- 0
if (check == "R_b") {
  k <- rowSums(pi10); z <- (k - mean(k)) / sd(k)
  keep <- which(abs(z) <= 3); ndrop <- n - length(keep)
  write.csv(data.frame(k = 0:8, n_rows = sapply(0:8, function(v) sum(k == v)), z = (0:8 - mean(k)) / sd(k)),
            paste0(pref, "_k_distribution.csv"), row.names = FALSE)
}
pt <- stats(keep)
set.seed(20261010)
nk <- length(keep)
B <- t(sapply(1:1000, function(b) { idx <- keep[sample(nk, nk, replace = TRUE)]; stats(idx) }))
write.csv(B, paste0(pref, "_bootstrap_draws.csv"), row.names = FALSE)
q <- function(x) quantile(x, c(0.025, 0.975), names = FALSE)
summ <- data.frame(check = check, n_rows_used = nk, n_dropped = ndrop,
  T1 = pt[["T1"]], U8 = pt[["U8"]], D = pt[["D"]], T3minusT1 = pt[["T3minusT1"]], rank_T1_of_18 = pt[["rank_T1"]],
  T1_lowest_of_18 = pt[["lowest"]] == 1,
  T1_ci_lo = q(B[, "T1"])[1], T1_ci_hi = q(B[, "T1"])[2], D_ci_lo = q(B[, "D"])[1], D_ci_hi = q(B[, "D"])[2],
  D_boot_se = sd(B[, "D"]), p_value = min(1, 2 * mean(B[, "D"] <= 0)),
  share_resamples_T1_lowest = mean(B[, "lowest"]), n_resamples = nrow(B), seed = 20261010)
summ$same_direction_and_significance <- summ$T1_lowest_of_18 & summ$D > 0 & summ$D_ci_lo > 0
write.csv(summ, paste0(pref, "_summary.csv"), row.names = FALSE)
write.csv(data.frame(model = names(pt), value = format(pt, digits = 17)), paste0(pref, "_point_estimates.csv"), row.names = FALSE)
print(t(summ))
