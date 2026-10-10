# PREREG: 25_914AN0

Written 2026-10-11 about 02:15 IST, before any analysis code was run. No R or Python analysis code was executed to write this file (files were only downloaded, hashed, listed and read; no package was installed; data_divisionlevel.RDS was not decompressed or loaded).

The main text was read in full. Its headline Soviet numbers are printed only in prose (Figure 1 is a coefficient plot); the printed table with these estimates (Table A2.3) and the war-level table (Table A6.17) are in the authors' online appendix, which is NOT the file Cambridge hosts as "supplementary material" (see Sources and Inconsistencies). Targets below copy the appendix table values; the prose values are recorded beside them.

## Sources

- Paper: Lyall, Jason, and Yuri M. Zhukov. 2025. "Fratricidal Coercion in Modern War." International Organization 79(1): 173-192. DOI https://doi.org/10.1017/S002081832400033X (open access, CC BY 4.0).
- Text read (publisher PDF): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/FD297F9402D9C3E599F68CA114DA1313/S002081832400033Xa.pdf/div-class-title-fratricidal-coercion-in-modern-war-div.pdf , HTTP 200, 525,088 bytes, sha256 926451f9c4bc04a176458d301e739de8bb659acd7e65116a0321e6f517c457d8. Page numbers below are printed journal pages.
- Cambridge "Supplementary Material" (the link the article gives on p. 191): https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS002081832400033X/resource/name/S002081832400033Xsup001.pdf , 2,797,413 bytes, sha256 f59c6098705cc917eb29f1cf50a0edfcd7aaf2cf3608122e17d6994380e214b5. It is a 28-page author manuscript dated October 22, 2024 (main text only, no appendix tables).
- Online appendix with the tables (author-hosted, found by web search; not linked from the article): https://zhukovyuri.github.io/files/2024_LyallZhukov_appendix.pdf , "Appendices: Fratricidal Coercion in Modern War", 36 pages, PDF creation date 2024-09-03, 1,603,062 bytes, sha256 c9ad51f649253cd5250d6d3d9fcad5756d1adf4ffebb63ee08e623384bc9582c. Linked as "Appendix" from https://zhukovyuri.github.io/publications/ . Its Tables A2.3 and A6.17 print the same numbers as the authors' own output files `results/tabA2_3.tex` and `results/tabA6_17.tex` inside the deposit's `Replication_IO.tar.xz` (generated 2024-09-27).
- Dataset: "Replication Data for: Fratricidal Coercion in Modern War", Harvard Dataverse, https://doi.org/10.7910/DVN/914AN0 , version 1.0, released 2024-10-15, Dataverse licence CC0 1.0 (the README says CC-BY-NC-SA, see Inconsistencies). File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/914AN0 (copy: `data_statement_raw/dataverse_914AN0.json`). All 10 files downloaded with `?format=original`, User-Agent "repro-audit-2026"; md5 of each matches the Dataverse md5. sha256 list: `prereg_download_checksums.sha256` (scratch copy in /workspace/audit_runs/25_914AN0/prereg/).

| datafile id | path | URL | bytes | sha256 |
|---|---|---|---|---|
| 10577249 | data/data_divisionlevel.RDS | https://dataverse.harvard.edu/api/access/datafile/10577249 | 33,141,809 | 5bde93bb0fdb41be9c3515126c92efc08081574b80973589ea3dda0f241da771 |
| 10577250 | data/data_battlelevel.RDS | https://dataverse.harvard.edu/api/access/datafile/10577250 | 264,153 | 4c532aff34d173e8b3614de6e00541209b36d8fe283b7050c360b721de931bc3 |
| 10577252 | data/data_warlevel.RDS | https://dataverse.harvard.edu/api/access/datafile/10577252 | 23,565 | 115296fa97e98001aada17d6272b00674d64cf76862207153b221b5a69fc53b1 |
| 10577251 | data/fronts_ref.RDS | https://dataverse.harvard.edu/api/access/datafile/10577251 | 1,645 | 03b8c4e57c9988f94d0b4e077889d37906d765e7f92a2535ddfe336d622509c1 |
| 10577247 | code/functions.R | https://dataverse.harvard.edu/api/access/datafile/10577247 | 24,048 | 28b5af1bd14d8bba9c907cb500f08c4357d438e2dc455eb21683391b575c5f8e |
| 10577253 | code/master.R | https://dataverse.harvard.edu/api/access/datafile/10577253 | 1,032 | 2852b2b9647815b23decd7ea931616462982e6781a5951da9fb82380455d7aeb |
| 10577246 | code/run1_setup.R | https://dataverse.harvard.edu/api/access/datafile/10577246 | 2,045 | c36efa3f2c678dc272b51026f250c19773778394b891a376e77bd3495931ccda |
| 10577248 | code/run2_main.R | https://dataverse.harvard.edu/api/access/datafile/10577248 | 111,887 | 1c73e9014685efa8de61da5d7d16fd98d11abb43be8c5af468289259afad382b |
| 10577255 | README.md | https://dataverse.harvard.edu/api/access/datafile/10577255 | 9,789 | 7ca196560f3e4d392be85fe6add6054db7c6ffb5f8d9f4a1a1f2c189a719bb80 |
| 10577256 | Replication_IO.tar.xz | https://dataverse.harvard.edu/api/access/datafile/10577256 | 31,463,800 | a205d9a97daccf8f8244efd5a4cb2f793301d24a5ffb0386b050d236737fa1b2 |

