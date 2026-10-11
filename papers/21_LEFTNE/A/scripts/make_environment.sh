#!/bin/bash
# Writes environment.txt for 21_LEFTNE agent A.
P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A
E=$P/environment.txt
{
echo "# Environment, paper 21_LEFTNE, agent A"
echo "Written: $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M:%S IST')"
echo; echo "## OS"; uname -a; cat /etc/os-release
echo; echo "## CPU / memory"; nproc; free -m
echo; echo "## Python"; python3 --version
echo; echo "## R"; R --version | head -1
echo "R_LIBS_USER for all runs: /workspace/audit_runs/21_LEFTNE/A/rlib (CRAN source installs, Ncpus=1); system site-library for Debian r-cran-* binaries."
echo "Exception: outputs/targets_extracted_lavaan0619_system.csv was produced with R_LIBS_USER empty (system Debian lavaan 0.6.19) as a version cross-check."
echo; echo "## apt packages added by this agent (environment only)"
for p in libarchive-dev catdoc antiword; do dpkg -l $p 2>/dev/null | awk '/^ii/{print $2, $3}'; done
echo "(libarchive-dev: system library for CRAN 'archive', a qualtRics dependency; catdoc: SI .doc table check; antiword: tried first for the SI, truncated Table A5, not used for scoring)"
echo; echo "## Seeds"
echo "Authors: set.seed(20241130) at 02- Replication_Appendix.R line 147 (mediate bootstrap). Audit R_a: set.seed(20261011), K = 1000, reset before each study."
echo; echo "## R sessionInfo and package versions (rlib first)"
cd /workspace/audit_runs/21_LEFTNE/A/data
R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/A/rlib Rscript -e 'P<-c("here","car","survey","margins","interplot","aod","dplyr","foreign","nnet","ggplot2","reshape2","Rmisc","tidyverse","broom","dotwhisker","janitor","qualtRics","jtools","mediation","gtools","gridExtra","huxtable","DT","ggsci","hrbrthemes","haven","effectsize","readr","purrr","emmeans","ggpubr","lavaan","ggeffects","prediction","scales","insight","parameters","performance","bayestestR","datawizard","archive","interactionTest"); for (p in P) cat(sprintf("%-16s %-10s %s\n", p, as.character(packageVersion(p)), dirname(find.package(p)))); suppressMessages(invisible(lapply(c("lavaan","car","dplyr","mediation","jtools","huxtable"), library, character.only=TRUE))); print(sessionInfo())' 2>&1
echo; echo "Full sessionInfo of each authors-script run is printed at the end of outputs/text_log.txt and outputs/appendix_log.txt."
} > $E
echo written $E
