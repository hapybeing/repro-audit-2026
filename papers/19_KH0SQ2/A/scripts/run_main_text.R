# Step B: run main_text_figs_JEPP_FINAL.R whole, unchanged, top-level expression by expression (as Rscript does:
# print visible values, stop at the first error), and record coef(res1) after l. 325 and coef(res1b) after l. 363
# for the T2/T1 cross-check (res1 is overwritten at l. 639, so it is captured right after its l. 325 assignment).
.OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/A/outputs"
setwd("/workspace/audit_runs/19_KH0SQ2/A/deposit")
pdf(file.path(.OUT, "Rplots.pdf"))
.ex <- parse("main_text_figs_JEPP_FINAL.R", keep.source = TRUE)
.sr <- attr(.ex, "srcref")
.cap <- new.env()
.cap$rows <- list(); .cap$status <- "completed"
for (.i in seq_along(.ex)) {
  .l <- .sr[[.i]][1]
  .r <- tryCatch({ .v <- withVisible(eval(.ex[[.i]], globalenv())); if (.v$visible) print(.v$value); NULL },
                 error = function(e) e)
  if (inherits(.r, "error")) { .cap$status <- paste0("error at line ", .l, ": ", conditionMessage(.r)); cat("ERROR at line", .l, ":", conditionMessage(.r), "\n"); break }
  if (.l == 325) { cf <- summary(get("res1"))$coefficients; .cap$rows[["res1"]] <- data.frame(object = "res1_l325_UK", term = rownames(cf), estimate = cf[,1], se = cf[,2], p = cf[,4], nobs = nobs(get("res1"))) }
  if (.l == 363) { cf <- summary(get("res1b"))$coefficients; .cap$rows[["res1b"]] <- data.frame(object = "res1b_l363_FR", term = rownames(cf), estimate = cf[,1], se = cf[,2], p = cf[,4], nobs = nobs(get("res1b"))) }
}
dev.off()
write.csv(do.call(rbind, .cap$rows), file.path(.OUT, "crosscheck_main_text.csv"), row.names = FALSE)
writeLines(c(.cap$status, paste("expressions:", length(.ex), "last evaluated index:", .i)), file.path(.OUT, "main_text_status.txt"))
