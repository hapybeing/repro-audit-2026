# Pre-registered robustness checks R_a, R_b, R_c and supplementary S1, S2 (PREREG.md section 3),
# run exactly as written on pubdef <- d[d$pub_def == 1, ] built from the Path A d
# (Path A run with the date environment fix; see diffs/README.md).
# Usage: Rscript robustness.R <scratch objs dir> <REPO B dir>
args <- commandArgs(trailingOnly = TRUE)
S <- args[1]; B <- args[2]
o <- readRDS(file.path(S, "pathA_fixed_objects.rds"))
d <- o$d
pubdef <- d[d$pub_def == 1, ]
x <- pubdef$secret_alliances; y <- pubdef$disputes
res <- list()

# R_a: nonparametric bootstrap, 1000 reps
RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(20261009)
rb <- numeric(1000)
for (b in 1:1000) {
  idx <- sample.int(nrow(pubdef), replace = TRUE)
  rb[b] <- cor(pubdef$secret_alliances[idx], pubdef$disputes[idx])
}
q <- quantile(rb, c(0.025, 0.975), type = 7)
write.csv(data.frame(rep = 1:1000, r_b = rb), file.path(B, "outputs", "R_a_bootstrap_draws.csv"), row.names = FALSE)
res$R_a <- data.frame(id = "R_a", estimate = cor(x, y), se = sd(rb), ci_lo = q[1], ci_hi = q[2],
                      p_value = NA, n = nrow(pubdef), n_dropped = NA, note = "full-sample r; bootstrap SE and percentile CI")

# R_b: drop |z| > 3 on either variable
zx <- (x - mean(x)) / sd(x); zy <- (y - mean(y)) / sd(y)
keep <- !(abs(zx) > 3 | abs(zy) > 3)
tb <- cor.test(x[keep], y[keep])
res$R_b <- data.frame(id = "R_b", estimate = unname(tb$estimate), se = NA, ci_lo = tb$conf.int[1], ci_hi = tb$conf.int[2],
                      p_value = tb$p.value, n = sum(keep), n_dropped = sum(!keep),
                      note = sprintf("dropped |z|>3: on disputes %d, on secret_alliances %d", sum(abs(zy) > 3), sum(abs(zx) > 3)))

# R_c: OLS slope with year-clustered HC1 SE
library(sandwich); library(lmtest)
m <- lm(disputes ~ secret_alliances, data = pubdef)
ct <- coeftest(m, vcov = vcovCL(m, cluster = ~year, type = "HC1"))
ci <- coefci(m, vcov. = vcovCL(m, cluster = ~year, type = "HC1"))
res$R_c <- data.frame(id = "R_c", estimate = ct["secret_alliances", 1], se = ct["secret_alliances", 2],
                      ci_lo = ci["secret_alliances", 1], ci_hi = ci["secret_alliances", 2],
                      p_value = ct["secret_alliances", 4], n = nobs(m), n_dropped = NA,
                      note = sprintf("OLS slope; clusters (years) = %d; conventional OLS SE %.6g p %.3g; t-based CI with df=%d",
                                     length(unique(pubdef$year)), summary(m)$coef[2, 2], summary(m)$coef[2, 4], m$df.residual))

# S1: pub_def >= 1
p1 <- d[d$pub_def >= 1, ]; t1 <- cor.test(p1$secret_alliances, p1$disputes)
res$S1 <- data.frame(id = "S1", estimate = unname(t1$estimate), se = NA, ci_lo = t1$conf.int[1], ci_hi = t1$conf.int[2],
                     p_value = t1$p.value, n = nrow(p1), n_dropped = NA, note = "pub_def >= 1")
# S2: year <= 2014
p2 <- pubdef[pubdef$year <= 2014, ]; t2 <- cor.test(p2$secret_alliances, p2$disputes)
res$S2 <- data.frame(id = "S2", estimate = unname(t2$estimate), se = NA, ci_lo = t2$conf.int[1], ci_hi = t2$conf.int[2],
                     p_value = t2$p.value, n = nrow(p2), n_dropped = NA, note = "pub_def == 1 and year <= 2014")

out <- do.call(rbind, res)
write.csv(out, file.path(B, "outputs", "robustness_results.csv"), row.names = FALSE)
print(out, digits = 8)
print(ct)
