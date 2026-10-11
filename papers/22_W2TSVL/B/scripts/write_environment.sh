#!/bin/bash
# Writes environment.txt (agent B)
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/22_W2TSVL/B
export R_LIBS_USER=/workspace/audit_runs/22_W2TSVL/B/rlib
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S %Z')"
echo "uname: $(uname -a)"; echo; cat /etc/os-release; echo
echo "Python: $(python3 --version 2>&1)"; echo "R: $(Rscript --version 2>&1)"
echo "R_LIBS_USER=$R_LIBS_USER (per-run library: stargazer, tableone from CRAN source; pure R, no compile)"
echo "Debian binaries via setup_env.sh (r-base, r-cran-tidyverse, haven, sandwich, lmtest, etc.) plus 'sudo apt-get install -y r-cran-gmodels' (tableone dependency)."
echo "Seeds: set.seed(20261011) once in scripts/robustness.R (R_a bootstrap, m1 loop then m7 loop). Authors' code uses no random numbers."
echo; echo "Session info at end of the authors' appendix script run:"; cat $P/outputs/sessionInfo_appendix.txt
echo; echo "Versions of packages used:"
Rscript -e 'for (p in c("haven","foreign","plyr","dplyr","MASS","broom","ggplot2","stargazer","tableone","survey","gmodels","labelled","sandwich","lmtest")) cat(sprintf("%-10s %s  %s\n", p, as.character(packageVersion(p)), dirname(dirname(system.file(package=p)))))'
} > $P/environment.txt
