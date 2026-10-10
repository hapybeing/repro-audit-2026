# Agent B: run the env-fixed authors' notebook top to bottom as far as it goes; record where and why it stops.
args <- commandArgs(trailingOnly = TRUE)
rmd <- args[1]; out_json <- args[2]
rfile <- sub("\\.Rmd$", "_purled.R", rmd)
knitr::purl(rmd, output = rfile, documentation = 0, quiet = TRUE)
exprs <- parse(rfile, keep.source = TRUE)
srcref_lines <- sapply(attr(exprs, "srcref"), function(s) s[1])
env <- new.env()
status <- list(stopped = FALSE, n_expressions = length(exprs), last_ok_expr = 0L)
for (i in seq_along(exprs)) {
  r <- tryCatch({suppressPackageStartupMessages(eval(exprs[[i]], envir = env)); NULL},
                error = function(e) e)
  if (!is.null(r)) {
    status$stopped <- TRUE
    status$failing_expr_index <- i
    status$failing_purled_line <- srcref_lines[i]
    status$failing_code <- paste(deparse(exprs[[i]]), collapse = " ")
    status$error_message <- conditionMessage(r)
    break
  }
  status$last_ok_expr <- i
}
status$objects_defined_before_stop <- sort(ls(env))
status$byonic_csv_exists_in_run_dir <- file.exists(file.path(dirname(rmd), "Byonic_results.csv"))
jsonlite::write_json(status, out_json, auto_unbox = TRUE, pretty = TRUE)
