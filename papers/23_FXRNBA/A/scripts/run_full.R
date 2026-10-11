# Full run (PREREG section 2 step 2): authors' script unchanged, then save target objects.
source("wildfire_data_analysis.R", echo = TRUE, max.deparse.length = Inf)
OUT <- Sys.getenv("OUTDIR")
saveRDS(list(iv3 = iv3, r3 = r3, d3_F = d3$F, d3_pr2 = d3$pr2, fs3_coef = coef(d3$fs), fs3_vcov = vcov(d3$fs),
             fs3_se = fixest::se(d3$fs), fs3_p = fixest::pvalue(d3$fs), fs3_nobs = nobs(d3$fs),
             iv3_summary_coef = summary(iv3)$coefficients,
             N_main = N_main, N_copoll = N_copoll, r1 = r1, r2 = r2, r4 = r4,
             d1F = d1$F, d2F = d2$F, d4F = d4$F, d1pr2 = d1$pr2, d2pr2 = d2$pr2, d4pr2 = d4$pr2,
             fixest_version = as.character(packageVersion("fixest"))),
        file.path(OUT, "table1_objects.rds"))
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_full.txt"))
cat("SAVED_FULL_OK\n")
