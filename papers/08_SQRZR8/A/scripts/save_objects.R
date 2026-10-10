.libPaths(c("/workspace/audit_runs/08_SQRZR8/A/rlib", .libPaths()))
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/A/outputs"
suppressPackageStartupMessages({library(estimatr); library(sjPlot)})
load("/workspace/audit_runs/08_SQRZR8/A/seg3.RData")
save(all_models, pca_emotion, data, covariates_str, results, file = file.path(OUT, "session_models.RData"))
tab_model(all_models$positive_emo_rv.mod2, all_models$negative_emo.mod2, all_models$neutral_emo_rv.mod2,
  all_models$general_attitude_fic.mod2, all_models$general_attitude_real.mod2, digits = 3, p.style = "stars",
  show.ci = FALSE, show.se = TRUE, collapse.se = TRUE, file = file.path(OUT, "tab_3_col1_models.html"))
print(tab_3, file = file.path(OUT, "tab_3.html"))
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_run.txt"))
cat("SAVED\n")
