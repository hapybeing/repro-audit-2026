"""Build results.json for 01_5BIH0P agent A from files in outputs/ (no hand-typed result numbers).
Internal-check reference values are parsed from PREREG.md (which copied them from the deposited FINAL_RESULTS_MMPBSA.dat)."""
import json, re, os, math
P = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/01_5BIH0P"
A = f"{P}/A"; O = f"{A}/outputs"
prereg = open(f"{P}/PREREG.md", encoding="utf-8").read()
num = r"(-?\d+\.\d+)"
ref = {"I1": float(re.search(r"I1: GB ΔTOTAL.*?Average = " + num, prereg).group(1)),
       "I2": float(re.search(r"I2: PB ΔTOTAL, Average = " + num, prereg).group(1))}
i3 = re.search(r"I3: GB ΔVDWAALS = " + num + r", ΔEEL = " + num + r", ΔEGB = " + num + r", ΔESURF = " + num, prereg)
ref.update({"I3a": float(i3.group(1)), "I3b": float(i3.group(2)), "I3c": float(i3.group(3)), "I3d": float(i3.group(4))})
assert json.load(open(f"{P}/targets.json")) == [], "targets.json is expected to be empty"

ic = json.load(open(f"{O}/internal_checks.json"))
rb = json.load(open(f"{O}/robustness.json"))
NOTE = "internal check, not a paper target (PREREG section 1, optional internal-consistency values); mean of 20 deposited per-frame Delta values from FINAL_RESULTS_MMPBSA.csv"
def tgt(i, desc, key, src, note=NOTE):
    pv = ref[i.split("_")[0]]; rv = None if key is None else (ic[key]["mean"] if isinstance(key, str) else key)
    d = {"id": i, "description": desc, "paper_value": pv, "paper_rounding_decimals": 2, "reproduced_value": rv, "source_file": src}
    if rv is None:
        d.update({"abs_diff": None, "rel_diff": None, "match_to_rounding": None, "within_5pct": None, "same_conclusion": None})
    else:
        d.update({"abs_diff": rv - pv, "rel_diff": (rv - pv) / abs(pv), "match_to_rounding": round(rv, 2) == pv,
                  "within_5pct": abs((rv - pv) / pv) <= 0.05, "same_conclusion": math.copysign(1, rv) == math.copysign(1, pv)})
    d["note"] = note
    return d
targets = [
    tgt("I1", "GB Delta TOTAL, average over 20 frames (kcal/mol), 2XWT seed 3, 310 K, 200 ns", "I1_GB_dTOTAL", "outputs/internal_checks.json",
        NOTE + f". Deposited SD 11.05 equals the population SD (ddof=0) {ic['I1_GB_dTOTAL']['sd_ddof0']:.4f}; sample SD (ddof=1) is {ic['I1_GB_dTOTAL']['sd_ddof1']:.4f}."),
    tgt("I2", "PB Delta TOTAL, average over 20 frames (kcal/mol)", "I2_PB_dTOTAL", "outputs/internal_checks.json"),
    tgt("I3a", "GB Delta VDWAALS average (kcal/mol)", "I3_GB_dVDWAALS", "outputs/internal_checks.json"),
    tgt("I3b", "GB Delta EEL average (kcal/mol)", "I3_GB_dEEL", "outputs/internal_checks.json"),
    tgt("I3c", "GB Delta EGB average (kcal/mol)", "I3_GB_dEGB", "outputs/internal_checks.json"),
    tgt("I3d", "GB Delta ESURF average (kcal/mol)", "I3_GB_dESURF", "outputs/internal_checks.json"),
]
amber = f"{O}/amber_gb_recompute.json"
amb = json.load(open(amber)) if os.path.exists(amber) else None
if amb and amb.get("igb5", {}).get("ran"):
    targets.append(tgt("I1_amber", "GB (igb=5) Delta TOTAL recomputed with AmberTools MMPBSA.py from deposited prmtops + 20-frame mdcrd",
                       amb["igb5"]["delta_total_mean"], "outputs/amber_gb_recompute.json",
                       "internal check (optional PREREG step 2), not a paper target; different AmberTools version and CPU architecture than the authors'"))

ra, rbb, rc = rb["R_a"], rb["R_b"], rb["R_c"]
NOPAPER = "No paper value exists for 2XWT, so comparison with the paper is not applicable (null). "
robust = [
 {"id": "R_a", "description": "bootstrap of mean per-frame GB Delta TOTAL, 10,000 resamples, numpy default_rng(20261009), 2.5/97.5 percentiles",
  "ran": True, "estimate": ra["bootstrap_mean"], "se_or_ci": f"95% percentile CI [{ra['ci_2.5']:.2f}, {ra['ci_97.5']:.2f}]",
  "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": NOPAPER + f"CI excludes 0: {ra['ci_excludes_0']}; same sign as the deposited GB mean (I1). p_value left null: the pre-registered check defines no test (descriptive one-sample t p={ra['p_t_full']:.3g} is in the source file)."},
 {"id": "R_b", "description": "drop frames with |z|>3 (ddof=1) on per-frame GB Delta TOTAL; if none, trim 1 lowest and 1 highest frame",
  "ran": True, "estimate": rbb["mean"], "se_or_ci": f"SEM {rbb['sem']:.2f} (n={rbb['n']})", "p_value": None,
  "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": NOPAPER + f"No frame had |z|>3 (max |z| = {rbb['max_abs_z']:.3f}), so the pre-registered fallback (5% trimming each side) was applied."},
 {"id": "R_c", "description": "Poisson-Boltzmann instead of Generalized Born: mean per-frame PB Delta TOTAL from the same file",
  "ran": True, "estimate": rc["mean"], "se_or_ci": f"SEM {rc['sem']:.2f} (ddof=1, n={rc['n']})", "p_value": None,
  "same_direction_and_significance_as_paper": None, "source_file": "outputs/robustness.json",
  "note": NOPAPER + f"Same sign as GB estimate: {rc['same_sign_as_GB']} (PB positive, GB negative), as anticipated descriptively in PREREG."},
]
if amb and "igb2" in amb:
    g2 = amb["igb2"]
    robust.append({"id": "R_c2", "description": "GB recomputed with igb=2 instead of igb=5 on the same 20 frames (AmberTools MMPBSA.py)",
                   "ran": bool(g2.get("ran")), "estimate": g2.get("delta_total_mean"), "se_or_ci": g2.get("sem_text", ""), "p_value": None,
                   "same_direction_and_significance_as_paper": None, "source_file": "outputs/amber_gb_recompute.json", "note": NOPAPER + g2.get("note", "")})

