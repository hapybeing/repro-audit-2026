# Code-review evidence for Appendix line 87 (Table A3, Study 2 demographics, partisanship tabulated from Study 1 'df').
# Writes outputs/code_review_check.json. wd = RUNDIR/data.
suppressPackageStartupMessages({library(dplyr); library(janitor); library(jsonlite)})
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs"
df <- readRDS("Qualtrics_2019.RDS"); df <- df %>% filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa")
d2 <- readRDS("NORC.RDS"); d2 <- d2 %>% filter(TREATMENT == "Trump" | TREATMENT == "Clinton" | TREATMENT == "Alexa")
t1 <- df %>% tabyl(PARTISANSHIP, sort = TRUE) %>% adorn_pct_formatting()
res <- list(study1_nrow_3arm = nrow(df), study2_nrow_3arm = nrow(d2),
  line87_output_df_PARTISANSHIP = t1,
  norc_has_PARTISANSHIP = "PARTISANSHIP" %in% names(d2),
  norc_PARTISANSHIP_tabyl = d2 %>% tabyl(PARTISANSHIP, sort = TRUE) %>% adorn_pct_formatting(),
  norc_columns_matching_part = grep("part", names(d2), ignore.case = TRUE, value = TRUE),
  norc_party_table = { t <- table(d2$party, useNA = "ifany"); names(t)[is.na(names(t))] <- "NA"; as.list(t) },
  norc_party_share_1 = mean(d2$party == 1, na.rm = TRUE))
write_json(res, file.path(OUT, "code_review_check.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA); print(toJSON(res, auto_unbox = TRUE, pretty = TRUE))
