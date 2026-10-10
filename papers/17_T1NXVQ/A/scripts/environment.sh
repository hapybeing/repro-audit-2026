#!/bin/bash
# Agent A 17_T1NXVQ: write environment.txt
RUN=/workspace/audit_runs/17_T1NXVQ/A
A=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/A
{
echo "# environment (agent A, 17_T1NXVQ), written $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST')"
uname -a; cat /etc/os-release
echo; echo "## Python (venv $RUN/venv)"; $RUN/venv/bin/python -V; $RUN/venv/bin/pip freeze
echo; echo "## R library order: $RUN/rlib first, then Debian site libraries"
echo "Seeds: set.seed(1) before each fit (authors' code); bootstrap draws seed i: set.seed(i), reticulate::py_set_seed(i, disable_hash_randomization = TRUE); step 6 i = 1..K, R_a i = 1001..1000+K"
echo "Pinned versions tried: miscTools 0.6-26, maxLik 1.5-2, texreg 1.38.6, infotheo 1.2.0.1 (installed, used); reticulate 1.28 (installed but unusable with Python >= 3.12, replaced by Debian 1.41.0.1); igraph 1.4.1 (build failed, Debian 2.1.4 used); rgeos 0.6-4, rgdal 1.6-7 (build failed, E3)."
R_LIBS_USER=$RUN/rlib RETICULATE_PYTHON=$RUN/venv/bin/python Rscript -e 'suppressMessages({library(pspm); library(reticulate); library(igraph); library(maxLik); library(sf); library(raster); library(cshapes); library(texreg); library(infotheo)}); ip <- installed.packages(); cat("\n## Package versions and LibPath for packages loaded\n"); s <- sessionInfo(); print(s); pk <- c(names(s$otherPkgs), names(s$loadedOnly)); print(ip[pk, c("Version","LibPath")]); print(reticulate::py_config())'
} > $A/environment.txt 2>&1
