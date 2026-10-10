<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch1_code_observations.csv` applies. For 01_5BIH0P: unverified agent observation: 01-3, 01-4; verified finding: 01-1, 01-2. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# LOG: 01_5BIH0P, Agent B (independent second pass)

All times IST (Asia/Kolkata), 2026-10-09. Scratch: /workspace/audit_runs/01_5BIH0P/B/. Saved results: this folder.
Isolation: I did not open, list or read REPO/papers/01_5BIH0P/A/, /workspace/audit_runs/01_5BIH0P/A/, the project work/
folder, any batch report, or any other paper's folder. (The sandbox tool printed names of files other agents created
under those paths as change notices; I did not open them.)

## 21:12 Start
- Read REPO/PROTOCOL.md, REPO/AGENT_RUNBOOK.md, META.md, PREREG.md, targets.json (empty list `[]`).
- Downloaded paper full text XML from Europe PMC (PMC10950042) and the supplementary zip (Europe PMC supplementaryFiles).
  Downloaded Dataverse dataset JSON (version 6.0, released 2025-12-17, 146 files, none restricted).

## 21:13 to 21:15 Paper check (scripts/paper_scan.py -> outputs/paper_scan.json)
- 2XWT / TSH / K1-70 occur only in Table 1: row "2XWT b, 5 seeds, TSH receptor in complex with autoantibody K1-70 mAb, 200 ns",
  footnote b "Free binding energy calculations are available." No computed number for 2XWT in text, captions or the text of the
  three supplementary files (Supporting file 3 uses 6RP8 as its worked example).
- The paper's computed numbers concern 5DK3 (RMSD 0.36 / 1.52 nm) and 6UMT (binding free energies, Figure 5). Neither complex is in
  this dataset. I agree with PREREG: no reproducible paper target; targets stay `[]`.
- Not checked: text inside the 12 images embedded in Supporting file 1 and the main figure images (no OCR).

## 21:14 to 21:16 Downloads (raw/, checksums.sha256)
- Per-file downloads from https://dataverse.harvard.edu/api/access/datafile/<id> with User-Agent "repro-audit-2026".
  Every downloaded data file's MD5 matched the Dataverse metadata checksum; sha256 recorded in checksums.sha256.
  Largest file 4.98 MB; nothing near 50 MB; trr/tpr/cpt/edr/gro not downloaded.

## 21:16 to 21:18 Internal checks I1 to I3 (scripts/internal_checks.py -> outputs/internal_checks.json, outputs/per_frame_delta.csv)
- Parsed the GB and PB "Delta Energy Terms" tables (20 frames: 10, 110, ..., 1910) in FINAL_RESULTS_MMPBSA.csv.
- Means match the author summary in FINAL_RESULTS_MMPBSA.dat to 2 decimals for every Delta term:
  GB dTOTAL -103.6975 (author -103.70), PB dTOTAL 14.423 (14.42), dVDWAALS -97.823 (-97.82), dEEL -668.974 (-668.97),
  dEGB 681.823 (681.82), dESURF -18.724 (-18.72).
- SD: author SDs match population SD (ddof=0), e.g. GB dTOTAL 11.052 vs author 11.05; the PREREG text says "sample SD (ddof=1)",
  which gives 11.339. Both are written to the output. Means are not affected.
- Delta = Complex - Receptor - Ligand recomputed per frame from the CSV agrees within 0.01 (rounding of the 2-decimal CSV).
- RESULTS_gmx_MMPBSA.h5 (gmx_MMPBSA's own per-frame store) gives the same per-frame Delta TOTAL (max |diff| 0.0 after rounding to
  2 dp) and mean -103.6976 (GB), 14.4223 (PB).

## 21:18 Robustness (scripts/robustness.py -> outputs/robustness.json), exactly as PREREG section 3
- R_a: bootstrap mean -103.748, 95% percentile CI [-108.186, -98.625]; excludes 0.
- R_b: max |z| = 2.899, no frame with |z| > 3; fallback trim (drop -122.02 and -70.82): mean -104.506, SEM 1.821 (n=18).
- R_c: PB mean 14.423 (SEM 2.360), opposite sign to GB (-103.698). Optional R_c2 (igb=2) not run (keep shared CPUs light).

## 21:19 to 21:23 Deposited Python code: xvg2csv.py (scripts/xvg_format_check.py -> outputs/xvg_format_check.json)
- xvg2csv.py and xvg2csv-1.py are identical. Under Python 3.12: `SyntaxError: Missing parentheses in call to 'print'`.
  No python2 available. Env fix: print statements -> print() (diffs/xvg2csv.py.diff). No logic change.
- Ran it on 2xwt-rs3-310k-200ns-rmsd.xvg, 2xwt-rs3-400ns-310k-rmsd.xvg, 2xwt-rs3-400ns-310k-rmsf.xvg. All three outputs are
  byte-identical to the deposited original CSVs behind the .tab files. This is a format check, not a reproduction (the .xvg are
  themselves author outputs; the trajectories that produced them are not deposited).
- Code review findings (details in results.json "bugs"): line 31 '@ s' prefix test catches '@ subtitle', giving the column label
  "fter lsq fit to Protein"; line 25 hard-codes "Time (ps)" although the RMSD files are in ns (-tu ns); line 36 writes no header
  when the .xvg has no legend lines (rmsf), and Dataverse ingest then used the residue 1 row as variable names ("1", "0.3080"),
  so the ingested rmsf .tab has 673 cases instead of 674. Effects are on deposited derived files only, not on any paper number.
- Observation (not a bug): 400 ns RMSD series starts at 4.4786 nm at t=0 and stays near 4.45 nm; it has 40,002 rows with time
  200.0000153 ns duplicated. The 200 ns series starts at 0.0005 nm and ends at 0.6465 nm. Cannot explain without trajectories.

## 21:16 to 21:20 AmberTools install (optional step 2)
- micromamba 2.9.0, conda-forge ambertools 26.0 (linux-aarch64, nompi), Python 3.11, own pkgs cache (a shared cache lock was held by
  another process, so I used a private CONDA_PKGS_DIRS). Installed in about 4 minutes, well under the 30 min cap.

## 21:24 onward GB rerun with sander (scripts/run_gb.sh; scripts/gb_recompute.py -> outputs/gb_recompute_gb.json)
- First launch failed: `/usr/bin/time: No such file or directory` (my wrapper); removed `time`, relaunched 21:24.
- sander run with the deposited gmx_MMPBSA inputs unchanged (_GMXMMPBSA_gb_decomp_{lig,rec,com}.mdin: imin=5, igb=5, gbsa=2,
  surften=0.0072, idecomp=1), deposited prmtops, dummy inpcrd and 20-frame mdcrd.0 files. One system at a time, OMP_NUM_THREADS=1,
  nice 10.
- ESURF: cpptraj LCPO `surf :*` on each mdcrd (scripts/B_*_surf.cpptraj.in); SASA identical to the deposited
  _GMXMMPBSA_*_gb_surf.dat.0 files (checked in gb_recompute.py). ESURF = 0.0072 * SASA, as in gmx_MMPBSA.
- Ligand finished 21:29 (20 frames); first frame terms equal the deposited Ligand row to the CSV's 2 decimals.
- Receptor finished 21:39, complex finished 21:52 (sander wall time about 28 min in total for the three systems on a shared,
  loaded machine). Copies of my sander mdout and SASA files: outputs/amber/.

## 21:53 GB rerun result (scripts/gb_recompute.py -> outputs/gb_recompute_gb.json)
- Per-system TOTAL per frame vs deposited CSV: max |diff| 0.0048 (complex), 0.0047 (receptor), 0.0044 (ligand) kcal/mol, i.e.
  within the 2-decimal rounding of the CSV. SASA from my cpptraj run identical to the deposited surf.dat files.
- Delta TOTAL over 20 frames: mean -103.6976 kcal/mol, population SD 11.052; max per-frame |diff| vs deposited 0.0047.
  This reproduces I1 (-103.70) from the deposited intermediates with an independent sander build (Amber 26 vs authors' Amber 21).
- PB not rerun (authors' PB took 46 min on their machine; not pre-registered as required). Optional R_c2 (igb=2) not run.

## 21:54 Results
- scripts/build_results.py reads outputs/*.json and writes results.json (targets [], internal_checks, robustness, bugs).
- Proposed class C, confidence medium (reasons in results.json). Wall clock 21:12 to 21:55.
