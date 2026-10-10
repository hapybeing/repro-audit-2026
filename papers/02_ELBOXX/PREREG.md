# PREREG: 02_ELBOXX

Written 2026-10-09 (IST), before any analysis code was run. No correlation, regression or test from the paper was computed while writing this file.

## 0. Identifiers and sources

- Paper: Peter Bils and Bradley C. Smith, "The Logic of Secret Alliances", American Journal of Political Science, first published 20 June 2025; issue version Vol. 70, Issue 3 (July 2026), pp. 1062-1076. Open access, CC BY 4.0.
  - DOI: https://doi.org/10.1111/ajps.12997
  - Full text (HTML): https://onlinelibrary.wiley.com/doi/full/10.1111/ajps.12997
  - PDF: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/ajps.12997 (blocked by a Cloudflare interstitial for curl, web_fetch and the audit browser on 2026-10-09; the HTML was read via a fetch fallback).
- Dataset: "Replication Data for: The Logic of Secret Alliances", Harvard Dataverse, version 1.0, released 2025-05-22.
  - DOI: https://doi.org/10.7910/DVN/ELBOXX
  - File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/ELBOXX
- The article states the Cornell Center for Social Sciences verified that the Dataverse code replicates the numerical results in the main text.
- Note for the audit: REPO/PROTOCOL.md does not exist in the repo at the time of writing (only AGENT_RUNBOOK.md, CHANGELOG_METHOD.md and others). This PREREG follows AGENT_RUNBOOK.md and the dispatch instructions.

### Dataverse files (file id, name, bytes)

| id | file | bytes | note |
|---|---|---|---|
| 11182351 | AJPS_analysis_data.RData | 96774 | contains data.frame `d` (17511 x 9: year, state, defense, secret, secret_def, pub_def, statenme, disputes, secret_alliances) and `.Random.seed` |
| 11182345 | AJPS_rep_secretally.Rproj | 205 | RStudio project file |
| 11182343 | analysis_data_creation.R | 3056 | builds `d` from raw data |
| 11182348 | replication.R | 1122 | the two correlation tests |
| 11182352 | visualization.R | 2178 | Figure 3 |
| 11182346 | atop5_1a.tab | 182753 | ingested from original `atop5_1a.csv` |
| 11182349 | atop5_1sy.tab | 1237121 | ingested from original `atop5_1sy.csv` |
| 11182354 | dyadic_mid_4.02.tab | 1746401 | ingested from original `dyadic_mid_4.02.csv` |
| 11336347 | README.txt | 2588 | |
| 11182347 | LOG.pdf | 47691 | authors' log of replication.R output |
| 11182350 | secret_time.pdf | 5681 | Figure 3 |
| 11182355 | atop_5_1_codebook.pdf | 473040 | |
| 11182353 | Dyadic MID Codebook V4.0.pdf | 240299 | |

sha256 of files downloaded while writing this PREREG (scratch: /workspace/audit_runs/02_ELBOXX/prereg/):
- AJPS_analysis_data.RData 4cec4ad954551714c01b51e153275ab00d14cfef3c95d6cc1b479be955d49390
- README.txt 63f249236865c26e49cef699c34b053cdc1572147d1f679633ecd08e840ac82a
- replication.R 08865dff479a7589fc7f65237105d875eb559c64277c40094680ae12f06b7cdb
- analysis_data_creation.R 559b5f17b333656630fc2d8216832a9e52642ac7fa3b6c4e138b3bf586dfaf82
- visualization.R e3321b51326170fed397b82756387fb86bd789f46e7971dd7da9614eeacca7db
- LOG.pdf b80514416ca7df32554dd4e7a395133230cd8f95a751eb2692f4160cb11e6a68
- AJPS_rep_secretally.Rproj 3a81ccc25a62f1a31c7d3404389935ced50831abea5e848408745ad1a1bf6126

## 1. Headline results

The paper is primarily a formal (game-theoretic) model. The abstract's main claim is theoretical: "the possibility of secret alliances has general effects on deterrence, possibly undermining the deterrent value of concurrent public alliances." There are no regression tables. The only quantitative empirical results are two Pearson correlations reported in the text of the Discussion section, subsection "Secret alliances and conflict" (manuscript pages 25 and 26 per comments in replication.R; exact journal page in the 1062-1076 range could not be confirmed because the PDF was blocked). Figure 3 (share of alliances that are secret by year) is figure only, no numeric value, and is not a target.

