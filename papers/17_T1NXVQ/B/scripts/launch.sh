#!/bin/bash
# usage: launch.sh <name> <Rscript file> ; env passed through. Waits for >= 3072 MB available, logs it, runs one heavy R process.
name=$1; scr=$2
while true; do av=$(free -m | awk '/Mem:/{print $7}'); [ "$av" -ge 3072 ] && break; sleep 15; done
echo "$(date -u +%FT%TZ) START $name available_MB=$av" >> /workspace/audit_runs/17_T1NXVQ/B/heavy_launch.log
R_LIBS_USER=/workspace/audit_runs/17_T1NXVQ/B/rlib RETICULATE_PYTHON=/workspace/audit_runs/17_T1NXVQ/B/venv/bin/python3 Rscript $scr > /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B/outputs/run_$name.log 2>&1
echo "$(date -u +%FT%TZ) END $name exit=$? " >> /workspace/audit_runs/17_T1NXVQ/B/heavy_launch.log
