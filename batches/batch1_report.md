# Batch 1 report, revision 2 (papers 01 to 05)

Audit run by Gaurang Kumar (GitHub: hapybeing). Protocol: PROTOCOL.md, seed 20261009. Method changes since revision 1: CHANGELOG_METHOD.md #4.
Revision 1 is kept as batch1_report_v1.md. Every number here comes from a saved output file named next to it.

## Sample
Papers whose Harvard Dataverse deposit contains R or Python code, released 2023 to 2026. Data presence was not an eligibility criterion. Frame, draw, screening counts and the pre-registration timestamp: SELECTION.md.

## Counts (batches/batch1_counts_rule4.json)
Rule: materials = the deposit plus every location the article's own data statement points to.
- Main: A 2, B 0, C 3, D 0, E 0 (5 papers)
- Excluding 01 (no computational target): A 2, C 2 (4 papers)
- If the uncited OSF copy for 04 were counted: A 3, C 2
- If 02 were judged run as-is with a 2026 clock: A 1, B 1, C 3

## Per paper (batches/batch1_results_rule4.csv)
| Paper | Agents A / B | Class (rule 4) | Alternative |
|---|---|---|---|
| 01 ThermoPCD (10.1093/database/baae015) | C / C | C | no computational target for this deposit |
| 02 Secret alliances (10.1111/ajps.12997) | A / A | A | B as-is (clock deviation) |
| 03 Circular sortase (10.1021/jacs.4c12585) | C / C | C | none; no external data location exists |
| 04 Rural populism (10.1177/23780231251317227) | A / A | C | A with authors' uncited OSF copy |
| 05 COVID misinformation (10.37016/mr-2020-188) | A / A | A | none |

Targets vs paper, with table/page locations: batch1_targets.md. 15 of 15 computable targets (02, 04, 05) match the paper at its rounding for both agents.

## Data statements (papers/*/DATA_STATEMENT.md)
- 01: points only to Harvard Dataverse. The production trajectory the deposit's analyses read is not in the collection (333 .xtc files searched). The paper's computed results concern other complexes, not 2XWT.
- 03: points only to the Dataverse deposit. No ProteomeXchange/PRIDE accession found. The PSM export the code reads is not deposited anywhere.
- 04: the article has no data statement and cites no external location; the deposit is one R script. Data were on a public OSF page we found. Open item: the Sage supplementary file could not be read.
- 02 and 05: deposit alone is complete.

## 02: deviation and robustness
- Deviation: exact match needs the system clock set to the authors' run date (papers/02_ELBOXX/diffs/DEVIATION_clock.md). As-is, T4 0.05589 vs 0.05441 and T5 0.04119 vs 0.03963, both within 5% (A/outputs/clock_comparison.json).
- The targeted correlation is a supporting exhibit, not the paper's headline claim; the paper's main contribution is a formal model and the authors call this pattern "consistent with" rather than confirmatory (HEADLINE_CHECK.md).
- Pre-registered checks: bootstrap and year-clustered OLS hold; the |z| > 3 outlier drop (123 of 3811 rows) gives r 0.011, p 0.50.
- Exploratory, NOT pre-registered (A/outputs/exploratory_outlier.json): Spearman rho 0.049 (p 0.0025); winsorized 1/99 r 0.124; log(x+1) both r 0.088; dropping |z| > 3 on secret_alliances only (66 rows, years 1882 to 1918) r 0.004 (p 0.81); on disputes only r 0.118. Reading: a small positive rank association survives, but the size of r 0.163 comes mostly from high-secrecy years before 1919.

## 05: verified code finding (papers/05_FNTC1J/SDO_FINDING.md, A/outputs/sdo_check.json)
- MisinfoCT_HSK.r line 1035 averages SDO1 to SDO4 plus reversed copies of items 1 and 3, so items 1 and 3 cancel: the index equals 4 + (SDO2 + SDO4)/6. Shown algebraically and numerically.
- Effect on the SDO coefficient (Table A1, p. 16): authors' index OR 1.164 (CI 1.027 to 1.320, p 0.018 raw); corrected 4-item index OR 1.054 (CI 0.995 to 1.117, p 0.071). The paper's Bonferroni-adjusted p was already not significant (0.337). Headline targets barely move (T1 1.300 to 1.3075).
- Removal of row "1400" (line 1770) changes no reported value at the paper's rounding.

## Code observations (batch1_code_observations.csv)
Verified findings are listed above or in that file; everything else is an unverified agent observation and is not part of any public summary. Measurement-validity opinions (e.g. on how 02 defines disputes) are out of scope.

## Plain-language summary
Of five randomly drawn papers, two reproduced exactly from what the article points to, and three could not be fully checked because needed files are not where the article says (for one of these, 04, the data were on a public page the article does not cite, and with it the paper reproduces exactly). No paper showed a discrepancy that changes its conclusion. In 02, one pre-specified outlier check weakened a supporting correlation, which needs follow-up. In 05, a coding slip in a control index changes one secondary coefficient, not the headline result.
