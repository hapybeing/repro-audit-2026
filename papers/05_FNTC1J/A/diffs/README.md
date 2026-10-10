# diffs/ (05_FNTC1J, agent A)

`MisinfoCT_HSK.r.diff` is a unified diff from the deposited `MisinfoCT_HSK.r` (sha256 fd86537e...cf157) to the file that was run. It has three hunks:

1. Line 19 (new): `View <- function(...) invisible(NULL)`. Environment fix. `utils::View()` at original lines 1159 and 1225 errors in a non-interactive `Rscript` session. The stub only prints nothing; it draws no random numbers, so the RNG stream from `set.seed(2000)` is unchanged.
2. Original line 3142: a bare separator line of 50 dashes (no `#`) is turned into a comment. Under `source()` R parses it together with the next expression as unary minus applied to the assignment `count_both_ones <- ...`, which fails with `object 'count_both_ones' not found` and stops the script. Interactively (RStudio, line by line) it would not stop anything. Not strictly an environment fix, but it is a typo in a separator line, changes no analysis, and is after all code that produces T1 to T5 (original lines 1648 to 2344).
3. Original line 3153: print-only line `cor(ds_analysis_paper2_CTBs_Ant$COVID_CTB, ds_analysis_paper2_CTBs_Ant$misinfo_covid_beliefs)` is commented out. At that point the object does not contain these columns (they are added when the object is rebuilt at original line 3207), so a top-to-bottom run stops with `'x' must be numeric`. No assignment, no RNG use, after all target code.

Not changed: working directory (set by the runner to the run dir, which has `published/`, `_tables/`, `_figures/`, `_data/` created before the run); `pacman` installed so line 17 runs as written.

The runner `scripts/run_authors.R` sources the file in two consecutive parts in the same R session (split after original line 2344) and saves a checkpoint between them. This does not change what is executed or its order.

`scripts/MisinfoCT_HSK_Rc_vs_envfixed.diff` (in scripts/, not an environment fix) is the single-line change for robustness check R_c.
