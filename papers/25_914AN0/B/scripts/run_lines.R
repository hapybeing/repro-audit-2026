# Helper: evaluate a verbatim line range of the authors' run2_main.R in the global env, echoing code.
run_lines <- function(from, to, file="code/run2_main.R") {
  L <- readLines(file, encoding="UTF-8")[from:to]
  cat(sprintf("#### run2_main.R lines %d-%d\n", from, to))
  exprs <- parse(text=L, keep.source=TRUE, encoding="UTF-8")
  for (e in exprs) { print(system.time(res <- withVisible(eval(e, envir=globalenv())))); if (res$visible) print(res$value) }
  invisible(NULL)
}
memlog <- function(tag) { m <- system("free -m", intern=TRUE); cat("MEM", tag, format(Sys.time()), "\n", m[1:2], sep="\n"); g <- gc(); print(g) }
