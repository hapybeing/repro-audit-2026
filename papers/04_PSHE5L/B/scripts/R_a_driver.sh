#!/bin/bash
# Runs R_a in resumable chunks of 150 replicates (each call capped at 590 s), single-threaded.
export R_LIBS_USER=/workspace/audit_runs/04_PSHE5L/B/rlib OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
OUT=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/B/outputs/R_a_boot.csv
for i in $(seq 1 20); do
  n=$( [ -f $OUT ] && tail -n +2 $OUT | wc -l || echo 0 )
  [ "$n" -ge 1000 ] && break
  timeout 590 Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/B/scripts/R_a_bootstrap_B.R $OUT 150
done
echo ALLDONE $(date)
