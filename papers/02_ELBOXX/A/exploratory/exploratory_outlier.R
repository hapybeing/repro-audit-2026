# EXPLORATORY, NOT PRE-REGISTERED. 02_ELBOXX, Agent A, added 2026-10-10 after an external reviewer's comment on R_b.
# Reviewer: the pre-registered |z| > 3 rule (R_b) on skewed count variables trims the upper tail by construction.
# These checks probe whether the main correlation (M2, T1: pub_def == 1, secret_alliances vs disputes) is
# tail-driven. They do NOT replace R_a/R_b/R_c and do NOT change the classification.
# Input: the run-of-record analysis frame d saved by scripts/run_pathA.R under faketime 2025-05-06
#        (identical to the shipped d in AJPS_analysis_data.RData).
# Usage: Rscript exploratory_outlier.R <d.rds> <out.json>
args <- commandArgs(trailingOnly = TRUE)
d <- readRDS(args[1]); outfile <- args[2]
library(jsonlite)
pubdef <- d[d$pub_def == 1, ]
x <- pubdef$secret_alliances; y <- pubdef$disputes
stopifnot(!anyNA(x), !anyNA(y))
n <- length(x)

skew_g1 <- function(v) { m <- mean(v); m2 <- mean((v - m)^2); m3 <- mean((v - m)^3); m3 / m2^1.5 }   # moment skewness g1
skew_G1 <- function(v) { k <- length(v); skew_g1(v) * sqrt(k * (k - 1)) / (k - 2) }                    # adjusted Fisher-Pearson G1
describe <- function(v) list(n = length(v), mean = mean(v), sd = sd(v), min = min(v), max = max(v),
  quantiles = as.list(setNames(quantile(v, c(.01, .25, .5, .75, .95, .99), type = 7), c("p01","p25","p50","p75","p95","p99"))),
  share_zero = mean(v == 0), n_distinct = length(unique(v)), skewness_g1 = skew_g1(v), skewness_G1_adjusted = skew_G1(v))

pear <- function(xx, yy) { tt <- cor.test(xx, yy, method = "pearson")
  list(n = length(xx), estimate = unname(tt$estimate), p = tt$p.value, ci_low = tt$conf.int[1], ci_high = tt$conf.int[2],
       ci_method = "Fisher z (cor.test)") }

# bootstrap helper (percentile CI) for robustness of CIs on rank-based estimate
RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(20261010)
B <- 2000
boot_idx <- replicate(B, sample.int(n, replace = TRUE))

# 1. Spearman rho on full data
st <- suppressWarnings(cor.test(x, y, method = "spearman", exact = FALSE))
rho <- unname(st$estimate)
se_fieller <- sqrt(1.06 / (n - 3))
zr <- atanh(rho)
rb <- apply(boot_idx, 2, function(i) cor(x[i], y[i], method = "spearman"))
spearman <- list(n = n, estimate = rho, p = st$p.value,
  ci_low = tanh(zr - qnorm(.975) * se_fieller), ci_high = tanh(zr + qnorm(.975) * se_fieller),
  ci_method = "Fisher z with Fieller-Hartley-Pearson SE sqrt(1.06/(n-3))",
  p_method = "cor.test(method='spearman', exact=FALSE): t approximation, ties present",
  bootstrap = list(B = B, seed = 20261010, ci_low = unname(quantile(rb, .025, type = 7)),
                   ci_high = unname(quantile(rb, .975, type = 7)), se = sd(rb)),
  n_ties_note = sprintf("x has %d distinct values, y has %d distinct values", length(unique(x)), length(unique(y))))

# 2. Pearson after winsorizing each variable at its 1st and 99th percentiles (quantile type 7)
wins <- function(v) { q <- quantile(v, c(.01, .99), type = 7); pmin(pmax(v, q[[1]]), q[[2]]) }
xw <- wins(x); yw <- wins(y)
winsor <- c(pear(xw, yw), list(
  cutoffs = list(secret_alliances = as.list(setNames(quantile(x, c(.01, .99), type = 7), c("p01", "p99"))),
                 disputes = as.list(setNames(quantile(y, c(.01, .99), type = 7), c("p01", "p99")))),
  n_values_changed = list(secret_alliances = sum(xw != x), disputes = sum(yw != y)),
  skewness_g1_after = list(secret_alliances = skew_g1(xw), disputes = skew_g1(yw))))

# 3. Pearson after log(v + 1); both variables are non-negative counts with zeros, so log1p is used
lx <- log1p(x); ly <- log1p(y)
log_both <- c(pear(lx, ly), list(transform = "log(x+1) on both variables",
  skewness_g1_after = list(secret_alliances = skew_g1(lx), disputes = skew_g1(ly))))
log_y_only <- c(pear(x, ly), list(transform = "log(disputes+1) only"))
log_x_only <- c(pear(lx, y), list(transform = "log(secret_alliances+1) only"))

# 4. Decomposition of the pre-registered R_b drop (which variable's |z|>3 rule removes the signal)
zx <- (x - mean(x)) / sd(x); zy <- (y - mean(y)) / sd(y)
rb_x_only <- c(pear(x[abs(zx) <= 3], y[abs(zx) <= 3]), list(rule = "drop |z|>3 on secret_alliances only", n_dropped = sum(abs(zx) > 3),
  min_secret_alliances_dropped = min(x[abs(zx) > 3]), n_distinct_years_dropped = length(unique(pubdef$year[abs(zx) > 3])),
  years_dropped = sort(unique(pubdef$year[abs(zx) > 3])),
  share_of_all_disputes_in_dropped_rows = sum(y[abs(zx) > 3]) / sum(y)))
rb_y_only <- c(pear(x[abs(zy) <= 3], y[abs(zy) <= 3]), list(rule = "drop |z|>3 on disputes only", n_dropped = sum(abs(zy) > 3)))
keep <- abs(zx) <= 3 & abs(zy) <= 3
rb_both <- c(pear(x[keep], y[keep]), list(rule = "drop |z|>3 on either (same as pre-registered R_b, recomputed here for reference)", n_dropped = sum(!keep)))

res <- list(
  label = "EXPLORATORY, NOT PRE-REGISTERED",
  paper_id = "02_ELBOXX",
  purpose = "Reviewer check: is the M2 correlation (T1) robust or driven by the upper tail of skewed count variables?",
  added = "2026-10-10 (IST), after pre-registered results were known; does not change R_a/R_b/R_c or the class",
  generated_by = "papers/02_ELBOXX/A/exploratory/exploratory_outlier.R",
  input = list(file = basename(args[1]), description = "run-of-record d (Path A, faketime 2025-05-06), identical to shipped d",
               sample = "pub_def == 1", x = "secret_alliances", y = "disputes"),
  r_version = R.version.string, run_time = format(Sys.time(), tz = "UTC", usetz = TRUE),
  reference_pearson_full = pear(x, y),
  skewness = list(secret_alliances = describe(x), disputes = describe(y),
                  skewness_definition = "g1 = m3 / m2^1.5 (population moments); G1 = g1 * sqrt(n(n-1))/(n-2)"),
  checks = list(spearman_full = spearman, pearson_winsor_1_99 = winsor, pearson_log1p_both = log_both,
                pearson_log1p_disputes_only = log_y_only, pearson_log1p_secret_only = log_x_only,
                Rb_decomposition = list(x_only = rb_x_only, y_only = rb_y_only, either = rb_both)))
write_json(res, outfile, auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("wrote", outfile, "\n")
