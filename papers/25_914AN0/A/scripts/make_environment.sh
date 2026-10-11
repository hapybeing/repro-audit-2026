#!/bin/bash
# Writes environment.txt (OS, R, package versions, seeds, date IST).
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M %Z')"
echo "== uname -a"; uname -a
echo "== /etc/os-release"; cat /etc/os-release
echo "== nproc: $(nproc)"; free -m
echo "== Seeds: R_a set.seed(20261011) once, then sample(n, n, replace=TRUE) per replicate. Authors' S1/S4 target blocks use no RNG."
echo "== Per-run library: /workspace/audit_runs/25_914AN0/A/rlib (R_LIBS_USER); system site-library for the rest"
echo "== Package install log (outputs/install_log.tsv):"; cat $P/outputs/install_log.tsv
echo "== V8 installed from CRAN with DOWNLOAD_STATIC_LIBV8=1"
echo "== R sessionInfo after loading run1_setup.R packages:"
R_LIBS_USER=/workspace/audit_runs/25_914AN0/A/rlib Rscript -e 'suppressMessages(source("/workspace/audit_runs/25_914AN0/A/Replication_IO/code/run1_setup.R")); print(sessionInfo()); ip <- installed.packages(); cat("\n== Versions of key packages and their library:\n"); for(p in c("lfe","fixest","lme4","Matrix","data.table","dplyr","SUNGEO","Formula","xtable","ggplot2","robustlmm","Matching","optimx","nlme","stringr","tidyselect","V8","sf")) cat(p, as.character(packageVersion(p)), find.package(p), "\n")' 2>&1
} > $P/environment.txt
