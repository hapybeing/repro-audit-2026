# Agent B, 09_4U8CTG. Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3), run exactly as written.
# Reads the zemmour data frame exactly as 02 builds it (saved by extract_targets.R).
args <- commandArgs(trailingOnly = TRUE)
outdir <- normalizePath(args[1], mustWork = TRUE)
load(file.path(outdir, "session_02_models.RData"))
term <- "treatmentwin_mainstream"
out <- list(); log <- character()
L <- function(...) { s <- paste0(...); log <<- c(log, s); cat(s, "\n") }
L("zemmour rows: ", nrow(zemmour), "; treatment levels: ", paste(levels(factor(zemmour$treatment)), collapse = ","))
L("reference level: ", levels(factor(zemmour$treatment))[1])

# ---- R_a stratified case bootstrap ----
set.seed(20261010)
B <- 2000
boot_fun <- function(dat, dv) {
  dat <- dat[!is.na(dat[[dv]]), ]
  idx_by_arm <- split(seq_len(nrow(dat)), dat$treatment, drop = TRUE)
  est <- numeric(B)
  for (b in seq_len(B)) {
    idx <- unlist(lapply(idx_by_arm, function(ix) ix[sample.int(length(ix), length(ix), replace = TRUE)]), use.names = FALSE)
    d <- dat[idx, ]
    est[b] <- coef(lm(as.formula(paste(dv, "~ treatment")), data = d))[term]
  }
  orig <- coef(lm(as.formula(paste(dv, "~ treatment")), data = dat))[term]
  ci <- unname(quantile(est, c(0.025, 0.975)))
  p <- min(1, 2 * min(mean(est >= 0), mean(est <= 0)))
  list(dv = dv, n = nrow(dat), estimate = unname(orig), boot_se = sd(est), ci_low = ci[1], ci_high = ci[2],
       p_value = p, n_na_boot = sum(is.na(est)))
}
ra1 <- boot_fun(zemmour, "swd_ch")
ra2 <- boot_fun(zemmour, "affect_LREM_ch")   # continues same RNG stream
# ---- R_b outlier exclusion |z| > 3 ----
rb_fun <- function(dat, dv) {
  dat <- dat[!is.na(dat[[dv]]), ]
  z <- (dat[[dv]] - mean(dat[[dv]])) / sd(dat[[dv]])
  drop <- abs(z) > 3
  d2 <- dat[!drop, ]
  m <- lm(as.formula(paste(dv, "~ treatment")), data = d2)
  s <- summary(m)$coefficients
  list(dv = dv, n_before = nrow(dat), n_dropped = sum(drop), n_after = nrow(d2),
       dropped_arms = paste(as.character(dat$treatment[drop]), collapse = ";"),
       dropped_values = paste(dat[[dv]][drop], collapse = ";"),
       estimate = s[term, 1], se = s[term, 2], p_value = s[term, 4])
}
rb1 <- rb_fun(zemmour, "swd_ch"); rb2 <- rb_fun(zemmour, "affect_LREM_ch")
# ---- R_c ANCOVA ----
diag_n <- sum(zemmour$swd_ch != (zemmour$swd_w2 - zemmour$swd_w1), na.rm = TRUE)
diag_na <- sum(is.na(zemmour$swd_ch != (zemmour$swd_w2 - zemmour$swd_w1)))
diag_n2 <- sum(zemmour$affect_LREM_ch != (zemmour$affect_LREM_w2 - zemmour$affect_LREM_w1), na.rm = TRUE)
L("R_c diagnostic: rows with swd_ch != swd_w2 - swd_w1: ", diag_n, " (comparisons NA: ", diag_na, ")")
L("R_c diagnostic (secondary): rows with affect_LREM_ch != affect_LREM_w2 - affect_LREM_w1: ", diag_n2)
rc_fun <- function(f) {
  m <- lm(f, data = zemmour); s <- summary(m)$coefficients
  list(formula = deparse(f), n = nobs(m), estimate = s[term, 1], se = s[term, 2], p_value = s[term, 4])
}
rc1 <- rc_fun(swd_w2 ~ treatment + swd_w1); rc2 <- rc_fun(affect_LREM_w2 ~ treatment + affect_LREM_w1)
tab <- rbind(
  data.frame(check = "R_a", outcome = "swd_ch", estimate = ra1$estimate, se = ra1$boot_se, ci_low = ra1$ci_low, ci_high = ra1$ci_high, p_value = ra1$p_value, n = ra1$n, note = paste0("B=2000 stratified; NA boot estimates=", ra1$n_na_boot)),
  data.frame(check = "R_a", outcome = "affect_LREM_ch", estimate = ra2$estimate, se = ra2$boot_se, ci_low = ra2$ci_low, ci_high = ra2$ci_high, p_value = ra2$p_value, n = ra2$n, note = paste0("B=2000 stratified; NA boot estimates=", ra2$n_na_boot)),
  data.frame(check = "R_b", outcome = "swd_ch", estimate = rb1$estimate, se = rb1$se, ci_low = NA, ci_high = NA, p_value = rb1$p_value, n = rb1$n_after, note = paste0("dropped ", rb1$n_dropped, " arms=", rb1$dropped_arms, " values=", rb1$dropped_values)),
  data.frame(check = "R_b", outcome = "affect_LREM_ch", estimate = rb2$estimate, se = rb2$se, ci_low = NA, ci_high = NA, p_value = rb2$p_value, n = rb2$n_after, note = paste0("dropped ", rb2$n_dropped, " arms=", rb2$dropped_arms, " values=", rb2$dropped_values)),
  data.frame(check = "R_c", outcome = "swd_w2", estimate = rc1$estimate, se = rc1$se, ci_low = NA, ci_high = NA, p_value = rc1$p_value, n = rc1$n, note = paste0(rc1$formula, "; diag rows swd_ch != w2-w1: ", diag_n)),
  data.frame(check = "R_c", outcome = "affect_LREM_w2", estimate = rc2$estimate, se = rc2$se, ci_low = NA, ci_high = NA, p_value = rc2$p_value, n = rc2$n, note = paste0(rc2$formula, "; diag rows affect ch != w2-w1: ", diag_n2))
)
write.csv(tab, file.path(outdir, "robustness.csv"), row.names = FALSE)
print(tab, digits = 8)
writeLines(log, file.path(outdir, "robustness_log.txt"))
