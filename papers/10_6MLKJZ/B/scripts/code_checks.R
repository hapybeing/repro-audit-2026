# Agent B: code-review checks (join duplication at 03 lines ~121-122; civic sample composition behind T3).
args <- commandArgs(TRUE); RUN <- args[1]; OUT <- args[2]; SURV <- args[3]
suppressPackageStartupMessages({library(cregg); library(data.table); library(jsonlite)})
d <- readRDS(file.path(RUN, "pooled_df2.rds"))
out <- list()
key <- paste(d$respondentIndex, d$task, d$profile)
rc <- table(d$respondentIndex)
out$rows_total <- nrow(d); out$distinct_resp_task_profile <- length(unique(key))
out$duplicated_rows <- sum(duplicated(key))
out$respondents_with_32_rows <- sum(rc == 32); out$respondents_with_16_rows <- sum(rc == 16)
out$rows_per_resp_by_sector <- lapply(split(as.integer(rc[as.character(d$respondentIndex)]), addNA(d$sector)), function(z) as.list(table(z)))
dd <- d[!duplicated(key), ]
out$dedup_rows <- nrow(dd)
lab2var <- c("Gender"="Gender","Age"="Age","Nationality"="Citizenship","Household\nComposition"="Composition","Reason for\nUnemployment"="Unemployment","Supportive\nBehavior"="Supportive","Duration of\nUnemployment"="Since","Education\nLevel"="Education")
fixf <- function(x){x<-as.data.frame(x); x$feature<-as.character(x$feature); m<-c(lab2var,setNames(unname(lab2var),unname(lab2var))); x$feature<-unname(m[x$feature]); x}
f8 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education
mm <- fixf(cj(dd, f8, estimate = "mm", by = ~ sector, id = ~ respondentIndex))
md <- fixf(cj(dd, f8, estimate = "mm_diff", by = ~ sector, id = ~ respondentIndex))
write.csv(mm, file.path(OUT, "code_check_dedup_fig1_mm.csv"), row.names = FALSE)
write.csv(md, file.path(OUT, "code_check_dedup_fig2_mmdiff.csv"), row.names = FALSE)
orig <- fixf(read.csv(file.path(OUT, "cj_marginal_means_grouped_sector.csv")))
mg <- merge(orig[, c("sector","feature","level","estimate","std.error")], mm[, c("sector","feature","level","estimate","std.error")], by = c("sector","feature","level"), suffixes = c("_authors","_dedup"))
out$fig1_max_abs_estimate_change_dedup <- max(abs(mg$estimate_authors - mg$estimate_dedup))
out$fig1_max_rel_se_change_dedup <- max(abs(mg$std.error_dedup / mg$std.error_authors - 1))
md$excl0 <- md$lower > 0 | md$upper < 0
out$fc1_count_dedup <- sum(md$excl0 & md$feature %in% c("Gender","Age","Citizenship","Composition","Unemployment","Supportive"))
out$excl0_levels_dedup <- paste(md$feature, md$level)[md$excl0]
e <- mm[mm$sector == "Private Sector" & mm$feature == "Composition" & mm$level == "2 Adults, 3 Childr.", ]
out$E1_dedup <- list(estimate = e$estimate, lower = e$lower, upper = e$upper)
# civic composition behind T3
civ <- unique(d[grepl("civic", d$Sample), c("respondentIndex","sector")])
s <- fread(SURV, data.table = FALSE, select = c("v9","sector","student","v184_ger"))
out$survey_rows <- nrow(s); out$survey_distinct_v9 <- length(unique(s$v9))
civ$in_survey <- civ$respondentIndex %in% s$v9
sm <- s[match(civ$respondentIndex, s$v9), ]
out$civic_respondents <- nrow(civ)
out$civic_not_in_survey_data <- sum(!civ$in_survey)
out$civic_in_survey_sector_na_or_empty <- sum(civ$in_survey & (is.na(sm$sector) | sm$sector == ""))
out$civic_sector_values_in_survey <- as.list(table(sm$sector, useNA = "ifany"))
out$civic_v184_ger_values <- as.list(table(sm$v184_ger, useNA = "ifany"))
out$civic_by_sector_and_v184_ger <- as.data.frame(table(sector = sm$sector, v184_ger = sm$v184_ger, useNA = "ifany"))
write_json(out, file.path(OUT, "code_checks.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA)
cat(toJSON(out, auto_unbox = TRUE, pretty = TRUE, digits = 6))
