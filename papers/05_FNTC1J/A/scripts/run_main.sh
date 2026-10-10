#!/bin/bash
# Main reproduction run: env-fixed authors' script, one R session, single-threaded.
export R_LIBS_USER=/workspace/audit_runs/05_FNTC1J/A/rlib OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 LANG=C.UTF-8 LC_ALL=C.UTF-8
cd /workspace/audit_runs/05_FNTC1J/A
rm -f _tables/* _figures/* _data/* published/ds_analysis_MisinfoCT.rds Rplots.pdf
Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/scripts/run_authors.R MisinfoCT_HSK.r /workspace/audit_runs/05_FNTC1J/A/session_main.RData > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/outputs/run_main_console.txt 2>&1
echo "EXIT $?" >> /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/outputs/run_main_console.txt
