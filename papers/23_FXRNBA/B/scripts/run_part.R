# Sources the authors' wildfire_data_analysis.R lines 1-668 unchanged (Table 1 block) and saves Table 1 objects.
# Run with working directory = /workspace/audit_runs/23_FXRNBA/B/run, LC_ALL=C.UTF-8, R_LIBS_USER set to the per-run rlib.
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B/outputs"
src <- readLines("wildfire_data_analysis.R")
writeLines(src[1:668], "/workspace/audit_runs/23_FXRNBA/B/part_1_668.R")
source("/workspace/audit_runs/23_FXRNBA/B/part_1_668.R", echo = TRUE, max.deparse.length = Inf)
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B/outputs"
saveRDS(list(iv3_est = iv3$est, iv3_vcov = iv3$vcov, r3 = r3, d3_F = d3$F, d3_pr2 = d3$pr2,
             fs3_coef = coef(d3$fs), fs3_vcov = vcov(d3$fs), fs3_nobs = nobs(d3$fs),
             fs3_glm_coef = coef(iv3$fitX.LZ),
             iv3_summary_coef = tryCatch(summary(iv3)$coefficients, error = function(e) conditionMessage(e)),
             N_main = N_main, N_copoll = N_copoll, r1 = r1, r2 = r2, r4 = r4,
             d1F = d1$F, d2F = d2$F, d4F = d4$F, d1pr2 = d1$pr2, d2pr2 = d2$pr2, d4pr2 = d4$pr2,
             fixest_version = as.character(packageVersion("fixest")),
             ivtools_version = as.character(packageVersion("ivtools"))),
        file.path(OUT, "table1_objects_part.rds"))
saveRDS(seattle_main, "/workspace/audit_runs/23_FXRNBA/B/seattle_main.rds")
file.copy("table_1_main_results.html", file.path(OUT, "table_1_main_results_part.html"), overwrite = TRUE)
cat("PART RUN SAVED\n")
