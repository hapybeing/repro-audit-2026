#!/bin/bash
# Runs the authors' replication.R unchanged, working dir = folder with data.dta; saves the session for extraction
cd /workspace/audit_runs/07_JH9DBC/A/run
FIXLIB=${FIXLIB:-/workspace/audit_runs/07_JH9DBC/A/rlib} Rscript -e '.libPaths(c(Sys.getenv("FIXLIB"), "/workspace/audit_runs/07_JH9DBC/A/rlib", .libPaths())); t0<-Sys.time(); source("replication.R", echo=TRUE, max.deparse.length=Inf); cat("ELAPSED", format(Sys.time()-t0), "\n"); save.image("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A/outputs/session.RData")' > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A/outputs/replication_stdout.txt 2>&1
echo "EXIT $?" >> /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A/outputs/replication_stdout.txt
cp -f Rplots.pdf /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A/outputs/Rplots.pdf 2>/dev/null
