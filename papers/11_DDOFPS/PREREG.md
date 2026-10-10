# PREREG: 11_DDOFPS

Written 2026-10-10, about 21:15 IST, before any analysis code was run. No analysis code was executed to write this file. The deposited R script was read as text only. To identify which deposited file each `import()`/`read.xlsx()` call refers to, the pre-registration agent opened the xlsx files with Python openpyxl and looked at sheet names, column headers, row counts, the `ano` frequencies and the value frequencies of four columns (APE4, APE3, OBJ1, numpartido) over the whole programs file. No cross-tabulation by year, no correlation and no chi-square was computed, so no target value was seen in the data before this file was written.

The main text was read in full (Portuguese). Source note: SciELO's direct PDF and HTML URLs return HTTP 403 (a "bunny-shield" bot challenge) to scripted downloads, and the SciELO ArticleMeta JATS XML carries front matter and references but no body. The full text was therefore read (a) through the web_fetch tool on the DOI landing page (SciELO HTML, Portuguese, not saved, no hash) and (b) from a PDF printed by a browser session from the live SciELO PDF viewer. All target values and page numbers below were checked against the text extracted from (b) with `pdftotext`.

- Paper: Figueiredo, A. C.; Schaefer, B. M.; Meireles, F.; Freitas, C. M. de. "Banco de Dados de Propaganda Eleitoral (HGPE) dos candidatos a deputado federal do Estado do Rio de Janeiro - 1998-2018". DADOS, Rio de Janeiro, v. 68, n. 1, 2025, e20230099 (Nota Tecnica; published online 19 Jul 2024). DOI https://doi.org/10.1590/dados.2025.68.1.001 . CC BY 4.0.
- Text sources read:
  - SciELO HTML (pt): https://www.scielo.br/j/dados/a/5KCvrPtYzZNWj4MFNZBRPLB/?lang=pt (via web_fetch, 2026-10-10).
  - SciELO PDF (pt): https://www.scielo.br/j/dados/a/5KCvrPtYzZNWj4MFNZBRPLB/?format=pdf&lang=pt , saved by browser print as `/workspace/audit_runs/11_DDOFPS/prereg/paper_pt_browserprint.pdf` (17 pages, 580,573 bytes, sha256 45558bbbc82081530534de93efed0678013c40b0d93b67ecaf1f00c9bf3935b1). A browser print is not byte-identical to the publisher file; another agent's copy will have a different hash. Printed page numbers ("N / 17") equal PDF page indices.
  - ArticleMeta JATS (front matter only): https://articlemeta.scielo.org/api/v1/article/?code=S0011-52582025000100700&collection=scl&format=xmlrsps (23,868 bytes, sha256 0b2caea937ad70e6eee91351db32c7f898bfa1fe803930aec6fb6d92da81bd7c).
  - Short excerpts: `data_statement_raw/statement_and_target_excerpts.txt`.
- Dataset: "Replication Data for: Banco de dados propaganda eleitoral (HGPE) dos candidatos a deputado federal do Estado do Rio de Janeiro - 1998-2018", Harvard Dataverse, https://doi.org/10.7910/DVN/DDOFPS , version 1 (only version), released 2024-01-03, licence CC0 1.0, 9 files, none restricted. File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/DDOFPS (saved response sha256 7b084346c180d886beedadef7fea173d1be0296c6a485e5b538badf9bc413199). Downloaded 2026-10-10 about 15:28 UTC with User-Agent "repro-audit-2026"; every file's md5 matched the Dataverse md5.

