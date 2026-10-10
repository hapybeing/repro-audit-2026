# Protocol (fixed before any selection or results)

Written 2026-10-09 (IST), before the sampling frame was inspected and before any paper was drawn.
Any later change is logged in `CHANGELOG_METHOD.md` with what changed, why, and when.
(Note: this file was lost from the workspace at about 20:30 IST and restored verbatim at 21:12 IST; see CHANGELOG_METHOD.md #3.)

## 1. Sampling frame
- Repository: Harvard Dataverse (https://dataverse.harvard.edu), an open repository named in the spec.
- Frame = every published dataset released 2023-01-01 to 2026-12-31 (Dataverse `dateSort`) that contains at least one
  file whose Dataverse content type is R (`type/x-r-syntax`, `text/x-r-notebook`, `text/x-r-markdown`) or
  Python (`text/x-python`, `text/x-python-script`, `application/x-ipynb+json`).
- Built by `scripts/01_build_frame.py` from the public Search API (no sign-in). Output: `selection/frame_raw.csv`,
  which is `candidates.csv` (title, dataset DOI, link, code language), plus `selection/frame_meta.json` (build time).

## 2. Random order
- Seed: **20261009**. Frame rows sorted by dataset DOI, then permuted with `numpy.random.default_rng(20261009).permutation`.
- Script: `scripts/02_select.py`. The permuted order is saved before screening starts.

## 3. Screening (applied strictly in random order; first 25 eligible are selected)
A dataset is eligible only if all hold:
- E1. It is the data/code for one specific peer-reviewed journal article with a DOI, published 2023-2026.
- E2. The article full text is openly readable without sign-in (publisher OA or an open repository copy, checked via Unpaywall).
- E3. No file in the dataset is restricted or needs a request/sign-in.
- E4. No Stata (.do/.ado), MATLAB (.m), SPSS (.sps) or SAS (.sas) code files are present. (Data files such as .dta are fine if read from R/Python.)
- E5. Total dataset size is 5 GB or less (pre-set compute feasibility limit for a 2-CPU / 7 GB RAM sandbox).
- E6. The licence permits use (CC0 / CC-BY / similar, or Dataverse default terms). Redistribution in our repo only if the licence allows; otherwise link + checksum.
Each screened dataset gets a row in `selection/screening.csv` with pass/fail per criterion and a reason. Screening never looks at results, author names or "suspiciousness".

Field = the Dataverse `subject` metadata of the dataset. If the first 25 eligible papers cover fewer than 3 subjects,
the latest-drawn papers of the most common subject are replaced, one at a time, by the next eligible dataset in random
order from a different subject, until 3 subjects are covered. (Decided now, before seeing the frame.)

## 4. Order and batches
Audit order = screening order of the 25 selected. Batch k = positions 5k-4 .. 5k. No reordering or swapping once any result exists.

## 5. Per paper (Agent A)
0. Before running anything, record in `papers/<id>/PREREG.md`: the headline result(s) (the main quantitative claim(s) in the abstract
   and the table/figure that reports them, with the paper's numbers copied from the paper), and the 3 robustness checks:
   (a) different random seed or bootstrap resample, (b) exclude extreme outliers (rule stated in advance, default |z| > 3 on the
   outcome, or top/bottom 1% where z is meaningless), (c) one alternative reasonable analysis choice.
1. Reproduce in a clean environment (fresh R library / Python venv). Only environment fixes allowed (package versions, paths); each as a diff in `papers/<id>/diffs/`.
2. Run the robustness checks exactly as pre-registered.
3. Code review: real bugs only, with file, line and evidence.
4. Every number reported is written to `papers/<id>/A/outputs/*.json|csv` by a script; no hand-typed numbers.
5. Environment record: OS, R/Python version, package versions, seeds, date.

## 6. Independent second pass (Agent B)
A separate agent, in a separate directory, given only: paper DOI, dataset DOI, and `PREREG.md` (targets copied from the paper + check definitions).
It does not see Agent A's logs, diffs or outputs. It re-downloads and re-runs from scratch. Then `scripts/compare_ab.py` compares A and B.
Any disagreement in classification or in a key number beyond rounding is flagged in the batch report, not resolved silently.

## 7. Classification
- A: reproduced exactly (matches to the paper's reported rounding).
- B: reproduced approximately (all headline numbers within 5% relative, same direction and same significance conclusion).
- C: not reproduced, materials incomplete or unclear (missing files, code that cannot produce the reported table, undocumented steps).
- D: not reproduced, discrepancy remains and affects the conclusion. Only if the discrepancy survives both A and B clean runs.
- E: could not run (reason stated, e.g. exceeds compute, missing system dependency that cannot be installed).
Robustness outcomes are reported separately and do not change the class.

## 8. Confidence (per paper)
- high: A and B agree, headline numbers matched by script, environment close to the authors'.
- medium: A and B agree but something needed judgement (which number is headline, package version drift, partial run).
- low: A and B disagree, or key steps could not be verified.

## 9. Reporting
Counts only per batch, no percentages. Tables generated by `scripts/make_tables.py` from saved outputs.
No author contact, no public posts other than this repo, no personal logins.
