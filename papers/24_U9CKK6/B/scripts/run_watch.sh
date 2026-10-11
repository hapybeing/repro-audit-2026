#!/bin/bash
# Usage: run_watch.sh <label> <Rscript file> ; runs Rscript in RUNDIR under /usr/bin/time -v (if present), samples RSS and
# MemAvailable every 5 s to logs/<label>_mem.tsv, kills R if RSS > 3000 MB (PREREG F1/F2 trigger) or MemAvailable < 400 MB.
RUN=/workspace/audit_runs/24_U9CKK6/B/run; L=/workspace/audit_runs/24_U9CKK6/B/logs; label=$1; script=$2; shift 2
export R_LIBS_USER=/workspace/audit_runs/24_U9CKK6/B/rlib
cd $RUN
avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo); echo "START $(date -u +%FT%TZ) MemAvailable_MB=$avail" > $L/${label}_mem.tsv
TIMEBIN=""; [ -x /usr/bin/time ] && TIMEBIN="/usr/bin/time -v"
$TIMEBIN Rscript "$script" "$@" > $L/${label}.out 2>&1 &
pid=$!; peak=0
while kill -0 $pid 2>/dev/null; do
  rp=$(pgrep -P $pid -f "R" | head -1); [ -z "$rp" ] && rp=$pid
  rss=$(ps -o rss= -p $(pgrep -f "exec/R.*$(basename $script)" | head -1) 2>/dev/null | awk '{print int($1/1024)}'); rss=${rss:-0}
  av=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  [ "$rss" -gt "$peak" ] && peak=$rss
  echo -e "$(date -u +%T)\t$rss\t$av" >> $L/${label}_mem.tsv
  if [ "$rss" -gt 3000 ] || [ "$av" -lt 400 ]; then echo "KILL rss=$rss avail=$av $(date -u +%T)" >> $L/${label}_mem.tsv; pkill -f "exec/R.*$(basename $script)"; fi
  sleep 5
done
wait $pid; rc=$?
echo "END $(date -u +%FT%TZ) rc=$rc peak_rss_MB=$peak" >> $L/${label}_mem.tsv
