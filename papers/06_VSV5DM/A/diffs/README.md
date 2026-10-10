# Environment fixes (agent A, 06_VSV5DM)

No source file of the authors was edited. The purled `multivariate.R` is byte-for-byte what `knitr::purl("Multivariate Analysis.Rmd", documentation = 0)` produced.

1. `00_output_dirs.diff`: created the three output folders the code writes into (`Total Activity Analysis_RaceAndGender/`, `Total Activity Analysis_RaceAndGenderAndParty_v1/`, `..._v2/`) in the run directory. They are not in the deposit; the deposit README says the runner must create them. Without them every `ggexport`/`htmlreg(file=)`/`print(xtable, file=)` call fails. Allowed by PREREG section 2.
2. Packages: `margins` 0.3.28, `texreg` 1.40, `betareg` 3.2.6, `eeptools` 1.3.0 installed from CRAN source into a clean per-run library (`R_LIBS_USER=/workspace/audit_runs/06_VSV5DM/A/rlib`, `Ncpus=1`). All other packages (including `rtweet` 2.0.0, `prediction` 0.3.18) came from Debian r-cran-* binaries in /usr/lib/R/site-library installed by REPO/scripts/setup_env.sh and a concurrent agent's apt run. `rtweet` was available as a Debian binary, so `library(rtweet)` was NOT commented out.
