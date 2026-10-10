# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3)
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/A/outputs"
m <- readRDS(file.path(OUT, "S1_S10_models.rds"))
spec <- list(res4 = list(term = "TreatmentQuota", target = "T1"), res1 = list(term = "TreatmentQuota", target = "T2"),
             resg1 = list(term = "resp_genderMale", target = "T3"), resg2 = list(term = "resp_genderMale", target = "T4"))
# estimation samples (rows used by the fit)
getdata <- function(nm) { f <- m[[nm]]; mf <- model.frame(f); names(mf)[names(mf) == "(weights)"] <- "Weight"; mf }
# R_a bootstrap
set.seed(20261010)
ra <- list()
for (nm in names(spec)) {
  d <- getdata(nm); fo <- formula(m[[nm]]); term <- spec[[nm]]$term; n <- nrow(d)
  b <- numeric(2000)
  for (i in 1:2000) { idx <- sample(n, n, replace = TRUE); b[i] <- coef(lm(fo, data = d[idx, ], weights = Weight))[term] }
  nna <- sum(is.na(b)); bb <- b[!is.na(b)]
  q <- quantile(bb, c(.005, .025, .05, .95, .975, .995), names = FALSE)
  ra[[nm]] <- data.frame(check = "R_a", model = nm, target = spec[[nm]]$target, term = term, n = n,
    estimate = unname(coef(m[[nm]])[term]), boot_se = sd(bb), ci90_lo = q[3], ci90_hi = q[4], ci95_lo = q[2], ci95_hi = q[5],
    ci99_lo = q[1], ci99_hi = q[6], p_boot = min(1, 2 * min(mean(bb <= 0), mean(bb >= 0))), n_na = nna)
  write.csv(data.frame(draw = 1:2000, coef = b), file.path(OUT, paste0("R_a_draws_", nm, ".csv")), row.names = FALSE)
}
ra <- do.call(rbind, ra); write.csv(ra, file.path(OUT, "R_a_bootstrap.csv"), row.names = FALSE); print(ra)
# R_b weight outliers |z|>3 within country estimation sample
rb <- list()
for (nm in names(spec)) {
  d <- getdata(nm); term <- spec[[nm]]$term
  z <- (d$Weight - mean(d$Weight)) / sd(d$Weight); keep <- abs(z) <= 3
  zs <- (d$Support - mean(d$Support)) / sd(d$Support)
  f <- lm(formula(m[[nm]]), data = d[keep, ], weights = Weight); cf <- summary(f)$coefficients
  rb[[nm]] <- data.frame(check = "R_b", model = nm, target = spec[[nm]]$target, term = term, n_before = nrow(d),
    n_dropped = sum(!keep), n_after = nobs(f), estimate = cf[term, 1], se = cf[term, 2], p = cf[term, 4],
    support_absz_gt3_dropped = sum(abs(zs) > 3), support_z_min = min(zs), support_z_max = max(zs))
}
rb <- do.call(rbind, rb); write.csv(rb, file.path(OUT, "R_b_weight_outliers.csv"), row.names = FALSE); print(rb)
# R_c unweighted
rc <- list()
for (nm in names(spec)) {
  d <- getdata(nm); term <- spec[[nm]]$term
  f <- lm(formula(m[[nm]]), data = d); cf <- summary(f)$coefficients
  rc[[nm]] <- data.frame(check = "R_c", model = nm, target = spec[[nm]]$target, term = term, n = nobs(f),
    estimate = cf[term, 1], se = cf[term, 2], p = cf[term, 4])
}
rc <- do.call(rbind, rc); write.csv(rc, file.path(OUT, "R_c_unweighted.csv"), row.names = FALSE); print(rc)
