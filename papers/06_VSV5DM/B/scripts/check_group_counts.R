# Code-review check: compare hard-coded group sizes in the Rmd with counts in the deposited data.
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/06_VSV5DM/B/outputs"
load("/workspace/audit_runs/06_VSV5DM/B/run/StateLeg_COVIDFacebookActivity.Rdata")
sink(file.path(OUT, "group_counts_check.txt"))
cat("table(by_leg$poc):\n"); print(table(by_leg$poc, useNA = "ifany"))
cat("\ntable(by_leg$rpg):\n"); print(table(by_leg$rpg, useNA = "ifany"))
b2 <- subset(by_leg, rpg != "Independent White Men" & rpg != "Republican Men of Color" & rpg != "Republican Women of Color")
cat("\nnrow(by_leg2) =", nrow(b2), "\n"); print(table(b2$rpg))
vars <- c("covid","rpg","senator","age_rescaled","leader_or_chair","X.voteTrump2016_resclaed","Last.Vote.Share","Bill.Sponsor.2019_rescaled","COVID.Rate.per.100.000_rescaled","perc_white","Population.Density..Per.sq.mile._rescaled","College_Educated_rescaled","median_income_rescaled","State","general_rescaled")
cat("\nMissing values per model variable in by_leg2:\n"); print(sapply(b2[vars], function(x) sum(is.na(x))))
cat("complete cases:", sum(complete.cases(b2[vars])), "\n")
for (v in c("race_gender","race_ethnicity","rg","race")) if (v %in% names(by_leg)) {cat("\n", v, "\n"); print(table(by_leg[[v]]))}
cat("\nclass(by_leg$race_gender):", class(by_leg$race_gender), "\nlevels in group_by order:", paste(levels(factor(by_leg$race_gender)), collapse = " / "), "\n")
sink()
