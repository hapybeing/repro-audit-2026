#!/bin/bash
# Runs the full purled Multivariate Analysis.Rmd in RUNDIR; log to outputs/.
RUN=/workspace/audit_runs/06_VSV5DM/B/run
OUT=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/06_VSV5DM/B/outputs
export R_LIBS_USER=/workspace/audit_runs/06_VSV5DM/B/rlib
cd "$RUN"
mkdir -p "Total Activity Analysis_RaceAndGender" "Total Activity Analysis_RaceAndGenderAndParty_v1" "Total Activity Analysis_RaceAndGenderAndParty_v2"
Rscript -e 'knitr::purl("Multivariate Analysis.Rmd", output="multivariate.R", documentation=0)'
Rscript -e 'source("multivariate.R", echo=TRUE, max.deparse.length=Inf); writeLines(capture.output(sessionInfo()), "sessionInfo_main.txt")' > "$OUT/multivariate_full_run.log" 2>&1
echo "exit=$?" >> "$OUT/multivariate_full_run.log"
