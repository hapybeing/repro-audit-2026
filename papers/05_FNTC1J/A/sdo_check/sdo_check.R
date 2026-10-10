# Stage 2 (SDO check), 05_FNTC1J, Agent A.
# Inputs: item-level data from stage1_items.R; model checkpoints of (a) the main reproduction run (authors' index)
# and (b) the pre-registered R_c run (whole script rerun from set.seed(2000) with the 4-item index at line 1035);
# the deposited script (for the exact code line); the paper's pdftotext output (for the reported numbers).
# Output: one JSON file. Every number in it is computed or parsed here; nothing is typed by hand.
# Usage: Rscript sdo_check.R <items.rds> <main_ckpt.RData> <rc_ckpt.RData> <orig_script.r> <paper.txt> <out.json>
args <- commandArgs(trailingOnly = TRUE)
suppressMessages({library(sandwich); library(lmtest); library(jsonlite); library(psych)})
items <- readRDS(args[1]); main <- new.env(); load(args[2], envir = main); rc <- new.env(); load(args[3], envir = rc)
orig <- readLines(args[4], encoding = "UTF-8"); paper <- readLines(args[5], encoding = "UTF-8")
out <- list(paper_id = "05_FNTC1J", agent = "A", generated_at_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
            r_version = R.version.string,
            inputs = list(items = args[1], main_checkpoint = args[2], rc_checkpoint = args[3], script = args[4], paper_text = args[5]))

## 1. Code location ---------------------------------------------------------------------------------------------
ln <- grep('SDO_index = rowMeans(dplyr::select(., starts_with("SDO")), na.rm = TRUE)', orig, fixed = TRUE)
ln_r1 <- grep("SDO1_r <- 12 - ", orig, fixed = TRUE); ln_r3 <- grep("SDO3_r <- 12 - ", orig, fixed = TRUE)
ln_alpha <- grep('calculate_alpha(c("SDO1_r", "SDO2", "SDO3_r", "SDO4"))', orig, fixed = TRUE)
ln_1400 <- grep('!= "1400"', orig, fixed = TRUE)
out$code <- list(file = "MisinfoCT_HSK.r (deposited, sha256 fd86537e...cf157)",
  sdo_index_line = ln, sdo_index_code = trimws(orig[ln]),
  reverse_SDO1_line = ln_r1, reverse_SDO1_code = trimws(orig[ln_r1]),
  reverse_SDO3_line = ln_r3, reverse_SDO3_code = trimws(orig[ln_r3]),
  authors_reliability_check_line = ln_alpha, authors_reliability_check_code = trimws(orig[ln_alpha]),
  row1400_line = ln_1400, row1400_code = trimws(orig[ln_1400]), row1400_comment = trimws(orig[ln_1400 - 1]),
  columns_selected_by_starts_with_SDO = attr(items, "selected_columns"),
  corrected_code = 'SDO_index = rowMeans(dplyr::select(., c("SDO1_r", "SDO2", "SDO3_r", "SDO4")), na.rm = TRUE)')

## 2. Paper values (parsed from pdftotext) ----------------------------------------------------------------------
hdr <- grep("(COVID-19|Wintterlin) +[0-9]+ *$", paper)
page_of <- function(i) { h <- max(hdr[hdr < i]); as.integer(sub(".* ([0-9]+) *$", "\\1", paper[h])) }
tabs <- grep("^ *Table (A[1-4]|B1[ab])\\.", paper)
tab_of <- function(i) { t <- max(tabs[tabs < i]); trimws(paper[t]) }
nums <- function(s) as.numeric(regmatches(s, gregexpr("-?[0-9]+\\.[0-9]+|-?[0-9]+", s))[[1]])
sdo_rows <- grep("^ *Social Dominance +[-0-9]", paper)
paper_rows <- lapply(sdo_rows, function(i) {
  tb <- tab_of(i); v <- nums(sub("^ *Social Dominance", "", paper[i]))
  r <- list(table = tb, page = page_of(i), text_line = i, raw = trimws(paper[i]))
  if (grepl("Table A[12]", tb)) r$values <- list(log_odds = v[1], se = v[2], y_std = v[3], odds_ratio = v[4], ci_low = v[5], ci_high = v[6],
                                                 stars = grepl("\\*", paper[i]))
  if (grepl("Table A[34]", tb)) r$values <- list(estimate = v[1], std_beta = v[2], ci_low = v[3], ci_high = v[4], std_ci_low = v[5], std_ci_high = v[6],
                                                 stars = grepl("\\*", paper[i]))
  r })
