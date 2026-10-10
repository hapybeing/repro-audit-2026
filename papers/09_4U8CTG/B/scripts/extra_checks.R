# Agent B, 09_4U8CTG: code-review check of make_mht_table labels (02 lines 1727-1731 in deposit) and context numbers.
args <- commandArgs(trailingOnly = TRUE); outdir <- normalizePath(args[1])
load(file.path(outdir, "session_02_models.RData"))
labels_in_code <- c("Intercept", "In-group Government", "In-group Parliament", "Out-group Government", "Placebo")
mk <- function(m, nm) { s <- summary(m)$coefficients
  data.frame(model = nm, position = seq_len(nrow(s)), actual_term = rownames(s), label_in_code = labels_in_code,
             p_original = s[, 4], p_bonferroni = p.adjust(s[, 4], "bonferroni"), p_holm = p.adjust(s[, 4], "holm")) }
d <- rbind(mk(model_1_ez, "model_1_ez"), mk(model_1_ez_lrem, "model_1_ez_lrem")); rownames(d) <- NULL
truth <- c("(Intercept)" = "Intercept", treatmentdanger_contr = "Placebo", treatmentwin_govt = "In-group Government",
           treatmentwin_mainstream = "Out-group Government", treatmentwin_parl = "In-group Parliament")
d$label_matches_term <- unname(truth[d$actual_term]) == d$label_in_code
write.csv(d, file.path(outdir, "mht_label_check.csv"), row.names = FALSE)
print(d)
cat("treatment levels:", levels(factor(zemmour$treatment)), "\n")
print(table(zemmour$treatment))
# Figure label checks (02 lines 587-590 Fig D1 x labels; 743-746/754 Fig D4 fill labels; 642/672-674 Fig D2 legend).
# A positional label vector on a discrete scale / factor() is matched to the sorted factor levels.
lv <- levels(zemmour$treatment)
lab_d1 <- c("Control", "Placebo Social Norm", "In-group Government", "In-group Parliament", "Out-group Government")
true_lab <- c(control = "Control", danger_contr = "Placebo Social Norm", win_govt = "In-group Government",
              win_parl = "In-group Parliament", win_mainstream = "Out-group Government")
fig <- data.frame(figure = "D1 x-axis and D4 fill", level = lv, label_shown = lab_d1, correct_label = unname(true_lab[lv]))
d2_lv <- c("control","win_parl","win_govt","win_mainstream","danger_contr")
d2_leg <- c("Control", "T1a", "T1b", "T2", "Placebo")
a4 <- c(control = "Control", win_govt = "T1a", win_parl = "T1b", win_mainstream = "T2", danger_contr = "Placebo")  # Table A4 (deposit 02 lines 1339-1343)
fig <- rbind(fig, data.frame(figure = "D2 legend", level = d2_lv, label_shown = d2_leg, correct_label = unname(a4[d2_lv])))
fig$match <- fig$label_shown == fig$correct_label
write.csv(fig, file.path(outdir, "figure_label_check.csv"), row.names = FALSE); print(fig)
