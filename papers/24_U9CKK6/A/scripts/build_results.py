#!/usr/bin/env python3
"""Build results.json for 24_U9CKK6 agent A from files in outputs/ (no typed reproduced numbers)."""
import csv, json, math, re, statistics, os
from datetime import datetime
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A"
P = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6"
def rd(p): return list(csv.DictReader(open(p, encoding="utf-8")))
tg = json.load(open(f"{P}/targets.json"))
ex = rd(f"{O}/outputs/targets_extracted.csv")
def get(model, term):
    r = [x for x in ex if x["model"] == model and x["term"] == term]; assert len(r) == 1; return r[0]
def rround(x, d):  # R round(x, d): IEC 60559 round half to even on the decimal; adequate here (no exact .5 ties)
    return round(x, d)
spec = {"T1": ("cycle_AE_fit2", "challenge:days_to_nat", "***"), "T2": ("cycle_AE_fit2", "days_to_EP", "***"),
        "T3": ("cycle_AE_fit2", "challenge", "***"), "T4": ("cycle_AE_fit2", None, None),
        "T5": ("AUT_sal_model", "challenge:aut_sal", "**"), "T6": ("EU_sal_model", "challenge:EU_sal", "*")}
def bucket(p): return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
targets = []
for t in tg:
    model, term, stars = spec[t["id"]]; pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    if term is None:
        r = get(model, "challenge"); val = float(r["nobs"]); val = int(val)
        same = abs(val - pv) <= 5; note = "nobs(cycle_AE_fit2); same_conclusion rule |N - 266854| <= 5 (PREREG)."
    else:
        r = get(model, term); val = float(r["estimate"]); p = float(r["p_naive"])
        b = bucket(p); same = (val > 0) and (b == stars)
        note = (f"SE {float(r['se']):.6f}, naive p {p:.3g} (texreg default, pre-registered), star bucket {b} vs paper {stars}; "
                f"printed SE in paper: see PREREG; reproduced SE rounds to {round(float(r['se']), 2):.2f}.")
    ad = val - pv; rel = ad / pv if pv != 0 else None
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
        "reproduced_value": val, "source_file": "outputs/targets_extracted.csv",
        "abs_diff": ad, "rel_diff": rel, "match_to_rounding": rround(val, dec) == pv,
        "within_5pct": (abs(rel) <= 0.05) if rel is not None else None, "same_conclusion": same,
        "note": note + (" within_5pct is computed against the 1-2 significant-digit printed value as the runbook defines it and is not informative here (PREREG section 1); match_to_rounding is the meaningful test." if t["id"] != "T4" else "")})
# robustness
rb = {r["check"] + "|" + r["target"]: r for r in rd(f"{O}/outputs/robustness_bc.csv")}
orig = float(get("cycle_AE_fit2", "challenge:days_to_nat")["estimate"])
rob = []
# R_a
K = rd(f"{O}/outputs/R_a_K.csv")[0]; Kn = int(float(K["K"]))
bt = rd(f"{O}/outputs/R_a_partial.csv")
ok = [float(x["estimate"]) for x in bt if x["ok"] == "TRUE" and int(x["draw"]) <= Kn and x["estimate"] not in ("", "NA")]
failed = [x for x in bt if x["ok"] != "TRUE" and int(x["draw"]) <= Kn]
conv = sum(1 for x in bt if x["ok"] == "TRUE" and x["conv_messages"] not in ("", "NA"))
dropped = sum(1 for x in bt if x["dropped_cols"] not in ("", "NA"))
def q7(v, p):
    v = sorted(v); h = (len(v) - 1) * p; lo = math.floor(h); return v[lo] + (h - lo) * (v[min(lo + 1, len(v) - 1)] - v[lo])
if len(ok) >= 2:
    bse = statistics.stdev(ok); lo, hi = q7(ok, 0.025), q7(ok, 0.975)
    pn = math.erfc(abs(orig / bse) / math.sqrt(2)); ci_ex = lo > 0 or hi < 0
    same_a = orig > 0 and ci_ex and pn < 0.001
    complete = len(ok) + len(failed) >= Kn
    rob.append({"id": "R_a", "description": "Party-cluster bootstrap of T1 (204 party_id clusters, set.seed(20261011), K = min(200, floor(3600/t)))",
        "ran": True, "estimate": orig, "se_or_ci": f"bootstrap SE {bse:.6f}; 95% percentile interval [{lo:.6f}, {hi:.6f}]",
        "p_value": pn, "same_direction_and_significance_as_paper": same_a, "source_file": "outputs/R_a_partial.csv",
        "note": f"t_first = {float(K['t_first_secs']):.1f} s, K = {Kn} ({K['status']}); successful refits {len(ok)}, failed refits {len(failed)}, "
                f"refits with lme4 convergence messages {conv}, refits with dropped rank-deficient columns {dropped}; "
                f"percentile interval excludes 0: {ci_ex}; normal p from estimate/bootstrap SE < 0.001: {pn < 0.001}. "
                f"Mean of bootstrap estimates {statistics.mean(ok):.6f}." + ("" if complete else " INCOMPLETE: fewer draws than K finished.")})
else:
    rob.append({"id": "R_a", "description": "Party-cluster bootstrap of T1", "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
                "same_direction_and_significance_as_paper": None, "source_file": "outputs/R_a_partial.csv", "note": "not enough draws finished"})