for (k in seq_along(paper_rows)) if (grepl("B1", paper_rows[[k]]$table)) { i <- paper_rows[[k]]$text_line; v <- nums(paper[i + 1])
  paper_rows[[k]]$raw_next_line <- trimws(paper[i + 1]); paper_rows[[k]]$values <- list(mean = v[1], sd = v[2], min = v[3], max = v[4]) }
out$paper_reported <- paper_rows
out$paper_scale_description <- trimws(paper[grep("Social dominance orientation was measured", paper) + 0:2])

## 3. Cancellation: algebra and numbers --------------------------------------------------------------------------
it <- items
x6 <- it$SDO_index_authors_expr
x4 <- rowMeans(it[, c("SDO1_r", "SDO2", "SDO3_r", "SDO4")], na.rm = TRUE); x4[is.nan(x4)] <- NA
x6[is.nan(x6)] <- NA
x6_manual <- rowMeans(it[, c("SDO1", "SDO2", "SDO3", "SDO4", "SDO1_r", "SDO3_r")], na.rm = TRUE); x6_manual[is.nan(x6_manual)] <- NA
m24 <- rowMeans(it[, c("SDO2", "SDO4")], na.rm = TRUE); m24[is.nan(m24)] <- NA
cc <- complete.cases(it[, c("SDO1", "SDO2", "SDO3", "SDO4")])
pat <- apply(!is.na(it[, c("SDO1", "SDO2", "SDO3", "SDO4")]), 1, function(z) paste(c("SDO1", "SDO2", "SDO3", "SDO4")[z], collapse = "+"))
pat[pat == ""] <- "none"
# general closed form with na.rm: k = number of present items among SDO1,SDO3 (each contributes x + (12 - x) = 12 over 2 columns)
k13 <- (!is.na(it$SDO1)) + (!is.na(it$SDO3)); k24 <- (!is.na(it$SDO2)) + (!is.na(it$SDO4))
s24 <- rowSums(it[, c("SDO2", "SDO4")], na.rm = TRUE)
closed <- (12 * k13 + s24) / (2 * k13 + k24); closed[(2 * k13 + k24) == 0] <- NA
ex <- head(which(cc), 5)
out$cancellation <- list(
  algebra = paste0("SDO1_r = 12 - SDO1 and SDO3_r = 12 - SDO3 (lines ", ln_r1, " and ", ln_r3, "). ", paste("With all four items present the authors' index is",
    "(SDO1 + SDO2 + SDO3 + SDO4 + (12 - SDO1) + (12 - SDO3)) / 6 = (24 + SDO2 + SDO4) / 6 = 4 + (SDO2 + SDO4) / 6.",
    "SDO1 and SDO3 drop out. With na.rm = TRUE and some items missing, SDO1 and SDO1_r are missing together (same for SDO3),",
    "so the index is (12 * k13 + SDO2 + SDO4) / (2 * k13 + k24), where k13 and k24 count the present items among {SDO1, SDO3} and {SDO2, SDO4}:",
    "still no dependence on the values of SDO1 or SDO3. The intended index is (SDO1_r + SDO2 + SDO3_r + SDO4) / 4 = (24 - SDO1 - SDO3 + SDO2 + SDO4) / 4.",
    "Items 1 and 3 are the pro-equality statements (We must consider all groups..., Group equality should be our ideal), so the original index",
    "contains no information from the two reverse-keyed items and is a linear rescaling of the SDO2 + SDO4 sum with slope 1/6 and range 1 to 9 instead of 1 to 11.")),
  n_rows_item_stage = nrow(it),
  authors_expr_equals_mean_of_6_columns_max_abs_diff = max(abs(x6 - x6_manual), na.rm = TRUE),
  all_SDO1_plus_SDO1r_eq_12 = all((it$SDO1 + it$SDO1_r)[!is.na(it$SDO1)] == 12),
  all_SDO3_plus_SDO3r_eq_12 = all((it$SDO3 + it$SDO3_r)[!is.na(it$SDO3)] == 12),
  SDO1_and_SDO1r_missing_together = all(is.na(it$SDO1) == is.na(it$SDO1_r)),
  SDO3_and_SDO3r_missing_together = all(is.na(it$SDO3) == is.na(it$SDO3_r)),
  n_complete_4_items = sum(cc),
  complete_rows_max_abs_diff_from_4_plus_SDO2_SDO4_over_6 = max(abs(x6[cc] - (4 + (it$SDO2[cc] + it$SDO4[cc]) / 6))),
  all_rows_max_abs_diff_from_closed_form = max(abs(x6 - closed), na.rm = TRUE),
  missingness_patterns = as.list(table(pat)),
  n_index_missing_before_imputation = sum(is.na(x6)),
  partial_derivative_check = {
    # perturb SDO1 and SDO3 on complete rows (stay within 1..11) and recompute the authors' 6-column mean
    p <- it[cc, ]; p$SDO1 <- ifelse(p$SDO1 <= 6, p$SDO1 + 5, p$SDO1 - 5); p$SDO3 <- ifelse(p$SDO3 <= 6, p$SDO3 + 5, p$SDO3 - 5)
    p$SDO1_r <- 12 - p$SDO1; p$SDO3_r <- 12 - p$SDO3
    y6 <- rowMeans(p[, c("SDO1", "SDO2", "SDO3", "SDO4", "SDO1_r", "SDO3_r")])
    y4 <- rowMeans(p[, c("SDO1_r", "SDO2", "SDO3_r", "SDO4")])
    list(description = "SDO1 and SDO3 shifted by 5 points on every complete row (reversed copies recomputed); change in each index",
         authors_index_max_abs_change = max(abs(y6 - x6[cc])), corrected_index_mean_abs_change = mean(abs(y4 - x4[cc]))) },
  example_rows = lapply(ex, function(i) list(id = it$id[i], SDO1 = it$SDO1[i], SDO2 = it$SDO2[i], SDO3 = it$SDO3[i], SDO4 = it$SDO4[i],
    SDO1_r = it$SDO1_r[i], SDO3_r = it$SDO3_r[i], authors_index = x6[i], four_plus_SDO2_SDO4_over_6 = 4 + (it$SDO2[i] + it$SDO4[i]) / 6,
    corrected_4item_index = x4[i])))

