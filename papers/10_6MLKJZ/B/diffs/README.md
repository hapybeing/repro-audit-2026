# Agent B environment changes (10_6MLKJZ)

No line of the authors' R code was changed. 01-04 in the run copy are byte-identical to the deposit (checked with `cmp`).

- `00_raw_data_lowercase_symlinks.diff`: the code reads `data_uhh.csv` and `data_hsvn.csv`; the deposit has `data_UHH.csv` and `data_HSVN.csv`. On case-sensitive Linux this fails, so two symlinks with the lower-case names were added in the run copy of `raw_data/`. `sam` (derived from the path) stays `uhh` / `hsvn`. Allowed by PREREG section 2.
- `01_package_cjoint_2.1.0.diff`: package version change, not a code change. With cjoint 2.1.3 (CRAN current) `prep_data()` fails inside `cjoint::read.qualtrics` with "replacement has 0 rows, data has 2048" (log: `outputs/run_authors_log_attempt1_cjoint213.txt`); 2.1.3 also renames the ID column to `respondent` and makes `respondentIndex` an integer, whereas the authors' code (01 lines 151 and 154) expects `Response.ID` and `respondent`. cjoint 2.1.0 was the CRAN version at the authors' last script revision (2023-07-11), so it was installed from the CRAN archive, with its archived dependency shinyBS 0.61.1. Allowed as a package-version environment fix (AGENT_RUNBOOK).
- cregg 0.4.0 installed from the CRAN archive (cregg was archived 2024-09-05), as PREREG section 2 says.
- Run copies: the authors' deposited PNGs were moved to `run/figures_authors/` and the deposited prep CSVs to `run/data/conjoint_data/prep_data_deposited/`, so that the code regenerates both; this is a scratch-directory layout choice, not a code change.
- Locale: LANG=C.UTF-8, LC_ALL=C.UTF-8. No encoding fix was needed: all 8 attributes have the expected level counts and no NA levels (`outputs/attribute_levels_check.csv`).