| datafile id | file | URL | bytes | sha256 |
|---|---|---|---|---|
| 7337781 | Análise dos Dados Nota Técnica.R | https://dataverse.harvard.edu/api/access/datafile/7337781 | 7111 | a057273fa5ef24c0d5b5d87fa3eae099c48f05d1f16d86d18002700964bb527b |
| 7337784 | bd_doxa_candidatos_HGPE.RData | https://dataverse.harvard.edu/api/access/datafile/7337784 | 457531 | 8c2da5a8e571d4a93b4c8816e5bb7d21936e65ba5a253d7ca7dfd08a139719c0 |
| 7337786 | bd_doxa_candidatos_HGPE.xlsx | https://dataverse.harvard.edu/api/access/datafile/7337786 | 2899317 | b8ad60be30d4aea100500c0dba56c7bb84785af6872f5e966bfca0583d8f8091 |
| 7337783 | bd_doxa_programas_HGPE.RData | https://dataverse.harvard.edu/api/access/datafile/7337783 | 303344 | e29a2e85403a107c40011c5edf6c3d446e50dbf52787a0f951c35b3cb77f0bcc |
| 7337779 | bd_doxa_programas_HGPE.xlsx | https://dataverse.harvard.edu/api/access/datafile/7337779 | 4281281 | f4c13ed57fdf32c9ceb3ea24cf8a8d6359e0009d2dfda50a563240be7d158d78 |
| 7337785 | bd_doxa_programas_HGPE_v2.xlsx | https://dataverse.harvard.edu/api/access/datafile/7337785 | 3709235 | 86560fe4f0dac023e451b5ac74899679081fc19f95b2e16fc642fbada207990f |
| 7337782 | Dicionário de Códigos Banco 2.pdf | https://dataverse.harvard.edu/api/access/datafile/7337782 | 43693 | b6e3ffb65bc1b7026fe88115bd9c373b059441f1ba1357c89a8cc548fef7fdb7 |
| 7337787 | HGPE_lei.xlsx | https://dataverse.harvard.edu/api/access/datafile/7337787 | 6676 | 9595adaf28d097337860099ee16348f0f8a8464ef113a5d3982639bb4ce31abb |
| 7337780 | Livro de Códigos 1.pdf | https://dataverse.harvard.edu/api/access/datafile/7337780 | 182075 | 1814893b3a51d4b403f0f8a395d33a15ef4a50412c25570cb0fea33f343da731 |

Checksums file: `/workspace/audit_runs/11_DDOFPS/prereg/checksums.sha256`. No README in the deposit; the two codebook PDFs and the `codigos` / `codigo_variaveis` sheets document the variables.

Structure seen (headers only): `bd_doxa_programas_HGPE.xlsx` and `_v2.xlsx` both have sheet `banco de dados` with 9439 data rows and 123 columns (identical header names; in v2 numeric columns such as `ano` and `numpartido` are stored as floats). `bd_doxa_candidatos_HGPE.xlsx` has sheets `Completo` (6083 rows, 52 columns), `codigos`, and `2002_2018` (4563 rows, 52 columns; years 2002, 2006, 2010, 2014, 2018). `HGPE_lei.xlsx` has one sheet (8 rows, 9 columns).

## 1. Headline results and targets

Nature of the paper: a technical note (Nota Tecnica) that describes two databases. The abstract's main claim is descriptive: the database covers 9,433 evening electoral programs in which 1,774 candidates took part. The only computed results are in the two "Descricao do banco" sections, as illustrations: frequencies and a chi-square test for appeals (Figuras 4 and 5), Pearson correlations between HGPE time and campaign revenue by year (Figura 6), and group means (Figuras 7 and 8). The paper prints no tables. Targets are therefore taken from the abstract's count (as printed for the deposited rows) and from the numbers printed in the text for the figures that the deposited script builds.

| id | quantity (exact statistic and code object) | paper value | decimals | location |
|---|---|---|---|---|
| T1 | Number of rows in the programs database: `sum(df$programas)` in section "### Figura 2" (lines 67-77), which equals `nrow(bd_doxa_programas)` | 9439 | 0 | PDF p. 7, "totalizando 9.439 observacoes (1998: 1.071; 2002: 1.778; 2006: 1.351; 2010: 1.610; 2014: 2.703; 2018: 926) (Figura 2)" |
| T2 | Pearson r, `HGPE_total` vs `VR_RECEITA_total`, year 2002, on `teste_2` (lines 206-211); the `r` column of the `stat_cor(aes(color = el))` layer of line 219 for group el == "2002" | 0.45 | 2 | PDF p. 11, Figura 6 paragraph, "0,45 (2002)" |
| T3 | Same statistic and object as T2, year 2018 | 0.72 | 2 | PDF p. 11, Figura 6 paragraph, "e 0,72 (2018)" |
| T4 | `table(bd_doxa_programas$ano, bd_doxa_programas$APE4)["2018", "Sim"]` (line 138; same table as `test`, line 148) | 40 | 0 | PDF p. 9, Figura 4 paragraph, "4,3% (40 de 926)" |
| T5 | `table(partidos_sel$numpartido, partidos_sel$APE3)["13", "Sim"]` (line 198), observed political appeals for PT | 602 | 0 | PDF p. 10, Figura 5 paragraph, "observada ... 602 e 417" (PT first) |
| T6 | `test2$expected["13", "Sim"]` (lines 180-183), chi-square expected count for PT | 524 | 0 | PDF p. 10, Figura 5 paragraph, "esperada: 524 e 342" (PT first) |

