# DATA_STATEMENT: 25_914AN0 (Fratricidal Coercion in Modern War, International Organization 79(1), 2025, doi 10.1017/S002081832400033X)

Written 2026-10-11 (IST). Checks run 2026-10-10 between about 20:38 and 20:43 UTC (2026-10-11 02:08 to 02:13 IST). No sign-in, no author contact. Files were only downloaded, hashed, listed and read; no analysis code was run.

## Source read
- Publisher PDF (open access, CC BY 4.0): https://www.cambridge.org/core/services/aop-cambridge-core/content/view/FD297F9402D9C3E599F68CA114DA1313/S002081832400033Xa.pdf/div-class-title-fratricidal-coercion-in-modern-war-div.pdf , HTTP 200, 525,088 bytes, sha256 926451f9c4bc04a176458d301e739de8bb659acd7e65116a0321e6f517c457d8. Excerpt: `data_statement_raw/statement_excerpt.txt`.

## Verbatim statement (p. 190, "Data Availability Statement")
"Replication files for this research note may be found at <https://doi.org/10.7910/DVN/914AN0>."

Related (p. 191, "Supplementary Material"): "Supplementary material for this research note is available at <https://doi.org/10.1017/S002081832400033X>."

## Locations the statement points to
1. Harvard Dataverse doi:10.7910/DVN/914AN0 (the audited deposit). Checked.
2. (Supplementary material, not a data location) Cambridge article page. Checked: its one supplementary file, `S002081832400033Xsup001.pdf` (2,797,413 bytes, sha256 f59c6098705cc917eb29f1cf50a0edfcd7aaf2cf3608122e17d6994380e214b5), is the 28-page author manuscript dated October 22, 2024. It contains no data, no code and no appendix tables. Its footnote repeats that replication materials are on Harvard's Dataverse.
No other data or code location is named in the article (no OSF, GitHub, or "on request").

## Reachability and completeness check
- Dataverse API (`data_statement_raw/dataverse_914AN0.json`, sha256 2c64a72f4e493bb9d657fa7a60d60a9011775d20f45f7dcdaaca1caa201624ca): HTTP 200, version 1.0, RELEASED 2024-10-15, licence CC0 1.0, 10 files, none restricted. All 10 downloaded without authentication (HTTP 200, md5 equal to Dataverse md5 for each).
- Files the code reads (every `readRDS(` and `source(` call in master.R, run1_setup.R, run2_main.R), compared with the deposit by `check_reads.py` (output `data_statement_raw/read_check.txt`):

| read call | in Dataverse at that path | in Replication_IO.tar.xz |
|---|---|---|
| code/functions.R | yes | yes |
| code/run1_setup.R | yes | yes |
| code/run2_main.R | yes | yes |
| data/data_divisionlevel.RDS | yes | yes (identical sha256) |
| data/data_battlelevel.RDS | yes | yes (identical sha256) |
| data/data_warlevel.RDS | yes | yes (identical sha256) |
| data/fronts_ref.RDS | yes | yes (identical sha256) |

- The code writes to `results/`; that folder is in the tar (with the authors' outputs) but not among the loose files; README says to create it.
- README mentions two items not in the deposit: `data/front_ref.RDS` (spelling; the file present and read by the code is `data/fronts_ref.RDS`) and `LICENSE.txt` (not read by any code). Searches, 2026-10-10 about 20:42 UTC: (a) Dataverse file list API above, query "LICENSE" in file names: 0 hits of 10 files; query "front_ref.RDS": 0 hits; "fronts_ref.RDS": 1 hit. (b) `tar -tJf Replication_IO.tar.xz` (70 entries): "LICENSE" 0 hits, "front_ref.RDS" 0 hits, "fronts_ref.RDS" 1 hit. Rule for a hit: a file name containing the query string, case-insensitive.
- No custom module, helper or table script is missing: run2_main.R sources only code/functions.R, which is deposited and defines every non-package function the target blocks call (`preprocez`, `ensemble_modz`, `phtest_felm`, `icc_fun`, `betamat`).

## Other location found by us (does not count under rule #4)
- The authors' online appendix with Tables A2.3 and A6.17 (the target tables): https://zhukovyuri.github.io/files/2024_LyallZhukov_appendix.pdf (sha256 c9ad51f649253cd5250d6d3d9fcad5756d1adf4ffebb63ee08e623384bc9582c), found by web search. It is a paper-text source, not a data or code location. Its table values match the authors' output files in the deposit tar (`results/tabA2_3.tex`, `results/tabA6_17.tex`).

## Finding
Deposit alone complete for the code's reads: the statement points only to the audited Dataverse deposit, which holds all four data files and all code the scripts read. The deposit lacks only the README-listed `LICENSE.txt`, which no code reads.
