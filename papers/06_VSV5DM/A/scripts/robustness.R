# Pre-registered robustness checks R_a, R_b, R_c (PREREG section 3). Usage: Rscript robustness.R <rundir> <outdir>
args <- commandArgs(TRUE); rundir <- args[1]; outdir <- args[2]
suppressMessages({library(margins); library(MASS)})
obj <- readRDS(file.path(rundir, "covid_model.rds"))
covid <- obj$covid
d <- obj$mf  # model.frame(covid), n = 635
stopifnot(nrow(d) == 635)
fml <- formula(covid)
levs <- levels(d$rpg)
dem3 <- c("Democratic Women of Color", "Democratic Men of Color", "Democratic White Women")
ame_direct <- function(fit, dat) {
  base <- dat; base$rpg <- factor(rep("Republican White Men", nrow(dat)), levels = levs)
  p0 <- predict(fit, newdata = base, type = "response")
  sapply(setdiff(levs, "Republican White Men"), function(l) {
    nd <- dat; nd$rpg <- factor(rep(l, nrow(dat)), levels = levs)
    mean(predict(fit, newdata = nd, type = "response") - p0)
  })
}
marg_tab <- function(fit, dat, label) {
  s <- as.data.frame(summary(margins(fit, variables = "rpg", data = dat)))
  s$group <- sub("^rpg", "", s$factor); s$check <- label
  s[, c("check", "group", "AME", "SE", "z", "p", "lower", "upper")]
}
# Check direct formula equals margins AME on original data
fit0 <- glm(fml, family = quasipoisson, data = d)
m0 <- marg_tab(fit0, d, "original")
dir0 <- ame_direct(fit0, d)
chk <- data.frame(group = names(dir0), direct = unname(dir0), margins = m0$AME[match(names(dir0), m0$group)])
chk$abs_diff <- abs(chk$direct - chk$margins); chk$within_1e6 <- chk$abs_diff < 1e-6
write.csv(chk, file.path(outdir, "R_a_direct_formula_check.csv"), row.names = FALSE); print(chk)

# R_a bootstrap
set.seed(20261010)
B <- 1000; n <- nrow(d); boot <- matrix(NA_real_, B, 3, dimnames = list(NULL, dem3)); dropped <- 0
for (b in 1:B) {
  idx <- sample(n, n, replace = TRUE); db <- d[idx, ]
  if (any(table(factor(db$rpg, levels = levs)) == 0) || any(table(factor(db$State, levels = levels(d$State))) == 0)) { dropped <- dropped + 1; next }
  fb <- tryCatch(glm(fml, family = quasipoisson, data = db), error = function(e) NULL)
  if (is.null(fb) || any(is.na(coef(fb)))) { dropped <- dropped + 1; next }
  db$rpg <- factor(db$rpg, levels = levs)
  boot[b, ] <- ame_direct(fb, db)[dem3]
}
ok <- complete.cases(boot); bt <- boot[ok, , drop = FALSE]
ra <- do.call(rbind, lapply(dem3, function(g) {
  x <- bt[, g]
  data.frame(check = "R_a", group = g, AME = unname(dir0[g]), boot_se = sd(x),
             lower = unname(quantile(x, .025)), upper = unname(quantile(x, .975)),
             p = min(1, 2 * min(mean(x <= 0), mean(x >= 0))), B_requested = B, B_used = sum(ok), dropped = dropped)
}))
write.csv(ra, file.path(outdir, "R_a_bootstrap.csv"), row.names = FALSE); print(ra)
write.csv(bt, file.path(outdir, "R_a_bootstrap_draws.csv"), row.names = FALSE)

# R_b outlier exclusion |z| > 3 on outcome
z <- (d$covid - mean(d$covid)) / sd(d$covid)
drop <- abs(z) > 3
db <- d[!drop, ]
fb <- glm(fml, family = quasipoisson, data = db)
rb <- marg_tab(fb, db, "R_b"); rb$n_used <- nrow(db); rb$n_dropped <- sum(drop)
rb$dropped_groups <- paste(names(table(as.character(d$rpg[drop]))), table(as.character(d$rpg[drop])), sep = ":", collapse = "; ")
write.csv(rb, file.path(outdir, "R_b_outlier_exclusion.csv"), row.names = FALSE); print(rb)

# R_c negative binomial
warns <- character(0)
fc <- withCallingHandlers(tryCatch(glm.nb(fml, data = d), error = function(e) {warns <<- c(warns, paste("ERROR:", conditionMessage(e))); NULL}),
                          warning = function(w) {warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning")})
if (!is.null(fc)) {
  rc <- marg_tab(fc, d, "R_c"); rc$theta <- fc$theta; rc$converged <- fc$converged
  rc$warnings <- if (length(warns)) paste(unique(warns), collapse = " | ") else ""
} else rc <- data.frame(check = "R_c", group = NA, AME = NA, SE = NA, z = NA, p = NA, lower = NA, upper = NA, theta = NA, converged = FALSE, warnings = paste(warns, collapse = " | "))
write.csv(rc, file.path(outdir, "R_c_negbin.csv"), row.names = FALSE); print(rc)
