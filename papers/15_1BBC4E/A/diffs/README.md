# diffs for 15_1BBC4E agent A

No file of the authors' deposit was changed. The three target scripts (Comparison.R, Share_Common_Sample.R, Agreement across all.R) were run unmodified via `source()` from the R project folder by `scripts/run_authors.R`, which only sets the working directory, opens a pdf device for the figures and saves the target objects afterwards.

Environment-only actions (no diff needed): installed corrr 0.4.5 and pacman 0.5.x from CRAN source into the per-run library /workspace/audit_runs/15_1BBC4E/A/rlib (`Ncpus=1`). kableExtra 1.4.0 and psych 2.4.12 were already present as Debian r-cran-* packages.