- Main result (M2, the empirical counterpart of the abstract's "undermining the deterrent value of concurrent public alliances"): among country-years in which the country is a member of a public defensive alliance, the correlation between the total number of active secret alliances in the system that year and the number of MIDs initiated against the country is ".1628, and 95% confidence interval of [.1317, .1935]".
- Secondary result (M1): correlation between yearly number of secret alliances and disputes, "estimated correlation coefficient of .05441 and a confidence interval of [.03963, .06916]".

Sample sizes are not printed in the paper. The authors' LOG.pdf shows df = 3809 for M2 (so N = 3811) and df = 17509 for M1 (N = 17511); these are not targets because they are not in the paper, but agents should record N from their output.

Source of the CI digits: the coefficients .05441 and .1628 were read from the Wiley HTML full text. The CI brackets are rendered as math and dropped by the text fetch; their digits ([.03963, .06916] and [.1317, .1935]) were read from search-indexed text of the Wiley full-text page and agree with the ResearchGate mirror and with the authors' LOG.pdf (0.03962549, 0.06916076; 0.1317231, 0.1935433). Medium confidence on CI digits, high confidence on the two coefficients.

### Targets

| id | value | decimals | location |
|---|---|---|---|
| T1 | 0.1628 | 4 | Discussion, "Secret alliances and conflict", second test: Pearson r, public defensive alliance country-years |
| T2 | 0.1317 | 4 | same sentence, lower bound of 95% CI |
| T3 | 0.1935 | 4 | same sentence, upper bound of 95% CI |
| T4 | 0.05441 | 5 | Discussion, "Secret alliances and conflict", first test: Pearson r, all country-years |
| T5 | 0.03963 | 5 | same sentence, lower bound of confidence interval |

## 2. Exact reproduction plan

Software in the authors' README: R 4.3.3 on macOS arm64, peacesciencer 1.1.0, logr 1.3.8, common 1.1.3, tidyverse 2.0.0 (dplyr 1.1.4 etc.), foreign 0.8-86. No random numbers are used in the analysis (`.Random.seed` in the RData is incidental).

Steps:
1. Download all files. For the three ingested tables, download the ORIGINAL CSVs, because analysis_data_creation.R reads `.csv` with `read.csv`:
   - https://dataverse.harvard.edu/api/access/datafile/11182346?format=original -> save as `atop5_1a.csv`
   - https://dataverse.harvard.edu/api/access/datafile/11182349?format=original -> save as `atop5_1sy.csv`
   - https://dataverse.harvard.edu/api/access/datafile/11182354?format=original -> save as `dyadic_mid_4.02.csv`
   Compare md5 of the downloaded originals with the md5 values in the Dataverse file list (atop5_1a 905d804cba32717aa49520c29dc87c35, atop5_1sy ed909cfc4fdb1c4f7beb3fc1c303b8d4, dyadic_mid_4.02 741ae2ea9637358bcf4c933083b1b564; for ingested files these normally refer to the original upload, a mismatch is a note, not a blocker). Record sha256.
2. Install into a per-run library: logr (1.3.8), common (1.1.3), peacesciencer (1.1.0, via `remotes::install_version`), tidyverse already present. peacesciencer 1.1.0 matters: `create_stateyears()` defines the state-year frame (1816-2024 in the authors' data, 17511 rows); another version may change N.
3. Path A (full pipeline, primary): set working directory to the folder with all files (replaces opening the .Rproj), run `Rscript replication.R`. It sources analysis_data_creation.R (builds `d`), then `logr::log_open()` writes `log/replication.log`, then:
   - M1: `cor.test(d$secret_alliances, d$disputes)` -> T4, T5.
   - M2: `pubdef <- d[d$pub_def == 1,]; cor.test(pubdef$secret_alliances, pubdef$disputes)` -> T1, T2, T3.
   Note `log_open()` with no file name may need an explicit name when run via Rscript; any such change is an environment fix and needs a diff.
4. Path B (shortcut, secondary): `load("AJPS_analysis_data.RData")`, then run the two `cor.test` lines above. Report both paths; Path A is the reproduction of record. Also compare the rebuilt `d` with the shipped `d` (dimensions and identical-ness per column).
5. Extract r, CI bounds (conf.int), t, df, p and N from the `htest` objects into a CSV in outputs/ and parse that in build_results.

Runtime: README says about 97 s; the two loops run over about 17.5k rows each. Trivial memory.

## 3. Robustness checks for the main result (M2, T1)

Analysis sample for all checks: `pubdef <- d[d$pub_def == 1, ]` built from the Path A `d` (Path B `d` if Path A fails; say which). Variables: x = `secret_alliances`, y = `disputes`. Significance threshold: two-sided 0.05. "Same direction and significance" means positive estimate and 95% interval excluding 0 (or p < 0.05).

- R_a (resampling): nonparametric bootstrap of the Pearson correlation, 1000 replicates, resampling rows of `pubdef` with replacement. In R: `RNGkind("Mersenne-Twister","Inversion","Rejection"); set.seed(20261009)`; for b in 1:1000, `idx <- sample.int(nrow(pubdef), replace = TRUE)`; `r_b <- cor(pubdef$secret_alliances[idx], pubdef$disputes[idx])`. Report the point estimate (full-sample r), bootstrap SE (sd of r_b), and percentile 95% CI (quantile type 7 at 0.025 and 0.975). No stochastic step exists in the authors' pipeline, so a seed re-run is not meaningful; this bootstrap is the nearest meaningful version.
- R_b (outliers): within `pubdef`, compute z-scores with the sample mean and sd (n-1) of `disputes` and of `secret_alliances`; drop every row with |z| > 3 on either variable; rerun `cor.test(x, y)` on the remaining rows. Report r, 95% CI, p and the number of rows dropped.
- R_c (alternative analysis choice: inference that respects the year-level predictor): `secret_alliances` is constant within year, so country-years in the same year are not independent. Fit `m <- lm(disputes ~ secret_alliances, data = pubdef)` and test the slope with year-clustered standard errors: `lmtest::coeftest(m, vcov = sandwich::vcovCL(m, cluster = ~year, type = "HC1"))`. Report slope, clustered SE, p. (The OLS slope has the same sign and the same conventional p as r; the change is only in the SE.)

Supplementary sensitivities (pre-registered here, report in notes, not part of R_a to R_c):
- S1: same as M2 but with `pubdef <- d[d$pub_def >= 1, ]`. The paper text says the sample is "country-years in which the given country was a member of a public defensive alliance", while the code keeps only `pub_def == 1` (exactly one public defensive alliance; `pub_def` is a count with max 14 in the shipped data). Shipped data: 3811 rows with `pub_def == 1` (matching LOG df = 3809) versus 8645 rows with `pub_def >= 1`. Agents should report this as an observation in code review and judge whether it is a bug; it is noted here, not decided.
- S2: M2 restricted to `year <= 2014`. Dyadic MID 4.02 has no disputes after 2014 and ATOP 5.1 has no secret alliances after 2018, so later country-years have values of 0 by construction (`d[is.na(d)] <- 0` and the dispute loop).

## 4. Other observations for code review (not decided here)

- Paper text for M1 says "total number of defensive secret alliances in a given year" and "we sum the total number of MIDs in a given year" (system-year level). The code uses `secret` (all secret alliances, `pubsecr == 2`, not `secret_def`) and correlates at country-year level (N = 17511) with country-level `disputes`.
- Paper text for M2 says disputes are "drawn from the MIDs 5.0 data"; the code uses dyadic MID 4.02 (`dyadic_mid_4.02.csv`).
- `secret_alliances` sums `secret` over all country-years in a year, so an alliance with k members is counted k times (alliance memberships, not alliances).
- replication.R comment for test 2 says "correlation between defensive alliances and concurrent secret alliances" while the code correlates secret alliances with disputes; the paper's sentence matches the code.
- README names the data file `AJPS_rep.RData` and a `codebook.pdf`; the Dataverse has `AJPS_analysis_data.RData` and no project codebook (only the ATOP and MID codebooks).

## 5. Feasibility

- Compute: seconds to a couple of minutes; under 10 MB of data; fine on 2 CPUs / 7 GB.
- Dependencies: R plus logr, common, peacesciencer 1.1.0 (pulls in its own dependencies; may need source builds), tidyverse, foreign; sandwich and lmtest for R_c. At the time of writing `/workspace/mamba/envs/r/bin/Rscript` did not exist on this machine (an R install appeared to be in progress per /workspace/mamba_r_install.log); agents must check R is available first.
- Risks: `create_stateyears()` output depends on the peacesciencer version; `log_open()` path behaviour under Rscript; the ingested `.tab` files must not be used in place of the original CSVs without a documented diff.
- Licence: dataset has custom Dataverse terms ("made available with limited information on how it can be used. You may wish to communicate with the Contact(s) specified before use"), no CC0. The bundled ATOP 5.1 and COW dyadic MID 4.02 data have their own terms of use. Treat as not redistributable: keep raw data in scratch only, commit checksums, links and our outputs, not the data files. The article itself is CC BY 4.0.
