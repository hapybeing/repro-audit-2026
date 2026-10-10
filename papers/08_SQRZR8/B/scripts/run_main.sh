#!/bin/bash
# Runs the authors' unchanged main_rep.R in a copy dir, then saves objects. Usage: bash run_main.sh
S=/workspace/audit_runs/08_SQRZR8/B; R=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/08_SQRZR8/B
mkdir -p $S/run; cp $S/dl/main_rep.R $S/dl/data_cleaned_rep.csv $S/run/; cd $S/run
export R_LIBS_USER=$S/rlib
Rscript -e 'source("main_rep.R", echo=TRUE, max.deparse.length=Inf); save(all_models, pca_emotion, data, covariates_str, results, file="session_models.RData"); cat("RUN_DONE\n")' > $R/outputs/main_rep_stdout.txt 2>&1
echo "exit $?" >> $R/outputs/main_rep_stdout.txt
cp session_models.RData $R/outputs/ 2>/dev/null
