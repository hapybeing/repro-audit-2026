# PREREG: 16_QZNVZ0

Written 2026-10-10 (IST, about 22:50 to 23:20), before any analysis code was run. No analysis code of the authors was executed to write this file. The main text was read in full from the publisher's open-access PDF; all target values below are copied from it. The deposit's files were downloaded and read (notebook source and the saved notebook outputs, readme, CSV header). The only operation on the data was a read-only row and value count of the regression CSV with Python's `csv` module (154,415 data rows, 97 columns, `Top10_Inst` stored as the strings True/False); no model was fit.

- Paper: Zhu, Yuner and Edmund W. Cheng (2025). "Multidimensional Diversity and Research Impact in Political Science: What 50 Years of Bibliometric Data Tell Us". Perspectives on Politics 23(2): 686 to 704 (first published online 2024-12-12, per OpenAlex). DOI https://doi.org/10.1017/S1537592724000641 . CC BY 4.0.
- Text source read: publisher PDF (open access), https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5D73412ABAA95A29464A350713C01FCE/S1537592724000641a.pdf/div-class-title-multidimensional-diversity-and-research-impact-in-political-science-what-50-years-of-bibliometric-data-tell-us-div.pdf , HTTP 200, 2,880,081 bytes, sha256 0266d0bb4881ba4834989aff0622f55f4c26ed17ad8c6f8636347a45021094ba (the PDF carries a per-download watermark, so re-downloads may hash differently).
- Online appendix read (search only, for data locations): https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS1537592724000641/resource/name/S1537592724000641sup001.docx , 510,618 bytes, sha256 0a718395350446356976fd6e04b71026001d4dd16972afe2a7ae144c53414ed7. Not used for targets.
- Dataset: "Multidimensional Diversity and Research Impact in Political Science: What 50 Years of Bibliometric Data Tells Us", Harvard Dataverse, https://doi.org/10.7910/DVN/QZNVZ0 , version 2.0 (released 2024-10-03 UTC), licence CC0 1.0. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/QZNVZ0 (saved as `data_statement_raw/dataverse_QZNVZ0.json`). All files public, none restricted. Every md5 below matched the Dataverse md5.

| file | datafile id | URL | bytes | sha256 |
|---|---|---|---|---|
| Regression.ipynb | 10577538 | https://dataverse.harvard.edu/api/access/datafile/10577538 | 338,571 | b1f3d45a092b29c8db03b13e2616d7bea5f48a99000e7dbd3ced85726d9a8b74 |
| regression_table_anonymous_final.csv | 10577540 | https://dataverse.harvard.edu/api/access/datafile/10577540 | 130,831,029 | 98cb66388c108f6615b6166b872c81c25db0157de374f68857578c0e9325a944 |
| Visualizations.ipynb | 10577537 | https://dataverse.harvard.edu/api/access/datafile/10577537 | 4,850,545 | a4e2d067ab1cda5f030747ecbff6136dd5bcde7439d5c887bc2a21b262b01f0f |
| timelines.tab (ingested) | 10577539 | https://dataverse.harvard.edu/api/access/datafile/10577539 | 13,979 | 3da779d7ed17dc57f49ae9eee74004a000349f71c1cbe1d91f4a6a54344ebe4c |
| timelines.csv (original of 10577539) | 10577539 | https://dataverse.harvard.edu/api/access/datafile/10577539?format=original | 14,025 | 4d4fb26518840bceddf0a5f747a0f5d3c31d21ec567c93d42c8a5bd76fea3c51 |
| journal_scatter.csv | 8940073 | https://dataverse.harvard.edu/api/access/datafile/8940073 | 28,818 | 81904370a03d63da533442e13744db25c7d9d98c47188c8cd0ba4364c5d22bea |
| readme.txt | 8940075 | https://dataverse.harvard.edu/api/access/datafile/8940075 | 1,136 | 80916bfdea37ce0c1a7dce7d5649477aa98576966ebad9772e5be0b68d2d8105 |

Checksums also in `data_statement_raw/prereg_download_checksums.sha256` (scratch copy: /workspace/audit_runs/16_QZNVZ0/prereg/checksums.sha256). Dataverse version 1.0 (2024-04-29 UTC) had a different Regression.ipynb (id 8940078), regression CSV (id 8940077, 131,755,141 bytes), timelines.tab (8940074) and Visualizations.ipynb (8940076). This audit uses version 2.0, the latest; `data_statement_raw/versions.json` lists both.

