#!/bin/bash
S=/workspace/audit_runs/17_T1NXVQ/B; P=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/17_T1NXVQ/B
{
echo "# environment, agent B, 17_T1NXVQ; written $(TZ=Asia/Kolkata date '+%Y-%m-%d %H:%M IST')"
uname -a; cat /etc/os-release | head -4; nproc; free -m | head -2
echo; echo "## R"; R --version | head -1
echo "R_LIBS_USER=$S/rlib (per-run library), then system site-library"
echo; echo "## R packages used (version, library)"
R_LIBS_USER=$S/rlib Rscript -e 'p <- c("pspm","igraph","maxLik","miscTools","reticulate","texreg","infotheo","R6","sp","foreach","doParallel","raster","plyr","dplyr","tidyr","ggplot2","scico","abind","gridExtra","cshapes","ggridges","survival","MASS","fasterize","sf","viridis","tidyverse","xtable","smoothr","stargazer","lfe","V8","rmapshaper","Rcpp"); for (x in p) cat(x, tryCatch(as.character(packageVersion(x)), error=function(e) "NOT INSTALLED"), tryCatch(dirname(find.package(x)), error=function(e) ""), "\n")'
echo "rgeos, rgdal: NOT INSTALLED (archived 0.6-4 / 1.6-7 failed to compile: sp.h missing); library() calls removed (E3)"
echo "igraph 1.4.1 (pinned) failed to compile (-Werror=format-security, rinterface.c:210); Debian r-cran-igraph 2.1.4 used"
echo "reticulate 1.28 (pinned) built but fails at load on Python 3.12 (config.py: import imp); Debian r-cran-reticulate 1.41.0.1 used"
echo; echo "## Python venv ($S/venv)"; $S/venv/bin/python --version; $S/venv/bin/pip freeze
echo; echo "## system packages installed by agent B with apt"; echo "libgdal-dev 3.10.3+dfsg-1, libgeos-dev 3.13.1-1, libproj-dev (for the rgeos/rgdal attempts)"
echo "V8 R package from CRAN source with DOWNLOAD_STATIC_LIBV8=1 (Debian r-cran-v8 conflicts with nodesource nodejs)"
echo; echo "## Seeds"; echo "fit: set.seed(1) inside the authors' estimation function; bootstrap: set.seed(i) and reticulate::py_set_seed(i, disable_hash_randomization=TRUE), i = authors' seeds 1..K and R_a seeds 1001..1000+K"
echo; echo "## sessionInfo of the baseline fit"; sed -n '/^R version/,$p' $P/outputs/run_pool_xsec.log
} > $P/environment.txt 2>&1
