## Pre-registered robustness checks R_a, R_b, R_c for 13_DX5T9G (PREREG.md section 3).
## Usage: Rscript robustness.R <Prepped_survey_data.csv> <outdir> <which: a|b|c>
## Uses the agent's own prepared data (weights w from the authors' 01 script).
suppressMessages({library(nnet); library(MASS)})
## Note: weights are passed as `weights = w` (the column w of the data frame passed in, identical values to tmp$w) so that multinom finds them inside a function.
args <- commandArgs(trailingOnly = TRUE)
data <- read.csv(file = args[1]); outdir <- args[2]; which <- args[3]
form_raw <- "factor(Y) ~ 1 + I(T_health_cap == \"Great\") + log(T_cases) + 
  + Authoritarianism + I(Age/100) +
  + Gender_male + Edu_university + I(I(LR != -99) * LR) + I(LR == -99)"
this_form <- as.formula(paste0(form_raw, "+ I(T_who == \"WHO\") + I(T_who == \"WHO.Ratified\")"))
rows <- c(WHO = '2:I(T_who == "WHO")TRUE', WHO.Ratified = '2:I(T_who == "WHO.Ratified")TRUE')
tid <- function(cc, r) ifelse(cc == "UK", ifelse(r == "WHO", "T1", "T2"), ifelse(r == "WHO", "T3", "T4"))

## Authors' estimation and summary (lines 55-66 of 03), with df = nrow of the combined data passed in
authors_fit <- function(tmp, df_n, weighted = TRUE) {
  set.seed(1230)
  if (weighted) mod <- multinom(formula = this_form, data = tmp, weights = w, Hess = TRUE, maxit = 500, trace = FALSE)
  else mod <- multinom(formula = this_form, data = tmp, Hess = TRUE, maxit = 500, trace = FALSE)
  theta <- mvrnorm(n = 5000, mu = c(t(coef(mod))), vcov(mod))
  res <- c()
  for (r in names(rows)) {
    x <- theta[, rows[[r]]]
    vn <- sub("^2:", "", rows[[r]])
    res <- rbind(res, data.frame(target = NA, var = r, Mean = mean(x), SD = sd(x),
                                 pvalue = 2 * pt(q = -1 * abs(mean(x) / sd(x)), df = df_n),
                                 MLE = coef(mod)["2", vn], N = nrow(tmp), convergence = mod$convergence))
  }
  res
}

if (which == "a") {
  set.seed(20261010)
  out <- c(); draws <- c()
  for (cc in c("UK", "US")) {
    tmp <- subset(data, Country == cc); n <- nrow(tmp)
    mod0 <- multinom(formula = this_form, data = tmp, weights = w, Hess = FALSE, maxit = 500, trace = FALSE)
    est <- sapply(rows, function(r) coef(mod0)["2", sub("^2:", "", r)])
    B <- matrix(NA, 1000, 2, dimnames = list(NULL, names(rows))); conv <- rep(NA, 1000)
    for (b in 1:1000) {
      bt <- tmp[sample(n, n, replace = TRUE), ]
      m <- multinom(formula = this_form, data = bt, weights = w, Hess = FALSE, maxit = 500, trace = FALSE)
      conv[b] <- m$convergence
      cf <- coef(m)
      for (r in names(rows)) { vn <- sub("^2:", "", rows[[r]]); if (vn %in% colnames(cf)) B[b, r] <- cf["2", vn] }
    }
    draws <- rbind(draws, data.frame(country = cc, b = 1:1000, convergence = conv, B))
    ok <- conv == 0
    for (r in names(rows)) {
      bb <- B[ok, r]
      out <- rbind(out, data.frame(target = tid(cc, r), country = cc, var = r, estimate_mle = est[[r]],
                                   boot_se = sd(bb), q005 = quantile(bb, 0.005), q025 = quantile(bb, 0.025),
                                   q975 = quantile(bb, 0.975), q995 = quantile(bb, 0.995),
                                   p_boot = if (est[[r]] < 0) min(2 * mean(bb >= 0), 1) else min(2 * mean(bb <= 0), 1),
                                   n_boot_used = sum(ok), n_nonconverged = sum(!ok)))
    }
  }
  write.csv(draws, file.path(outdir, "R_a_bootstrap_draws.csv"), row.names = FALSE)
  write.csv(out, file.path(outdir, "R_a_bootstrap.csv"), row.names = FALSE)
  print(out)
}

if (which == "b") {
  keep <- rep(TRUE, nrow(data)); info <- c()
  for (cc in c("UK", "US")) {
    ix <- which(data$Country == cc); w <- data$w[ix]
    z <- (w - mean(w)) / sd(w)
    drop <- abs(z) > 3; rule <- "|z(w)|>3"
    if (sum(drop) == 0) { drop <- w > quantile(w, 0.99, type = 7); rule <- "top 1% of w (no |z|>3)" }
    keep[ix[drop]] <- FALSE
    lc <- log(data$T_cases[ix]); zc <- (lc - mean(lc)) / sd(lc)
    za <- (data$Age[ix] - mean(data$Age[ix])) / sd(data$Age[ix])
    info <- rbind(info, data.frame(country = cc, rule = rule, n_dropped = sum(drop), n_absz_w_gt3 = sum(abs(z) > 3),
                                   n_absz_logcases_gt3 = sum(abs(zc) > 3), n_absz_age_gt3 = sum(abs(za) > 3)))
  }
  d2 <- data[keep, ]
  out <- c()
  for (cc in c("UK", "US")) {
    r <- authors_fit(subset(d2, Country == cc), df_n = nrow(d2)); r$country <- cc
    r$target <- sapply(r$var, function(v) tid(cc, v)); out <- rbind(out, r)
  }
  write.csv(info, file.path(outdir, "R_b_exclusion_info.csv"), row.names = FALSE)
  write.csv(out, file.path(outdir, "R_b_extreme_weights.csv"), row.names = FALSE)
  print(info); print(out)
}

if (which == "c") {
  out <- c()
  for (cc in c("UK", "US")) {
    r <- authors_fit(subset(data, Country == cc), df_n = nrow(data), weighted = FALSE); r$country <- cc
    r$target <- sapply(r$var, function(v) tid(cc, v)); out <- rbind(out, r)
  }
  write.csv(out, file.path(outdir, "R_c_unweighted.csv"), row.names = FALSE)
  print(out)
}
