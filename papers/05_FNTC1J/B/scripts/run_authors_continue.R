# Agent B driver v2: runs the authors' UNMODIFIED script top to bottom in ONE R session, expression by expression,
# like pasting the whole file into an interactive console: an error in one top-level expression is printed and
# logged, and execution continues with the next expression (instead of source() aborting).
# Environment fix: a no-op View() stub (utils::View fails in a non-interactive session).
# Because the shared sandbox can be recycled mid-run, the driver saves a checkpoint image (all objects incl. .Random.seed)
# after the first expression that ends at or beyond each line in CKPT_LINES. With a 4th argument "resume", it loads the
# latest checkpoint, re-attaches the packages that were attached, and continues with the next expression.
# Usage: Rscript run_authors_continue.R <script> <session_out.RData> <errors_out.csv> [resume]
args <- commandArgs(trailingOnly = TRUE)
.script <- args[1]; .out <- args[2]; .errf <- args[3]; .resume <- length(args) >= 4 && args[4] == "resume"
.ckf <- paste0(.out, ".checkpoint.RData")
View <- function(...) invisible(NULL)   # ENV FIX
.exprs <- parse(.script, keep.source = TRUE)
.srcr  <- attr(.exprs, "srcref")
.CKPT_LINES <- c(1300, 2400, 3000, 3425, 3436, 3600, 3675, 3685)
.start <- 1
.errs  <- data.frame(expr_index = integer(), first_line = integer(), last_line = integer(), message = character())
.done_ck <- integer()
if (.resume && file.exists(.ckf)) {
  load(.ckf, envir = globalenv())
  for (.p in rev(.ck_pkgs)) suppressPackageStartupMessages(library(.p, character.only = TRUE))
  .start <- .ck_i + 1
  cat("### RESUMED from checkpoint after expression", .ck_i, "(line", .srcr[[.ck_i]][3], ")\n")
}
.t0 <- Sys.time()
for (.i in seq.int(.start, length(.exprs))) {
  .l1 <- .srcr[[.i]][1]; .l2 <- .srcr[[.i]][3]
  cat(sprintf("\n> [L%d-%d] %s\n", .l1, .l2, paste(as.character(.srcr[[.i]]), collapse = "\n+ ")))
  .res <- tryCatch(withVisible(eval(.exprs[[.i]], envir = globalenv())),
                   error = function(e) { cat("Error:", conditionMessage(e), "\n"); structure(list(msg = conditionMessage(e)), class = "B_err") })
  if (inherits(.res, "B_err")) {
    .errs <- rbind(.errs, data.frame(expr_index = .i, first_line = .l1, last_line = .l2, message = .res$msg))
  } else if (isTRUE(.res$visible)) {
    tryCatch(print(.res$value), error = function(e) cat("Error in print:", conditionMessage(e), "\n"))
  }
  .due <- .CKPT_LINES[.CKPT_LINES <= .l2 & !(.CKPT_LINES %in% .done_ck)]
  if (length(.due)) {
    .done_ck <- c(.done_ck, .due); .ck_i <- .i
    .ck_pkgs <- sub("^package:", "", grep("^package:", search(), value = TRUE))
    save.image(.ckf); cat("### CHECKPOINT saved after expression", .i, "line", .l2, "\n")
  }
}
cat("\n### SCRIPT FINISHED; expressions:", length(.exprs), "; errors this segment:", nrow(.errs), "; elapsed:", format(Sys.time() - .t0), "\n")
cat("### RNGkind:", RNGkind(), "\n")
write.csv(.errs, .errf, row.names = FALSE)
save.image(.out)
