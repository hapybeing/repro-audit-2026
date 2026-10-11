# Diffs (paper 22_W2TSVL, agent A)

Both diffs are environment fixes named in PREREG.md section 2 and batch5_class_decisions.md item 3. No estimation line, sample filter or variable coding was changed.

- `appendix_A1_R.diff` (Framing Labor Action_Appendix A1.R): line 14 absolute Windows path replaced by `read_dta("OA23 Base UT-TEC.dta")` (the authors' own commented alternative in the main script, line 15); `install.packages()` lines 4, 5, 6, 138 and 282 commented out (packages installed beforehand into the per-run library).
- `main_R_script.diff` (Framing Labor Action_R script.R): line 14 absolute path replaced the same way; `install.packages()` lines 4 to 8 commented out.
- `browseURL()` (Appendix A1.R lines 166, 190, 216) was made a no-op by defining `browseURL <- function(...) invisible(NULL)` in the wrapper `scripts/run_appendix.R` before `source()`; the authors' file itself is not edited for this, so there is no diff.
