# Exploratory (not pre-registered) check of the p. 824 prose claim tied to Figure 2 left panel:
# "predicts a 0.2 point increase". Figure 2 left uses full_model_h1_graph (crosssection_linear.R lines 89-93),
# where resource_and_agriculture is recoded to "Both" (mean == 1) vs "None/Single" (mean < 1).
args <- commandArgs(TRUE); outdir <- if (length(args)) args[1] else "outputs"
suppressPackageStartupMessages(library(fixest))
load(file.path(outdir, "session.RData"))
ct <- coeftable(full_model_h1_graph)
est <- as.data.frame(mean_h1)[obs(full_model_h1), ]
out <- data.frame(item = c(paste0("full_model_h1_graph:", rownames(ct)[1]), "full_model_h1_graph:se", "full_model_h1_graph:p", "full_model_h1_graph:nobs",
                           "est_sample_n_resource_and_agriculture_eq_0", "est_sample_n_eq_0.5", "est_sample_n_eq_1",
                           "full_model_h1_max:resource_and_agriculture"),
                  value = c(ct[1,1], ct[1,2], ct[1,4], nobs(full_model_h1_graph),
                            sum(est$resource_and_agriculture == 0), sum(est$resource_and_agriculture == 0.5), sum(est$resource_and_agriculture == 1),
                            coef(full_model_h1_max)["resource_and_agriculture"]))
write.csv(out, file.path(outdir, "figure2_check.csv"), row.names = FALSE); print(out, digits = 6)
