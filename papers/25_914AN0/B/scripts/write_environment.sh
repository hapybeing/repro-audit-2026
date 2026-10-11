#!/bin/bash
# Writes environment.txt for agent B, paper 25_914AN0
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B; R=/workspace/audit_runs/25_914AN0/B
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M')"
echo "== uname -a"; uname -a
echo "== /etc/os-release"; cat /etc/os-release
echo "== nproc: $(nproc)"; free -m
echo "== R"; Rscript -e 'cat(R.version.string, "\n")'
echo "== R_LIBS_USER=$R/rlib (per-run library); system libraries /usr/lib/R/site-library, /usr/lib/R/library"
echo "== Package versions used (from R_LIBS_USER then system)"
R_LIBS_USER=$R/rlib Rscript -e 'p<-c("data.table","dplyr","stringr","lfe","lme4","nlme","Formula","xtable","optimx","ggplot2","robustlmm","Matching","fixest","SUNGEO","tidyselect","sf","terra","Matrix","Rcpp","RcppEigen","V8","dreamerr","sandwich"); for(x in p) cat(sprintf("%-12s %-12s %s\n", x, as.character(packageVersion(x)), dirname(find.package(x))))'
echo "== Install log (pins and fallbacks)"; cat $R/pkg_install.log
echo "== sessionInfo() of each stage: outputs/sessionInfo_s1a.txt, outputs/sessionInfo_s1b.txt, outputs/sessionInfo_s4.txt"
echo "== Seeds: authors' target blocks use no RNG. R_a bootstrap: set.seed(20261011) once, K=500 draws sample(n,n,replace=TRUE)."
echo "== Authors' stated environment (README): R 4.4.1, Ubuntu 22.04, fixest 0.12.0, lfe 3.0-0"
} > $P/environment.txt 2>&1
cp $R/pkg_install.log $P/outputs/pkg_install.log
