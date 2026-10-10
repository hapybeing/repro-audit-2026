# Diagnostic (PREREG R_c note): source the env-fixed authors' script up to the line just before
# the index block (original line 1029 'ds_MisInfoCT_datamanag <- ds_MisInfoCT_datamanag %>%'),
# then print which columns starts_with("SDO") selects, and compare the authors' SDO_index with the 4-item mean.
args <- commandArgs(trailingOnly = TRUE)
scr <- args[1]; outcsv <- args[2]
L <- readLines(scr, encoding = "UTF-8")
stop_at <- grep("^ds_MisInfoCT_datamanag <- ds_MisInfoCT_datamanag %>%$", L)
cm <- grep("ConspMent_index = rowMeans", L, fixed = TRUE)[1]
stop_at <- max(stop_at[stop_at < cm])
cat("Index block starts at line", stop_at, "of the env-fixed file (original line", stop_at - 1, ")\n")
cat(L[stop_at:(stop_at + 6)], sep = "\n")
tf <- tempfile(fileext = ".R"); writeLines(L[1:(stop_at - 1)], tf)
suppressMessages(source(tf, echo = FALSE))
ds <- ds_MisInfoCT_datamanag
sel <- names(dplyr::select(ds, dplyr::starts_with("SDO")))
cat("AUDIT names(dplyr::select(ds, starts_with('SDO'))):", sel, "\n")
x6 <- rowMeans(ds[, sel], na.rm = TRUE)
x4 <- rowMeans(ds[, c("SDO1_r", "SDO2", "SDO3_r", "SDO4")], na.rm = TRUE)
x2 <- 4 + (ds$SDO2 + ds$SDO4) / 6
cmp <- data.frame(
  n_rows = nrow(ds),
  selected_columns = paste(sel, collapse = ";"),
  n_selected = length(sel),
  all_SDO1_plus_SDO1r_eq_12 = all((ds$SDO1 + ds$SDO1_r)[!is.na(ds$SDO1)] == 12),
  all_SDO3_plus_SDO3r_eq_12 = all((ds$SDO3 + ds$SDO3_r)[!is.na(ds$SDO3)] == 12),
  n_complete_4items = sum(complete.cases(ds[, c("SDO1", "SDO2", "SDO3", "SDO4")])),
  cor_6col_vs_4item = cor(x6, x4, use = "complete.obs"),
  sd_6col = sd(x6, na.rm = TRUE), sd_4item = sd(x4, na.rm = TRUE),
  min_6col = min(x6, na.rm = TRUE), max_6col = max(x6, na.rm = TRUE),
  min_4item = min(x4, na.rm = TRUE), max_4item = max(x4, na.rm = TRUE),
  check.names = FALSE)
cc <- complete.cases(ds[, c("SDO1", "SDO2", "SDO3", "SDO4")])
cmp$max_abs_diff_6col_vs_4_plus_SDO2_SDO4_over_6_complete <- max(abs(x6[cc] - x2[cc]))
cmp$cor_6col_vs_mean_SDO2_SDO4 <- cor(x6, rowMeans(ds[, c("SDO2","SDO4")], na.rm=TRUE), use = "complete.obs")
print(t(cmp))
write.csv(cmp, outcsv, row.names = FALSE)
# Same check for every other starts_with() used in the index block (code review)
pref <- c("ConspMentality", "EpistBel_Truth", "EpistBel_IT", "EpistBel_AOT", "SDO", "TrustPolitical", "r_AltMed")
oth <- data.frame(prefix = pref, columns = sapply(pref, function(p) paste(names(dplyr::select(ds, dplyr::starts_with(p))), collapse = ";")))
print(oth, right = FALSE)
write.csv(oth, sub("\\.csv$", "_allprefixes.csv", outcsv), row.names = FALSE)
