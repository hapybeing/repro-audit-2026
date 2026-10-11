#!/bin/bash
# Writes environment.txt. Usage: bash make_environment.sh <A dir> <rlib>
A=$1; RL=$2
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M %Z')"
echo "uname: $(uname -a)"; echo; cat /etc/os-release; echo
echo "Python: $(python3 --version 2>&1)"
echo "Run settings: LC_ALL=C.UTF-8, R_LIBS_USER=$RL, Ncpus=1, working dir = RUNDIR (/workspace/audit_runs/23_FXRNBA/A/run)"
echo "Seeds: authors' Table 1 path has no RNG; R_a bootstrap set.seed(20261011) once (indices in outputs/Ra_boot_indices.rds)."
echo "Debian packages: 'time' reinstalled after sandbox restart (for /usr/bin/time). No r-cran-* binary existed for fixest, ivtools, weathermetrics, ahaz, dreamerr, stringmagic: installed from CRAN source into R_LIBS_USER."
echo; echo "== sessionInfo of the full run (outputs/sessionInfo_full.txt) =="; cat $A/outputs/sessionInfo_full.txt
echo; echo "== Package versions (R_LIBS_USER first, then system) =="
R_LIBS_USER=$RL Rscript -e 'ip <- installed.packages(fields="Packaged"); pk <- c("fixest","ivtools","ahaz","weathermetrics","dreamerr","stringmagic","tidyverse","dplyr","tidyr","kableExtra","knitr","sandwich","lmtest","haven","lubridate","MASS","data.table","Rcpp","survival","numDeriv"); for (p in pk) { i <- which(ip[,"Package"]==p)[1]; cat(sprintf("%-15s %-10s %s\n", p, ip[i,"Version"], ip[i,"LibPath"])) }'
echo; echo "== Full installed package list =="
R_LIBS_USER=$RL Rscript -e 'ip <- installed.packages(); write.table(ip[,c("Package","Version","LibPath")], row.names=FALSE, quote=FALSE)'
} > $A/environment.txt 2>&1
