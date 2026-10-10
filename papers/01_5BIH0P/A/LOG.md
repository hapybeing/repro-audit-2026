# LOG, 01_5BIH0P, agent A

Paper: Singh PK, Stan RC, ThermoPCD, Database 2024 baae015 (doi:10.1093/database/baae015).
Dataset: doi:10.7910/DVN/5BIH0P (2XWT, random seed 3, 310 K), version 6.0, 146 files, 938,233,575 bytes, CC0.
Scratch: /workspace/audit_runs/01_5BIH0P/A/. Saved results: this folder.

## 2026-10-09 21:11 IST  Start, reading
- Read PROTOCOL.md, AGENT_RUNBOOK.md, CHANGELOG_METHOD.md, META.md, PREREG.md, targets.json (`[]`).
- PREREG.md sha256 1189c28f...f303 matches batches/batch1_prereg_hashes.txt. PREREG not edited.
- Did not open anything under papers/*/B/. (The shared machine's file-change notices and one `ps` listing showed names of
  other agents' files/processes; I did not open or use them.)

## 2026-10-09 21:12 IST  Dataset metadata and targeted download
- Pulled the dataset JSON from the Dataverse API. 146 files, none restricted. Downloaded 38 small files (all < 6 MB, about
  27 MB total) via `scripts/download.py`: authors' scripts (xvg2csv.py, xvg2csv-1.py, em-md-nvt-npt-single*.sh), all MMPBSA
  results/inputs/intermediates needed for I1-I3 and the optional GB recompute, three .xvg/.tab pairs, md.mdp, topol.top, the
  gmx_MMPBSA logs, RESULTS_gmx_MMPBSA.h5. Every file matched Dataverse's stored MD5; sha256 in `checksums.sha256`.
- Did not download nvt.trr/npt.trr (323 MB each) or the large .log/.edr/.tpr/.cpt files; not needed.

## 2026-10-09 21:13 IST  Optional AmberTools install started (background, 30 min budget)
- micromamba + conda-forge `ambertools` for linux-aarch64. First attempt was interrupted when the sandbox recycled
  (about 21:21 IST, uptime reset); restarted from the package cache. Install finished 21:26:35 IST (AmberTools 26.0),
  about 14 minutes after starting, so within the 30 minute limit.

## 2026-10-09 21:14 IST  Verify "no paper target" independently
- Fetched the full text (Europe PMC PMC10950042 XML, sha256 in checksums). `scripts/evidence.py` -> `outputs/paper_evidence.json`.
- 2XWT occurs exactly once in the paper: a Table 1 row (5 seeds, "TSH receptor in complex with autoantibody K1-70 mAb",
  200 ns, footnote b "Free binding energy calculations are available"). No computed value for 2XWT anywhere in the text.
- The only computed numbers in the paper are the 5DK3 RMSDs (0.36 nm, 1.52 nm) and the 6UMT binding free energies
  (-114.2, -132, -148, -126.3 kJ/mol; "about 30%"). Neither complex is in this dataset (all file names refer to 2xwt only;
  `outputs/deposit_inventory.json`). I agree with PREREG: targets.json correctly empty.
- Deposit inventory: no .xtc file at all; .trr files are only em/nvt/npt. The analysis inputs named in the .xvg headers and
  gmx_MMPBSA log (dynamic-nopbc.xtc, dynamic-nopbc-2.xtc, system_reduced.xtc, COM_traj_0.xtc) are absent. PDB snapshots exist
  only for 250, 300, 350, 400 ns (the abstract describes PDB outputs every 50 ns). The abstract says "MD trajectories are
  freely available"; the production trajectory for this seed is not in this deposit (it may be elsewhere in ThermoPCD; not checked).
- Dataset title says 400 ns; Table 1 says 200 ns for 2XWT. The deposit holds 200 ns analyses (xvg created 2023-09-15) and
  400 ns analyses (created 2024-06-11, after acceptance 2024-02-22).

## 2026-10-09 21:15 IST  Authors' Python code (xvg2csv.py)
- Clean venv (Python 3.12.15, numpy 2.1.3, scipy 1.14.1). `python xvg2csv.py <file>.xvg` fails under Python 3:
  `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?` (saved verbatim).
- Env fix: print statements -> print() (`diffs/xvg2csv.py.diff`). Re-ran on 2xwt-rs3-310k-200ns-rmsd.xvg,
  2xwt-rs3-400ns-310k-rmsd.xvg, 2xwt-rs3-400ns-310k-rmsf.xvg. All three outputs are byte-identical to the deposited original
  .tab files (`outputs/xvg2csv_check.json`, CSVs in `outputs/authors_xvg2csv/`). This is a format check, not a reproduction:
  the .xvg inputs come from trajectories that are not deposited.
- em-md-nvt-npt-single.sh is the GROMACS MD pipeline itself (not run, per PREREG; GROMACS not installed, and 200-400 ns of MD
  for this system is far beyond the 2-CPU budget).

## 2026-10-09 21:17 IST  Internal checks I1-I3 and robustness R_a, R_b, R_c (as pre-registered)
- `scripts/internal_checks.py` parses FINAL_RESULTS_MMPBSA.csv (20 frames, 10..1910).
- I1-I3 means match the deposited summary to 2 decimals. Observed: the deposited SD/SEM (e.g. 11.05 / 2.47 for GB dTOTAL)
  equal the population SD (ddof=0), not the sample SD (ddof=1) that PREREG step 1 names; the PREREG targets are the averages,
  so this does not affect I1-I3. Both SDs are written to outputs/internal_checks.json.
- R_a: bootstrap as written (10,000, default_rng(20261009)). R_b: no frame with |z|>3, so the pre-registered fallback
  (drop lowest and highest of 20) was applied. R_c: PB mean instead of GB. Results in outputs/robustness.json.
- Supplementary (not pre-registered, labelled as such): per-frame Delta = Complex - Receptor - Ligand holds within 0.01
  (2-decimal rounding) for GB and PB; per-frame VDWAALS/EEL/EGB/BOND in the deposited sander GB mdout files equal the CSV
  within 0.005; ESURF = 0.0072 x LCPO area from *_gb_surf.dat.0 matches exactly after rounding
  (outputs/supplementary_consistency.json). A first version of the mdout parser also captured decomposition-check blocks
  and "1-4 EEL"; fixed to read the first energy block per frame before results were used.

## 2026-10-09 21:27 IST  Optional GB recompute with AmberTools (PREREG step 2) and R_c2 (igb=2)
- `scripts/run_gb_amber.sh <igb>`: MMPBSA.py on COM/REC/LIG.prmtop + _GMXMMPBSA_complex.mdcrd.0 (20 frames, all used).
- Attempt 1 (21:27): `InputError: Unknown variable intdiel in &gb` (AmberTools 26 MMPBSA.py has no intdiel/extdiel in &gb).
  Removed both from gb.in (intdiel=1.0 is the sander default).
- Attempt 2 (21:28): noticed MMPBSA.py writes extdiel=80.0 into the sander mdin while the authors' sander mdin (echoed in the
  deposited mdout) has no extdiel (sander default 78.5). Stopped that run before it finished. Switched to `-make-mdins`,
  removing extdiel=80.0, then `-use-mdins` (diff saved; see diffs/README.md).
- Attempt 3 (21:30) was killed when my foreground shell timed out (child of that shell). Relaunched detached (setsid) at 21:32.
- The machine load average was about 8 on 2 CPUs (other agents), so sander ran at roughly 30% of one CPU.
- igb=5 run: 21:32:27 to 21:39:51 IST, exit 0. Per-frame Complex/Receptor/Ligand/Delta VDWAALS, EEL, EGB, ESURF and TOTAL
  all agree with the deposited 2-decimal CSV within 0.005 (rounding), and the Delta TOTAL mean agrees with I1 to 2 decimals
  (`scripts/parse_amber.py` -> `outputs/amber_gb_recompute.json`; raw MMPBSA.py outputs in `outputs/amber/`).
  The first three complex frames' sander VDWAALS and EGB were also identical to 4 decimals with the authors' mdout (spot check).
- R_c2 (igb=2, same 20 frames, same mdin edit): 21:39:51 to 21:46:29 IST, exit 0. Result in outputs/amber_gb_recompute.json.

## 2026-10-09 21:48 IST  Code review
- Read in full: xvg2csv.py (44 lines; xvg2csv-1.py is byte-identical), em-md-nvt-npt-single.sh (10 commands; -1.sh identical),
  and the input decks used (mmpbsa.in, mmpbsa-1.in, md.mdp, the sander mdin echoed in the deposited GB mdout).
- Bugs (labels only, values unaffected): xvg2csv.py line 31/33 takes the GROMACS '@ subtitle' line as a series legend and
  truncates it ('fter lsq fit to Protein' header in the deposited RMSD .tab files); line 25 hard-codes 'Time (ps)' while the
  RMSD .xvg files are in ns (`-tu ns`). Evidence in outputs/xvg2csv_check.json.
- Not bugs, recorded as observations: the MD shell script covers only the first 200 ns segment (md_0_10); the extension
  segments (md_1_20, md_1_30, 400 ns) and the trajectory processing (trjconv to dynamic-nopbc*.xtc, system_reduced.xtc) are
  undocumented in the deposit. mmpbsa-1.in (endframe 4000, no &pb) does not correspond to any deposited result.
  md.mdp nsteps = 100,000,000 x 2 fs = 200 ns, consistent with Table 1.

## 2026-10-09 21:50 IST  Class decision and results
- Proposed class C (reasons in results.json class_reason and outputs/uncertainties.txt). Internal checks did not drive it.
- `scripts/build_results.py` builds results.json from outputs/.
