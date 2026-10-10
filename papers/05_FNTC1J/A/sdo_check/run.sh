#!/bin/bash
# SDO check for 05_FNTC1J (Agent A). Stage 1 rebuilds item-level data from the env-fixed authors' script (up to
# original line 1028, cheap: no mice); stage 2 loads the saved model checkpoints of the main run and of the
# pre-registered R_c run and writes ../outputs/sdo_check.json. Single-threaded, one R process at a time.
set -e
export R_LIBS_USER=/workspace/audit_runs/05_FNTC1J/A/rlib OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 LANG=C.UTF-8 LC_ALL=C.UTF-8
HERE=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/05_FNTC1J/A/sdo_check
RUN=/workspace/audit_runs/05_FNTC1J/A
W=$RUN/sdo_check; mkdir -p $W/_tables $W/_figures $W/_data $W/published
cp -n $RUN/published/raw_data_CTvsMisinfo.rds $W/published/ 2>/dev/null || true
cd $W
if [ ! -f $W/sdo_items.rds ]; then
  Rscript $HERE/stage1_items.R $RUN/MisinfoCT_HSK.r $W/sdo_items.rds > $HERE/stage1_console.txt 2>&1
fi
Rscript $HERE/sdo_check.R $W/sdo_items.rds $RUN/session_main_checkpoint_part1.RData $RUN/Rc/session_Rc_checkpoint_part1.RData \
  $RUN/orig/MisinfoCT_HSK.r $HERE/../outputs/paper_pdftotext.txt $HERE/../outputs/sdo_check.json > $HERE/sdo_check_console.txt 2>&1

python3 $HERE/make_finding.py >> $HERE/sdo_check_console.txt 2>&1
echo done
