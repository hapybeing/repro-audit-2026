# Stage S1b: fresh session; setup + functions; load s1a.rds; run2_main.R lines 62-73 verbatim; save mermods; then 76-90 and 110-157.
RUNDIR <- "/workspace/audit_runs/25_914AN0/B"; OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/scripts/run_lines.R")
setwd(file.path(RUNDIR, "Replication_IO"))
memlog("start S1b")
source("code/run1_setup.R")
source("code/functions.R")
s <- readRDS(file.path(RUNDIR, "inter/s1a.rds")); X_s <- s$X_s; yvarz <- s$yvarz; ylabz <- s$ylabz; ylabz_short <- s$ylabz_short; rm(s)
# Staging correction (run 2): readRDS returns a data.table with no column over-allocation (truelength 0). In the authors' one-session route
# X_s comes straight from line 58 and is over-allocated. Restore that state so the by-reference := inside ensemble_modz behaves as in one session.
data.table::setalloccol(X_s); cat("truelength(X_s) =", data.table::truelength(X_s), "\n")
t0 <- Sys.time()
run_lines(62, 73)
cat("ensemble time:", format(Sys.time()-t0), "\n")
saveRDS(mermods, file.path(OUT, "mermods.rds")); data.table::fwrite(mermods, file.path(OUT, "mermods.csv"))
cat("mermods saved, rows:", nrow(mermods), "\n"); memlog("after models")
run_lines(76, 90)
run_lines(110, 157)
writeLines(capture.output(sessionInfo()), file.path(OUT, "sessionInfo_s1b.txt"))
cat("S1b done\n")
