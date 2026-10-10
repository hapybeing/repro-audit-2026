# Diffs, 14_CJISMY agent B

- `crosssection_linear.R.diff` (file keeps the authors' CRLF line endings):
  - line 1 `library(specr)` commented out: specr was not installed in the run library when the main run was made; no specr function is called anywhere in crosssection_linear.R (read in full). Allowed by PREREG section 2 step 4.
  - the two `marginaleffects::plot_predictions` / `ggsave` blocks (Figure 2 and the H2/H3 null-result figure) wrapped in `try({ ... })` so a plotting failure cannot stop the run. Allowed by PREREG step 4. They did not fail in this run (both PDFs were written).
  - No model, data or table line changed.
- Not a file edit: the three data files were saved as `data/epro_data_h1.csv`, `data/epro_data_h2.csv`, `data/epro_geo_data_h3.csv` from `?format=original` downloads, because the deposit is flat and holds ingested .tab versions while the code reads `data/<name>.csv` (PREREG step 1).
