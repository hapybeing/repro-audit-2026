# Subset run (PREREG section 2 step 3): authors' lines 1-668 unchanged, then save target objects.
# Run with working directory = RUNDIR, LC_ALL=C.UTF-8.
OUT <- Sys.getenv("OUTDIR")
src <- readLines("wildfire_data_analysis.R", warn = FALSE)[1:668]
writeLines(src, "part_1_668.R")
source("part_1_668.R", echo = TRUE, max.deparse.length = Inf)
OUT <- Sys.getenv("OUTDIR")
saveRDS(list(iv3 = iv3, r3 = r3, d3_F = d3$F, d3_pr2 = d3$pr2, fs3_coef = coef(d3$fs), fs3_vcov = vcov(d3$fs),
             fs3_se = fixest::se(d3$fs), fs3_p = fixest::pvalue(d3$fs), fs3_nobs = nobs(d3$fs),
             iv3_summary_coef = summary(iv3)$coefficients,
             N_main = N_main, N_copoll = N_copoll, r1 = r1, r2 = r2, r4 = r4,
             d1F = d1$F, d2F = d2$F, d4F = d4$F, d1pr2 = d1$pr2, d2pr2 = d2$pr2, d4pr2 = d4$pr2,
             fixest_version = as.character(packageVersion("fixest"))),
        file.path(OUT, "table1_objects_part.rds"))
saveRDS(seattle_main, file.path(Sys.getenv("RUNDIR_SAVE"), "seattle_main.rds"))
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_part.txt"))
cat("SAVED_PART_OK\n")
