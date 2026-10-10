# Exploratory (not pre-registered), figures only: Comparison.R relabels factor levels by position
# (lines 105, 176, 183). Factor level order comes from sort(), which depends on the collation locale.
# This checks, for the locale of this run and for C and en_US.UTF-8, whether each positional label lands on the intended variable.
intended_cmp <- c(AnckarRegtype_n="CPR", fh_status_n="FH", HTW_RegType_n="ARD", Politytype_n="Polity",
  RegType_lied_n="LIED", RegType_magaloni_n="AoW", RegType_RoW_n="RoW")
labels_176 <- c("CPR","FH","ARD","Polity","LIED","AoW","RoW")
intended_ind <- c(AnckarRegtype_MP_Autocracy="CPR", HTW_RegType_MP_Autocracy="ARD", Politytype_Anocracy="Polity",
  RegType_lied_EA="LIED", RegType_magaloni_EA="AoW", RegType_RoW_EA="RoW", status_fh_PF="FH")
labels_183 <- c("CPR","ARD","Polity","LIED","AoW","RoW","FH")
res <- list()
for (loc in c(Sys.getlocale("LC_COLLATE"), "C", "en_US.UTF-8")) {
  ok <- suppressWarnings(Sys.setlocale("LC_COLLATE", loc)) != ""
  if (!ok) { res[[length(res)+1]] <- data.frame(locale=loc, line=NA, all_correct=NA, note="locale not available"); next }
  l1 <- levels(as.factor(names(intended_cmp))); l2 <- levels(as.factor(names(intended_ind)))
  res[[length(res)+1]] <- data.frame(locale=loc, line=176, all_correct=all(intended_cmp[l1]==labels_176), note=paste(l1, collapse=","))
  res[[length(res)+1]] <- data.frame(locale=loc, line=183, all_correct=all(intended_ind[l2]==labels_183), note=paste(l2, collapse=","))
}
r <- do.call(rbind, res); print(r)
write.csv(r, "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/B/outputs/factor_label_locale_check.csv", row.names=FALSE)
