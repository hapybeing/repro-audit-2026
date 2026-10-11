#!/bin/bash
export R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/A/rlib
cd /workspace/audit_runs/21_LEFTNE/A/data
s=$(date -u +%T); Rscript -e 'source("01- Replication_Text.R", echo=TRUE, max.deparse.length=Inf); cat("\n##SESSIONINFO\n"); print(sessionInfo())' > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/text_log.txt 2>&1; echo "text rc=$? start $s end $(date -u +%T)" > /workspace/audit_runs/21_LEFTNE/A/run_authors.status
mv Rplots.pdf /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/text_figures.pdf 2>/dev/null
s=$(date -u +%T); Rscript -e 'source("02- Replication_Appendix.R", echo=TRUE, max.deparse.length=Inf); cat("\n##SESSIONINFO\n"); print(sessionInfo())' > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/appendix_log.txt 2>&1; echo "appendix rc=$? start $s end $(date -u +%T)" >> /workspace/audit_runs/21_LEFTNE/A/run_authors.status
mv Rplots.pdf /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/appendix_figures.pdf 2>/dev/null
echo ALLDONE >> /workspace/audit_runs/21_LEFTNE/A/run_authors.status