Statistic ambiguities (first listed is the pre-registered one):
- T2, T3: (1) `r` reported by `ggpubr::stat_cor` (Pearson, default `method = "pearson"`, computed with `cor.test` on complete rows of the group), read from `ggplot2::layer_data()` of the plot in line 219; (2) cross-check only: `cor.test(HGPE_total, VR_RECEITA_total)` by year on `teste_2`. Both should be identical; if they differ, (1) is the target value and the difference is logged.
- T6: (1) `test2$expected["13","Sim"]` rounded to 0 decimals; no other candidate seen.
- p-value for the Figura 4 chi-square (used only in the T4 conclusion criterion): the paper prints "p-valor > 0,001". Candidates: (1) Pearson chi-square p of `chisq.test(table(ano, APE4))` read as p < 0.001 (the text calls the difference statistically significant, which only fits p < 0.001); (2) the literal reading p > 0.001. Reading (1) is pre-registered; both values are reported.
- p-value for T2, T3: (1) `p` column of the same stat_cor layer (two-sided `cor.test` p).

Only one N is printed per object. Other N-like values: the abstract and note 2 give 9,433 programs (9,439 rows minus 6 rows from 1998 without information); note 3 gives 2,203 candidate participations summed over years and 1,774 distinct candidates; the second database has 6,083 cases (PDF p. 7). The deposited script computes none of 9,433, 1,774, 2,203 or 6,083 (it reads sheet `2002_2018`, 4563 rows, for Figuras 3, 6 and 7). They are not targets.

Secondary numbers (context, not targets; agents may report them, labelled): APE4 share overall 1.8% and in 2018 4.3% (PDF p. 9); expected 2018 APE4 count 16 (note 9, PDF p. 15; `test$expected["2018","Sim"]`); MDB (15) observed 417 and expected 342 (PDF p. 10); r = 0.61 (2006), 0.61 (2010), 0.69 (2014) (PDF p. 11); Figura 7 means 198 and 42 seconds (2002) and 30 and 5 (2018) (PDF p. 12), which the script does not compute (it only draws boxplots).

