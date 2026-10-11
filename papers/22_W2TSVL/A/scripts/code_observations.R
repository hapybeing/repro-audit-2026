# Data facts behind the code observations. Writes outputs/code_observations_check.json
args <- commandArgs(TRUE); OUT <- args[1]
suppressMessages({library(jsonlite); library(MASS)})
dta <- readRDS("outputs/dta_prepared.rds")
mods <- readRDS(file.path(OUT, "models_appendix.rds"))
res <- list(
  d3_label_13 = names(attr(dta$d3, "labels"))[attr(dta$d3, "labels") == 13],
  d3_eq_13_n = sum(dta$d3 == 13), d3_eq_14_n = sum(dta$d3 == 14),
  education_levels_NA_n = sum(is.na(dta$education_levels)),
  education_NA_among_d3_13 = sum(is.na(dta$education_levels[dta$d3 == 13])),
  unions_class = class(dta$unions),
  tableA4_mean_unions_by_group_as_coded = suppressWarnings(as.list(tapply(dta$unions, dta$Treatment, function(x) mean(x, na.rm = TRUE)))),
  tableA4_mean_unions_numeric_by_group = as.list(round(tapply(as.numeric(as.character(dta$unions)), dta$Treatment, mean, na.rm = TRUE), 4)),
  tableA4_typed_constants_unions = c(Control = 3.25, Strike = 3.08, Pro_strike = 3.41, Anti_strike = 2.96, Double_frame = 3.17),
  tableA4_mean_support_by_group = as.list(round(tapply(dta$Support_teachers, dta$Treatment, mean, na.rm = TRUE), 4)),
  tableA4_typed_constants_support = c(Control = 4.36, Strike = 4.18, Pro_strike = 4.91, Anti_strike = 4.40, Double_frame = 4.43),
  n_rows = nrow(dta)
)
write_json(res, file.path(OUT, "code_observations_check.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA)
cat(toJSON(res, auto_unbox = TRUE, pretty = TRUE))
