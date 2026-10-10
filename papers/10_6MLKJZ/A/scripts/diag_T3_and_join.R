# Diagnostics (not pre-registered targets): (1) who are the civic respondents with sector NA (T3 context);
# (2) code-review evidence for the many-to-many left_join at 03_data_prep_and_merge.R line 133 (file line ~300).
suppressMessages({library(cregg); library(jsonlite); library(data.table)})
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]
d <- readRDS(file.path(rundir, "pooled_df2.rds"))
C2 <- fread(file.path(rundir, "data/survey_data/survey_data.csv"), data.table = FALSE)
civ <- unique(d$respondentIndex[grepl("civic", d$Sample)])
na_sec <- unique(d$respondentIndex[grepl("civic", d$Sample) & is.na(d$sector)])
r1 <- list(
  survey_data_rows = nrow(C2), survey_data_unique_v9 = length(unique(C2$v9)),
  civic_resp_in_pooled = length(civ), civic_resp_found_in_survey_data = sum(civ %in% C2$v9),
  civic_sectorNA = length(na_sec), civic_sectorNA_not_in_survey_data = sum(!(na_sec %in% C2$v9)),
  civic_sectorNA_in_survey_data = sum(na_sec %in% C2$v9),
  civic_sectorNA_in_survey_v184_ger = as.list(table(C2$v184_ger[C2$v9 %in% na_sec], useNA = "ifany")),
  civic_with_sector_v184_ger = as.list(table(C2$v184_ger[C2$v9 %in% setdiff(civ, na_sec)], useNA = "ifany")),
  survey_data_sector_table = as.list(table(C2$sector, useNA = "ifany")),
  survey_data_student_table = as.list(table(C2$student, useNA = "ifany")))
# join duplication
rp <- table(d$respondentIndex)
r2 <- list(rows_pooled_df2 = nrow(d), respondents = length(rp), rows_per_resp = as.list(table(rp)),
  sector_resp_with_32_rows = sum(rp[unique(d$respondentIndex[!is.na(d$sector)])] == 32),
  sector_resp_with_16_rows = sum(rp[unique(d$respondentIndex[!is.na(d$sector)])] == 16))
dd <- d[, setdiff(names(d), "ebal")]; dd <- dd[!duplicated(dd), ]
r2$rows_after_dedup <- nrow(dd)
f1 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Citizenship + Since + Education
f2 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education
a <- read.csv(file.path(outdir, "cj_marginal_means_grouped_sector.csv")); b <- as.data.frame(cj(dd, f1, estimate = "mm", by = ~ sector, id = ~ respondentIndex))
m <- merge(a[, c("sector","level","estimate","std.error")], b[, c("sector","level","estimate","std.error")], by = c("sector","level"), suffixes = c("_as_run","_dedup"))
r2$fig1_max_abs_diff_estimate <- max(abs(m$estimate_as_run - m$estimate_dedup)); r2$fig1_max_abs_diff_se <- max(abs(m$std.error_as_run - m$std.error_dedup))
a2 <- read.csv(file.path(outdir, "cj_marginal_means_grouped_sector_mmdiff.csv")); b2 <- as.data.frame(cj(dd, f2, estimate = "mm_diff", by = ~ sector, id = ~ respondentIndex))
m2 <- merge(a2[, c("level","estimate","lower","upper")], b2[, c("level","estimate","lower","upper")], by = "level", suffixes = c("_as_run","_dedup"))
r2$fig2_max_abs_diff_estimate <- max(abs(m2$estimate_as_run - m2$estimate_dedup))
r2$fig2_dedup_levels_CI_excl0 <- m2$level[m2$lower_dedup > 0 | m2$upper_dedup < 0]
write.csv(m, file.path(outdir, "code_check_join_dedup_fig1.csv"), row.names = FALSE)
# supplementary, NOT pre-registered: R_c omnibus test on de-duplicated rows (unclustered, as in R_c) and clustered
dds <- dd[dd$sector %in% c("Private Sector", "Public Sector"), ]; dds$sector <- droplevels(dds$sector)
an1 <- cregg::cj_anova(dds, f2, by = ~ sector)
an2 <- cregg::cj_anova(dds, f2, id = ~ respondentIndex, by = ~ sector)
capture.output(print(an1), print(an2), file = file.path(outdir, "supp_R_c_anova_dedup.txt"))
r3 <- list(note = "supplementary, not pre-registered", rows = nrow(dds),
  dedup_unclustered_F = an1$F[2], dedup_unclustered_p = an1[["Pr(>F)"]][2],
  dedup_clustered_stat = if (!is.null(an2$F)) an2$F[2] else NA, dedup_clustered_p = an2[["Pr(>F)"]][2])
res <- list(T3_context = r1, join_duplication = r2, supp_R_c_anova_dedup = r3)
write(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = NA), file.path(outdir, "diag_T3_and_join.json"))
cat(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = 8))
