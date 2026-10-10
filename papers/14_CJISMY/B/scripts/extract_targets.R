# Agent B, 14_CJISMY. Extract Table 1 (H1) quantities from the authors' run (PREREG section 2, step 5).
# Usage: Rscript extract_targets.R <session.RData> <outdir> <tag>
args <- commandArgs(trailingOnly = TRUE)
sess <- args[1]; outdir <- args[2]; tag <- if (length(args) >= 3) args[3] else "main"
suppressPackageStartupMessages(library(fixest))
load(sess)
fv <- as.character(packageVersion("fixest"))
mods <- list(model1_full_model_h1 = full_model_h1,
             model2_full_model_h1_n_resources = full_model_h1_n_resources,
             model3_full_model_h1_max = full_model_h1_max,
             model4_full_model_h1_n_resources_max = full_model_h1_n_resources_max)
lev <- levels(factor(mean_h1$none_one_or_both_nats_agri_char))
lev_raw <- if (is.factor(mean_h1$none_one_or_both_nats_agri_char)) levels(mean_h1$none_one_or_both_nats_agri_char) else paste0("(not a factor: ", class(mean_h1$none_one_or_both_nats_agri_char)[1], ")")
rows <- list()
for (m in names(mods)) {
  mo <- mods[[m]]
  ct <- coeftable(mo)
  for (v in rownames(ct)) {
    est <- ct[v, 1]; se <- ct[v, 2]; tv <- ct[v, 3]; pv <- ct[v, 4]
    rows[[length(rows) + 1]] <- data.frame(model = m, term = v, estimate = est, se_cluster = se, t = tv,
      p_fixest = pv, p_normal = 2 * pnorm(-abs(est / se)), nobs = nobs(mo),
      n_fe_groups = unname(mo$fixef_sizes["countries_gwid"]), n_obs_removed = length(mo$obs_selection$obsRemoved),
      r2 = unname(r2(mo, "r2")), adj_r2 = unname(r2(mo, "ar2")),
      factor_levels_in_order = paste(lev_raw, collapse = "|"), fixest_version = fv, run_tag = tag,
      stringsAsFactors = FALSE)
  }
}
out <- do.call(rbind, rows)
write.csv(out, file.path(outdir, paste0("targets_extracted", ifelse(tag == "main", "", paste0("_", tag)), ".csv")), row.names = FALSE)

# Factor level counts, and relevelled Model 2 refit only if the reference level is not "Both" (PREREG step 5)
fl <- as.data.frame(table(mean_h1$none_one_or_both_nats_agri_char, useNA = "ifany"))
names(fl) <- c("level", "n_groups")
write.csv(fl, file.path(outdir, paste0("factor_levels", ifelse(tag == "main", "", paste0("_", tag)), ".csv")), row.names = FALSE)
cat("fixest", fv, "\nfactor levels (in order):", lev_raw, "\n")
cat("reference level:", lev_raw[1], "\n")
if (lev_raw[1] != "Both") {
  d <- as.data.frame(mean_h1)
  d$none_one_or_both_nats_agri_char <- relevel(factor(d$none_one_or_both_nats_agri_char), ref = "Both")
  m2r <- feols(disagreement ~ none_one_or_both_nats_agri_char + n_orgs + regaut + groupsize + incidence_flag + status_pwrrank + any_multiethnic + nightlight_total_pc_log + n_tek_groups | countries_gwid,
               cluster = ~countries_gwid, data = d)
  ct <- coeftable(m2r)
  rr <- data.frame(model = "model2_releveled_ref_Both", term = rownames(ct), estimate = ct[, 1], se_cluster = ct[, 2],
                   t = ct[, 3], p_fixest = ct[, 4], p_normal = 2 * pnorm(-abs(ct[, 1] / ct[, 2])), nobs = nobs(m2r),
                   fixest_version = fv, run_tag = tag, stringsAsFactors = FALSE)
  write.csv(rr, file.path(outdir, paste0("targets_releveled", ifelse(tag == "main", "", paste0("_", tag)), ".csv")), row.names = FALSE)
  cat("Releveled refit written.\n")
}
print(out[out$term %in% c("resource_and_agriculture", "none_one_or_both_nats_agri_charNone", "none_one_or_both_nats_agri_charSingle", "none_one_or_both_nats_agri_charBoth"),
          c("model", "term", "estimate", "se_cluster", "p_fixest", "nobs", "n_fe_groups")])
