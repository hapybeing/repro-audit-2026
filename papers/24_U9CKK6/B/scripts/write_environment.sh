#!/bin/bash
# Writes environment.txt (run after all R jobs; one R process at a time).
B=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/B; out=$B/environment.txt
export R_LIBS_USER=/workspace/audit_runs/24_U9CKK6/B/rlib
{ echo "Written: $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST')"; echo; echo "== uname -a"; uname -a; echo; echo "== /etc/os-release"; cat /etc/os-release
  echo; echo "== CPU/RAM"; nproc; free -m; echo; echo "== Python"; python3 --version
  echo; echo "== R per-run library: $R_LIBS_USER (CRAN source installs, Ncpus=1); Debian binaries in /usr/lib/R/site-library"
  echo "Debian r-cran packages installed by this agent via apt: r-cran-ggeffects r-cran-skimr r-cran-zoo r-cran-sjmisc (others by scripts/setup_env.sh)"
  echo "Seeds: R_a bootstrap set.seed(20261011) (draws pre-generated, outputs/R_a_draws.rds). Target models involve no randomness."
  echo "Saved model files (scratch, not in repo; sha256):"; (cd /workspace/audit_runs/24_U9CKK6/B/run/models && sha256sum *.rds && ls -l *.rds)
  echo; echo "== sessionInfo after loading the packages the run scripts load"
  Rscript -e 'suppressMessages({library(lme4);library(texreg);library(sjPlot);library(sjstats);library(fixest);library(ggplot2);library(ggeffects);library(zoo);library(skimr);library(tidyverse);library(Matrix)}); print(sessionInfo()); cat("\nlibPaths:\n"); print(.libPaths()); ip <- installed.packages()[, c("Package","Version","LibPath")]; cat("\nAll installed packages:\n"); write.table(ip, sep="\t", quote=FALSE, row.names=FALSE)'
} > $out 2>&1
echo written $out