## 1. Headline results and targets

Main claim (abstract, p. 686): "Papers written by racial/ethnic minorities and Global South scholars are significantly less cited. However, collaborating with outgroup scholars can effectively overcome this citation gap. We also find that papers written by women receive more citations than those written by men, after controlling for journal prestige and research topics. Furthermore, when we limit our investigation to leading universities, citation gaps diminish. However, scholars of African descent continue to experience entrenched citation disadvantages even if they are affiliated with highly prestigious universities."

These claims are reported in Table 2 ("Regression models predicting article citations", p. 697): OLS of log10(citations + 1) on author identity, team diversity, controls and 49 topic shares. The text says "we mainly report model 1's results" (p. 698). In the notebook, Model 1 is `results_1` (cell 4), Model 4 (top 50 institutions) is `results_4` (cell 7). All coefficients are unstandardized OLS B; the notebook uses statsmodels default (nonrobust) standard errors.

| id | quantity (code object) | paper value | decimals | location |
|---|---|---|---|---|
| T1 | B, Gender = Female, Model 1 (`results_1.params["FA_Female"]`) | 0.04 | 2 | Table 2, p. 697, row "Gender = Female", Model 1 column B (printed ".04***", SE "(0)", t 11.0) |
| T2 | B, Hispanic/Latino (ref Anglo-Saxon), Model 1 (`results_1.params["FA_Hispanic/Latino"]`) | -0.07 | 2 | Table 2, p. 697, row "Hispanic/Latino", Model 1 (printed "-.07*** (.01)", t -10.8); prose p. 698 gives -.075, t = -10.8 |
| T3 | B, Region = South, Model 1 (`results_1.params["FA_South"]`) | -0.02 | 2 | Table 2, p. 697, row "Region = South", Model 1 (printed "-.02*** (.01)", t -4.0) |
| T4 | B, Cross-National, Model 1 (`results_1.params["International"]`) | 0.09 | 2 | Table 2, p. 697, row "Cross-National", Model 1 (printed ".09*** (.01)", t 14.8); prose p. 698 gives .088, t = 14.8 |
| T5 | B, African/African American, Model 4 T50 institutions (`results_4.params["FA_African"]`) | -0.09 | 2 | Table 2, p. 697, row "African/African American", Model 4 (printed "-.09*** (.02)", t -4.9) |
| T6 | N, Model 1 (`results_1.nobs`) | 68558 | 0 | Table 2, p. 697, row "N", Model 1 ("68,558") |

Printed table values are pre-registered (brief: prefer table over prose). Secondary context to be reported but not targets: the printed t-values above (1 decimal, the most discriminating printed figure), prose values -.075 (T2) and .088 (T4), Slavic B -.073 t -9.9 (prose p. 698), Adjusted R2 .428 (Model 1) and .422 (Model 4), Model 4 N 16,025.

Mapping notes. Table row "Cross-National" maps to column `International`; "Cross-Racial/Ethnic" to `Cross_Ethnic`; "%Outgroup References" to `Cited_Outgroup`; "Affiliation Prestige" to `FA_Affliation_Weight` (Model 1, 3, 4) or `Team_Affliation_Weight` (Model 2). The mapping is by row order and matching t-values in the saved notebook output; the paper does not name the columns.

