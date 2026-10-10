#!/usr/bin/env python3
"""Builds results.json from outputs/targets_extracted.csv, outputs/robustness.csv and ../targets.json."""
import csv, json, os, re
from datetime import datetime
P = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A"
tg = json.load(open(os.path.join(P, "..", "targets.json")))
ex = {r["model"]: r for r in csv.DictReader(open(os.path.join(P, "outputs/targets_extracted.csv")))}
rb = {r["id"]: r for r in csv.DictReader(open(os.path.join(P, "outputs/robustness.csv")))}
meta = json.load(open(os.path.join(P, "outputs/run_meta.json")))
def stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "none"
paper_sig = {"T1": (True, "***"), "T2": (True, "***"), "T3": (False, "none"), "T5": (True, "**")}
src = {"T1": ("model1B", "estimate"), "T2": ("model2B", "estimate"), "T3": ("model3B", "estimate"),
       "T4": ("model1B", "nobs"), "T5": ("model2G", "estimate"), "T6": ("model2G", "nobs")}
targets = []
for t in tg:
    m, field = src[t["id"]]; r = ex[m]
    rep = float(r[field]) if field == "estimate" else int(float(r[field]))
    pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    ad = rep - pv; rd = ad / abs(pv)
    match = round(rep, d) == round(pv, d)
    note = ""
    if field == "estimate":
        p = float(r["p_value"]); sig, pst = paper_sig[t["id"]]
        same = (rep < 0) and ((p < 0.05) == sig)
        note = (f"{m}: SE {float(r['se']):.6f}, p {p:.3g} ({r['p_type']}, vcov: {r['vcov']}); star band reproduced {stars(p)} vs paper {pst}")
        if t["id"] == "T5":
            note += f"; lmerTest Satterthwaite p {float(r['p_satterthwaite']):.3g}"
        if t["id"] == "T2":
            hl = []
            okall = True
            for mm in ["model1", "model2", "model4"]:
                e = float(ex[mm]["estimate"]); hl.append(f"{mm} {e:.4f} (SE {float(ex[mm]['se']):.4f})")
                okall = okall and e < 0 and 0.03 <= round(abs(e), 2) <= 0.06
            note += "; headline check Table 2 multilevel interaction: " + ", ".join(hl) + f"; negative and |est| in [0.03,0.06] at 2 dp: {okall}"
    else:
        same = rep == pv
        others = ["model1B","model2B","model3B","model4B"] if t["id"] == "T4" else ["model1G","model2G","model3G","model4G"]
        note = "nobs " + ", ".join(f"{o}={int(float(ex[o]['nobs']))}" for o in others) + "; groups " + r["n_groups"]
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
        "reproduced_value": rep, "source_file": "outputs/targets_extracted.csv", "abs_diff": ad, "rel_diff": rd,
        "match_to_rounding": match, "within_5pct": abs(rd) <= 0.05, "same_conclusion": same, "note": note})
desc = {"R_a": "Cluster (district) bootstrap of model2B, seed 20261010, 1000 replicates, duplicated districts get new FE ids; percentile 95% CI",
        "R_b": "Drop rows with |z| > 3 on voto_pro_gober (600-row data), refit model2B; secondary 1st/99th percentile trim if 0 rows dropped",
        "R_c": "model2B with SE clustered by state (vcov = ~id_estado)"}
rob = []
for k in ["R_a", "R_b", "R_c"]:
    r = rb[k]; e = float(r["estimate"]); p = float(r["p_value"])
    if k == "R_a":
        lo, hi = float(r["ci_low"]), float(r["ci_high"])
        sec = f"95% percentile CI [{lo:.4f}, {hi:.4f}]; bootstrap SE {float(r['se']):.4f}"
        ok = e < 0 and hi < 0
        note = f"replicates used {r['n_used']}, not estimable {r['n_failed']}; p = 2*min share (>=0, <=0)"
    else:
        sec = f"SE {float(r['se']):.4f}"
        ok = e < 0 and p < 0.05
        note = (f"rows dropped {r['rows_dropped']}, nobs {r['nobs']}; " if k == "R_b" else f"clusters {r['n_clusters']}; ") + r["extra"]
    rob.append({"id": k, "description": desc[k], "ran": True, "estimate": e, "se_or_ci": sec, "p_value": p,
                "same_direction_and_significance_as_paper": ok, "source_file": "outputs/robustness.csv", "note": note})
ex2 = {r["model"]: r for r in csv.DictReader(open(os.path.join(P, "outputs/targets_extracted_fixest0142.csv")))}
cmp = "; ".join(f"{t['id']}: {src[t['id']][0]} {src[t['id']][1]} = {ex2[src[t['id']][0]][src[t['id']][1]]}" for t in tg)
meta["uncertainties"].append("Comparison run with current CRAN fixest 0.14.2 (outputs/targets_extracted_fixest0142.csv): " + cmp + "; Table B vcov there: " + ex2["model2B"]["vcov"] + ", SE model2B " + ex2["model2B"]["se"])
allA = all(t["match_to_rounding"] for t in targets)
allB = all(t["within_5pct"] and t["same_conclusion"] for t in targets)
cls = "A" if allA else ("B" if allB else "D")
res = {"paper_id": "07_JH9DBC", "agent": "A", "run_date_ist": meta["run_date_ist"], "ran": True, "could_not_run_reason": "",
       "targets": targets, "robustness": rob, "bugs": meta["bugs"], "env_fixes": meta["env_fixes"],
       "proposed_class": cls, "class_reason": meta["class_reason_A"] if cls == "A" else "Computed class from targets; see targets notes.",
       "confidence": meta["confidence"], "confidence_reason": meta["confidence_reason"],
       "time_minutes": round((datetime.fromisoformat(meta["end_utc"]) - datetime.fromisoformat(meta["start_utc"])).total_seconds() / 60), "uncertainties": meta["uncertainties"],
       "code_review_scope": meta["code_review_scope"], "unverified_observations": meta["unverified_observations"]}
json.dump(res, open(os.path.join(P, "results.json"), "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]] for t in targets}))
print(cls)
