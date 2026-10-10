# Driver for pre-registered Step A (PREREG.md section 2). Runs Appendix_plus.R lines 892-958 unchanged
# in a fresh session after adding the load("all_merged.RData") that the script has commented out at l. 18.
RUNDIR <- "/workspace/audit_runs/19_KH0SQ2/A"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/A/outputs"
setwd(file.path(RUNDIR, "deposit")); load("all_merged.RData")
src <- readLines("Appendix_plus.R")
cat("Lines 892-958 first/last:\n"); cat(src[892], "\n", src[958], "\n")
eval(parse(text = src[892:958]))
saveRDS(list(res1=res1,res2=res2,res3=res3,resg1=resg1,res4=res4,res5=res5,res6=res6,resg2=resg2), file.path(OUT, "S1_S10_models.rds"))
for (nm in c("res1","res2","res3","resg1","res4","res5","res6","resg2")) { cat("\n=====", nm, "\n"); print(summary(get(nm))) }
cat("\ntable(all$country):\n"); print(table(all$country))
