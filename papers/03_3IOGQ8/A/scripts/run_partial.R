# Partial execution of the authors' notebook (Agent A, paper 03_3IOGQ8).
# Runs chunk 1 (constants, libraries, functions) and chunk 2 (read Byonic export), the
# only chunks that can be reached before the first missing input. Each top-level
# expression is evaluated separately so that every error is recorded verbatim, then
# execution continues. Nothing in the authors' analysis code is changed (only the
# working-directory env fix in diffs/01_working_directory.diff).
# Usage: Rscript run_partial.R <path to env-fixed Rmd> <output log path>
args <- commandArgs(trailingOnly = TRUE)
rmd <- args[1]; out <- args[2]
lines <- readLines(rmd)
starts <- grep("^```\\{r\\}", lines); ends <- grep("^```\\s*$", lines)
ends <- sapply(starts, function(s) min(ends[ends > s]))
log <- c(sprintf("Partial run of %s at %s", rmd, format(Sys.time(), tz = "Asia/Kolkata", usetz = TRUE)),
         sprintf("Chunks in file: %d", length(starts)))
env <- globalenv()
for (k in 1:2) {
  code_lines <- lines[(starts[k] + 1):(ends[k] - 1)]
  first_line <- starts[k] + 1
  exprs <- parse(text = code_lines, keep.source = TRUE)
  srcref <- attr(exprs, "srcref")
  log <- c(log, sprintf("== Chunk %d (Rmd lines %d-%d): %d top-level expressions", k, first_line, ends[k] - 1, length(exprs)))
  n_err <- 0
  for (i in seq_along(exprs)) {
    ln <- first_line + srcref[[i]][1] - 1
    txt <- paste(trimws(as.character(srcref[[i]])[1]), collapse = " ")
    res <- tryCatch({ suppressMessages(suppressWarnings(eval(exprs[[i]], envir = env))); "OK" },
                    error = function(e) paste0("ERROR: ", conditionMessage(e)))
    if (res != "OK") {
      n_err <- n_err + 1
      log <- c(log, sprintf("Rmd line %d: %s", ln, substr(txt, 1, 120)), sprintf("   -> %s", res))
    }
  }
  log <- c(log, sprintf("Chunk %d: %d expression(s) raised errors", k, n_err))
}
log <- c(log, sprintf("exists('Byonic_df') after chunk 2: %s", exists("Byonic_df")),
         sprintf("file.exists('Byonic_results.csv') in %s: %s", getwd(), file.exists("Byonic_results.csv")),
         sprintf("Chunks 3-%d not run: every one depends on Byonic_df / experiment*_list built in chunk 2 (and chunk 3 on mzML files at placeholder paths).", length(starts)))
writeLines(log, out)
cat(log, sep = "\n")
