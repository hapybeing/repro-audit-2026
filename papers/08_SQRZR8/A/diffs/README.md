# diffs/ for 08_SQRZR8 agent A

No file of the authors was changed. main_rep.R was run byte-identical to the deposit (sha256 4782d605...7c79, `cmp` against the download before the run).

Environment-only steps (no diff, because no file was edited):
- Packages not in Debian trixie (ltm, coefplot, sjPlot, mediation and some newer dependencies CRAN pulled in) were installed from CRAN source into a per-run library. main_rep.R calls `mediation::mediate` (line 238) without `library(mediation)`; this works once the package is installed, so no `library()` line was added.
- The data file was downloaded with `?format=original` and saved as data_cleaned_rep.csv, as PREREG.md instructs.
- The driver scripts/run_main.R sets `.libPaths()`, calls `set.seed(20261009)` (main_rep.R sets no seed; this only affects the Figure 3 mediation bootstrap) and then `source("main_rep.R", echo=TRUE)`, then saves objects. This is an execution wrapper, not an edit.
- The reproduction result comes from scripts/run_all_segments.sh, which runs lines 1-252, 253-331 and 332-449 of the unchanged main_rep.R in original order in three R processes joined by save.image()/load() (PREREG section 2 execution allowance), after a sandbox recycle killed a single-process run. scripts/run_segment.R reads the lines verbatim from the deposited file.
