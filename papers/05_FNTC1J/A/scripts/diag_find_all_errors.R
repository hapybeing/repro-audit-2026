# DIAGNOSTIC ONLY (not the reproduction run): evaluate every top-level expression of the given script in order,
# continuing after errors, to list every expression that fails in a top-to-bottom run. Output: CSV of failures.
args <- commandArgs(trailingOnly = TRUE)
ex <- parse(args[1], keep.source = TRUE, encoding = "UTF-8")
sr <- attr(ex, "srcref")
fails <- data.frame(line = integer(), code = character(), error = character())
for (i in seq_along(ex)) {
  r <- tryCatch({ withVisible(eval(ex[[i]], envir = globalenv())); NULL },
                error = function(e) conditionMessage(e))
  if (!is.null(r)) {
    fails[nrow(fails) + 1, ] <- list(sr[[i]][1], substr(paste(as.character(sr[[i]]), collapse = " "), 1, 200), r)
    cat("FAIL at line", sr[[i]][1], ":", r, "\n")
  }
}
write.csv(fails, args[2], row.names = FALSE)