log = open(f"{A}/LOG.md", encoding="utf-8").read()
ts = re.findall(r"^## (\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) IST", log, re.M)
mins = [int(h) * 60 + int(m) for _, h, m in ts]
res = {
 "paper_id": "01_5BIH0P", "agent": "A", "run_date_ist": ts[0][0],
 "ran": True,
 "could_not_run_reason": "No paper target exists for this dataset (targets.json is empty): the paper's only computed numbers concern 5DK3 and 6UMT, which are not in DVN/5BIH0P. What did run: the authors' xvg2csv.py (after a Python 2 to 3 print fix), the pre-registered internal checks I1-I3 and robustness checks R_a-R_c on the deposited per-frame MMPBSA data" + ("; the optional AmberTools 26 GB recompute (igb=5) from the deposited prmtops and 20-frame trajectory, plus R_c2 (igb=2)" if (amb and amb.get('igb5', {}).get('ran')) else "; the optional AmberTools GB recompute did not complete (see LOG.md)") + ". The production MD trajectory is not deposited, so no MD-derived quantity could be regenerated.",
 "targets": targets, "robustness": robust,
 "supplementary_checks": json.load(open(f"{O}/supplementary_consistency.json")),
 "bugs": [
  {"file": "xvg2csv.py (identical in xvg2csv-1.py)", "line": 31,
   "description": "Legend detection `if l.startswith(\"@ s\")` also matches the GROMACS '@ subtitle' line, and line 33 `' '.join(l.split()[3:])[1:-1]` then drops the first word and first character, so the CSV column header is wrong.",
   "evidence": "Deposited 2xwt-rs3-310k-200ns-rmsd.tab and 2xwt-rs3-400ns-310k-rmsd.tab (original-format downloads) have header 'Time (ps),fter lsq fit to Protein'; the .xvg has no '@ s0 legend' line, only '@ subtitle \"Protein after lsq fit to Protein\"'. Labels only; numeric values are unaffected (outputs/xvg2csv_check.json)."},
  {"file": "xvg2csv.py (identical in xvg2csv-1.py)", "line": 25,
   "description": "First column header is hard-coded as 'Time (ps)', but the RMSD .xvg files were produced with `gmx rms ... -tu ns`, so the deposited RMSD .tab files label nanosecond values as picoseconds.",
   "evidence": "xvg header 'xaxis label \"Time (ns)\"' and command '-tu ns'; last time value 400.0000305 in the 400 ns file and 200.0000153 in the 200 ns file, while the .tab header says 'Time (ps)' (outputs/xvg2csv_check.json). Labels only."}
 ],
 "env_fixes": ["diffs/xvg2csv.py.diff: xvg2csv.py is Python 2 (print statements) and raises SyntaxError under Python 3.12; print statements converted to print() calls, output text unchanged. No python2 interpreter on the machine.",
               "diffs/mmpbsa_gb_mdin_extdiel.diff: optional AmberTools GB recompute only (not the authors' code). AmberTools 26 MMPBSA.py rejects intdiel/extdiel in &gb and writes extdiel=80.0; removed so sander's default 78.5 applies, as in the authors' sander mdin."],
 "proposed_class": "C",
 "class_reason": "The paper reports no computed number for 2XWT (it appears only as a Table 1 metadata row), and the deposit lacks the production trajectories that its own analysis files were made from, so the materials cannot produce any reported paper number; nothing was blocked by compute or an uninstallable dependency, which is what E describes. The deposited code and MMPBSA intermediates that could be run were run (including a GB recompute with AmberTools) and are internally consistent, but that is not reproduction of a paper number.",
 "confidence": "medium",
 "confidence_reason": "Class needed judgement (no paper target exists; C vs E is a definitional call), and A/B agreement is not yet known.",
 "time_minutes": (max(mins) - min(mins)) if mins else None,
 "uncertainties": []
}
unc = open(f"{O}/uncertainties.txt", encoding="utf-8").read().strip().splitlines() if os.path.exists(f"{O}/uncertainties.txt") else []
res["uncertainties"] = [u.lstrip("- ").strip() for u in unc if u.strip()]
json.dump(res, open(f"{A}/results.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ("proposed_class", "time_minutes")}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in targets])
