# diffs/ README (06_VSV5DM, agent B)

No file of the authors was edited, so this folder holds no .diff files.

Environment fixes applied without changing any authors' file:
1. Created the empty output folders the code writes to, inside RUNDIR (/workspace/audit_runs/06_VSV5DM/B/run):
   `Total Activity Analysis_RaceAndGender/`, `Total Activity Analysis_RaceAndGenderAndParty_v1/`, `Total Activity Analysis_RaceAndGenderAndParty_v2/` (the last one is named in the README but never written to).
   Reason: `ggexport()`, `htmlreg(file=)` and `print(xtable, file=)` fail if the folder does not exist. Done by `scripts/run_main.sh` (mkdir -p).
2. `rtweet` (archived on CRAN 2025-04-07) was installed as the Debian binary `r-cran-rtweet 2.0.0+dfsg-1`, so `library(rtweet)` (Rmd line 15) runs unchanged; the PREREG fallback of commenting it out was not needed.
3. The R code was extracted from the Rmd with `knitr::purl(..., documentation = 0)` as the PREREG says (outputs/multivariate.R); the purled file is byte-for-byte the code chunks, no edits.
