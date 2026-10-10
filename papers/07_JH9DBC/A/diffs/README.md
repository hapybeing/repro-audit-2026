# Diffs for 07_JH9DBC, agent A

No file of the authors was changed. `replication.R` was run byte-identical to the deposit (sha256 41a35296...; see ../checksums.sha256), so there is no .diff file.

Environment-only fixes (no file edits, so nothing to diff):
1. Working directory set to the folder holding `data.dta` by `scripts/run_authors.sh` (`cd` before `Rscript`), as the script header asks ("Set working directory to source file location").
2. `data.dta` obtained with `?format=original` (datafile 11944075), as PREREG.md instructs.
3. Packages installed into a per-run library: fixest, sjPlot, cobalt, WeightIt (current CRAN, with their missing dependencies). WeightIt is called as `WeightIt::weightit` (line 214) without `library()`, so it only needed to be installed.
4. Package version: the primary run uses fixest 0.12.1 (CRAN archive, the CRAN release from 2024-06-13 until fixest 0.13.x in 2025) in a separate library. Reason: fixest 0.13.0 changed two defaults (NEWS.md: "the new default VCOV is `iid` for all estimations" and "the default is to remove all observations that are perfectly fit by the fixed-effects (this includes the singletons)"). With fixest 0.14.2, `model1B` to `model4B` report IID standard errors and 586 observations (14 singleton districts dropped), whereas the supplement's Table B says SEs are clustered by district and reports 600 observations. Coefficients are identical in both versions. The 0.14.2 run is kept in outputs/*_fixest0142.* for comparison.
