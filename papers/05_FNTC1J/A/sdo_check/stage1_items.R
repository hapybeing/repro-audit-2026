# Stage 1 (SDO check): source the env-fixed authors' script from the top up to the line just before the index block
# (original line 1029 'ds_MisInfoCT_datamanag <- ds_MisInfoCT_datamanag %>%'), i.e. the data exactly as the
# authors' line 1035 sees it, then save the item-level SDO data plus the authors' own expression evaluated on it.
# No mice, no models. Usage: Rscript stage1_items.R <env_fixed_script> <out.rds>
args <- commandArgs(trailingOnly = TRUE)
scr <- args[1]; out <- args[2]
L <- readLines(scr, encoding = "UTF-8")
cm <- grep("ConspMent_index = rowMeans", L, fixed = TRUE)[1]
st <- grep("^ds_MisInfoCT_datamanag <- ds_MisInfoCT_datamanag %>%$", L); st <- max(st[st < cm])
cat("Index block starts at env-fixed line", st, "\n")
tf <- tempfile(fileext = ".R"); writeLines(L[1:(st - 1)], tf, useBytes = TRUE)
suppressMessages(source(tf, echo = FALSE))
ds <- ds_MisInfoCT_datamanag
sel <- names(dplyr::select(ds, dplyr::starts_with("SDO")))
cat("starts_with('SDO') selects:", sel, "\n")
# The authors' exact expression (line 1035), evaluated inside the same mutate() idiom:
auth <- (ds %>% dplyr::mutate(SDO_index = rowMeans(dplyr::select(., starts_with("SDO")), na.rm = TRUE)))$SDO_index
items <- data.frame(id = ds$id, SDO1 = ds$SDO1, SDO2 = ds$SDO2, SDO3 = ds$SDO3, SDO4 = ds$SDO4,
                    SDO1_r = ds$SDO1_r, SDO3_r = ds$SDO3_r, SDO_index_authors_expr = auth,
                    rowname = rownames(ds), stringsAsFactors = FALSE)
attr(items, "selected_columns") <- sel
saveRDS(items, out)
cat("saved", nrow(items), "rows to", out, "\n")
