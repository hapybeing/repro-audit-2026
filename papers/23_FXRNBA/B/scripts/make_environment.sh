#!/bin/bash
# Writes environment.txt for 23_FXRNBA agent B.
B=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/23_FXRNBA/B
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S %Z')"
echo "uname -a: $(uname -a)"
echo "--- /etc/os-release"; cat /etc/os-release
echo "--- Python: $(python3 --version 2>&1)"
echo "--- Locale used for R runs: LC_ALL=C.UTF-8 (script itself calls Sys.setenv(LANG='en'))"
echo "--- R_LIBS_USER=/workspace/audit_runs/23_FXRNBA/B/rlib (per-run library, CRAN source installs)"
echo "--- Seeds: authors' Table 1 path has no seed; R_a bootstrap set.seed(20261011)"
echo "--- sessionInfo after loading the authors' packages"
R_LIBS_USER=/workspace/audit_runs/23_FXRNBA/B/rlib LC_ALL=C.UTF-8 Rscript -e 'suppressPackageStartupMessages({library(haven);library(tidyverse);library(fixest);library(ivtools);library(sandwich);library(lmtest);library(weathermetrics);library(lubridate);library(knitr);library(kableExtra);library(MASS);library(splines)}); print(sessionInfo()); ip<-installed.packages()[,c("Package","Version","LibPath")]; cat("\n--- all installed packages\n"); write.table(ip, row.names=FALSE, quote=FALSE, sep="\t")'
} > $B/environment.txt 2>&1
