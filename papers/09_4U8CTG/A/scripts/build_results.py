#!/usr/bin/env python3
"""Agent A, 09_4U8CTG: build results.json from files in outputs/. Paper values from targets.json (copied from PREREG)."""
import csv, json, os, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(HERE); OUT = os.path.join(A, "outputs")
PAPER = os.path.dirname(A)
targets_pre = {t["id"]: t for t in json.load(open(os.path.join(PAPER, "targets.json")))}
rows = list(csv.DictReader(open(os.path.join(OUT, "targets_extracted.csv"))))
def get(model, term="treatmentwin_mainstream"):
    for r in rows:
        if r["model"] == model and r["term"] == term:
            return r
    raise KeyError(model)
def rnd(x, d): return float(f"{x:.{d}f}")
T = []
def tgt(tid, val, src, conclusion, note):
    p = targets_pre[tid]; pv = p["paper_value"]; d = p["paper_rounding_decimals"]
    e = {"id": tid, "description": p["description"], "paper_value": pv, "paper_rounding_decimals": d,
         "reproduced_value": val, "source_file": src}
    if val is None:
        e.update(abs_diff=None, rel_diff=None, match_to_rounding=None, within_5pct=None, same_conclusion=None)
    else:
        e["abs_diff"] = val - pv; e["rel_diff"] = (val - pv) / abs(pv)
        e["match_to_rounding"] = rnd(val, d) == pv; e["within_5pct"] = abs(e["rel_diff"]) <= 0.05
        e["same_conclusion"] = conclusion
    e["note"] = note; T.append(e)
SRC = "outputs/targets_extracted.csv"
m1 = get("model_1_ez"); est1 = float(m1["estimate"]); p1 = float(m1["p"]); se1 = float(m1["se"])
tgt("T1", est1, SRC, est1 < 0 and p1 < 0.05,
    f"model_1_ez, term treatmentwin_mainstream; classical SE {se1:.6f} (paper 0.63), two-sided p {p1:.6f}. "
    "Regenerated tables_supplementary_materials/tableD3_ez_swd.tex compared with the deposited copy: see outputs/table_comparison_summary.txt.")
n1 = int(m1["nobs"]); tgt("T2", n1, SRC, abs(n1 - 123) <= 5, "nobs(model_1_ez)")
m3 = get("model_1_ez_lrem"); est3 = float(m3["estimate"]); p3 = float(m3["p"]); se3 = float(m3["se"])
tgt("T3", est3, SRC, est3 < 0 and p3 >= 0.05,
    f"model_1_ez_lrem, term treatmentwin_mainstream; classical SE {se3:.6f} (paper 0.34), two-sided p {p3:.6f}.")
n3 = int(m3["nobs"]); tgt("T4", n3, SRC, abs(n3 - 120) <= 5, "nobs(model_1_ez_lrem)")
na = "Not run: FES 2022 microdata (study1_fes_panel.csv, built by 00 from ELIPSS wave 3/4 files) are not in the deposit and are restricted at ELIPSS; registration not permitted under audit rules. Study 1 code in 02 was skipped (diffs/02_supplementary_materials.R.diff)."
tgt("T5", None, None, None, na); tgt("T6", None, None, None, na)

# robustness
rb = list(csv.DictReader(open(os.path.join(OUT, "robustness.csv"))))
def rr(check, dv): return next(r for r in rb if r["check"] == check and r["dv"] == dv)
R = []
desc = {"R_a": "Stratified case bootstrap within treatment arms, set.seed(20261010), B = 2000, percentile 95% CI; T1 (secondary T3)",
        "R_b": "Drop rows with |z| > 3 on the outcome within the analysis sample, refit lm(dv ~ treatment), classical SE; T1 (secondary T3)",
        "R_c": "ANCOVA lm(swd_w2 ~ treatment + swd_w1), classical SE; T1 (secondary lm(affect_LREM_w2 ~ treatment + affect_LREM_w1))"}