## 4. Descriptives, correlation, alpha ----------------------------------------------------------------------------
desc <- function(x) list(n = sum(!is.na(x)), mean = mean(x, na.rm = TRUE), sd = sd(x, na.rm = TRUE), min = min(x, na.rm = TRUE), max = max(x, na.rm = TRUE))
alpha_of <- function(cols, keys = FALSE) {
  a <- suppressWarnings(suppressMessages(psych::alpha(it[, cols], check.keys = keys, warnings = FALSE)))
  list(columns = cols, raw_alpha = a$total$raw_alpha, std_alpha = a$total$std.alpha, n_complete = sum(complete.cases(it[, cols])),
       mean_inter_item_r = a$total$average_r) }
rmat <- cor(it[, c("SDO1", "SDO2", "SDO3", "SDO4")], use = "pairwise.complete.obs")
# indices as entered in the models (after mice), matched by id over the 2962 rows of model_CTB
# Rows are matched by row name (original raw-data row names, kept through the script), not by id: the id column has duplicates.
rn_main <- rownames(main$model_CTB$data); rn_rc <- rownames(rc$model_CTB$data)
stopifnot(all(rn_main %in% it$rowname), all(rownames(main$ds_MisInfoCT_analysis) %in% it$rowname))
s_main <- main$model_CTB$data$SDO_index; s_rc <- rc$model_CTB$data$SDO_index[match(rn_main, rn_rc)]
dup_ids <- unique(it$id[duplicated(it$id)]); dup_rows <- it$rowname[it$id %in% dup_ids]
out$index_comparison <- list(
  descriptives_item_stage = list(authors_index = desc(x6), corrected_4item_index = desc(x4)),
  descriptives_model_data = list(authors_index = desc(s_main), corrected_4item_index_Rc = desc(s_rc)),
  check_authors_index_in_main_model_equals_item_stage = {
    j <- match(rn_main, it$rowname); ok <- !is.na(x6[j]); nd <- ok & !(rn_main %in% dup_rows)
    list(n_compared = sum(ok), max_abs_diff_all = max(abs(s_main[ok] - x6[j][ok])),
         n_compared_excluding_duplicate_id_rows = sum(nd), max_abs_diff_excluding_duplicate_id_rows = max(abs(s_main[nd] - x6[j][nd]))) },
  duplicate_ids = list(
    note = "Side finding: the id column is not unique. The imputation step (lines 1210-1218) averages mice output by id and writes it back by id, so for duplicated ids every imputed column, including observed SDO_index values, is replaced by the mean over the respondents sharing that id.",
    n_duplicated_ids = length(dup_ids), n_rows_with_duplicated_id = length(dup_rows), rownames = dup_rows,
    n_rows_in_model_CTB = sum(rn_main %in% dup_rows),
    n_rows_where_observed_SDO_index_was_overwritten = { j <- match(rn_main, it$rowname); sum(!is.na(x6[j]) & abs(s_main - x6[j]) > 1e-9) }),
  correlation = list(
    item_stage_complete_4_items = cor(x6[cc], x4[cc]),
    item_stage_all_available = cor(x6, x4, use = "complete.obs"),
    item_stage_n_all_available = sum(!is.na(x6) & !is.na(x4)),
    model_data_2962_rows_main_vs_Rc_imputed = cor(s_main, s_rc, use = "complete.obs"),
    model_data_n = sum(!is.na(s_main) & !is.na(s_rc)),
    authors_index_vs_sum_SDO2_SDO4_complete = cor(x6[cc], it$SDO2[cc] + it$SDO4[cc]),
    corrected_index_vs_mean_SDO1r_SDO3r_complete = cor(x4[cc], (it$SDO1_r[cc] + it$SDO3_r[cc]) / 2),
    authors_index_vs_mean_SDO1r_SDO3r_complete = cor(x6[cc], (it$SDO1_r[cc] + it$SDO3_r[cc]) / 2)),
  item_correlations_pairwise = as.list(setNames(as.vector(rmat[upper.tri(rmat)]),
    apply(which(upper.tri(rmat), arr.ind = TRUE), 1, function(z) paste(colnames(rmat)[z[1]], colnames(rmat)[z[2]], sep = "_")))),
  cronbach_alpha = list(
    note = "psych::alpha, check.keys = FALSE, item-stage data (after the authors' -1 to NA recodes, before imputation). The authors' index is the mean of 6 columns; its alpha as a 6-column scale is reported, plus the alpha of what it effectively measures (SDO2, SDO4). The paper reports no alpha for SDO.",
    authors_index_6_columns_as_averaged = alpha_of(c("SDO1", "SDO2", "SDO3", "SDO4", "SDO1_r", "SDO3_r")),
    authors_index_effective_items_SDO2_SDO4 = alpha_of(c("SDO2", "SDO4")),
    corrected_4item_index = alpha_of(c("SDO1_r", "SDO2", "SDO3_r", "SDO4")),
    raw_items_unreversed_SDO1_to_SDO4 = alpha_of(c("SDO1", "SDO2", "SDO3", "SDO4"))))

