# Agent B wrapper: runs the authors' 01-04 unchanged in RUN/analysis, saves cj() results and pooled_df2.
# Usage: Rscript run_authors.R <RUN_analysis_dir> <OUT_dir>
args <- commandArgs(TRUE); setwd(args[1]); OUT <- args[2]
warns <- character(0)
wh <- function(w) { warns <<- c(warns, paste0("[", sc, "] ", conditionMessage(w))); invokeRestart("muffleWarning") }
for (sc in c("01_preparation_function.R","02_plot_function.R","03_data_prep_and_merge.R","04_analysis.R")) {
  cat("=== sourcing", sc, format(Sys.time()), "\n")
  withCallingHandlers(source(sc, echo = FALSE, print.eval = TRUE), warning = wh)
}
cat("=== done", format(Sys.time()), "\n")
writeLines(warns, file.path(OUT, "run_authors_warnings.txt"))
for (nm in c("marginal_means_grouped_sector","marginal_means_grouped_sector_mmdiff","marginal_means_grouped_student",
             "marginal_means_grouped_student_mmdiff","x1","marginal_means_grouped_sector_children","marginal_means_grouped_student_children"))
  write.csv(as.data.frame(get(nm)), file.path(OUT, paste0("cj_", nm, ".csv")), row.names = FALSE)
saveRDS(pooled_df2, file.path(dirname(args[1]), "pooled_df2.rds"))
capture.output(table(match_data$D), file = file.path(OUT, "table_match_data_D.txt"))
capture.output(sessionInfo(), file = file.path(OUT, "sessionInfo_run.txt"))
