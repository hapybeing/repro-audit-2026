# Agent B: T1-T6 sample sizes and FC1-FC3 figure-claim checks, from objects produced by the authors' code.
args <- commandArgs(TRUE); RUN <- args[1]; OUT <- args[2]
suppressPackageStartupMessages({library(jsonlite)})
d <- readRDS(file.path(RUN, "pooled_df2.rds"))
nd <- function(x) length(unique(x))
civ <- grepl("civic", d$Sample)
rows <- list(
 c("T1","civic & sector == Private Sector", nd(d$respondentIndex[civ & d$sector %in% "Private Sector"])),
 c("T2","civic & sector == Public Sector", nd(d$respondentIndex[civ & d$sector %in% "Public Sector"])),
 c("T3","civic (all)", nd(d$respondentIndex[civ])),
 c("T4","student == Public Administration", nd(d$respondentIndex[d$student %in% "Public Administration"])),
 c("T5","student == General Student Sample", nd(d$respondentIndex[d$student %in% "General Student Sample"])),
 c("T6","student == Social Work", nd(d$respondentIndex[d$student %in% "Social Work"])),
 c("sec_all_private","all pooled_df2, sector == Private Sector", nd(d$respondentIndex[d$sector %in% "Private Sector"])),
 c("sec_all_public","all pooled_df2, sector == Public Sector", nd(d$respondentIndex[d$sector %in% "Public Sector"])),
 c("sec_civic_na_sector","civic & sector NA", nd(d$respondentIndex[civ & is.na(d$sector)])),
 c("sec_total_respondents","all pooled_df2", nd(d$respondentIndex)),
 c("sec_rows_total","rows of pooled_df2", nrow(d))
)
for (s in levels(factor(d$Sample))) rows[[length(rows)+1]] <- c(paste0("sample_label_", gsub("\n.*","",s)), gsub("\n"," ",s), nd(d$respondentIndex[d$Sample == s]))
# cross-tab student x Sample
tab <- as.data.frame(table(sample = gsub("\n.*","",d$Sample), student = addNA(d$student), sector = addNA(d$sector)))
tab <- tab[tab$Freq > 0,]; tab$respondents <- tab$Freq/16
write.csv(tab, file.path(OUT, "sample_by_student_sector_rows.csv"), row.names = FALSE)
# duplicates check: respondents with != 16 rows
rc <- table(d$respondentIndex); rows[[length(rows)+1]] <- c("sec_resp_not_16_rows","respondents whose row count != 16", sum(rc != 16))
ss <- as.data.frame(do.call(rbind, rows)); names(ss) <- c("id","definition","n")
write.csv(ss, file.path(OUT, "sample_sizes.csv"), row.names = FALSE)
print(ss)
# attribute level check
feats <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive","Since","Education")
lv <- data.frame(feature = feats, n_levels = sapply(feats, function(f) nlevels(d[[f]])),
                 n_NA = sapply(feats, function(f) sum(is.na(d[[f]]))),
                 levels = sapply(feats, function(f) paste(levels(d[[f]]), collapse = "|")))
write.csv(lv, file.path(OUT, "attribute_levels_check.csv"), row.names = FALSE); print(lv)
# FC checks
# cj() reports features by their Hmisc labels set in 03 lines 46-51; map back to variable names
lab2var <- c("Gender"="Gender","Age"="Age","Nationality"="Citizenship","Household\nComposition"="Composition",
             "Reason for\nUnemployment"="Unemployment","Supportive\nBehavior"="Supportive",
             "Duration of\nUnemployment"="Since","Education\nLevel"="Education")
mm <- read.csv(file.path(OUT, "cj_marginal_means_grouped_sector.csv"))
md <- read.csv(file.path(OUT, "cj_marginal_means_grouped_sector_mmdiff.csv"))
stopifnot(all(mm$feature %in% names(lab2var)), all(md$feature %in% names(lab2var)))
mm$feature <- unname(lab2var[mm$feature]); md$feature <- unname(lab2var[md$feature])
cat("sector groups in Figure 1 output:", paste(unique(mm$sector), collapse=" | "), " rows:", nrow(mm), "\n")
fc1f <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive")
md$excl0 <- md$lower > 0 | md$upper < 0
write.csv(md, file.path(OUT, "fc1_mmdiff_table.csv"), row.names = FALSE)
fc1 <- sum(md$excl0[md$feature %in% fc1f])
fc1_extra <- list(Since = sum(md$excl0[md$feature == "Since"]), Education = sum(md$excl0[md$feature == "Education"]))
fc1_levels <- md[md$excl0, c("feature","level","estimate","lower","upper")]
rng <- aggregate(estimate ~ sector + feature, mm, function(x) max(x) - min(x))
fc2_by <- lapply(split(rng, rng$sector), function(z) list(ranges = setNames(as.list(z$estimate), z$feature), largest = z$feature[which.max(z$estimate)]))
fc2 <- all(sapply(fc2_by, function(z) z$largest == "Composition"))
fc3 <- lapply(split(mm[mm$feature == "Citizenship" & mm$level %in% c("Syria","Germany"),], mm$sector[mm$feature == "Citizenship" & mm$level %in% c("Syria","Germany")]),
  function(z) setNames(lapply(seq_len(nrow(z)), function(i) as.list(z[i, c("estimate","std.error","lower","upper")])), z$level))
strict <- all(sapply(fc3, function(z) z$Syria$upper < 0.5 && z$Germany$lower > 0.5))
lenient <- all(sapply(fc3, function(z) z$Syria$estimate < 0.5 && z$Germany$estimate > 0.5))
res <- list(FC1 = list(count_excluding_0 = fc1, paper_claim = 0, same_conclusion = fc1 == 0, levels_excluding_0 = fc1_levels,
                       not_in_FC1_counts = fc1_extra, source = "outputs/cj_marginal_means_grouped_sector_mmdiff.csv"),
            FC2 = list(by_sector = fc2_by, same_conclusion = fc2, source = "outputs/cj_marginal_means_grouped_sector.csv"),
            FC3 = list(by_sector = fc3, strict_same_conclusion = strict, lenient_same_conclusion = lenient, source = "outputs/cj_marginal_means_grouped_sector.csv"),
            note_md_BY = unique(md$BY))
write_json(res, file.path(OUT, "figure_claims.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA)
cat(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = 6))
