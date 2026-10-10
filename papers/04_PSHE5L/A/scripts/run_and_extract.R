# Usage: Rscript run_and_extract.R <patched_script.R> <outdir> <prefix>
# Sources the (environment-patched) authors' script top to bottom in this session,
# then writes the structural model results to CSV. Run with R_LIBS_USER set to the fresh library.
args <- commandArgs(trailingOnly = TRUE)
script <- args[1]; outdir <- args[2]; prefix <- args[3]
.libPaths(c("/workspace/audit_runs/04_PSHE5L/A/rlib", .libPaths()))
cat("lavaan", as.character(packageVersion("lavaan")), "from", find.package("lavaan"), "\n")
cat("semTools", as.character(packageVersion("semTools")), "from", find.package("semTools"), "\n")
source(script, echo = TRUE, max.deparse.length = Inf, spaced = FALSE)
library(lavaan)
ss <- standardizedSolution(structural)
write.csv(ss, file.path(outdir, paste0(prefix, "_stdsol.csv")), row.names = FALSE)
pe <- parameterEstimates(structural, standardized = TRUE)
write.csv(pe, file.path(outdir, paste0(prefix, "_pe.csv")), row.names = FALSE)
fm <- fitMeasures(structural, c("chisq", "df", "chisq.scaled", "df.scaled", "cfi.robust", "tli.robust", "srmr", "rmsea.robust"))
fit <- data.frame(measure = c(names(fm), "nobs", "ntotal_rows_in_data", "converged"),
                  value = c(as.numeric(fm), lavInspect(structural, "nobs"), nrow(rural), as.numeric(lavInspect(structural, "converged"))))
write.csv(fit, file.path(outdir, paste0(prefix, "_fit.csv")), row.names = FALSE)
if (exists("structural_ctrl")) {
  fc <- fitMeasures(structural_ctrl, c("chisq", "df", "chisq.scaled", "df.scaled", "cfi.robust", "tli.robust", "srmr", "rmsea.robust"))
  write.csv(data.frame(measure = c(names(fc), "nobs"), value = c(as.numeric(fc), lavInspect(structural_ctrl, "nobs"))),
            file.path(outdir, paste0(prefix, "_ctrl_fit.csv")), row.names = FALSE)
  write.csv(standardizedSolution(structural_ctrl), file.path(outdir, paste0(prefix, "_ctrl_stdsol.csv")), row.names = FALSE)
}
writeLines(capture.output(sessionInfo()), file.path(outdir, paste0(prefix, "_sessionInfo.txt")))
cat("EXTRACTION_DONE\n")
