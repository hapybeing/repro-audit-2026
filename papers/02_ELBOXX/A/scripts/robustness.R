# Pre-registered robustness checks R_a, R_b, R_c and supplementary S1, S2 (PREREG.md section 3),
# run on a saved analysis data frame `d`. Usage: Rscript robustness.R <d.rds> <label> <outdir>
args <- commandArgs(trailingOnly = TRUE)
d <- readRDS(args[1]); label <- args[2]; outdir <- args[3]
library(sandwich); library(lmtest)
pubdef <- d[d$pub_def == 1, ]
out <- list(); add <- function(...) out[[length(out) + 1]] <<- data.frame(d_source = label, ...)
ct <- function(id, x, y, note) { tt <- cor.test(x, y)
  add(check = id, n = length(x), estimate = unname(tt$estimate), se = NA, ci_low = tt$conf.int[1],
      ci_high = tt$conf.int[2], p = tt$p.value, n_dropped = NA, note = note) }
# R_a bootstrap
RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(20261009)
rb <- numeric(1000)
for (b in 1:1000) { idx <- sample.int(nrow(pubdef), replace = TRUE)
  rb[b] <- cor(pubdef$secret_alliances[idx], pubdef$disputes[idx]) }
q <- quantile(rb, c(0.025, 0.975), type = 7)
add(check = "R_a", n = nrow(pubdef), estimate = cor(pubdef$secret_alliances, pubdef$disputes), se = sd(rb),
    ci_low = q[[1]], ci_high = q[[2]], p = NA, n_dropped = NA,
    note = sprintf("bootstrap 1000 reps seed 20261009; NA replicates=%d; share of reps <= 0: %g", sum(is.na(rb)), mean(rb <= 0, na.rm = TRUE)))
write.csv(data.frame(rep = 1:1000, r = rb), file.path(outdir, paste0("Ra_boot_reps_", label, ".csv")), row.names = FALSE)
# R_b outliers |z|>3 on either variable
zx <- (pubdef$secret_alliances - mean(pubdef$secret_alliances)) / sd(pubdef$secret_alliances)
zy <- (pubdef$disputes - mean(pubdef$disputes)) / sd(pubdef$disputes)
keep <- !(abs(zx) > 3 | abs(zy) > 3)
tt <- cor.test(pubdef$secret_alliances[keep], pubdef$disputes[keep])
add(check = "R_b", n = sum(keep), estimate = unname(tt$estimate), se = NA, ci_low = tt$conf.int[1], ci_high = tt$conf.int[2],
    p = tt$p.value, n_dropped = sum(!keep),
    note = sprintf("dropped |z|>3: on secret_alliances %d, on disputes %d", sum(abs(zx) > 3), sum(abs(zy) > 3)))
# R_c OLS slope with year-clustered SE (HC1)
m <- lm(disputes ~ secret_alliances, data = pubdef)
cc <- coeftest(m, vcov = vcovCL(m, cluster = ~year, type = "HC1"))
ci <- coefci(m, vcov. = vcovCL(m, cluster = ~year, type = "HC1"))["secret_alliances", ]
add(check = "R_c", n = nobs(m), estimate = cc["secret_alliances", 1], se = cc["secret_alliances", 2],
    ci_low = ci[1], ci_high = ci[2], p = cc["secret_alliances", 4], n_dropped = NA,
    note = sprintf("OLS slope, vcovCL cluster=year HC1; clusters=%d; t df=%d; conventional OLS SE=%g p=%g",
                   length(unique(pubdef$year)), m$df.residual, summary(m)$coef[2, 2], summary(m)$coef[2, 4]))
# S1 pub_def >= 1
s1 <- d[d$pub_def >= 1, ]; ct("S1", s1$secret_alliances, s1$disputes, "pub_def >= 1")
# S2 year <= 2014
s2 <- pubdef[pubdef$year <= 2014, ]; ct("S2", s2$secret_alliances, s2$disputes, "pub_def == 1 and year <= 2014")
res <- do.call(rbind, out)
write.csv(res, file.path(outdir, paste0("robustness_", label, ".csv")), row.names = FALSE)
options(digits = 10); print(res[, 1:9])
