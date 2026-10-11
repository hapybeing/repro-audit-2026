#!/bin/bash
# Usage: run_with_memwatch.sh <Rscript file> <tag> [rss_limit_mb=3072] [min_avail_mb=400]
# Refuses to start if MemAvailable < 3072 MB (brief: never start a heavy step with under 3 GB available).
# Samples the R process every 2 s (VmRSS, VmHWM, MemAvailable) to <tag>_mem.csv and kills R if
# VmRSS > rss_limit_mb (PREREG F1/F2 trigger: peak RSS above about 3 GB) or MemAvailable < min_avail_mb.
SCR=$1; TAG=$2; LIM=${3:-3072}; MINAV=${4:-400}
LOGD=/workspace/audit_runs/24_U9CKK6/A/logs; mkdir -p $LOGD
AV=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
echo "$(TZ=Asia/Kolkata date '+%F %T') PRESTART MemAvailable_MB=$AV" > $LOGD/${TAG}_status.txt
if [ "$AV" -lt 3072 ]; then echo "REFUSED low memory" >> $LOGD/${TAG}_status.txt; exit 3; fi
R --no-save --no-restore -f "$SCR" > $LOGD/${TAG}.Rout 2>&1 &
PID=$!
echo "PID $PID" >> $LOGD/${TAG}_status.txt
echo "time_ist,vmrss_mb,vmhwm_mb,memavail_mb" > $LOGD/${TAG}_mem.csv
while kill -0 $PID 2>/dev/null; do
  RSS=$(awk '/VmRSS/{print int($2/1024)}' /proc/$PID/status 2>/dev/null); HWM=$(awk '/VmHWM/{print int($2/1024)}' /proc/$PID/status 2>/dev/null)
  AV=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
  echo "$(TZ=Asia/Kolkata date '+%F %T'),$RSS,$HWM,$AV" >> $LOGD/${TAG}_mem.csv
  if [ -n "$RSS" ] && [ "$RSS" -gt "$LIM" ]; then echo "$(TZ=Asia/Kolkata date '+%F %T') KILLED_RSS rss=$RSS hwm=$HWM avail=$AV" >> $LOGD/${TAG}_status.txt; kill -9 $PID; fi
  if [ -n "$AV" ] && [ "$AV" -lt "$MINAV" ]; then echo "$(TZ=Asia/Kolkata date '+%F %T') KILLED_AVAIL rss=$RSS hwm=$HWM avail=$AV" >> $LOGD/${TAG}_status.txt; kill -9 $PID; fi
  sleep 2
done
wait $PID; RC=$?
echo "$(TZ=Asia/Kolkata date '+%F %T') EXIT $RC" >> $LOGD/${TAG}_status.txt
