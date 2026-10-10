#!/usr/bin/env python3
"""Agent A, 17_T1NXVQ: build results.json from files in outputs/ only (numbers are never typed here).
Paper values come from targets.json (copied from PREREG.md). Class text and notes are judgement and are set in
outputs/class_decision.json (written by hand AFTER reading the outputs; it holds no numbers)."""
import csv, json, math, os, re
REPO = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo"
P = f"{REPO}/papers/17_T1NXVQ"; A = f"{P}/A"; O = f"{A}/outputs"

def rd(path):
    p = os.path.join(O, path)
    if not os.path.exists(p): return None
    with open(p) as f: return list(csv.DictReader(f))

def num(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None

targets_def = json.load(open(f"{P}/targets.json"))
tx = rd("targets_extracted.csv") or []
def tval(model, term=None, col="estimate"):
    for r in tx:
        if r["model"] == model and (term is None or r["term"] == term): return num(r[col])
    return None
bs = rd("boot_summary.csv") or []
def bval(model, sset, term):
    for r in bs:
        if r["model"] == model and r["seed_set"] == sset and r["term"] == term: return r
    return None

spec = {"T1": ("pool_xsec", "cuteth", "estimate"), "T2": ("pool_ldv", "cuteth_lag", "estimate"),
        "T3": ("pool_ldv", "cshp_lag", "estimate"), "T4": ("pool_ldv", "abram_sum", "estimate"),
        "T5": ("pool_xsec", None, "N_sum"), "T6": ("pool_ldv", None, "N_sum")}
targets = []
for t in targets_def:
    model, term, col = spec[t["id"]]
    rep = tval(model, term, col)
    pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    e = {"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
         "reproduced_value": rep, "source_file": "outputs/targets_extracted.csv", "abs_diff": None, "rel_diff": None,
         "match_to_rounding": None, "within_5pct": None, "same_conclusion": None, "note": ""}
    if rep is not None:
        e["abs_diff"] = abs(rep - pv); e["rel_diff"] = (rep - pv) / abs(pv)
        e["match_to_rounding"] = (round(rep, dec) == pv) if dec > 0 else (int(round(rep)) == int(pv))
        e["within_5pct"] = abs(e["rel_diff"]) <= 0.05
        if term is None:
            e["same_conclusion"] = abs(e["rel_diff"]) <= 0.01
            e["note"] = "same_conclusion rule: reproduced count within 1% of the printed count (PREREG)."
        else:
            b = bval(model, "authorseeds", term)
            if b is None or num(b["boot_sd"]) is None:
                e["note"] = "same_conclusion null: no step-6 bootstrap draws for this model (see LOG.md); not inferred from maxLik SE."
            else:
                lo, hi = num(b["ci_lo_1.96sd"]), num(b["ci_hi_1.96sd"])
                e["same_conclusion"] = bool(rep > 0 and lo > 0)
                e["note"] = (f"Reduced bootstrap, authors' seeds {b['seeds']} (K draws ok = {b['n_draws_ok']}, failed = {b['n_draws_failed']}): "
                             f"estimate +/- 1.96 x SD = [{lo:.4f}, {hi:.4f}], SD = {num(b['boot_sd']):.4f} (outputs/boot_summary.csv). "
                             "Printed 120-draw percentile brackets are out of scope (PREREG section 2).")
    else:
        e["note"] = "not produced (see LOG.md)"
    targets.append(e)

def rob_fit(variant, model, term):
    rows = rd(f"fit_{model}_{variant}.csv")
    if not rows: return None, None
    for r in rows:
        if r["term"] == term: return num(r["estimate"]), num(r["maxlik_se"])
    return None, None

def counts(model, variant):
    r = rd(f"counts_{model}_{variant}.csv"); return r[0] if r else None

robust = []
# R_a
b = bval("pool_xsec", "ra_seeds", "cuteth"); b2 = bval("pool_ldv", "ra_seeds", "cuteth_lag")
ratio = rd("boot_sd_ratio.csv") or []
def ratio_of(model, term):
    for r in ratio:
        if r["model"] == model and r["term"] == term: return r
    return None
if b and num(b["boot_sd"]) is not None:
    p = num(b["point_estimate"]); lo, hi = num(b["ci_lo_1.96sd"]), num(b["ci_hi_1.96sd"])
    rr = ratio_of("pool_xsec", "cuteth")
    note = (f"Seeds {b['seeds']}; draws ok {b['n_draws_ok']}, failed {b['n_draws_failed']}; mean of draws {num(b['boot_mean']):.4f}, "
            f"SD {num(b['boot_sd']):.4f}; percentile 2.5/97.5 of the draws (descriptive, small K) {num(b['perc_2.5']):.4f} / {num(b['perc_97.5']):.4f}.")
    if rr: note += f" SD ratio R_a/step-6 = {num(rr['sd_ratio_ra_over_authorseeds']):.3f}; differs by more than a factor 1.5: {rr['differs_more_than_1.5x']}."
    if b2 and num(b2["boot_sd"]) is not None:
        note += (f" Secondary T2 (cuteth_lag, pool_ldv): estimate {num(b2['point_estimate']):.4f}, seeds {b2['seeds']}, SD {num(b2['boot_sd']):.4f}, "
                 f"interval [{num(b2['ci_lo_1.96sd']):.4f}, {num(b2['ci_hi_1.96sd']):.4f}].")
    else:
        note += " Secondary T2 (pool_ldv) R_a draws (seeds 1001-1004) not run: stopped to stay near the about-2-hour wall-time limit after two sandbox restarts (LOG.md 01:57, 02:29)."
    robust.append({"id": "R_a", "description": "Different bootstrap seeds: parametric bootstrap draws with seeds 1001..1000+K (K as in step 6), primary T1 cuteth (pool_xsec)",
                   "ran": True, "estimate": p, "se_or_ci": f"estimate +/- 1.96 x SD of draws: [{lo:.4f}, {hi:.4f}]", "p_value": None,
                   "same_direction_and_significance_as_paper": bool(p > 0 and lo > 0), "source_file": "outputs/boot_summary.csv", "note": note})
else:
    robust.append({"id": "R_a", "description": "Different bootstrap seeds 1001..1000+K", "ran": False, "estimate": None, "se_or_ci": "",
                   "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": "outputs/boot_summary.csv",
                   "note": "not run or no successful draws (see LOG.md)"})

for rid, variant, desc in [("R_b", "rb", "Outlier exclusion: edges with |z| > 3 on length.norm or elevmean.norm (static lattice) set to NA, both Table 1 models refitted"),
                           ("R_c", "rc", "Alternative analysis choice: penalty sigma2 = 1000 instead of 10, both Table 1 models refitted")]:
    est, se = rob_fit(variant, "pool_xsec", "cuteth")
    if est is None:
        robust.append({"id": rid, "description": desc, "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
                       "same_direction_and_significance_as_paper": None, "source_file": f"outputs/fit_pool_xsec_{variant}.csv", "note": "not run (see LOG.md)"})
        continue
    # significance read from outputs/robustness_significance.csv (written by scripts/boot_summary.R, PREREG section 3 rule)
    sg = [r for r in (rd("robustness_significance.csv") or []) if r["model"] == "pool_xsec" and r["variant"] == variant]
    sd = num(sg[0]["sd_boot_step6"]) if sg else None
    sig = None if not sg or sg[0]["same_dir_and_sig"] in ("", "NA") else (sg[0]["same_dir_and_sig"] == "TRUE")
    note = f"maxLik stdEr (descriptive) {se:.4f}."
    cm, cv = counts("pool_xsec", "main"), counts("pool_xsec", variant)
    if cm and cv:
        note += (f" pool_xsec vertices summed over periods: main {cm['N_sum']}, {variant} {cv['N_sum']}; edges main {cm['N_edges_sum']}, {variant} {cv['N_edges_sum']}.")
    if variant == "rb":
        fl = rd("rb_flags_pool_xsec.csv")
        if fl: note += f" Flagged lattice edges: length.norm {fl[0]['flag_length']}, elevmean.norm {fl[0]['flag_elev']}, union {fl[0]['flag_union']} of {fl[0]['n_edges_graph']}."
    e2, s2 = rob_fit(variant, "pool_ldv", "cuteth_lag")
    b2 = bval("pool_ldv", "authorseeds", "cuteth_lag")
    if e2 is not None:
        sd2 = num(b2["boot_sd"]) if b2 else None
        note += f" Secondary T2 cuteth_lag (pool_ldv): {e2:.4f} (maxLik SE {s2:.4f})"
        note += f", significant with step-6 SD: {bool(e2 > 0 and e2 - 1.96 * sd2 > 0)}." if sd2 is not None else ", step-6 SD not available."
        cm2, cv2 = counts("pool_ldv", "main"), counts("pool_ldv", variant)
        if cm2 and cv2: note += f" pool_ldv vertices: main {cm2['N_sum']}, {variant} {cv2['N_sum']}; edges main {cm2['N_edges_sum']}, {variant} {cv2['N_edges_sum']}."
    else:
        note += " Secondary pool_ldv (T2 cuteth_lag) refit not run: stopped to stay near the about-2-hour wall-time limit after two sandbox restarts (LOG.md 02:29)."
    robust.append({"id": rid, "description": desc, "ran": True, "estimate": est,
                   "se_or_ci": ("" if sd is None else f"estimate +/- 1.96 x SD_boot(step 6) = [{est - 1.96 * sd:.4f}, {est + 1.96 * sd:.4f}]"),
                   "p_value": None, "same_direction_and_significance_as_paper": sig,
                   "source_file": f"outputs/fit_pool_xsec_{variant}.csv; outputs/robustness_significance.csv; outputs/boot_summary.csv",
                   "note": note + " p_value null: the pre-registered rule is estimate - 1.96 x SD_boot(step 6, K = 4) > 0; no p-value is defined."})

# informative comparison of reproduced step-6 draws with the deposited pool_se.ls.rds rows (same seeds)
bvd = rd("boot_vs_deposited.csv") or []
other = []
if bvd:
    other.append({"id": "boot_vs_deposited", "description": "Reproduced step-6 bootstrap draws (authors' seeds 1..K) vs rows 1..K of the deposited pool_se.ls.rds beta_boot (informative, PREREG step 6)",
                  "n_compared": len(bvd), "max_abs_diff": max(num(r["abs_diff"]) for r in bvd), "source_file": "outputs/boot_vs_deposited.csv"})
kf = os.path.join(O, "boot_K.json")
if os.path.exists(kf):
    k = json.load(open(kf))
    other.append({"id": "bootstrap_K", "description": "Reduced bootstrap size K chosen by the pre-registered rule K = min(10, floor(25/t)), t = first draw minutes",
                  "first_draw_minutes": k["first_draw_minutes"], "K": k["K"], "source_file": "outputs/boot_K.json"})
cd = json.load(open(f"{O}/class_decision.json")) if os.path.exists(f"{O}/class_decision.json") else {}
log = open(f"{A}/LOG.md").read()
res = {"paper_id": "17_T1NXVQ", "agent": "A", "run_date_ist": cd.get("run_date_ist", "2026-10-11"),
       "ran": any(t["reproduced_value"] is not None for t in targets),
       "could_not_run_reason": cd.get("could_not_run_reason", ""),
       "targets": targets, "robustness": robust, "bugs": cd.get("bugs", []), "env_fixes": cd.get("env_fixes", []),
       "proposed_class": cd.get("proposed_class"), "class_reason": cd.get("class_reason", ""),
       "confidence": cd.get("confidence"), "confidence_reason": cd.get("confidence_reason", ""),
       "time_minutes": cd.get("time_minutes"), "uncertainties": cd.get("uncertainties", []),
       "other_checks": other + cd.get("other_checks", [])}
json.dump(res, open(f"{A}/results.json", "w"), indent=1)
for t in targets: print(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"])
for r in robust: print(r["id"], r["ran"], r["estimate"], r["same_direction_and_significance_as_paper"])
