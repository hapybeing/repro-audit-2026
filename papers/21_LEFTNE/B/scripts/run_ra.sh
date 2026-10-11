#!/bin/bash
# Runs R_a (study1 then study2), resuming in time slices until each finishes (exit 3 = slice ended, resume).
O=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/B
for s in Ra1 Ra2; do
  for i in $(seq 1 12); do
    while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 1500 ]; do echo "waiting for memory" >> $O/outputs/Ra_run_log.txt; sleep 30; done
    Rscript $O/scripts/robustness.R $s >> $O/outputs/Ra_run_log.txt 2>&1; st=$?
    [ $st -eq 3 ] || break
  done
done
echo "RA_DONE" >> $O/outputs/Ra_run_log.txt
