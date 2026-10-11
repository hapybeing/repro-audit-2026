#!/bin/bash
export R_LIBS_USER=/workspace/audit_runs/21_LEFTNE/A/rlib
L=/workspace/audit_runs/21_LEFTNE/A/install.log
for p in lavaan aod Rmisc interplot interactionTest margins janitor jtools huxtable dotwhisker hrbrthemes performance effectsize mediation archive qualtRics; do
  if Rscript -e "q(status=as.integer(!requireNamespace('$p',lib.loc='$R_LIBS_USER',quietly=TRUE)))" 2>/dev/null; then echo "have $p" >>$L; continue; fi
  while true; do
    ma=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
    nr=$(pgrep -f "exec/R" | wc -l)
    if [ "$ma" -ge 1500 ]; then break; fi
    echo "$(date -u +%T) wait $p MemAvailable=${ma}MB" >>$L; sleep 20
  done
  echo "$(date -u +%T) install $p (MemAvailable=${ma}MB)" >>$L
  Rscript -e "options(Ncpus=1); install.packages('$p', repos='https://cloud.r-project.org', lib=Sys.getenv('R_LIBS_USER'), Ncpus=1, dependencies=c('Depends','Imports','LinkingTo'))" >>$L 2>&1
done
echo "$(date -u +%T) DONE" >>$L
