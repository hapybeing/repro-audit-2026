#!/bin/bash
# Runs one of the authors' scripts unchanged, in a fresh R session, with the default graphics device set to a cairo PNG device
# (environment fix: the default pdf() device of Rscript stops with "invalid font type" for hrbrthemes' Roboto Condensed font).
# Usage: run_author_script.sh "<script file>" <logname>
O=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/B
cd /workspace/audit_runs/21_LEFTNE/B/data
export R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/B/rlib
Rscript -e "options(device = function(...) grDevices::png(file.path('$O/outputs/figures', '${2}_%03d.png'), width = 1200, height = 900, type = 'cairo')); source('$1', echo=TRUE, max.deparse.length=Inf)" > $O/outputs/$2.txt 2>&1
echo "exit status $?" >> $O/outputs/$2.txt