r = rb["R_b_outliers_absz_gt3|T1"]
rob.append({"id": "R_b", "description": "T1 refit after dropping |z| > 3 on embed_dict_scale within the cycle_AE_fit2 estimation sample",
    "ran": True, "estimate": float(r["estimate"]), "se_or_ci": f"SE {float(r['se']):.6f}", "p_value": float(r["p_naive"]),
    "same_direction_and_significance_as_paper": float(r["estimate"]) > 0 and float(r["p_naive"]) < 0.001,
    "source_file": "outputs/robustness_bc.csv", "note": f"rows dropped {r['rows_dropped']}, nobs {r['nobs']}"})
for tid, b in [("T5", (0.001, 0.01)), ("T6", (0.01, 0.05))]:
    r = rb[f"R_b_outliers_absz_gt3_secondary|{tid}"]; e = float(r["estimate"]); p = float(r["p_naive"])
    rob.append({"id": f"R_b_secondary_{tid}", "description": f"Secondary R_b: {tid} refit after dropping |z| > 3 on the outcome within its estimation sample",
        "ran": True, "estimate": e, "se_or_ci": f"SE {float(r['se']):.6f}", "p_value": p,
        "same_direction_and_significance_as_paper": e > 0 and b[0] <= p < b[1], "source_file": "outputs/robustness_bc.csv",
        "note": f"rows dropped {r['rows_dropped']}, nobs {r['nobs']}; paper star bucket {b[0]} <= p < {b[1]}; p < 0.05: {p < 0.05}"})
r = rb["R_c_year_as_factor|T1"]
rob.append({"id": "R_c", "description": "T1 refit with year replaced by as.factor(year), nothing else changed",
    "ran": True, "estimate": float(r["estimate"]), "se_or_ci": f"SE {float(r['se']):.6f}", "p_value": float(r["p_naive"]),
    "same_direction_and_significance_as_paper": float(r["estimate"]) > 0 and float(r["p_naive"]) < 0.001,
    "source_file": "outputs/robustness_bc.csv", "note": f"nobs {r['nobs']}; estimate rounds to {round(float(r['estimate']), 2):.2f}"})
# sanity
for k, v in rb.items():
    if k.startswith("sanity"):
        pass
# time from LOG headings
heads = re.findall(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", open(f"{O}/LOG.md").read(), re.M)
tm = (datetime.strptime(heads[-1], "%Y-%m-%d %H:%M") - datetime.strptime(heads[0], "%Y-%m-%d %H:%M")).total_seconds() / 60
gof = {x["model"]: x for x in rd(f"{O}/outputs/model_gof.csv")}
allmatch = all(t["match_to_rounding"] for t in targets); allsame = all(t["same_conclusion"] for t in targets)
res = {"paper_id": "24_U9CKK6", "agent": "A", "run_date_ist": heads[0][:10], "ran": True, "could_not_run_reason": "",
  "targets": targets, "robustness": rob,
  "bugs": json.load(open(f"{O}/outputs/code_observations.json")),
  "env_fixes": [
    "diffs/run_table1_plain.diff, diffs/run_table2_plain.diff: .libPaths to per-run library, setwd to run folder, skip-if-saved wrapper and saveRDS after each model (PREREG section 2); authors' lines unchanged (outputs/range_identity_check.txt)",
    "diffs/run_table1_f1f2.diff, diffs/run_table2_f1f2.diff: pre-registered memory fallback F1 (blank unused text columns 4 and 6 after load) and F2 (rm + gc after each saveRDS; combined texreg built from saved models). Used because the plain Table 1 run passed 3 GB RSS (3199 MB) and was stopped by the watchdog during the third model; the two models it had saved are byte-identical to the F1/F2 ones (outputs/plain_vs_f1f2.csv)",
    "diffs/texreg_table1_from_rds.diff, diffs/texreg_table2_from_rds.diff: F2, authors' combined texreg call run on the saved models",
    "Packages installed from CRAN into the per-run library (texreg, sjstats, sjPlot, skimr, fixest and dependencies); lme4, Matrix, zoo, tidyverse from the system library; no version pins exist in the deposit (environment.txt)"],
  "proposed_class": "A" if (allmatch and allsame) else ("B" if allsame else "C"),
  "class_reason": ("All six targets match the printed Table 1 (Model 2) and Table 2 values to their rounding, with the same star buckets under the pre-registered texreg naive p; "
                   f"the full printed Table 1 fit statistics also match (Model 2 AIC {float(gof['cycle_AE_fit2']['AIC']):.2f}, logLik {float(gof['cycle_AE_fit2']['logLik']):.2f})."
                   if allmatch and allsame else "See targets."),
  "confidence": "high",
  "confidence_reason": "Exact match of every target and of printed AIC, log likelihood, N and group counts from the authors' verbatim lines; agreement with agent B not yet known.",
  "time_minutes": round(tm),
  "uncertainties": json.load(open(f"{O}/outputs/uncertainties.json"))}
json.dump(res, open(f"{O}/results.json", "w"), indent=1)
print(json.dumps({t["id"]: (t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]) for t in targets}, indent=0))
print([(r["id"], r["estimate"], r["p_value"], r["same_direction_and_significance_as_paper"]) for r in rob])
