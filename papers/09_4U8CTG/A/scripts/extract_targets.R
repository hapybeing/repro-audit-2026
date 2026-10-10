# Agent A, 09_4U8CTG. Sources the modified copy of 02 (missing-input skips only), then writes
# full-precision estimates for the target models. Run from the deposit root (RUNDIR/run).
# 02 starts with rm(list = ls()), so the start time is kept in an env var.
Sys.setenv(EXTRACT_T0 = format(as.numeric(Sys.time()), digits = 15))
# print.eval = TRUE: top-level values are printed as when 02 is run with Rscript or line by line;
# without it the texreg() calls inside sink() write empty .tex files (seen in run 1).
source("replication_scripts/02_supplementary_materials.R", echo = FALSE, print.eval = TRUE)
OUT <- Sys.getenv("OUTDIR")
save.image(file.path(OUT, "session_02.RData"))
rows <- list()
for (nm in c("model_1_ez", "model_2_ez", "model_3_ez", "model_4_ez",
             "model_1_ez_lrem", "model_2_ez_lrem", "model_3_ez_lrem", "model_4_ez_lrem")) {
  m <- get(nm)
  if (inherits(m, "lm_robust")) {
    tb <- data.frame(term = m$term, estimate = m$coefficients, se = m$std.error,
                     t = m$statistic, p = m$p.value, se_type = m$se_type)
    n <- m$nobs
  } else {
    s <- summary(m)$coefficients
    tb <- data.frame(term = rownames(s), estimate = s[, 1], se = s[, 2], t = s[, 3], p = s[, 4],
                     se_type = "classical")
    n <- nobs(m)
  }
  tb$model <- nm; tb$nobs <- n
  rows[[nm]] <- tb
}
res <- do.call(rbind, rows)
write.csv(res, file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
cat("elapsed_sec", as.numeric(Sys.time()) - as.numeric(Sys.getenv("EXTRACT_T0")), "\n")
