#!/bin/bash
# Usage: run_rmd.sh <Rmd path> <tag>   (tag = main | Rc)
# purl the Rmd (documentation=1) and source it with the deposited data folder as working directory.
set -u
RMD="$1"; TAG="$2"
A=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/18_YXC5K5/A
DATA=/workspace/audit_runs/18_YXC5K5/A/data
export R_LIBS_USER=/workspace/audit_runs/18_YXC5K5/A/rlib
cd "$DATA"
Rscript -e "knitr::purl('$RMD', output = '$A/outputs/analysis_$TAG.R', documentation = 1)" > "$A/outputs/purl_$TAG.log" 2>&1
Rscript -e "pdf('$A/outputs/plots_$TAG.pdf'); source('$A/outputs/analysis_$TAG.R', echo = TRUE, max.deparse.length = Inf); dev.off(); save.image('/workspace/audit_runs/18_YXC5K5/A/session_$TAG.RData')" > "$A/outputs/analysis_log_$TAG.txt" 2>&1
echo "exit status: $?" >> "$A/outputs/analysis_log_$TAG.txt"
tail -1 "$A/outputs/analysis_log_$TAG.txt"
