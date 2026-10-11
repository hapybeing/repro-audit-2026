#!/bin/bash
# Writes environment.txt. Usage: make_environment.sh OUTDIR RUNDIR
O=$1; RUN=$2
{
echo "Paper 22_W2TSVL, agent A. Written $(TZ=Asia/Kolkata date '+%F %T IST')"
echo "== uname"; uname -a
echo "== /etc/os-release"; cat /etc/os-release
echo "== R"; R --version | head -1
echo "== Python"; python3 --version
echo "== pdftotext"; pdftotext -v 2>&1 | head -1
echo "== R library paths used: R_LIBS_USER=/workspace/audit_runs/22_W2TSVL/A/rlib then system libs"
echo "== Installed into per-run rlib from CRAN source (Ncpus=1): stargazer, tableone, gmodels (tableone dependency). No Debian r-cran-stargazer or r-cran-tableone exists in trixie; r-cran-gmodels exists but was installed from CRAN together with tableone. All other packages are the system (Debian / setup_env.sh) copies."
echo "== Package versions"
cd $RUN && R_LIBS_USER=/workspace/audit_runs/22_W2TSVL/A/rlib Rscript -e 'pk<-c("haven","foreign","plyr","dplyr","MASS","broom","ggplot2","stargazer","tableone","gmodels","survey","sandwich","lmtest","jsonlite"); for(p in pk) cat(sprintf("%-10s %-10s %s\n", p, as.character(packageVersion(p)), dirname(find.package(p))))'
echo "== sessionInfo() at end of the authors' Appendix A1 script run"; cat $O/outputs/sessionInfo_appendix.txt
echo "== Seeds: authors' code uses no random numbers. Robustness R_a: set.seed(20261011) once, 1000 resamples for m1 then 1000 for m7 on the same stream (R default Mersenne-Twister, Inversion, sample.kind Rejection)."
echo "== Authors' environment (README): R 4.4.2, RStudio 2024.09.1, Windows (from the file path)."
} > $O/environment.txt
