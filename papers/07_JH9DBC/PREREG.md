# PREREG: 07_JH9DBC

Written 2026-10-10 (IST, about 17:20 to 17:55), before any analysis code was run. No analysis code (the authors' `replication.R` or any model fit) was executed to write this file. Deposit files were downloaded and read as text; the only data inspection was reading column headers and counting rows/missing cells per column in `data.tab` (no model, no summary statistic of any analysis variable).

## Paper and text source

- Paper: Ang, M. (2025). "Guilty by association: Party effects of corruption-related prosecutions". Party Politics, OnlineFirst, first published online 2025-08-13 (no volume, issue or pages assigned; Crossref metadata `prereg_raw/crossref_work.json`). DOI https://doi.org/10.1177/13540688251366827
- Dataset: "Replication Data for: "Guilty by association: Party effects of corruption-related prosecutions", Harvard Dataverse, https://doi.org/10.7910/DVN/JH9DBC , version 2, released 2025-08-18, licence CC0 1.0 (`prereg_raw/dataverse_JH9DBC.json`).

### What text could be read (stated plainly)

**The main article text (including Table 2, the table that reports the abstract's headline result) could NOT be read.** The Sage article is "Restricted access". OpenAlex lists it as bronze OA (`prereg_raw/openalex_work.json`), but on 2026-10-10 every public route failed:
- `curl` of https://journals.sagepub.com/doi/pdf/10.1177/13540688251366827?download=true : HTTP 403 Cloudflare page (11:50 UTC).
- Public web fetch of https://journals.sagepub.com/doi/full/10.1177/13540688251366827 : abstract page only, banner "Restricted access", "You currently have no access to this content" (about 11:51 UTC).
- Public browser, no sign-in (about 11:55 to 12:05 UTC): /doi/pdf/ and /doi/epub/ both redirect to the restricted abstract page (`prereg_raw/browser_access_check_findings.md`).
- Europe PMC search `DOI:10.1177/13540688251366827`: 0 hits. Semantic Scholar: no open-access PDF. UPF e-Repositori DSpace search `"Guilty by association" Ang` : 0 results (`prereg_raw/upf_search.json`, 11:52 UTC). Wayback Machine availability API for the Sage abs/full/pdf/epub/supplement URLs: no snapshots (11:53 UTC).
- No sign-in was attempted (audit rule).

What WAS read:
1. The publisher abstract page (public): the abstract and the data availability statement, copied verbatim below.
2. The publisher's **Supplementary Material** PDF, `sj-pdf-1-ppq-10.1177_13540688251366827.pdf` (15 pages, page labels i to xv), https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F13540688251366827&file=sj-pdf-1-ppq-10.1177_13540688251366827.pdf . It opens freely in a browser but could not be downloaded to the workspace (curl and fetch: Cloudflare 403), so **no sha256 of the PDF exists**. Instead: a browser agent transcribed Tables A, B and G at 200% zoom (`prereg_raw/browser_supplement_transcription.md`), and I checked every target value myself against saved browser screenshots: `prereg_raw/screenshots/supp_p05_tableA.png`, `supp_p06_tableB.png`, `supp_p13_tableG_top.png`, `supp_p13_tableG_bottom.png` (sha256 in `prereg_raw/checksums_prereg_raw.sha256` (paths relative to prereg_raw/)). The transcription and the screenshots agree on every target digit, sign and star.

Not used: a search-engine excerpt (Exa index) that appeared to contain the text of the main Table 2 with minus signs stripped. It was not a page I could open (the Exa library page shows the abstract only), so no number from it is used anywhere in this audit. An author draft from 2019 (https://ijlinz.es/wp-content/uploads/2019/03/Ang_Guilty_by_Association_draft.pdf) is a different, earlier version and is not used as a source of paper values.

Agents A and B: before comparing, re-open the supplement PDF in a browser (no sign-in) and confirm the six values below; if you can obtain the main article text through any public route, record the Table 2 values in your LOG.md as secondary context, but the pre-registered targets stay as written here.

## Dataset files (downloaded 2026-10-10 11:50 UTC, curl -L -A "repro-audit-2026"; scratch copy /workspace/audit_runs/07_JH9DBC/prereg/)

| file | datafile id | URL | bytes | sha256 |
|---|---|---|---|---|
| `replication.R` | 11944076 | https://dataverse.harvard.edu/api/access/datafile/11944076 | 19675 | 41a35296a741dc6efa63889290687a87f653aec443aecf2a8273069bc100d80c |
| `data.tab` (Dataverse ingested archival copy) | 11944075 | https://dataverse.harvard.edu/api/access/datafile/11944075 | 124613 | e67fa38a7a92b96e8cc040a1e6fdf24501d7a0ecea072f6f0a882a80c7004c26 |
| `data.dta` (original upload, Stata 14 format) | 11944075 | https://dataverse.harvard.edu/api/access/datafile/11944075?format=original | 257682 | a47e2c054847cae7d4f1a7f52e6ff82ea88816e9039491b1371b115c758a971a |
| `codebook.pdf` | 11946518 | https://dataverse.harvard.edu/api/access/datafile/11946518 | 78418 | d4c1c47bf168610a7f80e5cd30cb7108058b57ecbb2fb84744c37ea4c0f07a8a |

MD5 of `data.dta` (1c212f761e5be7a0df6c91fec65544f9), `replication.R` and `codebook.pdf` match the MD5s in the Dataverse metadata. No README in the deposit; the codebook defines the variables. `data.dta` is a Stata-format file but is read in R with `haven::read_dta`; Stata itself is not needed.

## 1. Headline result and targets

Abstract (verbatim, publisher abstract page): "I find a robust association: legislative candidates in districts of criminal governors received between 3 and 6% less votes than candidates in districts with no criminal governors."

The abstract's claim is reported in the main text's Table 2 (multilevel models, `model1` to `model4` in `replication.R` lines 32 to 79), which could not be read. The targets are therefore taken from the two published supplementary tables that re-estimate the Table 2 specifications and that `replication.R` also produces:
- Table B (supplement p. vi): the same four specifications as fixed-effects models with standard errors clustered by district (`model1B` to `model4B`, lines 249 to 292, `fixest::feols`).
- Table G (supplement p. xiii): the Table 2 multilevel specifications on the subset of states with a gubernatorial election (`model1G` to `model4G`, lines 568 to 622, `lme4::lmer`).

The estimand in all of them is the difference-in-differences interaction "Indicted x Year 2018" (`juicio:year_2018`): the change in the vote share of the governor's party's legislative candidates in 2018 relative to 2015 in districts of indicted governors. Values are vote-share proportions (0.052 = 5.2 points), matching the abstract's "between 3 and 6%" in units.

| id | quantity | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Table B Model 1 (FE, socioeconomic controls), coefficient "Year 2018 x Indicted" | -0.052 (SE 0.014, ***) | 3 | Supplement p. vi, Table B, row "Year 2018 x Indicted", column "Model 1" |
| T2 | Table B Model 2 (FE, + economic growth and homicides), coefficient "Year 2018 x Indicted" | -0.066 (SE 0.014, ***) | 3 | Supplement p. vi, Table B, row "Year 2018 x Indicted", column "Model 2" |
| T3 | Table B Model 3 (FE, + Scandal and Scandal x Year 2018), coefficient "Year 2018 x Indicted" | -0.034 (SE 0.019, no star) | 3 | Supplement p. vi, Table B, row "Year 2018 x Indicted", column "Model 3" |
| T4 | Table B Observations (all four models) | 600 | 0 | Supplement p. vi, Table B, row "Observations" (FE district 307 groups, FE party 5 groups) |
| T5 | Table G Model 2G (multilevel, election-states subset), coefficient "Indicted x Year 2018" | -0.051 (SE 0.017, **) | 3 | Supplement p. xiii, Table G, row "Indicted x Year 2018", column "Model 2G" |
| T6 | Table G Observations (all four models) | 297 | 0 | Supplement p. xiii, Table G, row "Observations" (district 152 groups, party 3 groups) |

Table notes (verbatim). Table B: "***p < 0.001; **p < 0.01; *p < 0.05. Fixed effects by party and district. Standard errors clustered by" (the line is cut at the page edge in the PDF; the section heading says "Models estimated with clustered standard errors by district"). Table G: "***p < 0.001; **p < 0.01; *p < 0.05".

Secondary context, not targets: Table B Model 4 interaction -0.066*** (0.014); Table G Model 1G -0.045** (0.017), 3G -0.006 (0.024), 4G -0.051** (0.017); Table A (p. v) N = 900 for every variable, Indicted mean 0.13, Year 2018 mean 0.33.

### Conclusion criterion for `same_conclusion`
- T1, T2, T3, T5 (coefficients): same_conclusion = true if the reproduced estimate has the same sign as the paper (negative) AND falls on the same side of p = 0.05 as the paper's stars imply (T1, T2, T5 significant at p < 0.05; T3 not significant, p >= 0.05). Whether the star band also matches (*** for T1, T2; ** for T5) is recorded in `note` but does not decide same_conclusion.
  - p-values for T1 to T3 are those `fixest` reports for the model as the authors' code fits it (default vcov, which for `feols` with fixed effects clusters by the first fixed effect, `unique_id`; t distribution as fixest computes it). Agents must record which vcov fixest actually used (`summary(model2B)` header).
  - p-value for T5: `lmer` gives no p-value. Use the two-sided normal (Wald z) p-value from estimate/SE as the primary; also report the lmerTest Satterthwaite p-value in `note` (secondary, does not decide).
- T4, T6 (N): same_conclusion = true only if `nobs()` equals the paper value exactly.
- Overall headline check (recorded in `note` of T2, not a target): the reproduced Table 2 interaction estimates for `model1`, `model2`, `model4` (multilevel, not comparable to a paper value because Table 2 is unread) are negative and their magnitudes lie between 0.03 and 0.06 rounded to two decimals, as the abstract states.

### Inconsistencies noticed while reading (described, not judged)
- Table A (supplement p. v) reports N = 900 for every variable including "Candidate's experience". In `data.tab`, `prev_exp_fleg` is blank for all 300 rows with elec_year 2012 (and `distrito` is blank for the same rows), so 600 non-missing values exist. Also, `replication.R` lines 199 to 207 compute the Table A summaries on `data` (2015 and 2018 only, 600 rows), whereas a Year 2018 mean of 0.33 and N = 900 correspond to the 900-row `dataall`.
- Table G row label "Indicted x Scandal" (Model 3G) vs. the code for `model3G` (line 596), which has `mentions_prop*year_2018` (Scandal x Year 2018), as in Table B Model 3 ("Scandal x Year 2018").
- Table G labels the grouping rows "FE district (no. groups)" and "FE party (no. groups)" although the models are random-intercept models (`(1|unique_id) + (1|partido_gober)`) and the table also reports Var(districts) and Var(parties).
- Code header comment (line 4) gives the DOI as 10.1177/1354068825136682 (one digit shorter than the article DOI 10.1177/13540688251366827).
- The code reads `data.dta`, while the Dataverse file list shows `data.tab` (ingested); the original `.dta` is only obtained with `?format=original`.
- Data availability statement says materials "will be made available in public repositories upon publication" and names no repository (see DATA_STATEMENT.md).
- Supplement Table B note line is cut at the page edge after "clustered by".

## 2. Reproduction plan

Single script, `replication.R`, run top to bottom in one R session with the working directory set to the folder holding `data.dta`.

1. Download `data.dta` with `https://dataverse.harvard.edu/api/access/datafile/11944075?format=original` (save as `data.dta`; verify sha256 a47e2c05...). Do not use `data.tab` as the input. Download `replication.R` (11944076). Verify sha256s against the table above.
2. Packages: haven, tidyr, dplyr, lme4, fixest, sjPlot, cobalt (all `library()`), plus WeightIt (called as `WeightIt::weightit`, line 214, never loaded). Install into a per-run library. No versions are pinned in the deposit and no sessionInfo is given (code dated "August 2025"); use current CRAN versions and record them. lmerTest is needed only for the secondary Satterthwaite p-value in the extraction script, not for the authors' code.
3. Line 18: `read_dta("data.dta")`; lines 21 and 22: `data` = rows with year_2012 == 0 (expected 600 rows, 307 districts, 5 parties).
4. Lines 32 to 79: Table 2 models (`model1` to `model4`). Lines 84 to 193: Figure 1 (`bootMer`, nsim = 1000, no seed set before it; figure only). Lines 211 to 242: Figure A. Lines 249 to 292: Table B (`model1B` to `model4B`). Lines 299 to 397: Tables C, D. Lines 402 to 486: Figure B placebo (`set.seed(100)`, 100 lmer fits). Lines 490 to 562: Table F. Lines 568 to 622: Table G (`model1G` to `model4G`).
5. The script prints nothing to file; models live in the session. Run as `Rscript -e 'source("replication.R", echo=TRUE, max.deparse.length=Inf); save.image("outputs/session.RData")'` with stdout/stderr logged to `outputs/`. Plots go to `Rplots.pdf` in a non-interactive session; keep it in `outputs/`.

Where each target comes from (extraction script `scripts/extract_targets.R`, loads `outputs/session.RData`, writes `outputs/targets_extracted.csv` with estimate, SE, p, vcov type and nobs):
- T1, T2, T3: `coeftable(model1B)`, `coeftable(model2B)`, `coeftable(model3B)`, the interaction term (expected name `juicio:year_2018`; `juicio` itself is dropped as collinear with the district fixed effect). Record `summary(modelxB)$se_type` or the vcov line.
- T4: `nobs(model1B)` (and confirm the same for 2B to 4B).
- T5: `fixef(model2G)["juicio:year_2018"]`, SE from `sqrt(diag(vcov(model2G)))`, Wald z p-value; Satterthwaite p from `lmerTest::as_lmerModLmerTest(model2G)` in `note`.
- T6: `nobs(model2G)` (and confirm for 1G, 3G, 4G).
- Also write `model1`, `model2`, `model4` (Table 2) interaction estimates and SEs to the CSV for the headline note.

Allowed environment fixes (each as a diff): installing packages; setting the working directory; a no-op wrapper if a plot device fails in a headless session. Not allowed: any change to models, data filters, or seeds.

## 3. Robustness checks (pre-registered)

All three checks target T2 (Table B Model 2, `model2B`: the specification the supplement itself uses as the reference "model 2 of table 2" for the placebo and Table F). Each check fits the identical `feols` formula of lines 258 to 267 on the 600-row `data` unless stated. Paper reference: -0.066, p < 0.001. "Same direction and significance" = estimate < 0 and p < 0.05 (or, for R_a, the 95% percentile interval excludes 0). Each check also reports, as secondary, the same quantity for the multilevel Table 2 Model 2 (`model2`, lines 42 to 52), which has no readable paper value.

**R_a. Cluster (district) bootstrap.** `set.seed(20261010)` once; 1000 replicates; in each, sample the 307 `unique_id` values with replacement, stack all rows of each drawn district, give each draw a new district id (so duplicates are separate fixed-effect groups), refit `model2B`'s formula with fixed effects `new_id + partido_gober`. Record the interaction coefficient per replicate. Report the original-sample estimate as `estimate`, the 2.5th and 97.5th percentiles as `se_or_ci`, the bootstrap SE, and as `p_value` min(1, 2 x min(share of replicates >= 0, share <= 0)). Replicates where the interaction is not estimable (e.g. no indicted district drawn) are counted and reported, not replaced. Pass = estimate < 0 and percentile CI excludes 0.

**R_b. Outlier exclusion on the outcome.** The outcome `voto_pro_gober` is continuous (a vote share), so the default rule applies: compute z = (y - mean(y)) / sd(y) over the 600 rows of `data`; drop rows with |z| > 3; refit `model2B`; report estimate, fixest default SE, p, rows dropped, and nobs. Stated now in case the rule drops no rows: if |z| > 3 drops 0 rows, R_b is reported as run with 0 rows dropped (estimate identical to the reproduced T2), and additionally a pre-specified secondary trim drops rows below the 1st or above the 99th percentile of `voto_pro_gober` (type-7 quantiles over the 600 rows) and refits; this secondary result is reported in `note` and does not replace the primary. Pass = estimate < 0 and p < 0.05.

**R_c. Standard errors clustered by state.** Treatment (`juicio`) is assigned at the state level (4 indicted states: Veracruz, Chihuahua, Sonora, Quintana Roo in the 2015/2018 data), while the authors cluster by district. Refit `model2B` unchanged and compute inference with `vcov = ~id_estado` (32 state clusters; fixest small-sample defaults). Report estimate (identical point estimate), state-clustered SE, p, and the number of clusters. Pass = estimate < 0 and p < 0.05. Secondary in `note`: the same for `model2` (multilevel) is not computed, since lmer has no cluster option; write "not applicable".

## 4. Known risks

- **Main text unread.** The headline Table 2 numbers are not in this pre-registration. The audit can only compare the supplementary Tables B and G. If no target in the supplement could be verified, the paper would have no readable target; that is not the case here, but the classification will rest on supplementary tables, and the report should say so.
- **Supplement not hashed.** The supplement PDF could not be saved to disk (Cloudflare), so the paper values rest on screenshots (hashed) plus a transcription. A later change of the PDF on Sage would not be detectable from a checksum.
- **Data file format.** `replication.R` reads `data.dta`; an agent who downloads the default (ingested `data.tab`) would hit "file not found" or read different types. Use `?format=original`.
- **Missing package call.** `WeightIt` is used via `::` but not loaded; it must be installed or the script stops at line 214, before Tables B and G. An install is an environment fix; running the later sections without Figure A would need a documented diff.
- **Figure B loop.** `get_model_data(mod, ...)[7, c(2,5,6)]` (line 438) depends on sjPlot's output row order; a different sjPlot version could change or break it. This is before Table F and G in the script. If it errors, the allowed fix is to run the remaining sections (Tables F and G) after it in the same session, recorded as a deviation; models in Table G do not depend on the loop.
- **Randomness.** Table B and G estimates are deterministic (no random step). `bootMer` (Figure 1, no seed) and the placebo loop (seed 100) only affect figures.
- **Compute.** Small: 600 rows. 2 x 1000 `bootMer` refits plus 100 placebo lmer fits, minutes on 2 CPUs. R_a: 1000 `feols` refits, about 1 minute.
- **Dependencies.** All on CRAN (fixest and lme4 compile C++; sjPlot pulls many packages). No Stata or proprietary software needed.
- **Licences.** Dataset CC0 1.0. Article copyright the author, restricted access.
