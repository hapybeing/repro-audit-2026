# Driver: runs the authors' unchanged main_rep.R and saves objects for extraction.
# Run from RUN dir (holds main_rep.R and data_cleaned_rep.csv). Not an edit of the authors' file.
.libPaths(c("/workspace/audit_runs/08_SQRZR8/A/rlib", .libPaths()))
# run 2 (run 1 lost its variables to rm(list = ls()) on main_rep.R line 8 and stopped after the authors' script ended)
set.seed(20261009)  # main_rep.R sets no seed; affects only the mediation bootstrap (Figure 3), not targets
options(audit_t0 = Sys.time())  # main_rep.R line 8 runs rm(list = ls()); options survive it
source("main_rep.R", echo = TRUE, max.deparse.length = Inf)
OUT <- Sys.getenv("OUTDIR")  # read after source() because main_rep.R clears the global environment
cat("\nELAPSED_MIN", as.numeric(difftime(Sys.time(), getOption("audit_t0"), units = "mins")), "\n")
save(all_models, pca_emotion, data, covariates_str, results, file = file.path(OUT, "session_models.RData"))
sjPlot::tab_model(all_models$positive_emo_rv.mod2, all_models$negative_emo.mod2, all_models$neutral_emo_rv.mod2,
  all_models$general_attitude_fic.mod2, all_models$general_attitude_real.mod2, digits = 3, p.style = "stars",
  show.ci = FALSE, show.se = TRUE, collapse.se = TRUE, file = file.path(OUT, "tab_3_col1_models.html"))
print(tab_3, file = file.path(OUT, "tab_3.html"))
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_run.txt"))
cat("RUN_DONE\n")
