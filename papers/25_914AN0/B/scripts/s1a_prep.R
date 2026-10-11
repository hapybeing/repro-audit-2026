# Stage S1a (PREREG section 2): setup + functions, run2_main.R lines 55 and 58 verbatim, then 98-107 (Table A1.1). Saves X_s etc.
RUNDIR <- "/workspace/audit_runs/25_914AN0/B"; OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/scripts/run_lines.R")
setwd(file.path(RUNDIR, "Replication_IO"))
memlog("start S1a")
source("code/run1_setup.R")
source("code/functions.R")
run_lines(55, 55); memlog("after line 55")
run_lines(58, 58); memlog("after line 58")
cat("nrow(X) =", nrow(X), " nrow(X_s) =", nrow(X_s), "\n")
run_lines(98, 107)
saveRDS(list(X_s=X_s, yvarz=yvarz, ylabz=ylabz, ylabz_short=ylabz_short), file.path(RUNDIR, "inter/s1a.rds"))
cat("S1a saved\n"); memlog("end S1a")
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_s1a.txt"))
