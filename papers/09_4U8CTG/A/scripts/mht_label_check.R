# Agent A, 09_4U8CTG. Code-review check of make_mht_table (02 lines 1727-1742): which coefficient
# each hard-coded row label is attached to. Rebuilds model_1_ez / model_1_ez_lrem as 02 does.
suppressPackageStartupMessages(library(tidyverse))
OUT <- Sys.getenv("OUTDIR")
fr_exp <- read_csv("data/study2_experiment_data.csv", show_col_types = FALSE) |>
  mutate(across(where(is.character), as.factor)) |>
  mutate(opened_quest = as.character(opened_quest)) |>
  filter(!is.na(treatment), !is.na(swd_ch))
zemmour <- fr_exp |> filter(block == "EZ")
labels_in_02 <- c("Intercept", "In-group Government", "In-group Parliament", "Out-group Government", "Placebo")
term_label <- c("(Intercept)" = "Intercept", treatmentdanger_contr = "Placebo", treatmentwin_govt = "In-group Government",
                treatmentwin_mainstream = "Out-group Government", treatmentwin_parl = "In-group Parliament")
out <- list()
for (dv in c("swd_ch", "affect_LREM_ch")) {
  s <- summary(lm(as.formula(paste(dv, "~ treatment")), data = zemmour))$coefficients
  out[[dv]] <- data.frame(dv = dv, row = seq_len(nrow(s)), label_in_02_table = labels_in_02,
                          actual_term = rownames(s), actual_term_label = unname(term_label[rownames(s)]),
                          p_value = s[, 4], label_matches = labels_in_02 == unname(term_label[rownames(s)]))
}
res <- do.call(rbind, out); rownames(res) <- NULL
cat("treatment levels:", levels(zemmour$treatment), "\n")
print(res)
write.csv(res, file.path(OUT, "mht_label_check.csv"), row.names = FALSE)
