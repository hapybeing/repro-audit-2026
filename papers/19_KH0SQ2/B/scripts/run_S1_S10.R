# Pre-registered driver (PREREG section 2, Step A). Adds only load("all_merged.RData"); lines 892-958 of Appendix_plus.R unchanged.
RUNDIR <- "/workspace/audit_runs/19_KH0SQ2/B"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/B/outputs"
setwd(file.path(RUNDIR, "deposit")); load("all_merged.RData")
src <- readLines("Appendix_plus.R"); eval(parse(text = src[892:958]))
saveRDS(list(res1=res1,res2=res2,res3=res3,resg1=resg1,res4=res4,res5=res5,res6=res6,resg2=resg2), file.path(OUT, "S1_S10_models.rds"))
saveRDS(list(uk2=uk2, fr2=fr2), file.path(RUNDIR, "est_samples.rds"))
cat("country counts in all:\n"); print(table(all$country))
cat("Treatment NA in all:", sum(is.na(all$Treatment)), "\n")
cat("done\n")
