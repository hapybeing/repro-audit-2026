#!/bin/bash
# usage: logit.sh "text"  -> appends timestamped IST entry
echo "- $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST'): $*" >> /workspace/audit_runs/21_LEFTNE/A/log_entries.md
