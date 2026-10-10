# Pre-registered robustness checks R_a, R_b, R_c for 06_VSV5DM (PREREG.md section 3).
# Uses the COVID quasi-Poisson model object saved by extract_targets.R (authors' code, Rmd line 485).
# Usage: Rscript robustness.R check   (direct-formula check, R_b, R_c)
#        Rscript robustness.R boot <start> <end>   (R_a resamples start..end, resumable; draws all made up front)
#        Rscript robustness.R bootsum
suppressPackageStartupMessages({library(margins); library(MASS)})
RUN <- "/workspace/audit_runs/06_VSV5DM/B/run"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/06_VSV5DM/B/outputs"
obj <- readRDS(file.path(RUN, "covid_model.rds"))
covid <- obj$covid; by_leg2 <- obj$by_leg2
fml <- formula(covid)
d0 <- by_leg2[rownames(model.frame(covid)), ]
stopifnot(nrow(d0) == 635)
levs <- levels(d0$rpg); base <- "Republican White Men"
dem3 <- c("Democratic White Women","Democratic Men of Color","Democratic Women of Color")
direct_ame <- function(fit, d, lv) {
  a <- d; a$rpg <- factor(lv, levels = levs)
  b <- d; b$rpg <- factor(base, levels = levs)
  mean(predict(fit, newdata = a, type = "response") - predict(fit, newdata = b, type = "response"))
}
marg_tab <- function(fit, d) {
  s <- as.data.frame(summary(margins(fit, variables = "rpg", data = d)))
  s$level <- sub("^rpg", "", s$factor); s
}
args <- commandArgs(TRUE)
if (args[1] == "check") {
  # Verify direct formula equals margins AME on original data
  m <- marg_tab(covid, d0)
  chk <- data.frame(level = m$level, margins_AME = m$AME,
                    direct_AME = sapply(m$level, function(l) direct_ame(covid, d0, l)))
  chk$abs_diff <- abs(chk$margins_AME - chk$direct_AME); chk$within_1e6 <- chk$abs_diff < 1e-6
  write.csv(chk, file.path(OUT, "R_a_direct_formula_check.csv"), row.names = FALSE); print(chk)
  # R_b outlier exclusion
  z <- (d0$covid - mean(d0$covid)) / sd(d0$covid)
  drop <- abs(z) > 3
  d1 <- d0[!drop, ]
  fb <- glm(fml, family = "quasipoisson", data = d1)
  mb <- marg_tab(fb, d1)
  mb$n_used <- nobs(fb); mb$n_dropped <- sum(drop)
  mb$dropped_groups <- paste(names(table(droplevels(d0$rpg[drop]))), table(droplevels(d0$rpg[drop])), sep = ":", collapse = "; ")
  mb$dropped_covid_values <- paste(sort(d0$covid[drop]), collapse = ";")
  mb$z_cut_value <- mean(d0$covid) + 3 * sd(d0$covid)
  write.csv(mb, file.path(OUT, "R_b_outlier_exclusion.csv"), row.names = FALSE); print(mb)
  # R_c negative binomial
  w <- character(0)
  fc <- withCallingHandlers(glm.nb(fml, data = d0), warning = function(x) {w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning")})
  mc <- marg_tab(fc, d0)
  mc$theta <- fc$theta; mc$theta_SE <- fc$SE.theta; mc$converged <- fc$converged
  mc$n_used <- nobs(fc); mc$warnings <- if (length(w)) paste(unique(w), collapse = " | ") else ""
  write.csv(mc, file.path(OUT, "R_c_negbin.csv"), row.names = FALSE); print(mc)
}
if (args[1] == "boot") {
  set.seed(20261010)
  n <- nrow(d0); B <- 1000
  idx <- lapply(1:B, function(i) sample(n, n, replace = TRUE))
  st <- as.integer(args[2]); en <- as.integer(args[3])
  res <- list()
  for (b in st:en) {
    d <- d0[idx[[b]], ]
    ok <- all(levs %in% as.character(d$rpg)) && all(unique(as.character(d0$State)) %in% as.character(d$State))
    r <- data.frame(b = b, dropped = !ok, reason = if (!ok) "level absent" else "", t(setNames(rep(NA_real_, 3), dem3)), check.names = FALSE)
    if (ok) {
      f <- glm(fml, family = quasipoisson, data = d)
      if (any(is.na(coef(f)))) { r$dropped <- TRUE; r$reason <- "NA coefficient" } else {
        for (l in dem3) r[[l]] <- direct_ame(f, d, l)
      }
    }
    res[[length(res) + 1]] <- r
  }
  out <- do.call(rbind, res)
  fn <- file.path(RUN, "boot_parts"); dir.create(fn, showWarnings = FALSE)
  write.csv(out, file.path(fn, sprintf("boot_%04d_%04d.csv", st, en)), row.names = FALSE)
  cat("done", st, en, "\n")
}
if (args[1] == "bootsum") {
  fs <- list.files(file.path(RUN, "boot_parts"), full.names = TRUE)
  bt <- do.call(rbind, lapply(fs, read.csv, check.names = FALSE))
  bt <- bt[order(bt$b), ]; stopifnot(nrow(bt) == 1000, !any(duplicated(bt$b)))
  write.csv(bt, file.path(OUT, "R_a_bootstrap_draws.csv"), row.names = FALSE)
  keep <- bt[!bt$dropped, ]
  s <- do.call(rbind, lapply(dem3, function(l) {
    v <- keep[[l]]
    data.frame(level = l, original_AME = direct_ame(covid, d0, l), boot_SE = sd(v),
               ci_lower = unname(quantile(v, 0.025)), ci_upper = unname(quantile(v, 0.975)),
               p_boot = min(1, 2 * min(mean(v <= 0), mean(v >= 0))),
               B = 1000, n_dropped = sum(bt$dropped), n_used = nrow(keep), seed = 20261010)
  }))
  write.csv(s, file.path(OUT, "R_a_bootstrap_summary.csv"), row.names = FALSE); print(s)
}
