# Reads outputs/models_appendix.rds and writes outputs/targets_extracted.csv (pre-registered Wald z, two-sided normal p)
args <- commandArgs(TRUE); OUT <- args[1]
suppressMessages(library(MASS))
mods <- readRDS(file.path(OUT, "models_appendix.rds"))
dta <- readRDS("outputs/dta_prepared.rds")  # needed for drop1 refits (secondary LR p)
wald <- function(m, term) {
  ct <- coef(summary(m)); b <- ct[term, "Value"]; se <- ct[term, "Std. Error"]; z <- ct[term, "t value"]
  c(value = unname(b), se = unname(se), z = unname(z), p_wald = unname(2 * pnorm(-abs(z))))
}
rows <- list(
  data.frame(id = "T1", model = "m1", term = "anti_strike", t(wald(mods$m1, "anti_strike"))),
  data.frame(id = "T2", model = "m7", term = "pro_strike", t(wald(mods$m7, "pro_strike"))),
  data.frame(id = "T3", model = "m1", term = "pro_strike", t(wald(mods$m1, "pro_strike"))),
  data.frame(id = "T4", model = "m4", term = "anti_strike", t(wald(mods$m4, "anti_strike"))),
  data.frame(id = "T5", model = "m1", term = "nobs", value = nobs(mods$m1), se = NA, z = NA, p_wald = NA),
  data.frame(id = "T6", model = "m7", term = "nobs", value = nobs(mods$m7), se = NA, z = NA, p_wald = NA))
res <- do.call(rbind, rows)
res$n_slot <- c(NA, NA, NA, NA, mods$m1$n, mods$m7$n)
# Secondary (not pre-registered as class-setting): likelihood-ratio p via drop1 on the coefficient
lrp <- function(m, term) { d <- drop1(m, scope = as.formula(paste("~", term)), test = "Chisq"); d[term, "Pr(>Chi)"] }
res$p_lr_secondary <- c(lrp(mods$m1, "anti_strike"), lrp(mods$m7, "pro_strike"), lrp(mods$m1, "pro_strike"), lrp(mods$m4, "anti_strike"), NA, NA)
write.csv(res, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
print(res, digits = 8)
