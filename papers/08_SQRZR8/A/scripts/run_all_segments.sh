#!/bin/bash
# Runs main_rep.R in three segments in original order: 1-252, 253-331 (mediation + Figure 3), 332-449.
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/A; S=/workspace/audit_runs/08_SQRZR8/A
cd $S/run
[ -f $S/seg1.RData ] || Rscript $P/scripts/run_segment.R 1 252 none $S/seg1.RData > $P/outputs/main_rep_seg1_stdout.txt 2>&1 || exit 1
[ -f $S/seg2.RData ] || Rscript $P/scripts/run_segment.R 253 331 $S/seg1.RData $S/seg2.RData > $P/outputs/main_rep_seg2_stdout.txt 2>&1 || exit 2
[ -f $S/seg3.RData ] || Rscript $P/scripts/run_segment.R 332 449 $S/seg2.RData $S/seg3.RData > $P/outputs/main_rep_seg3_stdout.txt 2>&1 || exit 3
# (full image kept in scratch as $S/seg3.RData; copy into outputs/ removed for size, 67 MB)
Rscript $P/scripts/save_objects.R > $P/outputs/save_objects_stdout.txt 2>&1
echo ALL_DONE
