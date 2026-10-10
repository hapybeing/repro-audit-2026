# Code-observation evidence for line 177 ("\u00b445"): share of programs covered by the deposited filter
# versus the same filter with "45". The paper (PDF p. 10) says the selected main parties together
# account for more than 50% of programs. Args: RUNDIR OUTDIR
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]
load(file.path(rundir, "session_after_script.RData"))
np <- as.character(bd_doxa_programas$numpartido)
f_dep <- c("15", "13", "50", "22", "25", "\u00b445", "12", "11")
f_45 <- c("15", "13", "50", "22", "25", "45", "12", "11")
res <- data.frame(
  filter = c("deposited (\u00b445)", "with 45"),
  rows_selected = c(sum(np %in% f_dep), sum(np %in% f_45)),
  rows_total = nrow(bd_doxa_programas),
  rows_numpartido_nonNA = sum(!is.na(np)),
  rows_matching_literal_entry_with_accent = c(sum(np == "\u00b445", na.rm = TRUE), NA)
)
res$share_of_all_rows <- res$rows_selected / res$rows_total
res$share_of_nonNA_numpartido <- res$rows_selected / res$rows_numpartido_nonNA
write.csv(res, file.path(outdir, "party_share_check.csv"), row.names = FALSE)
print(res)
