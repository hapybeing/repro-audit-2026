# Environment fixes (Agent B, 05_FNTC1J)

FINAL RUN: the authors' file `MisinfoCT_HSK.r` (sha256 fd86537e...) was run UNMODIFIED, top to bottom, in one R session,
by `scripts/run_authors_continue.R` (diffs/03). No line of the authors' file was changed for the reproduction.

- `03_continue_on_error_driver.diff` (used for the final run): the whole driver shown as a diff against nothing. It
  (1) defines `View <- function(...) invisible(NULL)` before running, because `utils::View()` (script lines 1159, 1225)
  fails non-interactively; (2) parses the script and evaluates each top-level expression in order in the global
  environment, printing visible values (as an interactive console does); an expression that errors is printed and logged
  to `outputs/errors_main.csv` and execution continues, which is what happens when the whole file is pasted/run in an
  interactive console, instead of `source()` aborting at the first error; (3) saves the session (`save.image`).
  Folders `published/`, `_tables/`, `_figures/`, `_data/` were created in the run folder and the rds placed in
  `published/` as the script's relative paths expect.
- `01_view_stub_driver.diff` (attempts 1 and 2 only): first driver, `source(echo=TRUE)` plus the View() stub. With it the
  unmodified script stopped at line 3142 (after both target models were fitted).
- `SUPERSEDED_02_line3142_stray_dash_separator.diff` (attempt 2 only, NOT used in the final run): commented out the bare
  `-----` line 3142. Attempt 2 then stopped at line 3153 (`cor()` on a factor). Rather than editing the authors' file
  error by error, the final run used driver 03 on the unmodified file.
- Not an env fix: `scripts/MisinfoCT_HSK_Rc_vs_original.diff` is the pre-registered R_c change (line 1035 only), used only
  for the robustness check and run with the same driver 03.
