# Descriptive facts about the public OSF extract relevant to code review (no model fitting).
d <- read.csv("/workspace/audit_runs/04_PSHE5L/A/raw/Rural_Populism_Dataset.csv")
out <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/outputs/data_facts.txt"
sink(out)
cat("nrow", nrow(d), "ncol", ncol(d), "\n"); print(names(d))
cat("any NA:", anyNA(d), "\n")
for (v in setdiff(names(d), "WTS")) { cat("\n==", v, "\n"); print(table(d[[v]], useNA = "ifany")) }
cat("\nWTS summary\n"); print(summary(d$WTS)); cat("WTS == 0:", sum(d$WTS == 0), "\n")
cat("Q15==8:", sum(d$Q15 == 8), " XQ14 in 4/5:", sum(d$XQ14 %in% 4:5), " either:", sum(d$Q15 == 8 | d$XQ14 %in% 4:5), "\n")
cat("WTS==0 & Q15==8:", sum(d$WTS == 0 & d$Q15 == 8), "\n")
cat("rows minus Q15==8:", nrow(d) - sum(d$Q15 == 8), "\n")
cat("rows minus XQ14 4/5:", nrow(d) - sum(d$XQ14 %in% 4:5), "\n")
# Any item with code outside 1-7 among model indicators
items <- c(grep("^Q23", names(d), value = TRUE), "Q25B", "Q25C", "Q25D")
for (v in items) cat(v, "range", range(d[[v]]), "\n")
sink()
