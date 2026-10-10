#!/bin/bash
# Idempotent: installs system R (Debian r-base 4.5.x) + common CRAN binaries. The sandbox can be recycled, so run this
# at the start of any run if `Rscript` is missing. Logs to /tmp/setup_env.log
if command -v Rscript >/dev/null 2>&1; then echo "R present: $(Rscript --version 2>&1 | head -1)"; exit 0; fi
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq r-base r-base-dev libcurl4-openssl-dev libssl-dev libxml2-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype-dev libpng-dev libtiff-dev libjpeg-dev cmake \
  r-cran-tidyverse r-cran-data.table r-cran-haven r-cran-lme4 r-cran-readxl r-cran-sandwich r-cran-lmtest r-cran-remotes \
  r-cran-sessioninfo r-cran-lavaan r-cran-psych r-cran-mice r-cran-boot r-cran-car r-cran-fixest > /tmp/setup_env.log 2>&1 || \
sudo apt-get install -y -qq r-base r-base-dev r-cran-tidyverse r-cran-data.table r-cran-haven r-cran-remotes r-cran-sessioninfo >> /tmp/setup_env.log 2>&1
Rscript --version