## 5. SDO coefficient in every model with an SDO row in the paper's tables -----------------------------------------
glm_row <- function(m, term = "SDO_index") {
  V <- sandwich::vcovHC(m, type = "HC3"); ct <- lmtest::coeftest(m, vcov = V); ci <- lmtest::coefci(m, vcov = V)
  pa <- p.adjust(ct[, 4], method = "bonferroni")
  list(log_odds = ct[term, 1], se_hc3 = ct[term, 2], odds_ratio = exp(ct[term, 1]), or_ci_low = exp(ci[term, 1]), or_ci_high = exp(ci[term, 2]),
       p_raw = ct[term, 4], p_bonferroni = pa[[term]], n_terms_bonferroni = nrow(ct), nobs = nobs(m),
       or_per_sd_of_index = exp(ct[term, 1] * sd(model.frame(m)[[term]])), sd_of_index_in_model = sd(model.frame(m)[[term]])) }
targets_of <- function(mc, mm) {
  g <- function(m, term) { V <- sandwich::vcovHC(m, type = "HC3"); ct <- lmtest::coeftest(m, vcov = V)
    list(odds_ratio = exp(ct[term, 1]), se_hc3 = ct[term, 2], p_bonferroni = p.adjust(ct[, 4], "bonferroni")[[term]]) }
  list(T1_CT_ConspMent = g(mc, "ConspMent_index"), T2_misinfo_ConspMent = g(mm, "ConspMent_index"),
       T3_CT_Truth = g(mc, "EpistBel_Truth_index"), T4_misinfo_Truth = g(mm, "EpistBel_Truth_index"), T5_nobs_CT = nobs(mc)) }
