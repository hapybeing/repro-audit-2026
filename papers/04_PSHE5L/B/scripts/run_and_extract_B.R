# Agent B runner: source the (environment-patched) authors' script top to bottom,
# capture console output, then write the pre-registered extraction files.
# Usage: Rscript run_and_extract_B.R <patched_script.R> <outdir> <prefix>
args <- commandArgs(trailingOnly = TRUE)
script <- args[1]; outdir <- args[2]; prefix <- args[3]
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
con <- file(file.path(outdir, paste0(prefix, "_full_script_output.txt")), open = "wt")
sink(con, split = FALSE); sink(con, type = "message")
env <- new.env()
res <- tryCatch({
  source(script, local = env, echo = TRUE, max.deparse.length = Inf, print.eval = TRUE)
  "completed"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("\n#### SOURCE RESULT:", res, "\n")
sink(type = "message"); sink()
close(con)
cat("source result:", res, "\n")

library(lavaan)
wfit <- function(fit, name) {
  fm <- fitMeasures(fit, c("chisq", "df", "pvalue", "chisq.scaled", "df.scaled", "cfi.robust", "tli.robust",
                           "srmr", "rmsea.robust"))
  out <- data.frame(measure = c("nobs", "ntotal", names(fm)),
                    value = c(lavInspect(fit, "nobs"), lavInspect(fit, "ntotal"), as.numeric(fm)))
  write.csv(out, file.path(outdir, paste0(prefix, "_", name, "_fit.csv")), row.names = FALSE)
}
if (exists("structural", envir = env)) {
  s <- get("structural", envir = env)
  write.csv(standardizedSolution(s), file.path(outdir, paste0(prefix, "_structural_stdsol.csv")), row.names = FALSE)
  write.csv(parameterEstimates(s), file.path(outdir, paste0(prefix, "_structural_pe.csv")), row.names = FALSE)
  wfit(s, "structural")
}
if (exists("structural_ctrl", envir = env)) {
  sc <- get("structural_ctrl", envir = env)
  write.csv(standardizedSolution(sc), file.path(outdir, paste0(prefix, "_structural_ctrl_stdsol.csv")), row.names = FALSE)
  wfit(sc, "structural_ctrl")
}
if (exists("measurement", envir = env)) wfit(get("measurement", envir = env), "measurement")
writeLines(capture.output(sessionInfo()), file.path(outdir, paste0(prefix, "_sessionInfo.txt")))
