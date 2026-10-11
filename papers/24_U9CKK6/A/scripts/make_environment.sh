#!/bin/bash
# Writes environment.txt for 24_U9CKK6 agent A.
O=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A
{
echo "# environment.txt (agent A, 24_U9CKK6), written $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST')"
echo "## uname -a"; uname -a
echo "## /etc/os-release"; cat /etc/os-release
echo "## CPUs / memory"; nproc; free -m
echo "## R"; R --version | head -1
echo "## Python"; python3 --version
echo "## Seeds: target models use no randomness; R_a bootstrap set.seed(20261011), draws saved in outputs/R_a_draws.rds"
echo "## Run settings: R_LIBS (per-run) /workspace/audit_runs/24_U9CKK6/A/rlib first in .libPaths(); Ncpus=1; MAKEFLAGS=-j1; one R process at a time"
echo "## Package sources: rlib (CRAN source builds, 2026-10-11): texreg sjstats sjPlot skimr fixest + deps; system library (Debian r-cran-* via scripts/setup_env.sh): lme4 Matrix zoo tidyverse dplyr ggplot2 ggeffects"
echo "## sessionInfo after loading the packages of 6_analysis1.R and 9_analysis4.R"
R --no-save --no-restore -q -e '.libPaths(c("/workspace/audit_runs/24_U9CKK6/A/rlib", .libPaths())); suppressMessages({library(lme4); library(texreg); library(sjPlot); library(sjstats); library(fixest); library(ggplot2); library(ggeffects); library(zoo); library(skimr); library(tidyverse)}); print(sessionInfo()); ip <- installed.packages(); cat("\n## installed packages (name version libpath)\n"); write.table(ip[, c("Package","Version","LibPath")], quote=FALSE, row.names=FALSE)'
} > $O/environment.txt 2>&1