Significance. Table 2 prints stars but the extracted text shows no star legend. Pre-registered reading: * p < .05, ** p < .01, *** p < .001, two-sided, from statsmodels nonrobust OLS t-tests (`results_k.pvalues`), as in the saved notebook output ("Covariance Type: nonrobust"). Candidate p-values, first one pre-registered: (1) nonrobust OLS p; (2) heteroskedasticity-robust p (not in the authors' code, report only if computed in R_c-style exploration and labelled exploratory).

Conclusion criterion for `same_conclusion`:
- T1, T4: B > 0 and nonrobust p < .001.
- T2, T3, T5: B < 0 and nonrobust p < .001.
- T6: `same_conclusion` true if N is within 1% of 68,558 (686 rows); `match_to_rounding` needs exact equality. Under CHANGELOG #6(a) an N-only mismatch with matching estimates is classed C, not D.

Inconsistencies noticed while reading (described, not judged). The saved notebook outputs in Regression.ipynb (version 2.0, run dated "Sat, 28 Sep 2024") were compared with Table 2:
1. Model 2 N: Table 2 prints 68,558 for Model 2; the saved output of `results_2` shows "No. Observations: 39690".
2. Model 2 "Others": Table 2 prints "-.005 (.01)" with t -2.7; the saved output shows Team_Other t -0.372 and Team_South t -2.651 (Table 2 prints -2.7 for both rows).
3. Stars that differ from the saved p-values: Model 1 "Others" printed ** (saved p 0.000, t -3.806); Model 2 "%Outgroup References" printed * (saved p 0.099); Model 4 "Others" printed * (saved p 0.158); Model 3 "Author Reputation" (t 9.4) and "Author Publication" (t 4.3) printed with no stars (saved p 0.000). None of these rows is a target.
4. Model 3 has no "Region = South" estimate in Table 2, and the notebook's model_3 regressor list omits `FA_South` (models 1, 2, 4 and S1 to S4 include it). The text does not mention this.
5. Several SEs are printed as "(0)" (e.g. T1); the saved SE for FA_Female is 0.004.
6. The deposit readme gives the title "Diversity, Inequality, and Opportunity Structure in Political Science: What 50 Years of Bibliometric Data Tells Us"; the article title differs.
7. The article reports 211,425 articles in the corpus (p. 686); the regression CSV has 154,415 rows; 153,470 have a non-empty `FA_Ethnicity`. The 68,558 model rows come from `missing='drop'` on the regressors. The construction of the regression table from the raw WoS records (name-based ethnicity, gender, topic model) is not in the deposit; the readme describes the deposit as the analysis data plus notebook "log files".
8. Model 2 (team-based) is filtered on non-missing `FA_Ethnicity` (first-author variable), the same row filter as Model 1, with team-based regressors.

## 2. Reproduction plan

Only `Regression.ipynb` produces the targets. It has 13 cells: cell 0 imports pandas, numpy, statsmodels.api; cell 1 `pd.read_csv('regression_table_anonymous_final.csv', index_col=0)`; cells 2 and 3 display columns and head; cells 4 to 7 fit Models 1 to 4 (Table 2); cells 8 to 11 fit S1 to S4 (top 20, 30, 40, 100; appendix Table S7); cell 12 empty. Each model is `sm.OLS(np.log10(y + 1), X, missing='drop').fit(maxiter=100)`. No randomness, no seed.

Steps:
1. Fresh venv: `python3 -m venv /workspace/audit_runs/16_QZNVZ0/<AGENT>/venv`; `pip install pandas numpy statsmodels nbconvert ipykernel` (for executing the notebook). No versions are pinned in the deposit; the notebook metadata records only Python 3.11.9 (kernel "Python 3 (ipykernel)", Windows path in a warning). So current releases are tried first. If cell 4 to 7 fail on current pandas/statsmodels (for example `fit(maxiter=...)` rejected), the allowed fix is to install the newest pandas and statsmodels releases that were current on 2024-09-28 (pandas 2.2.x, statsmodels 0.14.x, numpy 1.26.x or 2.1.x), recorded as an env fix.
2. Place `regression_table_anonymous_final.csv` in the working directory (name matches the read call; no path mapping needed).
3. Execute the notebook unchanged with `jupyter nbconvert --to notebook --execute Regression.ipynb --output outputs/Regression_executed.ipynb`, or extract the 13 code cells verbatim into `scripts/regression_verbatim.py` and append (after the authors' lines, changing none) an extraction block that writes, for `results_1`, `results_2`, `results_3`, `results_4`, `results_S1` to `results_S4`: params, bse, tvalues, pvalues, nobs, rsquared_adj to `outputs/regression_estimates.csv`. The appended block is recorded as a diff. Either way, `scripts/build_results.py` parses `outputs/regression_estimates.csv` (or the executed notebook's summaries) into results.json.
4. Target sources: T1 `results_1.params["FA_Female"]`; T2 `results_1.params["FA_Hispanic/Latino"]`; T3 `results_1.params["FA_South"]`; T4 `results_1.params["International"]`; T5 `results_4.params["FA_African"]`; T6 `results_1.nobs`.
5. Not needed for targets: `Visualizations.ipynb` (reads `timelines.csv` and `journal_scatter.csv`, plotly figures). If run, `timelines.csv` is the `?format=original` download of datafile 10577539 (Dataverse ingests it as `timelines.tab`); using the original is a path-only fix. The `.tab` is an alternative file but its format differs (tab separated).

Allowed environment fixes: package versions; working directory; running cells as a script with `print()` around `.summary()` if needed for capture. No change to row filters, regressor lists, outcome transform or `missing='drop'`.

Memory: CSV 131 MB, 154,415 x 97, about 0.2 to 0.4 GB as a DataFrame (one string column `Journal`, mixed-type `Journal_Rank`); each model copies at most 68,558 x 71 floats (about 40 MB). Peak expected under 1.5 GB. Pre-registered fallback if peak exceeds about 3 GB: add `usecols=` (the 80 columns the models use plus the index column) to the `read_csv` call only, recorded as an env fix; estimation lines unchanged. There are no seeds to preserve.

## 3. Robustness checks (pre-registered)

Primary quantity for all three checks: T2, B for `FA_Hispanic/Latino` in Model 1 (the largest gap named in the text). Each check also reports T1, T3, T4 (Model 1) as secondary, in `note` and in the check's output file. Estimation sample for Model 1 = the rows `results_1` actually used (`results_1.model.data.row_labels`, expected 68,558). Same regressors, same outcome `log10(Citations_Received + 1)`, same `sm.OLS`.

"Same direction and significance as paper" for the primary: B < 0 and p < .001 (paper prints ***). For secondaries: same sign as Table 2 and p < .001.

R_a. Nonparametric case bootstrap. `rng = numpy.random.default_rng(20261010)`; draw 1,000 resamples of the Model 1 estimation rows with replacement (`rng.integers(0, n, n)`), refit OLS with the identical columns on each, record B for `FA_Hispanic/Latino`. Report: estimate = full-sample B; `se_or_ci` = bootstrap SE and percentile 95% CI (2.5th, 97.5th percentiles); p_value = min(2 x share of bootstrap B >= 0, 1), reported as < 0.001 when zero of 1,000 cross (record the count). Same direction and significance = full-sample B < 0, the percentile 95% CI excludes 0, and none of the 1,000 bootstrap B is >= 0 (bootstrap p < .001 at this resolution). Rank-deficient resamples are counted and reported, not replaced.

R_b. Outlier exclusion on the outcome. The outcome is continuous. On the Model 1 estimation rows compute y = log10(Citations_Received + 1), z = (y - mean(y)) / sd(y) with sd ddof = 1; drop rows with |z| > 3; refit Model 1 unchanged on the rest. Report B, nonrobust SE, p for the primary and secondaries, and the number of rows dropped. Secondary for T5: the same rule applied within Model 4's own estimation rows, refit Model 4.

R_c. Alternative estimator for the count outcome: Poisson pseudo-maximum likelihood. On the Model 1 estimation rows, fit `sm.GLM(Citations_Received, X, family=sm.families.Poisson()).fit(cov_type="HC1")` with X identical to Model 1 (same 71 columns including `Const`), outcome the raw citation count instead of log10(count + 1). Report the coefficient (log-scale) for `FA_Hispanic/Latino`, its HC1 SE and p. Same direction and significance = coefficient < 0 and p < .001. Magnitudes are on a different scale and are not compared with Table 2. If IRLS fails to converge within statsmodels defaults, rerun once with `maxiter=300` and report that; if it still fails, report not run with the error.

## 4. Known risks

- Missing files: none for the targets. Every file the two notebooks read is in deposit version 2.0 (`timelines.csv` only as the original-format download of the ingested `timelines.tab`). The upstream data-construction code is not deposited, so the regression table itself cannot be rebuilt; this does not affect the targets.
- Inconsistency 1 (Model 2 N 68,558 printed vs 39,690 in the saved output) and the star mismatches are outside the targets; agents report them, they do not change the class.
- Dependencies: pure Python (pandas, numpy, statsmodels); no Stata or proprietary software. Version drift is unlikely to change OLS estimates; `fit(maxiter=100)` is passed as an unused keyword and could raise on some statsmodels versions (see fix in section 2).
- `Top*_Inst` columns are True/False strings in the CSV, parsed as bool by pandas; a pandas version that parses them as object would change Model 3 and 4 row filters (would show as N different from 5,249 / 16,025). Report if so.
- Compute: seconds per model; R_a about 1,000 OLS fits on 68,558 x 71, a few minutes on 2 CPUs.
- Paper read in full; no access problem.
