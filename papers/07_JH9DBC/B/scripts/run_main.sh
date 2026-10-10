#!/bin/bash
# Runs the authors' replication.R unchanged, top to bottom, in one R session (PREREG section 2 step 5).
set -u
RUN=/workspace/audit_runs/07_JH9DBC/B/run
OUT=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/B/outputs
mkdir -p $RUN; cp /workspace/audit_runs/07_JH9DBC/B/dl/replication.R /workspace/audit_runs/07_JH9DBC/B/dl/data.dta $RUN/
cd $RUN
export R_LIBS_USER=/workspace/audit_runs/07_JH9DBC/B/rlib
Rscript -e 'source("replication.R", echo=TRUE, max.deparse.length=Inf); save.image("session.RData")' > $OUT/replication_stdout.txt 2> $OUT/replication_stderr.txt
echo "EXIT $?" >> $OUT/replication_stdout.txt
cp -f session.RData $OUT/session.RData 2>/dev/null; cp -f Rplots.pdf $OUT/Rplots.pdf 2>/dev/null
