#!/usr/bin/env python3
"""Builds results.json from files in outputs/ (targets_extracted.csv, robustness.json, checks.json) and ../targets.json."""
import csv, json, os, math
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(B, "outputs")
tg = json.load(open(os.path.join(os.path.dirname(B), "targets.json")))
PRIMARY = "targets_extracted_fixest0121.csv"; SECOND = "targets_extracted_fixest_current.csv"
rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, PRIMARY)))}
rows2 = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, SECOND)))}
rob = json.load(open(os.path.join(O, "robustness.json")))
meta = json.load(open(os.path.join(O, "run_meta.json")))
stars = lambda p: "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "none"
paper_star = {"T1": "***", "T2": "***", "T3": "none", "T5": "**"}
paper_sig = {"T1": True, "T2": True, "T3": False, "T5": True}
targets = []
for t in tg:
    r = rows.get(t["id"]); d = t["paper_rounding_decimals"]
    if t["id"] in ("T4", "T6"):
        src = rows["T1" if t["id"] == "T4" else "T5"]
        val = int(float(src["nobs"]))
        others = [int(float(rows[k]["nobs"])) for k in (["T1","T2","T3","secB4"] if t["id"]=="T4" else ["secG1","T5","secG3","secG4"])]
        note = f"nobs across the four models: {others}. {src['note']}"
        same = (val == t["paper_value"]) and all(o == t["paper_value"] for o in others)
    else:
        val = float(r["estimate"]); p = float(r["p"]); se = float(r["se"])
        same = (val < 0) and ((p < 0.05) == paper_sig[t["id"]])
        note = (f"SE {se:.6f}, p {p:.6g} ({r['p_type']}; vcov {r['vcov']}); reproduced star band {stars(p)} vs paper {paper_star[t['id']]}; "
                f"SE rounded {round(se,3)}. {r['note']}")
    ad = val - t["paper_value"]; rd = ad / abs(t["paper_value"])
    m = round(val, d) == t["paper_value"] if d > 0 else int(round(val)) == t["paper_value"]
    r2 = rows2["T1" if t["id"] == "T4" else ("T5" if t["id"] == "T6" else t["id"])]
    v2 = int(float(r2["nobs"])) if t["id"] in ("T4","T6") else float(r2["estimate"])
    note += (f" | Run with fixest {r2['fixest_version']} (current CRAN, PREREG step 2 literally): value {v2}" + ("" if t["id"] in ("T4","T6") else f", SE {float(r2['se']):.6f}, p {float(r2['p']):.6g}, vcov {r2['vcov']}") + f" ({SECOND}).")
    targets.append(dict(id=t["id"], description=t["description"], paper_value=t["paper_value"], paper_rounding_decimals=d,
        reproduced_value=val, source_file="outputs/" + PRIMARY, abs_diff=ad, rel_diff=rd,
        match_to_rounding=bool(m), within_5pct=abs(rd) <= 0.05, same_conclusion=bool(same), note=note))
# headline note on T2
hl = []
for k in ("tab2_1", "tab2_2", "tab2_4"):
    v = float(rows[k]["estimate"]); hl.append((rows[k]["model"], v, round(abs(v), 2)))
ok = all(v < 0 and 0.03 <= mag <= 0.06 for _, v, mag in hl)
for t in targets:
    if t["id"] == "T2":
        t["note"] += " | Headline check (Table 2 multilevel, paper values unread): " + "; ".join(f"{m} {v:.6f} (|.|2dp={mag})" for m, v, mag in hl) + f"; negative and within 0.03 to 0.06: {ok}."
def rb(key, desc, pass_, est, seci, p, note):
    return dict(id=key, description=desc, ran=True, estimate=est, se_or_ci=seci, p_value=p, same_direction_and_significance_as_paper=pass_, source_file="outputs/robustness.json", note=note)
a, b, c = rob["R_a"], rob["R_b"], rob["R_c"]
robust = [
 rb("R_a", "Cluster (district) bootstrap of model2B, seed 20261010, 1000 replicates, percentile CI", a["pass"], a["estimate"],
    f"95% percentile CI [{a['ci_low']:.6f}, {a['ci_high']:.6f}], bootstrap SE {a['boot_se']:.6f}", a["p_value"],
    f"not-estimable replicates: {a['n_not_estimable']}. Secondary model2 (multilevel): {json.dumps(a['secondary_model2_multilevel'])}"),
 rb("R_b", "Drop |z|>3 on voto_pro_gober, refit model2B", b["pass"], b["estimate"], f"SE {b['se']:.6f} (fixest default)", b["p_value"],
    f"rows dropped {b['rows_dropped']}, nobs {b['nobs']}. Secondary 1/99 trim: {json.dumps(b['secondary_trim_1_99'])}. Secondary model2 (multilevel, |z|<=3 data): {json.dumps(b['secondary_model2_multilevel'])}"),
 rb("R_c", "model2B with SE clustered by state (vcov=~id_estado)", c["pass"], c["estimate"], f"SE {c['se']:.6f}, {c['n_clusters']} clusters", c["p_value"],
    f"indicted states: {c['indicted_states']}. Secondary model2: not applicable."),
]
res = dict(paper_id="07_JH9DBC", agent="B", run_date_ist="2026-10-10", ran=meta["ran"], could_not_run_reason=meta.get("could_not_run_reason",""),
    targets=targets, robustness=robust, bugs=meta["bugs"], env_fixes=meta["env_fixes"])
allA = all(t["match_to_rounding"] for t in targets); allB = all(t["within_5pct"] and t["same_conclusion"] for t in targets)
cls = "A" if allA else ("B" if allB else meta.get("fallback_class", "D"))
res["proposed_class"] = cls
res["class_reason"] = meta["class_reason"][cls]
res.update(confidence=meta["confidence"], confidence_reason=meta["confidence_reason"], time_minutes=meta["time_minutes"], uncertainties=meta["uncertainties"])
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]] for t in targets}), cls)
