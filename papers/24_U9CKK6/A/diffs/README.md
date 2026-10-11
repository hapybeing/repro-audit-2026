# Changes to the authors' code (agent A, 24_U9CKK6)

All diffs compare the authors' pre-registered line ranges, copied verbatim from the Dataverse files
(6_analysis1.R lines 1-53 and 346-416; 9_analysis4.R lines 1-123; sha256 in checksums.sha256), with the scripts actually run.
`outputs/range_identity_check.txt` (made by script) shows that no authors' line was removed or changed in any run script; only lines were added.

| diff | why |
|---|---|
| run_table1_plain.diff, run_table2_plain.diff | Env fixes: `.libPaths()` to the per-run library, `setwd()` to the run folder (the code uses relative paths `Data/`, `Tables/`); each model wrapped in `if (!file.exists(<rds>)) { ... }` and followed by `saveRDS()` so a sandbox restart costs one model (PREREG section 2). Save paths are literals because the authors' line 41 `rm(list=setdiff(ls(), "EP_eurobar_cent"))` deletes every other object. Models saved to scratch (`/workspace/audit_runs/24_U9CKK6/A/models/`), not to outputs/, because each is 11 to 29 MB (sha256 in LOG.md). |
| run_table1_f1f2.diff, run_table2_f1f2.diff | Same as plain, plus pre-registered memory fallback F1 (after `load()`: `EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_`, positions kept, neither column used) and F2 (`rm()` + `gc()` after each `saveRDS`; the combined `texreg(list(...), file = ...)` call wrapped in `if (FALSE)` and run instead from the saved models by texreg_table*_from_rds.R). Used because the plain Table 1 run passed 3 GB RSS and was stopped (see LOG.md). |
| texreg_table1_from_rds.diff, texreg_table2_from_rds.diff | F2: the authors' combined `texreg(list(...))` call, verbatim, preceded by `library(lme4)`, `library(texreg)` and `readRDS()` of the saved models. |

No estimation line, formula, sample filter, data file or option was changed. No seed is involved in the target models.
