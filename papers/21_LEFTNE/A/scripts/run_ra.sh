#!/bin/bash
export R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/A/rlib
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A
cd /workspace/audit_runs/21_LEFTNE/A/data
for st in Ra_study1 Ra_study2 Rb Rc; do
  if [ "$st" = Ra_study1 ] || [ "$st" = Ra_study2 ]; then s=${st#Ra_}; f=$P/outputs/Ra_summary_$s.csv; else f=$P/outputs/${st}_summary.csv; fi
  while [ ! -f "$f" ]; do
    while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 1500 ]; do sleep 20; done
    echo "$(date -u +%T) start $st" >> /workspace/audit_runs/21_LEFTNE/A/robust.status
    Rscript $P/scripts/robustness.R $st >> $P/outputs/robustness_${st}_log.txt 2>&1 || { echo "$(date -u +%T) $st rc=$?" >> /workspace/audit_runs/21_LEFTNE/A/robust.status; break; }
  done
  echo "$(date -u +%T) end $st" >> /workspace/audit_runs/21_LEFTNE/A/robust.status
done
echo ALLDONE >> /workspace/audit_runs/21_LEFTNE/A/robust.status
