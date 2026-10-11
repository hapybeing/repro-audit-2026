#!/bin/bash
# Writes environment.txt
O=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/B
{
echo "Date (IST): $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M')"
echo "uname -a: $(uname -a)"; echo; cat /etc/os-release; echo
echo "R library order used for the authors' scripts: R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/B/rlib, then /usr/local/lib/R/site-library, /usr/lib/R/site-library, /usr/lib/R/library"
echo "Seeds: authors' set.seed(20241130) (Appendix line 147, mediate bootstraps); R_a set.seed(20261011) once per study before drawing all K=1000 resamples."
echo "Graphics: default device set to cairo PNG (environment fix, see diffs/README.md)."
echo
echo "=== sessionInfo with rlib first, after loading all packages of both scripts plus lavaan ==="
R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/B/rlib Rscript -e 'P <- c("here","car","survey","margins","interplot","aod","dplyr","foreign","nnet","ggplot2","reshape2","Rmisc","ggpubr","tidyverse","broom","dotwhisker","janitor","qualtRics","jtools","mediation","gtools","gridExtra","huxtable","DT","ggsci","hrbrthemes","haven","effectsize","readr","purrr","emmeans","lavaan","ggeffects","survey"); invisible(suppressMessages(lapply(P, library, character.only=TRUE))); print(sessionInfo()); cat("\n=== package versions and library paths ===\n"); for (p in sort(unique(P))) cat(sprintf("%-12s %-10s %s\n", p, as.character(packageVersion(p)), dirname(find.package(p))))' 2>&1
echo
echo "=== packages installed into rlib (CRAN source) ==="
R_LIBS_USER= Rscript -e 'ip <- installed.packages(lib.loc="/workspace/audit_runs/21_LEFTNE/B/rlib")[, c("Package","Version")]; print(ip, quote=FALSE)'
echo; echo "Supplementary version check: system lavaan 0.6.19 (Debian r-cran-lavaan, already on the machine) gave identical T1-T6 (outputs/targets_extracted_lavaan0.6.19.csv)."
} > $O/environment.txt
