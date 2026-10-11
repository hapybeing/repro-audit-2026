# Diffs (agent B, 22_W2TSVL)

- appendix_A1_R.diff: `Framing Labor Action_Appendix A1.R`. Line 14 read the data from an absolute Windows OneDrive path; replaced by `read_dta("OA23 Base UT-TEC.dta")` (the authors' own commented alternative in the main script, line 15), with the Dataverse `?format=original` .dta placed in the run directory. install.packages() lines 4, 5, 6, 138, 282 commented out; the packages were installed beforehand (non-interactive run, no CRAN mirror set). Allowed by PREREG.md section 2.
- main_R_script.diff: `Framing Labor Action_R script.R`. Same path fix on line 14; install.packages() lines 4 to 8 commented out.
- Not a diff: browseURL() (appendix lines 166, 190, 216) was made a no-op in the wrapper scripts/run_appendix.R, not in the script. The main-script wrapper scripts/run_main.R wraps broom::tidy only to record coefficients.
- No estimation line, filter, recode or seed was changed.
