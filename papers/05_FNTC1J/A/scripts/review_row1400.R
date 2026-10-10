# Code review check: what is the row named "1400" that original line 1770 removes, judged by the preliminary model
# `model` (original lines 1688-1696) in this reproduction? Writes outputs/review_row1400.csv
args <- commandArgs(trailingOnly = TRUE)
suppressMessages(library(stats)); load(args[1])
cd <- cooks.distance(model); sr <- rstandard(model)
o <- order(cd, decreasing = TRUE)
r <- data.frame(n_model = nobs(model), row1400_in_model = "1400" %in% names(cd),
  row1400_cooks = unname(cd["1400"]), row1400_cooks_rank = match("1400", names(cd)[o]),
  row1400_std_resid = unname(sr["1400"]), row1400_position_in_data = match("1400", names(cd)),
  name_of_row_at_position_1400 = names(cd)[1400], cooks_at_position_1400 = unname(cd[1400]),
  rank_of_position_1400 = match(names(cd)[1400], names(cd)[o]),
  top3_cooks_rownames = paste(names(cd)[o][1:3], collapse = ";"), top3_cooks = paste(signif(cd[o][1:3], 4), collapse = ";"),
  n_abs_std_resid_gt3 = sum(abs(sr) > 3), threshold_4_over_n = 4 / nobs(model), n_cooks_gt_4_over_n = sum(cd > 4 / nobs(model)),
  row1400_outcome = as.character(model$y["1400"]), model_CTB_has_row1400 = "1400" %in% rownames(model.frame(model_CTB)))
print(t(r)); write.csv(r, args[2], row.names = FALSE)
# Impact: refit the final CTB and misinfo formulas on the data before the row "1400" removal (model$data, 2963 rows)
suppressMessages({library(sandwich); library(lmtest)})
d0 <- model$data
imp <- do.call(rbind, lapply(list(CTB = model_CTB, misinfo = model_misinfo), function(m) {
  m0 <- glm(formula(m), data = d0, family = binomial)
  ct <- coeftest(m0, vcov = vcovHC(m0, type = "HC3"))
  data.frame(nobs_with_row1400 = nobs(m0), or_consp_with = exp(coef(m0)["ConspMent_index"]), or_consp_final = exp(coef(m)["ConspMent_index"]),
             or_truth_with = exp(coef(m0)["EpistBel_Truth_index"]), or_truth_final = exp(coef(m)["EpistBel_Truth_index"]))
}))
imp$model <- rownames(imp); print(imp, digits = 6)
write.csv(imp, sub("\\.csv$", "_impact.csv", args[2]), row.names = FALSE)
