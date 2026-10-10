# PREREG: 01_5BIH0P

Written 2026-10-09 (IST), before any analysis code was run. No analysis code was run to write this file; only the paper, its
supplement, the Dataverse file list and a few small text files from the dataset were read.

- Paper: Singh PK, Stan RC. "ThermoPCD: a database of molecular dynamics trajectories of antibody-antigen complexes at physiologic
  and fever-range temperatures". Database (Oxford) 2024: baae015. DOI https://doi.org/10.1093/database/baae015
  (PMC10950042, PMID 38502609). Full text read from Europe PMC:
  https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10950042/fullTextXML
- Supplement read: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10950042/supplementaryFiles (baae015_supp.zip, containing
  Supporting files 1 to 3: computational methods, GROMACS analysis protocol, gmx_MMPBSA protocol using 6RP8 as the example).
- Dataset: "PDB - 2XWT: TSH receptor in complex with autoantibody K1-70 (310K, 37°C, 400 ns): random seed #3",
  DOI https://doi.org/10.7910/DVN/5BIH0P, Harvard Dataverse, version 6 (released 2025-12-17), deposited 2025-01-20,
  146 files, 938,233,575 bytes, licence CC0 1.0. File list: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/5BIH0P
- Note for the auditors: REPO/PROTOCOL.md does not exist in the repo at the time of writing (only AGENT_RUNBOOK.md and
  CHANGELOG_METHOD.md). This PREREG follows AGENT_RUNBOOK.md and the assignment brief.

## 1. Headline results and targets