`Replication_IO.tar.xz` (70 entries) contains the same README, 4 code files and 4 data files (each byte-identical to the loose copies, checked by sha256 of the streamed tar members) plus `results/` with the authors' own outputs (19 .tex tables, 41 .png figures). The gzip trailer of `data_divisionlevel.RDS` gives an uncompressed serialized size of 887,881,680 bytes (read from the last 4 bytes; the file was not decompressed).

## 1. Headline results and targets

Abstract main claim: "coercion keeps some soldiers from fleeing the battlefield, but at the cost of higher casualties and reduced initiative", and "countries employing fratricidal coercion are less likely to win wars." Reported by Figure 1 (p. 179; prose p. 180) with full estimates in appendix Table A2.3 (three-way fixed effects, outcome = percent of a division's monthly losses, regressor log(NKVD OO/SMERSH + 1), weights = number of personnel records), and for wars by appendix Table A6.17 (text p. 189).

| id | quantity | paper value | decimals | location | code object |
|---|---|---|---|---|---|
| T1 | NKVD coefficient, MIA share (MIA_100), FE pop-weights model | -1.432 | 3 | Appendix Table A2.3 (p. A6), row "Estimate", column MIA. Prose p. 180: "1.4-percentage-point decline" | `mermods[model_name=="FE pop weights" & outcome_name=="MIA_100", b]` = coefficient on `log(NKVD_OO + 1)` from `lfe::felm(model_fe, weights=N_SOLDIERS, exactDOF=T)` in `ensemble_modz` (functions.R lines 287-303), called at run2_main.R line 68 |
| T2 | NKVD coefficient, KIA share (KIA_100) | 0.629 | 3 | Appendix Table A2.3 (p. A6), column KIA. Prose p. 180 says 0.52 (see Inconsistencies) | same, `outcome_name=="KIA_100"` |
| T3 | NKVD coefficient, medals for valor share (WMED_100) | -0.287 | 3 | Appendix Table A2.3 (p. A6), column Medals. Prose p. 180 says -0.34 (see Inconsistencies) | same, `outcome_name=="WMED_100"` |
| T4 | NKVD coefficient, POW share (POW_100) | -0.176 | 3 | Appendix Table A2.3 (p. A6), column POW. Prose p. 180: "0.2-percentage-point decline" | same, `outcome_name=="POW_100"` |
| T5 | N (division-months) in the FE pop-weights models | 15142 | 0 | Appendix Table A2.3 (p. A6), row N (same for all 7 outcomes; Table A2.4 also prints 15142) | `mermods[model_name=="FE pop weights", n]` = `mod_fe["N"]` |
| T6 | Blocking units coefficient, P(victory), war-level LPM (Model 1) | -0.495 | 3 | Appendix Table A6.17 (p. A34), Model 1 "Victory", row "Blocking Units"; appendix text p. A34 "by 0.495"; article p. 189: "The probability of victory is 0.5 lower" | `mod_out[model_name=="Model 1" & x=="blocking", b]` from `fixest::feols(c(outcome_win,outcome_lose,outcome_other) ~ blocking + cinc + log(deploy_dist+1) + polity2_new + opp_geneva | name + decade, cluster=~name+conflict)`, run2_main.R lines 1381-1388 |

Statistic candidates where the paper is ambiguous (first listed is pre-registered):
- T2: (1) 0.629, Table A2.3; (2) 0.52, prose p. 180 ("increased the share of troops killed by 0.52 percentage points"; footnote 31 uses 0.0052).
- T3: (1) -0.287, Table A2.3; (2) -0.34, prose p. 180.
- T1, T4: table and prose agree after rounding (-1.432 vs 1.4; -0.176 vs 0.2). Desertion (-0.058 in Table A2.3, 0.06 in prose) is consistent and is context only, not a target.
- T6: table -0.495, article prose 0.5 (rounded); consistent.
- Inference: the paper reports 95% CIs, computed in the code as b +/- 1.96 x SE (felm default IID SE for T1 to T4; fixest two-way clustered SE for T6). No p-values are printed for these targets.

Other N values printed for related samples (context, not targets): 21,241 division-months total and 16,330 with combat information (p. 177); Table A2.3 Unit FE 982, Battle FE 129, Month FE 47; Table A6.17 N = 191, Country FE 90, Decade FE 7.

Conclusion criterion for `same_conclusion`:
- T1, T3, T4: reproduced b < 0 and its 95% CI (b +/- 1.96 x SE, as the code computes `l`, `u`) excludes 0.
- T2: reproduced b > 0 and 95% CI excludes 0.
- T5: same conclusion if N is within 5 of 15142 (an N-only mismatch with matching estimates is read under CHANGELOG #6a).
- T6: reproduced b < 0 and 95% CI (b +/- 1.96 x clustered SE, from `l`, `u` in `betamat`) excludes 0.

Inconsistencies noticed (described, not judged):
1. Prose p. 180 gives KIA +0.52 and medals -0.34; appendix Table A2.3 and the deposited `results/tabA2_3.tex` give 0.629 and -0.287. The same prose values appear in the October 2024 manuscript (Cambridge supplementary file, p. 11). MIA, POW and desertion prose values match the table.
2. The article (p. 179, Figure 1 note) points to "Table A3.3"; the appendix numbers the table A2.3. Figure 3 note (p. 188) points to "Table A6"; text p. 188 cites "Figure 6, last row" for LER, while the article's cross-national figure is Figure 3 (README calls it Figure 5, the manuscript numbering).
3. The article says supplementary material is at the Cambridge DOI; the file Cambridge hosts is the manuscript without appendix tables. The appendix with the tables is on the second author's website.
4. Prose and note 29 describe the estimates as the effect of "doubling NKVD presence"; the code reports the raw coefficient on `log(NKVD_OO+1)` with no log(2) scaling, and the appendix (p. A5) describes the same coefficient per one percent change in NKVD.
5. Appendix Figures A3.1 and A3.5 say 10,000 simulations; run2_main.R sets `nsim <- 1000` (lines 182, 409).
6. README lists `data/front_ref.RDS` and a `LICENSE.txt`; the deposit has `data/fronts_ref.RDS` (the name the code reads) and no LICENSE.txt. README says data are CC-BY-NC-SA; Dataverse lists CC0 1.0.
7. README states R 4.4.1 on Ubuntu 22.04, fixest 0.12.0, lfe 3.0-0; deposited .tex headers say "R 4.4.1 by xtable 1.8-4".

## 2. Reproduction plan

Layout: RUNDIR = /workspace/audit_runs/25_914AN0/<AGENT>/. Use the loose Dataverse files arranged as `RUNDIR/Replication_IO/{code,data,results}` (create `results/`; do not copy the authors' `results/` from the tar into it; keep the tar's `results/` separately as `authors_results/` for comparison only). Working directory = `RUNDIR/Replication_IO` (what master.R's `setwd(grep("Replication_IO$", ...))` resolves to). No file-name mapping is needed: every file the code reads exists under the exact path it reads (see DATA_STATEMENT.md).

Scope: only the code blocks that produce the targets are run:
- Block S1: run2_main.R lines 43-157 ("code chunk 1", first block: data load, `ensemble_modz`, Figure 1, Tables A1.1, A1.2, A2.3, A2.4). Targets T1 to T5.
- Block S4: run2_main.R lines 1310-1408 ("code chunk 4": Tables A6.16, A6.17). Target T6.
- Each block is preceded by `source("code/run1_setup.R")` in a fresh R session (as master.R does). The remaining blocks (placebo 1000x simulations, matching, sequential-g, cross-national battle models; README: 3-4 hours on 16 cores, `mc.cores=7`) are not needed for any target and are not run. The class rests on T1 to T6 only.

Environment (fresh per-run library `R_LIBS_USER=RUNDIR/rlib`):
- Pins from README tried first: fixest 0.12.0 (fallback 0.12.1, then current CRAN 0.14.2; with 0.14.x record any singleton removal and vcov default change, CHANGELOG #6b), lfe 3.0-0 (fallback current 3.1.1), lme4 1.1-35.3 (fallback the installed Debian lme4), SUNGEO 1.3.0 (fallback 1.4.0; sf and terra are already present as Debian binaries), robustlmm 3.3-1, Matching 4.10-14, optimx 2023-10.21, data.table 1.15.4, dplyr 1.1.4 (fallback for any of these: current CRAN). Matrix is not pinned (R 4.5 recommended package). If an archived version fails to compile under R 4.5 (for example -Werror=format-security), use the stated fallback and log it.
- All 17 packages in run1_setup.R must be installed before sourcing it. Otherwise its line `install.packages(new.packages, dependencies=TRUE, repos="http://cran.us.r-project.org")` would pull every Suggests dependency (very long). If one package cannot be installed at all, the allowed fix is to remove it from `list.of.packages` (diff), since `require()` only warns.
- Required env fix (diff): functions.R line 306, `mc.cores=min(length(yvarz),parallel::detectCores()/4)`. On this 2-CPU machine this is 0.5, which `parallel::mclapply` rejects ("'mc.cores' must be >= 1") outside the tryCatch, so `ensemble_modz` would stop. Change to `max(1, min(length(yvarz),parallel::detectCores()/4))` (= 1, sequential lapply). README itself says `mc.cores = 1` is acceptable. No RNG is used in `ensemble_modz`, so results do not depend on core count.
- Line 107 writes Table A1.1 to `results/tabA1_1.tex` after `print.xtable(file=tempfile())`; no fix needed. If a table export fails only because SUNGEO is missing, the allowed fix is to make that export line non-fatal (diff); estimates are read from the R objects, not the .tex.

Memory and staging. `data_divisionlevel.RDS` is about 888 MB serialized; with `preprocez()` copies, block S1 is expected to peak around 2 to 3.5 GB (estimate, not measured), above the 3 GB guide on a shared 7 GB machine (about 2.4 GB was free at writing time). Pre-registered default for S1 is therefore the staged fallback below, which keeps the authors' estimation lines unchanged:
- S1a (script `scripts/s1a_prep.R`): `source("code/run1_setup.R")`, `source("code/functions.R")`, then run2_main.R lines 55 and 58 verbatim (`X <- readRDS(...) %>% preprocez()`, `X_s <- X %>% .[ECH_DIV==1,] %>% .[!duplicated(...),]`). Also run lines 98-107 (Table A1.1, needs `X`). Save `X_s`, `yvarz`, `ylabz`, `ylabz_short` to `RUNDIR/inter/s1a.rds`; quit.
- S1b (fresh session, `scripts/s1b_models.R`): setup and functions as above, load `inter/s1a.rds`, run lines 62-73 verbatim (formulas, `mermods <- ensemble_modz(...)`, Hausman checks), `saveRDS(mermods, "outputs/mermods.rds")` immediately, then lines 76-90 and 110-157 verbatim (Figure 1, Tables A1.2, A2.3, A2.4).
- If `free -m` shows at least 5 GB available at start, S1 may instead be run in one session (lines 43-157 verbatim); record which route was used. Either route gives the same objects.
- Extraction: `scripts/extract_targets.R` reads `outputs/mermods.rds` (FE pop weights rows: b, l, u, n, N_DIV_ARMY, N_bxid, N_TID for all 7 outcomes) and the S4 `mod_out` (saved as `outputs/war_mod_out.rds` right after line 1388) and writes `outputs/targets_extracted.csv`. `scripts/build_results.py` builds results.json. Also diff the regenerated `results/tabA2_3.tex` and `results/tabA6_17.tex` against `authors_results/` (text diff saved to outputs/).
- Wall time estimate: S1 about 5 to 25 minutes (7 outcomes x 2 lmer crossed random-effects fits on about 15k rows plus 2 felm fits each); S4 under 1 minute. Every stage saves its output so a sandbox restart costs one stage.

## 3. Robustness checks (pre-registered)

Primary quantity for all checks: the NKVD coefficient for MIA (T1, FE pop-weights model). Secondary, reported but not the results.json primary: KIA (T2), Medals (T3), POW (T4). T6 has no robustness check. All refits use the exact authors' formula `model_fe` (run2_main.R line 64), `lfe::felm(..., weights = N_SOLDIERS, exactDOF = TRUE)`, on `X_s` from S1a, with `y` set to the outcome column as the code does. Estimation sample = rows of `X_s` with no missing value in y, NKVD_OO, AGE_1941, soldiers_dist, RUS_100, URBAN_PCT, POP_DENSITY, M_10km_ADM3, DIV_ARMY, TID, bxid, N_SOLDIERS; confirm it has 15142 rows (or the reproduced T5) before applying any rule. Note: `scale()` inside the formula is recomputed on each refit's data; this only rescales the controls and leaves the NKVD coefficient unaffected. "Same direction and significance" = same sign as the paper's table value and the 95% interval excludes 0.

R_a. Case bootstrap. On the estimation sample (n rows), `set.seed(20261011)` once, then for k in 1..K draw `sample(n, n, replace=TRUE)` and refit; record the NKVD coefficient for MIA first, then KIA, Medals, POW from the same resample (one draw per k, four refits). K = 500. Wall-time rule fixed now: time the first 10 replicates; if the projected total for K = 500 exceeds 60 minutes, use K = 200; if K = 200 still projects over 60 minutes, run MIA only at K = 200. Save results every 50 replicates to `outputs/ra_boot.csv` (resumable; on resume, regenerate the index draws from the same seed and skip completed k). Failed refits are counted and reported, not replaced. Report: original-sample estimate, bootstrap SE, percentile 95% CI (2.5th, 97.5th), p = min(1, 2 x share of draws on the other side of 0). Same direction and significance = percentile CI excludes 0 with the paper's sign.

R_b. Outlier exclusion on the outcome. Each outcome is a continuous percentage, so the default rule applies: within the estimation sample compute z = (y - mean(y)) / sd(y) (unweighted), drop rows with |z| > 3 for that outcome, refit the same model. Report the estimate, felm SE, 95% CI (b +/- 1.96 SE), p, rows dropped. Done separately per outcome (MIA primary).

R_c. Alternative analysis choice: standard errors clustered by unit. The authors' model uses felm's default IID standard errors on a division-month panel. Refit with the cluster part added, `y ~ log(NKVD_OO+1) + <same controls> | DIV_ARMY + TID + bxid | 0 | DIV_ARMY`, same weights and `exactDOF=TRUE`. The point estimate is identical by construction; report clustered SE, 95% CI (b +/- 1.96 SE), felm's clustered p, and number of clusters.

## 4. Known risks

- Package pins: lfe 3.0-0, fixest 0.12.0, lme4 1.1-35.3 and SUNGEO 1.3.0 are archived versions and may not compile under Debian R 4.5; fallbacks above. lme4 is not a target source, but `ensemble_modz` wraps all four models of an outcome in one tryCatch, so an lmer error would silently drop that outcome's FE result too (the outcome row would be missing from `mermods`). If that happens, log it; it is a C/E risk, not something to patch beyond a package-version change.
- fixest version: `betamat` calls `summary(mod, robust=TRUE)`; newer fixest may treat or reject that argument differently, and fixest 0.14.x removes singleton fixed effects by default, which can change N (191) and the clustered SE for T6 (90 country FE on 191 observations).
- run1_setup.R installs any missing package with `dependencies=TRUE`; pre-install to avoid hours of installs.
- mc.cores on 2 CPUs (env fix above) is required, else block S1 stops.
- Memory: about 888 MB serialized division-level data; staged route pre-registered. Do not run the placebo or simulation blocks (forks 7 processes, each holding the data).
- No missing data or code file for the targets was found. Deposit lacks only the README's LICENSE.txt, which no code reads.
- Classification risks: C if the code cannot regenerate Table A2.3 / A6.17 values; the prose-only values (0.52, -0.34) are not targets, so they cannot make a reproduced table a mismatch, but if both runs reproduce 0.629 and -0.287 the prose difference should be reported. E if lfe/fixest/lme4 cannot be installed in any version.
- Licence: Dataverse CC0 1.0; README says CC-BY-NC-SA; article CC BY 4.0. Public downloads only, no sign-in.
