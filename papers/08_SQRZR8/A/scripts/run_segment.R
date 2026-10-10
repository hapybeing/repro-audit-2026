# Segmented execution of the authors' unchanged main_rep.R (PREREG section 2 allowance): runs lines FROM..TO of
# main_rep.R in original order, after loading the saved image of the previous segment, then saves an image.
# Not an edit: the lines are read from the deposited file and sourced verbatim.
.libPaths(c("/workspace/audit_runs/08_SQRZR8/A/rlib", .libPaths()))
a <- commandArgs(TRUE); from <- as.integer(a[1]); to <- as.integer(a[2]); inimg <- a[3]; outimg <- a[4]
if (inimg != "none") {
  load(inimg, envir = globalenv())
  # packages attached by main_rep.R lines 14-19 must be re-attached in a new R process
  for (p in c("tidyverse","ltm","coefplot","ggpubr","estimatr","sjPlot")) suppressPackageStartupMessages(library(p, character.only = TRUE))
  rm(list = intersect(c("a","from","to","inimg","outimg"), ls()))  # drop driver variables saved in the image
} else set.seed(20261009)  # main_rep.R sets no seed; affects only the mediation bootstrap
a <- commandArgs(TRUE); from <- as.integer(a[1]); to <- as.integer(a[2]); inimg <- a[3]; outimg <- a[4]  # re-read after load()
L <- readLines("main_rep.R")[from:to]
tf <- tempfile(fileext = ".R"); writeLines(L, tf)
options(audit_t0 = Sys.time(), audit_outimg = outimg, audit_seg = c(from, to))  # main_rep.R line 8 clears globals; options survive
source(tf, echo = TRUE, max.deparse.length = Inf)
cat("\nSEGMENT", getOption("audit_seg"), "ELAPSED_MIN", as.numeric(difftime(Sys.time(), getOption("audit_t0"), units = "mins")), "\n")
save.image(getOption("audit_outimg"))
cat("SEGMENT_DONE\n")
