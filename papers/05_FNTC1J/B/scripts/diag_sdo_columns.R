# Agent B diagnostic: source the authors' script up to line 1028 (just before the index mutate at 1029),
# then print exactly which columns starts_with("SDO") selects at line 1035, and test what the resulting mean equals.
View <- function(...) invisible(NULL)
source("diag_prefix.r", echo = FALSE)
d <- ds_MisInfoCT_datamanag
sel <- names(dplyr::select(d, dplyr::starts_with("SDO")))
cat("### Columns selected by starts_with('SDO') just before line 1029:\n"); print(sel)
x <- as.data.frame(lapply(d[, sel], as.numeric))
orig <- rowMeans(x, na.rm = TRUE)
four <- rowMeans(x[, c("SDO1_r","SDO2","SDO3_r","SDO4")], na.rm = TRUE)
cc <- complete.cases(x)
s1 <- x$SDO1 + x$SDO1_r; s3 <- x$SDO3 + x$SDO3_r
out <- data.frame(
  n_rows = nrow(x), n_complete_sdo = sum(cc),
  sdo1_plus_sdo1r_all_equal_12 = all(s1[!is.na(s1)] == 12),
  sdo3_plus_sdo3r_all_equal_12 = all(s3[!is.na(s3)] == 12))
out$max_abs_diff_orig_vs_4_plus_SDO2_SDO4_over_6_complete <- max(abs(orig[cc] - (4 + (x$SDO2[cc] + x$SDO4[cc]) / 6)))
out$cor_orig_vs_4item_complete <- cor(orig[cc], four[cc])
out$cor_orig_vs_SDO2plusSDO4_complete <- cor(orig[cc], (x$SDO2 + x$SDO4)[cc])
out$mean_orig <- mean(orig, na.rm = TRUE); out$sd_orig <- sd(orig, na.rm = TRUE)
out$mean_4item <- mean(four, na.rm = TRUE); out$sd_4item <- sd(four, na.rm = TRUE)
out$alpha_4item_as_line982 <- psych::alpha(x[, c("SDO1_r","SDO2","SDO3_r","SDO4")])$total$raw_alpha
print(t(out))
write.csv(data.frame(selected_columns = sel), "diag_sdo_selected_columns.csv", row.names = FALSE)
write.csv(out, "diag_sdo_facts.csv", row.names = FALSE)