Conclusion criterion for `same_conclusion`:
- T1: reproduced count is 9439, or within 6 of it (the paper itself uses 9,433 and 9,439 for the same database).
- T2 and T3: each r > 0 with stat_cor p < 0.05 (note 10), AND reproduced r(2018) > r(2002) (the text's claim that the correlation becomes stronger over time).
- T4: the 2018 APE4 "Sim" count is larger than `test$expected["2018","Sim"]`, AND `chisq.test` p for ano x APE4 is < 0.001 (pre-registered reading (1) above).
- T5 and T6: observed (T5) > expected (T6) for party 13.

Inconsistencies noticed while reading (described, not judged):
- Abstract: 9,433 programs; text p. 7 and Figura 2: 9,439 observations; note 2 explains the 6-row difference.
- PDF p. 9: "p-valor > 0,001" next to "diferenca estatisticamente significante".
- Figura 5 text (PDF p. 10) says the main parties, which together account for more than 50% of programs, are used. The script's filter (line 177) is `numpartido %in% c("15", "13", "50", "22", "25", "´45", "12", "11")`: the entry for party 45 carries an acute accent byte (0xB4) before "45", so no row of party 45 can match and party 45 (PSDB) is left out. The Figura 5 legend (PDF p. 11) lists parties 11, 12, 13, 15, 22, 25 and 50, also without 45. The expected counts in T6 depend on which parties are in the table.
- Code section "### Figura 4" (line 120) is empty; the Figura 4 test sits under "### Qui-Quadrado".
- Figura 7 text gives means in seconds while the figure title says log seconds; the script computes no means.
- Dataverse description cites "Revista DADOS, v. 67, n. 4, 2024"; the article is printed as v. 68, n. 1, 2025, e20230099.
- The data availability statement appears in the SciELO HTML but not in the PDF (see DATA_STATEMENT.md).

## 2. Reproduction plan

One script, `Análise dos Dados Nota Técnica.R` (270 lines, Latin-1 encoded with CRLF line endings; lines 14 and 22 contain UTF-8 bytes in comments). Run top to bottom in one R session from RUNDIR. There is no randomness in the analysis (no seed, no simulation; `chisq.test` is used without `simulate.p.value`).

Script order and inputs (line numbers of the deposited file):
1. Line 4: `pacman::p_load(tidyverse, rio, janitor, hrbrthemes, patchwork, paletteer, ggplot2, directlabels)`. Later `library()` calls: openxlsx (92), gplots (125), corrplot (153, 185), vcd (158, 190), ggpubr (204).
2. Lines 10-63 (Figura 1): `import("HGPE_lei.xlsx")`. No target.
3. Lines 67-88 (Figura 2): `bd_doxa_programas <- import("bd_doxa_programas.xlsx")`; per-year counts in `df`. Target T1.
4. Lines 92-117 (Figura 3): `bd_doxa_candidatos <- read.xlsx("bd_doxa_candidatos.xlsx", sheet = "2002_2018")`. No target.
5. Lines 128-172 (Qui-Quadrado / Figura 4): tables and `test <- chisq.test(table(ano, APE4))`. Target T4 and the T4 criterion.
6. Lines 176-198 (Figura 5): `partidos_sel`, `test2`, `test2$expected`, `table(numpartido, APE3)`. Targets T5, T6.
7. Lines 204-229 (Figura 6): `teste_2 <- na.omit(select(el, ano, HGPE_total, VR_RECEITA_total, sg_partido))`; `sp <- ggscatter(...)`; `sp + stat_cor(aes(color = el))`. Targets T2, T3.
8. Lines 236-264 (Figura 7): boxplots only. No target.

Files the script reads versus the deposit: `HGPE_lei.xlsx` is deposited under that name. `bd_doxa_programas.xlsx` and `bd_doxa_candidatos.xlsx` are not deposited under those names (searches logged in DATA_STATEMENT.md). The deposit has `bd_doxa_programas_HGPE.xlsx`, `bd_doxa_programas_HGPE_v2.xlsx` and `bd_doxa_candidatos_HGPE.xlsx` (which has the sheet `2002_2018` the script asks for). Pre-registered mapping, applied as a path-only environment fix (copy the file under the name the script uses in RUNDIR, or edit the path string; either way saved as a diff/README entry):
- `bd_doxa_programas.xlsx` <- `bd_doxa_programas_HGPE.xlsx` (primary: this is the name the paper gives the database, PDF p. 7). Targets T1, T4, T5, T6 are additionally computed with `bd_doxa_programas_HGPE_v2.xlsx` as a labelled exploratory alternative (CHANGELOG #4e); it does not change the class.
- `bd_doxa_candidatos.xlsx` <- `bd_doxa_candidatos_HGPE.xlsx`.

Where each target comes from: an extraction script (`scripts/extract_targets.R`) sources the authors' script (or the session after it ran) and writes `outputs/targets_extracted.csv` with: `sum(df$programas)` and `nrow(bd_doxa_programas)` (T1); for each year, `r` and `p` from `ggplot2::layer_data(sp + ggpubr::stat_cor(aes(color = el)), i = length((sp + ggpubr::stat_cor(aes(color = el)))$layers))` mapped to years by group, plus the `cor.test` cross-check (T2, T3); `table(ano, APE4)`, `test$statistic`, `test$parameter`, `test$p.value`, `test$expected` (T4); `table(partidos_sel$numpartido, partidos_sel$APE3)`, `test2$expected`, `test2$p.value` (T5, T6). `scripts/build_results.py` builds `results.json` from that CSV.

Allowed environment fixes (each saved as a diff, nothing that touches an estimate):
- File names as mapped above.
- Encoding: if R fails to parse the Latin-1 file in a UTF-8 locale, source it with `source(file, encoding = "latin1")` or convert a copy with `iconv -f latin1 -t utf-8`. The byte 0xB4 in line 177 must remain the acute accent character (U+00B4) before "45"; it must not be deleted or changed to "45". Converting the two UTF-8 comment lines is harmless.
- Non-interactive graphics: plots go to the default `Rplots.pdf`; if `hrbrthemes::theme_ipsum_tw()` or font registration fails, make only that cosmetic call non-fatal (Figura 1 has no target).
- Package installs into the per-run library (CRAN current versions; the deposit pins nothing).

## 3. Robustness checks (pre-registered)

Primary quantity for all three checks: the 2018 Pearson correlation between `HGPE_total` and `VR_RECEITA_total` (T3) on `teste_2`. Each check also reports the same quantity for every year (2002, 2006, 2010, 2014) and the difference r(2018) - r(2002) as secondary. "Same direction and significance" for the primary quantity: estimate > 0 and p < 0.05 (two-sided), or, for R_a, the 95% percentile interval excludes 0.

R_a. Bootstrap resample. On `teste_2` as built by the authors' code, `set.seed(20261010)`, draw 2000 case resamples with replacement within each election year (stratified by `ano`, each year resampled to its own size), compute Pearson r per year in each resample. Report the original-sample r(2018) as the estimate, the 2.5th and 97.5th percentiles of the 2000 bootstrap r(2018) as `se_or_ci`, the bootstrap SE, and as p-value the two-sided bootstrap proportion min(2 * share of r <= 0, 1). Also report the share of resamples with r(2018) > r(2002). Same direction and significance = r(2018) > 0 and percentile CI excludes 0.

R_b. Outlier exclusion. Within each election year of `teste_2`, compute z of `VR_RECEITA_total` (the y variable of Figura 6) with the year's own mean and SD (`sd()`, n - 1); drop rows with |z| > 3; recompute Pearson r and `cor.test` p per year. Report r(2018), its 95% CI from `cor.test`, p, and the number of rows dropped per year. Same direction and significance = r(2018) > 0 and p < 0.05.

R_c. Alternative analysis choice: Spearman rank correlation instead of Pearson (both variables are money and seconds, so heavily skewed with many small values). `cor.test(HGPE_total, VR_RECEITA_total, method = "spearman", exact = FALSE)` per year on the same `teste_2`, no rows dropped. Report rho(2018) and p. Same direction and significance = rho(2018) > 0 and p < 0.05.

## 4. Known risks

- Missing file names (main risk): the script reads `bd_doxa_programas.xlsx` and `bd_doxa_candidatos.xlsx`, which are not in the deposit under those names. Files with the same structure exist under other names (`_HGPE`, `_HGPE_v2`). Under PROTOCOL.md section 7 and CHANGELOG #6, if the path mapping is accepted as an environment fix and all targets match, the class can be A or B; if the lead reads the renamed files as materials that are incomplete or unclear (two candidate programs files, no README saying which one the script used), the paper could be C. If v1 and v2 give different values for T1, T4, T5 or T6, that ambiguity is itself a C risk.
- Targets the code cannot produce: the abstract's 9,433 programs and 1,774 candidates, and the Figura 7 means, are not computed by the script. They are not targets, but a reader may see the abstract claim as not reproducible from code.
- p-value text "p-valor > 0,001" (T4 criterion) has two readings; reported both ways.
- Party 45 excluded by the "´45" entry: expected counts (T6) depend on this; the deposited code is run as is.
- Encoding of the script (Latin-1 plus stray UTF-8) may need an encoding argument; must not alter line 177.
- R is not currently installed in the sandbox (`Rscript` not found at 2026-10-10 21:10 IST): run `bash REPO/scripts/setup_env.sh` first. Packages: tidyverse, rio, janitor, hrbrthemes, patchwork, paletteer, directlabels, openxlsx, gplots, corrplot, vcd, ggpubr, pacman, all on CRAN. Risks on aarch64: hrbrthemes fonts (cosmetic only); ggpubr pulls many dependencies (car, rstatix); none are Stata or proprietary.
- Compute: trivial (two xlsx files of a few MB, no models).
- Data access: all 9 files public, no sign-in. The paper's PDF and HTML on SciELO block scripted downloads (HTTP 403 bot challenge), so Agent B may need a browser to read the paper; the targets are copied here with page numbers.
