#!/bin/bash
# Idempotent: installs system R (Debian r-base 4.5.x) + common CRAN binaries. The sandbox can be recycled, so run this
# at the start of any run if `Rscript` is missing. Logs to /tmp/setup_env.log
# Environment only (CHANGELOG_METHOD.md #6): a package with no Debian candidate (for example r-cran-fixest, which is not
# in Debian trixie) or a failed optional install is logged and skipped, never fatal; install it from CRAN into the
# per-run library instead (AGENT_RUNBOOK.md). apt waits up to 10 minutes for another agent's dpkg lock.
if command -v Rscript >/dev/null 2>&1; then echo "R present: $(Rscript --version 2>&1 | head -1)"; exit 0; fi
export DEBIAN_FRONTEND=noninteractive
APT="sudo apt-get -o DPkg::Lock::Timeout=600 install -y -qq"
LOG=/tmp/setup_env.log
sudo apt-get -o DPkg::Lock::Timeout=600 update -qq >> "$LOG" 2>&1
# Required: R itself and the build headers. Failure here is fatal.
$APT r-base r-base-dev libcurl4-openssl-dev libssl-dev libxml2-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
  libfreetype-dev libpng-dev libtiff-dev libjpeg-dev cmake >> "$LOG" 2>&1 || { echo "R install failed, see $LOG"; exit 1; }
# Optional CRAN binaries: install those with a Debian candidate, one at a time; skip and log the rest.
for p in r-cran-tidyverse r-cran-data.table r-cran-haven r-cran-lme4 r-cran-readxl r-cran-sandwich r-cran-lmtest \
         r-cran-remotes r-cran-sessioninfo r-cran-lavaan r-cran-psych r-cran-mice r-cran-boot r-cran-car r-cran-fixest; do
  cand=$(apt-cache policy "$p" 2>/dev/null | awk '/Candidate:/ {print $2}')
  if [ -z "$cand" ] || [ "$cand" = "(none)" ]; then
    echo "skip $p: no Debian candidate (install from CRAN into the per-run library)" | tee -a "$LOG"; continue
  fi
  $APT "$p" >> "$LOG" 2>&1 || echo "skip $p: apt install failed (see $LOG)" | tee -a "$LOG"
done
Rscript --version