lin_form <- function(y) as.formula(paste(y, "~ ConspMent_index + EpistBel_Truth_index + AltMed_index + EpistBel_IT_index + polorientation +",
  "MediaUse_socialMedia_index + religiousity + SDO_index + gender_male + EpistBel_AOT_index + MediaUse_traditional_index + age +",
  "MediaUse_online_index + edu_high + TrustScience + TrustPolitical_index + TrustMedia_index + TrustAltMed_index"))
lm_row <- function(d, y) {
  m <- lm(lin_form(y), data = d); s <- summary(m)$coefficients; ci <- confint(m)
  sdy <- sd(model.frame(m)[[y]]); sdx <- sd(model.frame(m)$SDO_index)
  V1 <- sandwich::vcovHC(m, type = "HC1"); ct1 <- lmtest::coeftest(m, vcov = V1)
  list(estimate = s["SDO_index", 1], se = s["SDO_index", 2], ci_low = ci["SDO_index", 1], ci_high = ci["SDO_index", 2], p = s["SDO_index", 4],
       std_beta = s["SDO_index", 1] * sdx / sdy, p_hc1 = ct1["SDO_index", 4], nobs = nobs(m),
       note = "OLS as in the authors' tab_model(model_lin) export (classical SE/CI, unadjusted p); p_hc1 = the authors' coeftest HC1 line, for reference") }
d_main <- main$ds_MisInfoCT_analysis; d_rc <- rc$ds_MisInfoCT_analysis
# (b2) isolate the index change: main-run imputed data, SDO_index replaced by the 4-item mean of the observed items;
# for rows where all 4 items are missing (index imputed by mice) the R_c run's imputed 4-item value is used.
swap <- function(d) { rn <- rownames(d); j <- match(rn, it$rowname); stopifnot(!anyNA(j)); v <- x4[j]
  miss <- is.na(v); v[miss] <- d_rc$SDO_index[match(rn[miss], rownames(d_rc))]; d$SDO_index <- v; attr(d, "n_from_rc_imputation") <- sum(miss); d }