diag = open(os.path.join(OUT, "R_c_diagnostic.txt")).read().strip().replace("\n", "; ")
for c, prim, sec in [("R_a", "swd_ch", "affect_LREM_ch"), ("R_b", "swd_ch", "affect_LREM_ch"), ("R_c", "swd_w2", "affect_LREM_w2")]:
    a = rr(c, prim); b = rr(c, sec)
    est = float(a["estimate"]); p = float(a["p"]); lo = float(a["ci_low"]); hi = float(a["ci_high"])
    same = (est < 0 and hi < 0) if c == "R_a" else (est < 0 and p < 0.05)
    bs, bp, bhi = float(b["estimate"]), float(b["p"]), float(b["ci_high"])
    bsame = (bs < 0 and not bhi < 0) if c == "R_a" else (bs < 0 and bp >= 0.05)
    note = f"n = {a['n']}. Secondary (LREM, {sec}): estimate {bs:.4f}, SE {float(b['se']):.4f}, 95% CI [{float(b['ci_low']):.4f}, {bhi:.4f}], p {bp:.4f}, n = {b['n']}; same as paper's 'negative, not significant at 5%': {bsame}."
    if c == "R_b":
        note += f" Primary dropped {a['dropped']} row(s) ({a['dropped_arms']}); secondary dropped {b['dropped']} ({b['dropped_arms']}). {a['extra']} (primary)."
    if c == "R_a":
        note += " p_value = min(1, 2*min(share >= 0, share <= 0)); SE = SD of bootstrap estimates."
    if c == "R_c":
        note += f" Diagnostic before fitting: {diag}."
    R.append({"id": c, "description": desc[c], "ran": True, "estimate": est,
              "se_or_ci": f"SE {float(a['se']):.4f}; 95% CI [{lo:.4f}, {hi:.4f}]" + (" (percentile)" if c == "R_a" else ""),
              "p_value": p, "same_direction_and_significance_as_paper": same,
              "source_file": "outputs/robustness.csv", "note": note})

mht = list(csv.DictReader(open(os.path.join(OUT, "mht_label_check.csv"))))
mis = [r for r in mht if r["dv"] == "swd_ch" and r["label_matches"] == "FALSE"]
bugs = [{"file": "replication_scripts/02_supplementary_materials.R", "line": 1729,
         "description": "make_mht_table attaches a fixed label vector (Intercept, In-group Government, In-group Parliament, Out-group Government, Placebo) to summary(model)$coefficients[, 4], whose rows follow the treatment factor levels (control, danger_contr, win_govt, win_mainstream, win_parl). Three of the five row labels in Tables D8 and D9 therefore sit next to another coefficient's p-value; the Out-group Government row is correct.",
         "evidence": "; ".join(f"row {r['row']} labelled '{r['label_in_02_table']}' holds p of {r['actual_term']} ({float(r['p_value']):.4f})" for r in mis) + ". Source: outputs/mht_label_check.csv. Does not touch any target."}]
lines = open(os.path.join(A, "LOG.md")).read()
ts = re.findall(r"\[(\d{2}):(\d{2}) IST\]", lines)
mins = None
if ts:
    t = [int(h) * 60 + int(m) for h, m in ts]; mins = max(t) - min(t)
res = {"paper_id": "09_4U8CTG", "agent": "A", "run_date_ist": "2026-10-10", "ran": True,
       "could_not_run_reason": "Partial: Study 2 targets T1 to T4 ran. Study 1 targets T5 and T6 could not run: FES 2022 inputs not in the deposit and registration-only at ELIPSS.",
       "targets": T, "robustness": R, "bugs": bugs,
       "env_fixes": ["diffs/02_supplementary_materials.R.diff: commented out the LaTeX/TinyTeX block (lines 108 to 117; tinytex::tinytex_root() errors on the system TeX Live and would stop the script) and every line that reads or uses the missing Study 1 FES inputs (lines 146 to 149, 162 to 192, 253 to 286, 1218 to 1262, 1454 to 1468, 1789 to 1815, 1818 to 1861). Study 2 code untouched.",
                     "Packages: texreg, stargazer, vtable, jtools, binom installed from CRAN source into a per-run R_LIBS_USER (no Debian binaries); everything else from Debian r-cran-* system binaries (see environment.txt)."],
       "proposed_class": "C",
       "class_reason": "Study 2 targets T1 to T4 reproduce exactly to the paper's rounding, but Study 1 targets T5 and T6 (half the abstract's main claim) rest on FES data available only on registration at ELIPSS, so under batch2_class_decisions.md item 2 the main class is C. Alternative class on openly available targets T1 to T4 only: A.",
       "alternative_class_open_targets_only": "A",
       "confidence": "high",
       "confidence_reason": "T1 to T4 parsed by script from the authors' unmodified Study 2 code and match to rounding; class follows a pre-fixed batch rule. A/B agreement not yet known.",
       "time_minutes": mins,
       "uncertainties": []}
unc_path = os.path.join(OUT, "uncertainties.txt")
if os.path.exists(unc_path):
    res["uncertainties"] = [l.strip() for l in open(unc_path) if l.strip()]
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]] for t in T}))
