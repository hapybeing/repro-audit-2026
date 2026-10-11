# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3), agent B.
# Uses the data frame as built by the authors' appendix script (outputs/dta_after_appendix_script.rds).
# Resumable: bootstrap draws and RNG state saved every 100 resamples.
suppressMessages({library(MASS); library(sandwich); library(lmtest)})
OUT <- Sys.getenv("OUTDIR")
dta <- readRDS(file.path(OUT, "dta_after_appendix_script.rds"))
mods <- readRDS(file.path(OUT, "models_appendix.rds"))
f1 <- unions ~ strike + pro_strike + anti_strike + double
f7 <- factor(Support_teachers) ~ strike + pro_strike + anti_strike + double
d1 <- as.data.frame(dta[!is.na(dta$unions) & !is.na(dta$Treatment), ])
d7 <- as.data.frame(dta[!is.na(dta$Support_teachers) & !is.na(dta$Treatment), ])
stopifnot(nrow(d1) == nobs(mods$m1), nrow(d7) == nobs(mods$m7))
wald <- function(m, term) { s <- summary(m)$coefficients; z <- s[term, "t value"]
  c(est = s[term, "Value"], se = s[term, "Std. Error"], p = 2 * pnorm(-abs(z))) }

## R_a bootstrap
K <- 1000; st <- file.path(OUT, "Ra_boot_state.rds")
if (file.exists(st)) { S <- readRDS(st); assign(".Random.seed", S$seed, envir = .GlobalEnv) } else {
  set.seed(20261011); S <- list(b1 = numeric(0), f1 = 0, b7 = numeric(0), f7 = 0, seed = .Random.seed) }
fitb <- function(d, f, term) { r <- tryCatch(polr(f, data = d, Hess = TRUE), error = function(e) NULL)
  if (is.null(r) || r$convergence != 0 || !(term %in% names(coef(r)))) return(NA_real_); unname(coef(r)[term]) }
for (which in c("1", "7")) {
  d <- if (which == "1") d1 else d7; f <- if (which == "1") f1 else f7; term <- if (which == "1") "anti_strike" else "pro_strike"
  bk <- paste0("b", which); fk <- paste0("f", which)
  while (length(S[[bk]]) < K) {
    for (i in 1:100) { v <- fitb(d[sample(nrow(d), nrow(d), replace = TRUE), ], f, term)
      S[[bk]] <- c(S[[bk]], v); if (is.na(v)) S[[fk]] <- S[[fk]] + 1 }
    S$seed <- .Random.seed; saveRDS(S, st); cat("saved", bk, length(S[[bk]]), "\n")
  }
}
write.csv(data.frame(draw = 1:K, m1_anti_strike = S$b1, m7_pro_strike = S$b7), file.path(OUT, "Ra_bootstrap_draws.csv"), row.names = FALSE)
bsum <- function(b, orig, label) { b2 <- b[!is.na(b)]
  q <- quantile(b2, c(0.025, 0.975, 0.005, 0.995))
  data.frame(check = "R_a", target = label, estimate = orig, se = sd(b2), ci95_lo = q[1], ci95_hi = q[2], ci99_lo = q[3], ci99_hi = q[4],
             p_value = min(2 * min(mean(b2 <= 0), mean(b2 >= 0)), 1), n_ok = length(b2), n_failed = sum(is.na(b)), n_dropped = NA, row.names = NULL) }
ra <- rbind(bsum(S$b1, coef(mods$m1)["anti_strike"], "T1"), bsum(S$b7, coef(mods$m7)["pro_strike"], "T2"))

## R_b age |z| > 3
age <- as.numeric(dta$d2); z <- (age - mean(age, na.rm = TRUE)) / sd(age, na.rm = TRUE)
drop <- !is.na(z) & abs(z) > 3
dk <- as.data.frame(dta[!drop, ])
rb1 <- polr(f1, data = dk, Hess = TRUE); rb7 <- polr(f7, data = dk, Hess = TRUE)
w1 <- wald(rb1, "anti_strike"); w7 <- wald(rb7, "pro_strike")
rb <- rbind(data.frame(check = "R_b", target = "T1", estimate = w1["est"], se = w1["se"], ci95_lo = NA, ci95_hi = NA, ci99_lo = NA, ci99_hi = NA,
                       p_value = w1["p"], n_ok = nobs(rb1), n_failed = NA, n_dropped = sum(drop), row.names = NULL),
            data.frame(check = "R_b", target = "T2", estimate = w7["est"], se = w7["se"], ci95_lo = NA, ci95_hi = NA, ci99_lo = NA, ci99_hi = NA,
                       p_value = w7["p"], n_ok = nobs(rb7), n_failed = NA, n_dropped = sum(drop), row.names = NULL))
writeLines(c(sprintf("age d2: n_nonmissing=%d mean=%.4f sd=%.4f min=%s max=%s n_missing=%d rows_dropped=%d",
  sum(!is.na(age)), mean(age, na.rm = TRUE), sd(age, na.rm = TRUE), min(age, na.rm = TRUE), max(age, na.rm = TRUE), sum(is.na(age)), sum(drop))),
  file.path(OUT, "Rb_age_summary.txt"))

## R_c linear model with HC2 SEs
l1 <- lm(as.numeric(unions) ~ strike + pro_strike + anti_strike + double, data = d1)
l7 <- lm(Support_teachers ~ strike + pro_strike + anti_strike + double, data = d7)
c1 <- coeftest(l1, vcov = vcovHC(l1, type = "HC2"))["anti_strike", ]
c7 <- coeftest(l7, vcov = vcovHC(l7, type = "HC2"))["pro_strike", ]
rc <- rbind(data.frame(check = "R_c", target = "T1", estimate = c1[1], se = c1[2], ci95_lo = NA, ci95_hi = NA, ci99_lo = NA, ci99_hi = NA,
                       p_value = c1[4], n_ok = nobs(l1), n_failed = NA, n_dropped = NA, row.names = NULL),
            data.frame(check = "R_c", target = "T2", estimate = c7[1], se = c7[2], ci95_lo = NA, ci95_hi = NA, ci99_lo = NA, ci99_hi = NA,
                       p_value = c7[4], n_ok = nobs(l7), n_failed = NA, n_dropped = NA, row.names = NULL))
res <- rbind(ra, rb, rc)
write.csv(res, file.path(OUT, "robustness_results.csv"), row.names = FALSE)
print(res, digits = 6)
