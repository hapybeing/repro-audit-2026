# Runs the authors' scripts 01-04 unchanged, in order, from analysis/ (as 04_analysis.R header asks),
# then saves the objects needed for targets and checks. Usage: Rscript run_authors.R RUNDIR OUTDIR
args <- commandArgs(trailingOnly = TRUE)
rundir <- args[1]; outdir <- args[2]
setwd(file.path(rundir, "analysis"))
options(warn = 1)
for (f in c("01_preparation_function.R", "02_plot_function.R", "03_data_prep_and_merge.R", "04_analysis.R")) {
  cat("\n######## sourcing", f, "\n")
  source(f, echo = TRUE, max.deparse.length = Inf, spaced = FALSE)
}
cat("\n######## warnings() after 04:\n"); print(warnings())
saveRDS(pooled_df2, file.path(rundir, "pooled_df2.rds"))
saveRDS(match_data, file.path(rundir, "match_data.rds"))
objs <- c("marginal_means_grouped_sector", "marginal_means_grouped_sector_mmdiff",
          "marginal_means_grouped_student", "marginal_means_grouped_student_mmdiff",
          "x1", "marginal_means_grouped_sector_children", "marginal_means_grouped_student_children")
for (o in objs) write.csv(as.data.frame(get(o)), file.path(outdir, paste0("cj_", o, ".csv")), row.names = FALSE)
writeLines(capture.output(print(table(match_data$D, useNA = "ifany"))), file.path(outdir, "table_match_data_D.txt"))
cat("\nDONE\n")
