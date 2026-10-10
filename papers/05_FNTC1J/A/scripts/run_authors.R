# Runs the env-fixed authors' script top to bottom in ONE R session.
# The file is split (at an expression boundary) into part 1 = everything up to and including the misinfo table export
# (original line 2344, which ends all code that produces T1-T5) and part 2 = the rest. Both parts are sourced in the
# same session, one after the other; a checkpoint with the model objects is saved between them so that a sandbox
# recycle during the slow later bootstraps does not lose the target objects. This does not change what is executed.
# Usage: Rscript run_authors.R <script_file> <out_rdata>
args <- commandArgs(trailingOnly = TRUE)
scr <- args[1]; out <- args[2]
cat("R_LIBS_USER =", Sys.getenv("R_LIBS_USER"), "\n.libPaths() =", .libPaths(), "\n")
cat("RNGkind:", RNGkind(), "\n")
L <- readLines(scr, encoding = "UTF-8")
cut <- grep('save_as_docx(ft, path = "_tables/2_glm_misinfo_final.docx")', L, fixed = TRUE)
stopifnot(length(cut) == 1)
cat("Split after line", cut, "of", length(L), "\n")
p1 <- file.path(dirname(out), "part1.R"); p2 <- file.path(dirname(out), "part2.R")
writeLines(L[1:cut], p1, useBytes = TRUE); writeLines(L[(cut + 1):length(L)], p2, useBytes = TRUE)
keep <- c("model", "model_CTB", "model_misinfo", "ds_analysis_paper2_CTBs_Ant", "ds_MisInfoCT_analysis", "mice_mice", "a")
source(p1, echo = TRUE, max.deparse.length = Inf, keep.source = TRUE, encoding = "UTF-8")
cat("\n=== AUDIT: part 1 finished (all T1-T5 code done); saving checkpoint ===\n")
save(list = intersect(keep, ls()), file = sub("\\.RData$", "_checkpoint_part1.RData", out))
writeLines(capture.output(sessionInfo()), sub("\\.RData$", "_sessionInfo_part1.txt", out))
source(p2, echo = TRUE, max.deparse.length = Inf, keep.source = TRUE, encoding = "UTF-8")
cat("\n=== AUDIT: script finished without error ===\n")
save(list = intersect(keep, ls()), file = out)
writeLines(capture.output(sessionInfo()), sub("\\.RData$", "_sessionInfo.txt", out))
