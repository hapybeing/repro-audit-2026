#!/bin/bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for k in $(seq 1 20); do
  n=$(( $(wc -l < /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/outputs/R_a_boot.csv) - 1 ))
  echo "$(TZ=Asia/Kolkata date) chunk $k start rows=$n"
  [ $n -ge 1000 ] && break
  timeout 590 Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/04_PSHE5L/A/scripts/R_a_bootstrap.R 500
done
echo "$(TZ=Asia/Kolkata date) ALL DONE"
