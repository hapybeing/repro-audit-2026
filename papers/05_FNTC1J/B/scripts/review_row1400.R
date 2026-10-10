# Agent B code review check: which case did line 1770 remove, and is it the case flagged by the script's own checks
# at lines 1757-1767 (plot(model, which = 4, id.n = 3) = top-3 Cook's distance; |standardized residual| > 3)?
# Uses model$data (the exact data object the initial glm at line 1701 received).
# Usage: Rscript review_row1400.R <session.RData> <outdir>
args <- commandArgs(trailingOnly = TRUE); e <- new.env(); load(args[1], envir = e)
suppressMessages(library(dplyr))
m0 <- e$model; pre <- as.data.frame(m0$data)
stopifnot(nrow(pre) == 2963, nobs(m0) == 2963)
aug <- broom::augment(m0) %>% mutate(index = 1:n())
cd <- cooks.distance(m0); sr <- rstandard(m0)
rk <- rank(-cd)
flag <- aug %>% filter(abs(.std.resid) > 3)
top3 <- names(sort(cd, decreasing = TRUE))[1:3]
pos1400_name <- rownames(pre)[1400]
out <- data.frame(
  n_rows_before_removal = nrow(pre), n_used_initial_model = nobs(m0),
  n_abs_std_resid_gt3 = nrow(flag),
  flagged_abs_std_resid_gt3_rownames = paste(flag$.rownames, collapse = ";"),
  top3_cooksd_rownames = paste(top3, collapse = ";"),
  top3_cooksd_values = paste(signif(cd[top3], 4), collapse = ";"),
  rowname_1400_exists = "1400" %in% rownames(pre),
  rowname_1400_cooksd = unname(cd["1400"]), rowname_1400_cooksd_rank = unname(rk["1400"]),
  rowname_1400_std_resid = unname(sr["1400"]),
  rowname_at_position_1400 = pos1400_name,
  position_1400_cooksd = unname(cd[pos1400_name]), position_1400_cooksd_rank = unname(rk[pos1400_name]),
  position_1400_std_resid = unname(sr[pos1400_name]),
  max_abs_std_resid = max(abs(sr)),
  rows_removed_by_line1770 = paste(setdiff(rownames(pre), rownames(as.data.frame(e$model_CTB$data))), collapse = ";"),
  nobs_model_CTB = nobs(e$model_CTB))
print(t(out))
write.csv(out, file.path(args[2], "review_row1400.csv"), row.names = FALSE)
