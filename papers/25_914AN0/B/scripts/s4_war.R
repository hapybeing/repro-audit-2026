# Stage S4: fresh session; setup; run2_main.R lines 1310-1388 verbatim; save mod_out; then 1389-1405 (Table A6.17).
RUNDIR <- "/workspace/audit_runs/25_914AN0/B"; OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/scripts/run_lines.R")
setwd(file.path(RUNDIR, "Replication_IO"))
source("code/run1_setup.R")
run_lines(1310, 1388)
# line 1312 rm(list=ls()) clears helpers and OUT, so re-create them
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/scripts/run_lines.R")
saveRDS(mod_out, file.path(OUT, "war_mod_out.rds")); data.table::fwrite(mod_out, file.path(OUT, "war_mod_out.csv"))
print(mod_out)
print(summary(mod[[1]]))
run_lines(1389, 1405)
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_s4.txt"))
cat("S4 done\n")
