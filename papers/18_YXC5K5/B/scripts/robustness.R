# Usage: Rscript robustness.R <session.RData> <label> <outlier_rule: none|z3>
# Implements PREREG section 3: hamming losses of the 18 LLM specs + 2 undergraduate rows by row position (authors' pairing as in the
# loaded session), optional |z|>3 exclusion on k = rowSums(pi10mat), and the percentile bootstrap (seed 20261010, 1000 resamples).
args <- commandArgs(trailingOnly = TRUE)
sess <- args[1]; label <- args[2]; rule <- args[3]
outdir <- "outputs"
load(sess)
m8 <- list("GPT 4 Turbo 8 Zero Shot" = gpt10matx, "GPT 4 Turbo 8 One Shot" = gpt10mat_onex, "GPT 4 Turbo 8 Few Shot" = gpt10mat_fewx,
           "GPT 4o 8 Zero Shot" = gpt4o10matx, "GPT 4o 8 One Shot" = gpt4o10mat_onex, "GPT 4o 8 Few Shot" = gpt4o10mat_fewx,
           "Claude Sonnet 3.5 8 Zero Shot" = claude10matx, "Claude Sonnet 3.5 8 One Shot" = claude10mat_onex, "Claude Sonnet 3.5 8 Few Shot" = claude10mat_fewx)
m4 <- list("GPT 4 Turbo 4 Zero Shot" = gpt4matx, "GPT 4 Turbo 4 One Shot" = gpt4mat_onex, "GPT 4 Turbo 4 Few Shot" = gpt4mat_fewx,
           "GPT 4o 4 Zero Shot" = gpt4o4matx, "GPT 4o 4 One Shot" = gpt4o4mat_onex, "GPT 4o 4 Few Shot" = gpt4o4mat_fewx,
           "Claude Sonnet 3.5 4 Zero Shot" = claude4matx, "Claude Sonnet 3.5 4 One Shot" = claude4mat_onex, "Claude Sonnet 3.5 4 Few Shot" = claude4mat_fewx)
B8 <- as.matrix(pi10mat); B4 <- as.matrix(pi4mat); H8 <- as.matrix(hum10matx); H4 <- as.matrix(hum4matx)
n0 <- nrow(B8)
stopifnot(all(sapply(c(m8, m4, list(H8, H4, B4)), nrow) == n0))
keep <- seq_len(n0); n_drop <- 0
if (rule == "z3") {
  k <- rowSums(B8); z <- (k - mean(k)) / sd(k)
  keep <- which(abs(z) <= 3); n_drop <- n0 - length(keep)
  write.csv(data.frame(k = as.integer(names(table(k))), n = as.integer(table(k)),
                       z = (as.integer(names(table(k))) - mean(k)) / sd(k)), file.path(outdir, paste0(label, "_k_distribution.csv")), row.names = FALSE)
}
hl <- function(B, M, idx) mean(sapply(seq_len(ncol(B)), function(j) mean(B[idx, j] != M[idx, j])))
all_hl <- function(idx) {
  c(sapply(m8, function(M) hl(B8, M, idx)), sapply(m4, function(M) hl(B4, M, idx)),
    "Undergraduate 8" = hl(B8, H8, idx), "Undergraduate 4" = hl(B4, H4, idx))
}
point <- all_hl(keep)
llm <- c(names(m8), names(m4))
T1 <- point[["GPT 4o 8 Few Shot"]]; D <- T1 - point[["Undergraduate 8"]]; T3mT1 <- point[["GPT 4o 4 Few Shot"]] - T1
rank_T1 <- sum(point[llm] < T1) + 1
lowest <- T1 <= min(point[llm])
set.seed(20261010)
n <- length(keep)
draws <- t(replicate(1000, { idx <- keep[sample(n, n, replace = TRUE)]; all_hl(idx) }))
bD <- draws[, "GPT 4o 8 Few Shot"] - draws[, "Undergraduate 8"]
bT1 <- draws[, "GPT 4o 8 Few Shot"]
share_lowest <- mean(apply(draws[, llm], 1, function(r) r[["GPT 4o 8 Few Shot"]] <= min(r)))
p <- min(1, 2 * mean(bD <= 0))
ciD <- quantile(bD, c(0.025, 0.975), names = FALSE); ciT1 <- quantile(bT1, c(0.025, 0.975), names = FALSE)
summ <- data.frame(label = label, rule = rule, n_rows = n, n_dropped = n_drop, T1 = T1, U8 = point[["Undergraduate 8"]], D = D,
                   T3_minus_T1 = T3mT1, rank_T1_among_18 = rank_T1, T1_lowest_of_18 = lowest,
                   T1_ci_lo = ciT1[1], T1_ci_hi = ciT1[2], D_ci_lo = ciD[1], D_ci_hi = ciD[2], D_boot_se = sd(bD), p_value = p,
                   share_resamples_T1_lowest = share_lowest,
                   crit_i = lowest, crit_ii = D > 0, crit_iii = ciD[1] > 0,
                   same_direction_and_significance = lowest && D > 0 && ciD[1] > 0)
write.csv(format(summ, digits = 17), file.path(outdir, paste0(label, "_summary.csv")), row.names = FALSE)
write.csv(data.frame(spec = names(point), hamming_loss = format(point, digits = 17)), file.path(outdir, paste0(label, "_point_estimates.csv")), row.names = FALSE)
write.csv(draws, file.path(outdir, paste0(label, "_bootstrap_draws.csv")), row.names = FALSE)
print(t(summ))
