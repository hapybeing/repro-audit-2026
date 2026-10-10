# Extract Table 1 (H1) model results from the authors' session (PREREG section 2 step 5).
# Usage (wd = RUNDIR): Rscript extract_targets.R <outdir>
args <- commandArgs(TRUE); outdir <- if (length(args)) args[1] else "outputs"
suppressPackageStartupMessages({library(fixest); library(dplyr)})
load(file.path(outdir, "session.RData"))
mods <- list(full_model_h1 = full_model_h1, full_model_h1_n_resources = full_model_h1_n_resources,
             full_model_h1_max = full_model_h1_max, full_model_h1_n_resources_max = full_model_h1_n_resources_max)
lv <- levels(mean_h1$none_one_or_both_nats_agri_char)
fxv <- as.character(packageVersion("fixest"))
rows <- list()
for (m in names(mods)) {
  ct <- coeftable(mods[[m]])
  rows[[m]] <- data.frame(model = m, term = rownames(ct), estimate = ct[, 1], se = ct[, 2], t = ct[, 3], p = ct[, 4],
                          p_normal = 2 * pnorm(-abs(ct[, 1] / ct[, 2])),
                          nobs = nobs(mods[[m]]), n_fe_groups = unname(mods[[m]]$fixef_sizes["countries_gwid"]),
                          r2 = unname(r2(mods[[m]], "r2")), adj_r2 = unname(r2(mods[[m]], "ar2")),
                          factor_levels = paste(lv, collapse = "|"), factor_class = class(mean_h1$none_one_or_both_nats_agri_char)[1],
                          fixest_version = fxv, row.names = NULL)
}
out <- do.call(rbind, rows)
write.csv(out, file.path(outdir, "targets_extracted.csv"), row.names = FALSE)
print(out[, 1:9], digits = 6)
cat("factor levels:", lv, "\n")
# Labelled deviation only if reference is not "Both"
if (length(lv) == 0 || lv[1] != "Both") {
  d <- mean_h1 %>% as.data.frame()
  d$none_one_or_both_nats_agri_char <- relevel(factor(d$none_one_or_both_nats_agri_char), ref = "Both")
  m2r <- feols(disagreement ~ none_one_or_both_nats_agri_char + n_orgs + regaut + groupsize + incidence_flag + status_pwrrank + any_multiethnic + nightlight_total_pc_log + n_tek_groups | countries_gwid,
               cluster = ~countries_gwid, data = d)
  ct <- coeftable(m2r)
  rr <- data.frame(model = "full_model_h1_n_resources_releveled_Both", term = rownames(ct), estimate = ct[,1], se = ct[,2], t = ct[,3], p = ct[,4],
                   nobs = nobs(m2r), fixest_version = fxv, row.names = NULL)
  write.csv(rr, file.path(outdir, "targets_releveled.csv"), row.names = FALSE); print(rr, digits = 6)
}
# group/level diagnostics
tab <- table(mean_h1$none_one_or_both_nats_agri_char, useNA = "ifany")
write.csv(as.data.frame(tab), file.path(outdir, "factor_level_counts.csv"), row.names = FALSE)
