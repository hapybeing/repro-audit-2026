# Agent B, 09_4U8CTG. Sources the audit copy of 02 (missing-input skip only) and extracts target quantities.
# Usage: cd RUNDIR (unpacked deposit with _replication.Rproj); Rscript extract_targets.R OUTDIR
args <- commandArgs(trailingOnly = TRUE)
outdir <- normalizePath(args[1], mustWork = TRUE)
assign(".audit_outdir", outdir, envir = globalenv())
.t0 <- Sys.time()
source("replication_scripts/02_supplementary_materials.R", echo = FALSE, print.eval = TRUE)  # print.eval so texreg() output inside sink() is written, as at top level in Rscript or the console
outdir <- get(".audit_outdir", envir = globalenv())   # 02 runs rm(list = ls()); dot-names survive ls()
cat("02 finished in", format(Sys.time() - .t0), "\n")
rows <- list()
for (nm in c("model_1_ez", "model_2_ez", "model_1_ez_lrem", "model_2_ez_lrem")) {
  m <- get(nm)
  if (inherits(m, "lm_robust")) {
    s <- summary(m)$coefficients
    df <- data.frame(model = nm, term = rownames(s), estimate = s[, "Estimate"], se = s[, "Std. Error"],
                     t = s[, "t value"], p = s[, "Pr(>|t|)"], nobs = m$nobs, se_type = m$se_type)
  } else {
    s <- summary(m)$coefficients
    df <- data.frame(model = nm, term = rownames(s), estimate = s[, 1], se = s[, 2],
                     t = s[, 3], p = s[, 4], nobs = nobs(m), se_type = "classical")
  }
  rows[[nm]] <- df
}
res <- do.call(rbind, rows); rownames(res) <- NULL
write.csv(res, file.path(outdir, "targets_extracted.csv"), row.names = FALSE)
save(zemmour, model_1_ez, model_1_ez_lrem, file = file.path(outdir, "session_02_models.RData"))
print(res, digits = 10)
writeLines(capture.output(sessionInfo()), file.path(outdir, "sessionInfo_02.txt"))