### What the paper claims
The paper is a database description. Its abstract makes no quantitative claim beyond counts (50 antibody:antigen complexes,
100 to 500 ns simulations). The only computed numbers in the text are:
- Pembrolizumab (PDB 5DK3) RMSD vs crystal after 100 ns: 0.36 nm at 310 K and 1.52 nm at 313 K (Results, "Comparisons between
  structures", 2 decimals).
- PD-1/PD-L2 (PDB 6UMT) mean binding free energies over three 500 ns seeds: -114.2 +/- 6.4, -132 +/- 2.9, -148 +/- 9.2 and
  -126.3 +/- 8.1 kJ/mol at 310, 311, 312 and 313 K (Results, "Assessing temperature-dependent changes in binding free energies",
  Figure 5; decimals 1, 0, 0, 1 as printed), and "about 30%" increase from 37 to 39 °C.

### Can this dataset reproduce them?
No. Both sets of numbers concern other complexes (5DK3, 6UMT) that are not in this dataset. This dataset holds only PDB 2XWT,
random seed 3, at 310 K.

For 2XWT the paper reports only descriptive metadata in Table 1 (row "2XWT b": 5 seeds, "TSH receptor in complex with
autoantibody K1-70 mAb", duration 200 ns, footnote b "Free binding energy calculations are available"). These are not computed
quantities. No RMSD, RMSF, Rg, SASA, H-bond count or binding free energy value for 2XWT appears in the main text, in Table 1, in
the figures (Figure 5 is 6UMT only) or in the three supplementary files.

**Conclusion: there is no reproducible paper target for this dataset. targets.json is an empty list.** The expected class under
the runbook scheme is therefore not A or B by construction; the auditing agents should decide between C (materials do not support
any reported number) and E, and say why.

### Observations that bear on classification (descriptive only)
- Table 1 lists 2XWT with a 200 ns duration; the dataset title says 400 ns. The dataset contains both 200 ns analysis files
  (2xwt-rs3-310k-200ns-*.xvg, created 2023-09-15 per their headers) and 400 ns analysis files (2xwt-rs3-400ns-310k-*.xvg,
  created 2024-06-11), so part of the dataset postdates the paper (accepted 2024-02-22).
- The production trajectory is not in the dataset. There is no .xtc file; the only .trr files are em.trr, nvt.trr and npt.trr
  (minimisation and 100 ps equilibration). The analysis commands in the .xvg headers read dynamic-nopbc.xtc / dynamic-nopbc-2.xtc,
  and the MMPBSA run read system_reduced.xtc; none of these is deposited. Production run inputs (md_0_10.tpr, md_1_20.tpr,
  md_1_30.tpr, checkpoints .cpt, final .gro, .edr energies, .log) are present, so the trajectory could in principle be regenerated
  by re-running GROMACS, but not bit-identically and not within the compute budget (see section 4).
- The MMPBSA intermediates for 2XWT seed 3, 310 K, 200 ns are present: COM/REC/LIG.prmtop, _GMXMMPBSA_{complex,receptor,ligand}.mdcrd.0
  (20 frames, frames 10 to 1910 every 100 of a 2000 frame, 200 ns trajectory; per gmx_MMPBSA-1.log), the GB and PB sander mdout
  files, RESULTS_gmx_MMPBSA.h5, FINAL_RESULTS_MMPBSA.dat/.csv. gmx_MMPBSA v1.5.2, run 2023-09-07, igb=5, temperature 310 K.
  gmx_MMPBSA.log (the short one) is a failed earlier attempt ("index.ndx do not exist"); gmx_MMPBSA-1.log is the completed run.

### Optional internal-consistency values (NOT paper targets; do not put in targets.json; do not use for the class)
These are author output values in FINAL_RESULTS_MMPBSA.dat (Dataverse file id 10835633), copied here before any recomputation so
that the auditors can, if they choose, check that the deposited per-frame data and intermediates reproduce the deposited summary.
They are reported as "internal check", not as reproduction of the paper.
- I1: GB ΔTOTAL (Delta, Complex - Receptor - Ligand), Average = -103.70 kcal/mol (SD 11.05, SEM 2.47, 20 frames), 2 decimals.
- I2: PB ΔTOTAL, Average = 14.42 kcal/mol (SD 10.29, SEM 2.30), 2 decimals.
- I3: GB ΔVDWAALS = -97.82, ΔEEL = -668.97, ΔEGB = 681.82, ΔESURF = -18.72 kcal/mol, 2 decimals.

## 2. Reproduction plan

### Paper targets
None (see section 1). Nothing to run for T-targets. Agents should set `ran` according to whether they ran the optional internal
checks, list `targets: []`, and explain in `could_not_run_reason` / `class_reason` that no 2XWT number is reported in the paper.

### Optional internal checks (if the agent runs anything)
Scripts in the dataset: xvg2csv.py and xvg2csv-1.py (identical, Python 2 syntax: `print "..."`; under Python 3 this needs either a
python2 interpreter or a print-statement fix recorded as an env-fix diff) and em-md-nvt-npt-single.sh / -1.sh (GROMACS grompp/mdrun
pipeline; do not run, it is the MD itself). There is no script that produces any summary statistic; gmx_MMPBSA produced I1 to I3.

Plan, in order of cost:
1. I1 to I3 from per-frame data (cheap, no MD software). Download FINAL_RESULTS_MMPBSA.csv (file id 10835674, 20,631 bytes). In
   the "GENERALIZED BORN" block, read the "Delta Energy Terms" table (20 rows, Frame # 10, 110, ..., 1910) and compute the mean and
   sample SD (ddof=1) of TOTAL, VDWAALS, EEL, EGB, ESURF. Repeat for the "POISSON BOLTZMANN" Delta table (TOTAL). Compare with
   I1 to I3 rounded to 2 decimals. Write per-frame table and summary to outputs/.
2. Optional, stronger: recompute GB energies from the deposited intermediates with AmberTools (MMPBSA.py or sander) using
   COM.prmtop, REC.prmtop, LIG.prmtop and _GMXMMPBSA_{complex,receptor,ligand}.mdcrd.0, igb=5, saltcon=0.0, surften=0.0072,
   intdiel=1.0, extdiel=78.5, LCPO surface, as in mmpbsa.in (file id 10835733) and _GMXMMPBSA_info (file id 10835682). Only GB
   (PB took 46 min on the authors' machine). Attempt only if AmberTools installs on aarch64 within about 30 minutes; otherwise
   record as not run.
3. The 200 ns and 400 ns RMSD/RMSF/Rg/SASA/H-bond .xvg files cannot be regenerated: the input trajectories are not deposited.
   Re-converting .xvg to .csv with xvg2csv.py and comparing to the Dataverse .tab files is a format check only, not a reproduction.

## 3. Robustness checks (pre-registered; apply to I1, the GB ΔTOTAL, since no paper target exists)

Data for all three: the 20 per-frame GB Delta TOTAL values from FINAL_RESULTS_MMPBSA.csv (step 1 above).

- R_a (resample): nonparametric bootstrap of the mean GB ΔTOTAL over the 20 frames, 10,000 resamples with replacement, numpy
  default_rng(seed=20261009). Report the bootstrap mean, the 2.5 and 97.5 percentile interval, and whether the interval excludes 0
  (the quantity a reader would care about: favourable binding, negative ΔG). A different MD random seed is not possible: only seed 3
  is in this dataset and the trajectory is not deposited.
- R_b (outliers): compute z = (x - mean) / SD (ddof=1) of per-frame GB ΔTOTAL; drop frames with |z| > 3; recompute the mean and
  SEM. If no frame has |z| > 3, report that and instead apply 5% trimming on each side (drop the single lowest and single highest of
  20 frames) and report that mean.
- R_c (alternative analysis choice): use the Poisson-Boltzmann model instead of Generalized Born, i.e. the mean of per-frame PB
  ΔTOTAL from the "POISSON BOLTZMANN" Delta table of the same file, and report whether it has the same sign as the GB estimate.
  (From the deposited summary, GB is -103.70 and PB is 14.42, so a sign difference is expected; record it descriptively.) As a
  second alternative, if step 2 ran, the auditor may additionally recompute GB with igb=2 instead of igb=5 on the same 20 frames;
  report it separately and label it R_c2.

None of these checks touches the paper's conclusions, because the paper reports no 2XWT number.

## 4. Feasibility notes

- Compute: the paper-level analyses (MD runs of 200 to 400 ns for a 674-residue solvated complex) are far beyond the 2 CPU,
  ~2 hour budget; regenerating the production trajectory is not feasible. Step 1 above is seconds. Step 2 (GB only, 20 frames, 674
  residues) took 8 min on the authors' machine for GB; expect a similar or longer time on 2 aarch64 CPUs.
- Data size: 938 MB total. Do NOT download the whole dataset. Large files are nvt.trr and npt.trr (323 MB each), md_0_10.log
  (15 MB), .edr, .gro, .tpr, .cpt files. Everything needed for the internal checks is under 15 MB: FINAL_RESULTS_MMPBSA.csv
  (id 10835674), FINAL_RESULTS_MMPBSA.dat (10835633), mmpbsa.in (10835733), _GMXMMPBSA_info (10835682), gmx_MMPBSA-1.log
  (10835681), COM.prmtop (10835644), REC.prmtop (10835740), LIG.prmtop (10835657), _GMXMMPBSA_complex.mdcrd.0 (10835632),
  _GMXMMPBSA_receptor.mdcrd.0 (10835658), _GMXMMPBSA_ligand.mdcrd.0 (10835628). Per-file URL:
  https://dataverse.harvard.edu/api/access/datafile/<id> with User-Agent "repro-audit-2026".
- Dependencies: step 1 needs only Python 3 (csv/numpy). Step 2 needs AmberTools (sander or MMPBSA.py); the authors used
  gmx_MMPBSA 1.5.2 with AmberTools (MMPBSA.py v16.0), ParmEd 3.4.3, Python 3.9.12 and GROMACS 2021.5 on x86_64 Ubuntu 20.04. The
  paper text says GROMACS 2020; the .xvg headers say GROMACS 2021.5. xvg2csv.py is Python 2.
- Licence: dataset CC0 1.0 (redistribution allowed, no conditions). Paper CC BY 4.0.
