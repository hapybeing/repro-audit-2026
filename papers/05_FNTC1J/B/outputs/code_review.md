# Code review, Agent B, 05_FNTC1J (`MisinfoCT_HSK.r`, 3703 lines, deposited version, sha256 fd86537e...)

Read in full: lines 1-1300 (loading, filtering, recoding, PCA, index construction, imputation), 1640-2130 (logistic
models and the Table A1 export), and the sections around every runtime error. Lines 1300-1640 (correlation tables)
and 2130-3703 (Table A2 export, linear models, bootstraps, plots) were skimmed, not read line by line.
Raw-data facts below were checked by code (scripts/diag_sdo_columns.R, scripts/review_row1400.R,
scripts/review_row1400_impact.R); numbers come from the output files named.

## 1. SDO index averages six columns, not the four scale items (line 1035)  [real bug; touches T1-T4 only via a control]
- Code: `SDO_index = rowMeans(dplyr::select(., starts_with("SDO")), na.rm = TRUE)`.
- Observed (outputs/diag_sdo_selected_columns.csv, printed just before line 1029): `starts_with("SDO")` selects
  `SDO1, SDO2, SDO3, SDO4, SDO1_r, SDO3_r` (six columns). Reversed copies were created at lines 377 and 387 as `12 - item`.
- Consequence (outputs/diag_sdo_facts.csv): SDO1 + SDO1_r = 12 and SDO3 + SDO3_r = 12 for every non-missing row, so for
  the 2506 of 2963 rows with all SDO items present the index equals exactly 4 + (SDO2 + SDO4)/6 (max abs difference
  8.9e-16; correlation with SDO2 + SDO4 = 1.000). Items 1 and 3 cancel and carry no information; for rows with some
  SDO items missing the mean is over whatever subset is present. Correlation of the used index with the intended
  4-item mean (`SDO1_r, SDO2, SDO3_r, SDO4`, the set used in the script's own reliability check at line 982) is 0.823
  on complete rows. Mean/SD of the used index 5.53/0.86 vs 4.39/1.99 for the 4-item mean.
- Does it touch T1-T5? SDO is a control in both target models, so T1-T4 are conditional on a mis-built control. The
  pre-registered check R_c rebuilds the index from the 4 items and reruns everything; its result is in
  outputs/Rc_targets.csv (see results.json R_c). T5 (N) is unaffected.

## 2. Hard-coded removal of raw row "1400" (line 1770) does not match the script's own outlier screen  [observation]
- Code: `subset(ds_analysis_paper2_CTBs_Ant, rownames(...) != "1400")`, comment "row 1400 influential outlier -> remove",
  after `plot(model, which = 4, id.n = 3)` (top 3 Cook's distance) and `filter(abs(.std.resid) > 3)` (lines 1757-1767).
- Row names here are the ORIGINAL raw-data row names (e.g. "165" ... "6052"), not positions.
- Observed in this run (outputs/review_row1400.csv): no case has |standardized residual| > 3 (max 2.90); the top 3 Cook's
  distances are rows "3102", "782", "759". Row "1400" has Cook's distance rank 2928 of 2963 and standardized residual -0.09.
  The case at POSITION 1400 (row name "2285") is also unremarkable (rank 1439).
- Because our run reproduces the paper's chi2 and odds ratios to all printed decimals, our data are very likely the
  authors' data, so the removed case appears not to be the one the comment describes. I cannot determine which case
  the author intended.
- Impact on targets (outputs/review_row1400_impact.csv): keeping the case gives N = 2963 and ORs 1.300433 / 1.332512
  (CT) and 1.196978 / 1.197531 (misinfo), identical to the reported values at 2 decimals. T5 would be 2963 instead
  of 2962. It explains why the linear Tables A3/A4 (which use a redefined data set at line 3207, without this removal)
  report N = 2963.

## 3. Runtime errors after the target computations  [real bugs, do not touch T1-T5]
Logged by the continue-on-error driver in outputs/errors_main.csv (outputs/errors_main_upto3677.csv for the part before the resume):
- Line 3142: a bare `--------------------------------------------------` line (not a comment). R joins it with the
  next statement (lines 3146-3148) into one expression `-...-count_both_ones <- ...` (lines 3142-3148), which fails with
  `object 'count_both_ones' not found`; line 3149 `print(count_both_ones)` then fails too. Line 827 has the same kind of bare dash line but is followed by a
  plain `freq(...)` call, so it only negates a printed table and does not error.
- Line 3153: `cor(ds_analysis_paper2_CTBs_Ant$COVID_CTB, ds_analysis_paper2_CTBs_Ant$misinfo_covid_beliefs)` fails
  (`'x' must be numeric`): that data frame has no `COVID_CTB` column, `$` partially matches `COVID_CTB_dummy` (a factor).
- Any further errors after line 3433 are listed in outputs/errors_main.csv.

## Checked and not found to be bugs
- Political orientation (CA05) is a factor with levels in scale order 1..7 followed by the two NA labels; the NA labels
  are set to NA (line 96) before `as.numeric` (line 357), so the numeric codes are correct.
- SDO reversal `12 - item` matches the 1-11 response scale (raw values 1..11, -1).
- Outcome dummies: items coded 1 / 2 / -1 / -9 in the raw data; `== 1` gives 1, "-1" (kept, not set to NA for C101-C103)
  counts as 0, -9 becomes NA and then 0 in `rowSums(na.rm = TRUE)`. The raw rds has no value labels, so I could not
  verify from the data that 1 means agreement; the paper's text was not re-checked for this. Not classed as a bug.
- `mice()` gets `id` as a predictor column (lines 1199-1203). A modelling choice, not a bug.
