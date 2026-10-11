# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3). Run in RUNDIR after run_appendix.R.
args <- commandArgs(TRUE); OUT <- args[1]
suppressMessages({library(MASS); library(sandwich); library(lmtest); library(jsonlite)})
dta <- readRDS("outputs/dta_prepared.rds")
f1 <- unions ~ strike + pro_strike + anti_strike + double
f7 <- factor(Support_teachers) ~ strike + pro_strike + anti_strike + double
d1 <- dta[!is.na(dta$unions) & !is.na(dta$Treatment), ]
d7 <- dta[!is.na(dta$Support_teachers) & !is.na(dta$Treatment), ]
m1 <- polr(f1, data = d1, Hess = TRUE); m7 <- polr(f7, data = d7, Hess = TRUE)
stopifnot(nrow(d1) == nobs(m1), nrow(d7) == nobs(m7))
res <- list(n_m1_rows = nrow(d1), n_m7_rows = nrow(d7))

## R_a bootstrap
K <- 1000; set.seed(20261011)
boot <- function(d, f, term, tag) {
  ck <- file.path(OUT, paste0("bootstrap_", tag, "_draws.csv"))
  n <- nrow(d); est <- rep(NA_real_, K); fail <- 0L
  for (k in 1:K) {
    idx <- sample(n, n, replace = TRUE)
    fit <- tryCatch(polr(f, data = d[idx, ], Hess = TRUE), error = function(e) NULL)
    if (is.null(fit) || fit$convergence != 0) fail <- fail + 1L else est[k] <- coef(fit)[term]
    if (k %% 100 == 0) write.csv(data.frame(rep = 1:k, estimate = est[1:k]), ck, row.names = FALSE)
  }
  e <- est[!is.na(est)]
  list(n_resamples = K, n_failed = fail, boot_se = sd(e),
       ci95 = unname(quantile(e, c(.025, .975))), ci99 = unname(quantile(e, c(.005, .995))),
       p_boot = min(2 * min(mean(e <= 0), mean(e >= 0)), 1))
}
t0 <- Sys.time()
ra1 <- boot(d1, f1, "anti_strike", "m1_anti_strike"); ra1$estimate <- unname(coef(m1)["anti_strike"])
ra7 <- boot(d7, f7, "pro_strike", "m7_pro_strike"); ra7$estimate <- unname(coef(m7)["pro_strike"])
ra1$same <- (sign(ra1$ci95[1]) == sign(ra1$estimate)) && (sign(ra1$ci95[2]) == sign(ra1$estimate)) && ra1$estimate < 0
ra7$same <- (sign(ra7$ci99[1]) == sign(ra7$estimate)) && (sign(ra7$ci99[2]) == sign(ra7$estimate)) && ra7$estimate > 0
res$R_a <- list(seed = 20261011, T1 = ra1, T2 = ra7, seconds = as.numeric(difftime(Sys.time(), t0, units = "secs")))

## R_b age outlier exclusion |z| > 3 over all rows
z <- (dta$d2 - mean(dta$d2, na.rm = TRUE)) / sd(dta$d2, na.rm = TRUE)
drop <- !is.na(z) & abs(z) > 3
dk <- dta[!drop, ]
wald <- function(m, term) { ct <- coef(summary(m)); z <- ct[term, "t value"]; list(estimate = ct[term, "Value"], se = ct[term, "Std. Error"], z = z, p = 2 * pnorm(-abs(z)), nobs = nobs(m)) }
rb1 <- polr(f1, data = dk, Hess = TRUE); rb7 <- polr(f7, data = dk, Hess = TRUE)
res$R_b <- list(rows_dropped_total = sum(drop), age_mean = mean(dta$d2, na.rm = TRUE), age_sd = sd(dta$d2, na.rm = TRUE),
                age_missing = sum(is.na(dta$d2)), max_abs_z = max(abs(z), na.rm = TRUE),
                T1 = wald(rb1, "anti_strike"), T2 = wald(rb7, "pro_strike"))
res$R_b$T1$same <- res$R_b$T1$estimate < 0 && res$R_b$T1$p < 0.05
res$R_b$T2$same <- res$R_b$T2$estimate > 0 && res$R_b$T2$p < 0.01

## R_c linear model with HC2
l1 <- lm(as.numeric(unions) ~ strike + pro_strike + anti_strike + double, data = d1)
l7 <- lm(Support_teachers ~ strike + pro_strike + anti_strike + double, data = d7)
hc <- function(l, term) { ct <- coeftest(l, vcov. = vcovHC(l, type = "HC2")); list(estimate = ct[term, 1], se_hc2 = ct[term, 2], t = ct[term, 3], p = ct[term, 4], nobs = nobs(l)) }
res$R_c <- list(T1 = hc(l1, "anti_strike"), T2 = hc(l7, "pro_strike"))
res$R_c$T1$same <- res$R_c$T1$estimate < 0 && res$R_c$T1$p < 0.05
res$R_c$T2$same <- res$R_c$T2$estimate > 0 && res$R_c$T2$p < 0.01

write_json(res, file.path(OUT, "robustness.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 8, pretty = TRUE), "\n")
