# Reads outputs/models_appendix.rds, writes outputs/targets_extracted.csv (agent B)
library(MASS)
OUT <- Sys.getenv("OUTDIR")
m <- readRDS(file.path(OUT, "models_appendix.rds"))
row <- function(id, mod, term) {
  s <- summary(m[[mod]])$coefficients
  z <- s[term, "t value"]
  data.frame(id = id, model = mod, term = term, value = unname(s[term, "Value"]), se = unname(s[term, "Std. Error"]),
             z = unname(z), p_wald = 2 * pnorm(-abs(unname(z))), nobs = NA, n_slot = NA, convergence = m[[mod]]$convergence)
}
r <- rbind(row("T1", "m1", "anti_strike"), row("T2", "m7", "pro_strike"), row("T3", "m1", "pro_strike"), row("T4", "m4", "anti_strike"))
for (x in list(c("T5", "m1"), c("T6", "m7"))) {
  r <- rbind(r, data.frame(id = x[1], model = x[2], term = "nobs", value = nobs(m[[x[2]]]), se = NA, z = NA, p_wald = NA,
                           nobs = nobs(m[[x[2]]]), n_slot = m[[x[2]]]$n, convergence = m[[x[2]]]$convergence))
}
write.csv(r, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
# all coefficients of m1, m4, m7, m10 for context
all <- do.call(rbind, lapply(names(m), function(k) { s <- summary(m[[k]])$coefficients
  data.frame(model = k, term = rownames(s), value = s[, 1], se = s[, 2], z = s[, 3], p_wald = 2 * pnorm(-abs(s[, 3])), row.names = NULL) }))
write.csv(all, file.path(OUT, "all_coefs_m1_m4_m7_m10.csv"), row.names = FALSE)
print(r, digits = 7)