mdat_swap <- swap(main$model_CTB$data); dsw <- swap(d_main)
m_ct_b2 <- glm(formula(main$model_CTB), data = mdat_swap, family = binomial)
m_mi_b2 <- glm(formula(main$model_misinfo), data = mdat_swap, family = binomial)
refit_check <- max(abs(coef(glm(formula(main$model_CTB), data = main$model_CTB$data, family = binomial)) - coef(main$model_CTB)))
out$sdo_coefficient <- list(
  versions = list(a_original = "authors' index (6-column mean), main reproduction run (matches paper Tables A1/A2)",
    b_corrected_Rc = "4-item index, pre-registered R_c run: whole script rerun from set.seed(2000), so mice re-imputed every variable",
    b2_corrected_same_imputation = "4-item index swapped into the main run's imputed data, all other variables identical to (a); isolates the index change",
    b2_rows_using_Rc_imputed_value = attr(mdat_swap, "n_from_rc_imputation")),
  refit_from_stored_data_max_abs_coef_diff = refit_check,
  Table_A1_logistic_CT = list(a_original = glm_row(main$model_CTB), b_corrected_Rc = glm_row(rc$model_CTB), b2_corrected_same_imputation = glm_row(m_ct_b2)),
  Table_A2_logistic_misinfo = list(a_original = glm_row(main$model_misinfo), b_corrected_Rc = glm_row(rc$model_misinfo), b2_corrected_same_imputation = glm_row(m_mi_b2)),
  Table_A3_linear_CT_count = list(a_original = lm_row(d_main, "COVID_CTB"), b_corrected_Rc = lm_row(d_rc, "COVID_CTB"), b2_corrected_same_imputation = lm_row(dsw, "COVID_CTB")),
  Table_A4_linear_misinfo_count = list(a_original = lm_row(d_main, "misinfo_covid_beliefs"), b_corrected_Rc = lm_row(d_rc, "misinfo_covid_beliefs"), b2_corrected_same_imputation = lm_row(dsw, "misinfo_covid_beliefs")))
out$targets_under_each_index <- list(a_original = targets_of(main$model_CTB, main$model_misinfo), b_corrected_Rc = targets_of(rc$model_CTB, rc$model_misinfo),
                                     b2_corrected_same_imputation = targets_of(m_ct_b2, m_mi_b2))

## 6. Row "1400" kept vs removed ------------------------------------------------------------------------------------
r1400 <- function(env, swapped = FALSE) {
  d0 <- env$model$data; if (swapped) d0 <- swap(d0)
  mc0 <- glm(formula(env$model_CTB), data = d0, family = binomial); mm0 <- glm(formula(env$model_misinfo), data = d0, family = binomial)
  cd <- cooks.distance(env$model)
  list(rows_before_removal = nrow(d0), row_1400_present = "1400" %in% rownames(d0),
       row_1400_values = as.list(d0["1400", c("COVID_CTB_dummy", "misinfo_covid_beliefs_dummy", "SDO_index", "ConspMent_index")]),
       row_1400_cooks_distance_prelim_model = unname(cd["1400"]), row_1400_cooks_rank = match("1400", names(sort(cd, decreasing = TRUE))),
       top3_cooks_rownames = names(sort(cd, decreasing = TRUE))[1:3],
       kept = list(targets = targets_of(mc0, mm0), SDO_CT = glm_row(mc0), SDO_misinfo = glm_row(mm0))) }
out$row1400 <- list(
  note = "kept = final glm formulas refit on the data before the line-1770 removal (preliminary model data, 2963 rows); removed = the paper's models (section 5)",
  a_original = r1400(main), b_corrected_Rc = r1400(rc), b2_corrected_same_imputation = r1400(main, swapped = TRUE))

writeLines(toJSON(out, auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null"), args[6])
cat("wrote", args[6], "\n")
str(out$sdo_coefficient$Table_A1_logistic_CT)
