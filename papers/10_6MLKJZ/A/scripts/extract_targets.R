# Computes T1-T6 and secondary sample-size context from pooled_df2 (saved by run_authors.R), and the
# attribute level check required by PREREG section 2. Usage: Rscript extract_targets.R RUNDIR OUTDIR
suppressMessages(library(dplyr))
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]
d <- readRDS(file.path(rundir, "pooled_df2.rds"))
nd <- function(x) length(unique(x))
civ <- grepl("civic", d$Sample)
rows <- list(
  c("T1", "civic & sector == Private Sector", nd(d$respondentIndex[civ & d$sector %in% "Private Sector"])),
  c("T2", "civic & sector == Public Sector",  nd(d$respondentIndex[civ & d$sector %in% "Public Sector"])),
  c("T3", "civic (all)",                      nd(d$respondentIndex[civ])),
  c("T4", "student == Public Administration", nd(d$respondentIndex[d$student %in% "Public Administration"])),
  c("T5", "student == General Student Sample",nd(d$respondentIndex[d$student %in% "General Student Sample"])),
  c("T6", "student == Social Work",           nd(d$respondentIndex[d$student %in% "Social Work"])),
  c("S_all_private", "all pooled_df2, sector == Private Sector (what by=~sector groups)", nd(d$respondentIndex[d$sector %in% "Private Sector"])),
  c("S_all_public",  "all pooled_df2, sector == Public Sector", nd(d$respondentIndex[d$sector %in% "Public Sector"])),
  c("S_civic_sector_NA", "civic & sector NA", nd(d$respondentIndex[civ & is.na(d$sector)])),
  c("S_total_respondents", "all pooled_df2", nd(d$respondentIndex)),
  c("S_total_rows", "rows of pooled_df2", nrow(d))
)
for (s in levels(d$Sample)) rows[[length(rows)+1]] <- c(paste0("S_samplelabel_", sub("\n.*", "", s)), paste("Sample label:", gsub("\n", " ", s)), nd(d$respondentIndex[d$Sample == s]))
for (s in levels(d$Sample)) for (st in c("Public Administration", "General Student Sample", "Social Work", NA)) {
  n <- nd(d$respondentIndex[d$Sample == s & (if (is.na(st)) is.na(d$student) else d$student %in% st)])
  if (n > 0) rows[[length(rows)+1]] <- c(paste0("S_cross_", sub("\n.*", "", s), "_", ifelse(is.na(st), "NA", gsub(" ", "", st))), paste("Sample x student", gsub("\n"," ",s), st), n)
}
md <- readRDS(file.path(rundir, "match_data.rds"))
rows[[length(rows)+1]] <- c("S_tableD_rows_D0", "table(match_data$D) at 03 line 94, D=0 (rows of task==1)", sum(md$D == 0))
rows[[length(rows)+1]] <- c("S_tableD_rows_D1", "table(match_data$D) at 03 line 94, D=1 (rows of task==1)", sum(md$D == 1))
rows[[length(rows)+1]] <- c("S_tableD_resp_D0", "distinct respondents in match_data with D=0", nd(md$respondentIndex[md$D == 0]))
rows[[length(rows)+1]] <- c("S_tableD_resp_D1", "distinct respondents in match_data with D=1", nd(md$respondentIndex[md$D == 1]))
rows[[length(rows)+1]] <- c("S_rows_per_resp_civic_min", "min rows per civic respondent", min(table(d$respondentIndex[civ])))
rows[[length(rows)+1]] <- c("S_rows_per_resp_civic_max", "max rows per civic respondent", max(table(d$respondentIndex[civ])))
out <- as.data.frame(do.call(rbind, rows), stringsAsFactors = FALSE); names(out) <- c("id", "definition", "value")
write.csv(out, file.path(outdir, "sample_sizes.csv"), row.names = FALSE)
print(out)
# attribute level check
feats <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive","Since","Education")
lv <- do.call(rbind, lapply(feats, function(f) data.frame(feature = f, n_levels = nlevels(d[[f]]),
        levels = paste(levels(d[[f]]), collapse = " | "), n_NA_rows = sum(is.na(d[[f]])))))
write.csv(lv, file.path(outdir, "attribute_levels_check.csv"), row.names = FALSE); print(lv)
cat("selected NA rows:", sum(is.na(d$selected)), " table(selected):", capture.output(print(table(d$selected))), "\n")
