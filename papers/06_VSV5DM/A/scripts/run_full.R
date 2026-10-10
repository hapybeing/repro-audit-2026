# Run the full purled authors' code expression by expression; errors are logged verbatim and the run continues.
# Usage: Rscript run_full.R <purled.R>  (wd = RUNDIR)
args <- commandArgs(TRUE); f <- args[1]
exprs <- parse(f, keep.source = TRUE)
srcs <- attr(exprs, "srcref")
nerr <- 0
for (i in seq_along(exprs)) {
  ln <- srcs[[i]][1]
  cat(sprintf("\n#### [expr %d, purled line %d] %s\n", i, ln, substr(paste(as.character(srcs[[i]]), collapse=" "), 1, 200)))
  r <- tryCatch(withVisible(eval(exprs[[i]], envir = globalenv())),
                error = function(e) { nerr <<- nerr + 1; cat("ERROR at purled line", ln, ":", conditionMessage(e), "\n"); NULL })
  if (!is.null(r) && r$visible) print(r$value)
}
cat("\nTOTAL ERRORS:", nerr, "\n")
