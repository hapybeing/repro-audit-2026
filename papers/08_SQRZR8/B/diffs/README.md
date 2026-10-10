# diffs/ for 08_SQRZR8 agent B

No file of the authors was changed. main_rep.R and data_cleaned_rep.csv were copied unchanged into the run folder and run with `source()`.

Environment-only arrangements (not code changes):
- data_cleaned_rep.csv downloaded with `?format=original` (datafile 12134916), as PREREG.md requires; md5 equals the Dataverse-listed value.
- Missing CRAN packages (ltm 1.2-0, coefplot 1.2.9, sjPlot 2.9.0, mediation 4.5.1 and their missing dependencies) installed into a per-run library (R_LIBS_USER=/workspace/audit_runs/08_SQRZR8/B/rlib). Installing `mediation` is what lets line 238 (`mediation::mediate`) run; no `library()` line was added.
- After `source()`, the objects all_models, pca_emotion, data, covariates_str and results were saved with `save()` (outside the authors' file) for the extraction and robustness scripts.
