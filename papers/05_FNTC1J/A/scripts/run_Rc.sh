#!/bin/bash
# R_c: whole R_c copy of the script, from the top, one session, authors' set.seed(2000). Separate run dir.
export R_LIBS_USER=/workspace/audit_runs/05_FNTC1J/A/rlib OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 LANG=C.UTF-8 LC_ALL=C.UTF-8
cd /workspace/audit_runs/05_FNTC1J/A/Rc
Rscript /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/scripts/run_authors.R MisinfoCT_HSK_Rc.r /workspace/audit_runs/05_FNTC1J/A/Rc/session_Rc.RData > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/outputs/run_Rc_console.txt 2>&1
echo "EXIT $?" >> /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/outputs/run_Rc_console.txt
