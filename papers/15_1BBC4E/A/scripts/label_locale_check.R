# Checks the positional relabelling of alphabetically ordered factor levels in Comparison.R lines 98-105 and 133-176 (Figures 1 and 4, not targets) under the current collation locale.
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/A/outputs"
loc <- Sys.getlocale("LC_COLLATE")
comparison <- c("RegType_lied_n", "RegType_RoW_n", "Politytype_n", "fh_status_n", "RegType_magaloni_n", "HTW_RegType_n", "AnckarRegtype_n")
truth <- c(RegType_lied_n="LIED", RegType_RoW_n="RoW", Politytype_n="Polity", fh_status_n="FH", RegType_magaloni_n="AoW", HTW_RegType_n="ARD", AnckarRegtype_n="CPR")
lv <- levels(as.factor(comparison)); assigned <- c("CPR", "FH", "ARD", "Polity", "LIED", "AoW", "RoW")  # Comparison.R line 176
d <- data.frame(locale=loc, original_level=lv, label_assigned_line176=assigned, correct_label=truth[lv], ok=assigned==truth[lv])
f <- file.path(OUT, "label_locale_check.csv"); write.csv(d, f, row.names=FALSE, append=FALSE)
print(d)
