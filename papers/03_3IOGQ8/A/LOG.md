# LOG, paper 03_3IOGQ8, Agent A

Scratch: /workspace/audit_runs/03_3IOGQ8/A/ (dl/, run/, rlib/, venv/). Saved results: this folder.
Times are IST (UTC+05:30).

## 2026-10-09

- 21:11 IST. Read PROTOCOL.md, AGENT_RUNBOOK.md, META.md, PREREG.md, targets.json. sha256 of PREREG.md = d5afdb29...1d6e, matches batches/batch1_prereg_hashes.txt. Did not read anything under papers/*/B/, other papers' runs, or ../work/p03.
- 21:11 IST. Downloaded fresh: Dataverse dataset metadata (API, version 1, released 2024-09-11) and the Rmd (datafile 10408478). Rmd sha256 5f364768...a538 equals PREREG; md5 equals Dataverse metadata md5. Dataset has exactly 3 files: two Thermo RAW (ids 10407991, 10407990) and the Rmd. None restricted. Only one dataset version exists. Licence CC0 1.0.
- 21:12-21:14 IST. Read the whole Rmd (3351 lines, 28 chunks). Input inventory (outputs/input_inventory.txt, by grep): the only file reads are `read.csv("Byonic_results.csv")` (line 498) and `openMSfile()` on three placeholder `.mzML.gz` paths (lines 671-679). No FASTA is read by the Rmd (the FASTA is a Byonic search input). Every later chunk depends on `Byonic_df` from line 498.
- 21:14-21:15 IST. Looked for an open route to the missing input:
  - Paper full text (Europe PMC PMC11638967 XML, sha256 b1a47451...a846, same as PREREG): only data pointer is 10.7910/DVN/3IOGQ8 ("Raw data" and "custom scripts"); no PRIDE/MassIVE/ProteomeXchange/Zenodo/GitHub accession; no data availability section beyond that.
  - bioRxiv preprint full text (PMC11451751): same, only the Dataverse DOI.
  - SI bundle from Europe PMC (zip sha256 9e609e20...5824; si_001.xlsx and si_002.pdf hashes equal PREREG). SI xlsx holds only per-proteoform summary Tables S2-S5 (157/179/73/98 rows). SI PDF (pdftotext) has no accession or repository mention.
  - PRIDE archive API keyword searches ("sortase histone", "Whedon", "cut-and-paste middle-down", "circular engineered sortase", "cW11"): no relevant project (cW11 hit 2 unrelated old projects). ProteomeCentral PROXI search ignored the search term (returned latest datasets), so it was uninformative. Web search: no deposit found.
  - Dataverse search for "Whedon": 3 datasets, the other two are different papers (2022, 2023).
  - Conclusion: no open, sign-in-free route to Byonic_results.csv or an equivalent PSM table. The RAW files are therefore NOT downloaded (no concrete open route uses them); their Dataverse MD5s are in checksums.sha256.
- 21:15 IST. Environment fix: diffs/01_working_directory.diff (line 10 placeholder path to run dir). R 4.5.0 system Rscript present; all needed CRAN packages present in the system library except mzR (Bioconductor; not available via apt here). mzR build not attempted: it is first used at line 671, after the stop at line 498.
- 21:16 IST. Partial run: scripts/run_partial.R evaluates chunk 1 and chunk 2 of the env-fixed Rmd expression by expression, logging every error (outputs/partial_run_log.txt). Result: chunk 1 only error is `library(mzR)` ("there is no package called 'mzR'"); chunk 2 stops at line 498 `read.csv("Byonic_results.csv")` with "cannot open the connection", and every later expression in the chunk fails for want of Byonic_df. Chunks 3-28 not run.
- 21:17 IST. Code review tests (scripts/code_review_tests.R -> outputs/code_review_tests.json), evaluating the authors' own functions/expressions verbatim on synthetic inputs:
  - Test 1: generate_ions_for_sequence on the H3.1 tail with K9me3. Neutral-loss (Kme3) b and c ions at fragment i equal the fragment i-1 ion minus the loss (TRUE), not fragment i minus the loss (FALSE). Off-by-one confirmed.
  - Test 2: TMT correction block (lines 2659-2686) on a synthetic scan with only reagent 126. 127 keeps its full 76 units of 126 spill, 126 loses 5.8 units, 128 becomes negative. Correction looks transposed vs the vectors' stated convention.
- 21:18 IST. SI published values extracted by scripts/si_published_values.py -> outputs/si_published_values.json (paper side only, for reference). Values equal PREREG (fc 1.35671135138228 MS275, 1.07715354602644 Corin; 179 rows Table S3; 100*(2^fc-1) = 156.10 and 110.99).
- 21:18 IST. The sandbox was recycled during the run (Rscript disappeared; another agent's apt-get held the dpkg lock). Waited for R to be reinstalled to record environment.txt and re-run both R scripts.
- 21:21 IST. R back (4.5.0, Debian). Re-ran scripts/run_partial.R and scripts/code_review_tests.R; outputs identical in content to the first run (same errors; same test results). Wrote environment.txt, checksums.sha256, diffs/README.md.
- Robustness R_a, R_b, R_c: NOT run. Each needs scan-level TMT reporter values that exist only inside the pipeline after line 498; no substitute from SI tables (PREREG section 3).
- Code review: read the whole Rmd (all 28 chunks; plotting chunks skimmed). 3 bugs recorded in results.json (1 confirmed by test, 1 probable confirmed on synthetic input against the code's own stated convention, 1 probable from code only). Observations not counted as bugs listed under uncertainties.
- Class: proposed C (materials incomplete: undeposited Byonic PSM export and FASTA, template code with placeholder paths and aliases). PREREG pre-stated E; Protocol section 7 lists missing files under C, while E is described as compute or install limits. Disagreement with PREREG wording recorded as an uncertainty.
- 21:21 IST. Built results.json with scripts/build_results.py (reads outputs/ and targets.json).
