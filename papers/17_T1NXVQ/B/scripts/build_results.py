#!/usr/bin/env python3
"""Agent B, 17_T1NXVQ: build results.json and outputs/summary_*.csv from files in outputs/ only."""
import csv, json, math, os, statistics as st, datetime
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); O = os.path.join(P, "outputs")
def rd(f):
    p = os.path.join(O, f)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else None
def est(f, term):
    r = rd(f)
    if not r: return None, None
    for x in r:
        if x["term"] == term: return float(x["estimate"]), x
    return None, r[0]
def boot(f, term):
    r = rd(f)
    if not r: return []
    return [float(x[term]) for x in r if x.get(term) not in (None, "", "NA")]
def sd(v): return st.stdev(v) if len(v) >= 2 else None
def pct(v, q):
    v = sorted(v); n = len(v)
    if n == 0: return None
    h = (n - 1) * q; lo = math.floor(h); hi = math.ceil(h)
    return v[lo] + (v[hi] - v[lo]) * (h - lo)   # R quantile type 7

T = json.load(open(os.path.join(P, "..", "targets.json")))
spec = {"T1": ("pool_xsec", "cuteth", "est"), "T2": ("pool_ldv", "cuteth_lag", "est"), "T3": ("pool_ldv", "cshp_lag", "est"),
        "T4": ("pool_ldv", "abram_sum", "est"), "T5": ("pool_xsec", None, "N"), "T6": ("pool_ldv", None, "N")}
targets = []; bsum = []
for t in T:
    model, term, kind = spec[t["id"]]; f = f"targets_{model}.csv"
    rows = rd(f); val = None; note = ""; sc = None
    if rows:
        if kind == "N": val = int(float(rows[0]["sum_N"]))
        else: val, _ = est(f, term)
    if val is None: note = f"outputs/{f} not produced"
    pv = t["paper_value"]; dec = t["paper_rounding_decimals"]
    ad = None if val is None else val - pv; rel = None if val is None else ad / pv
    m2r = None if val is None else (round(val, dec) == pv if dec > 0 else int(val) == int(pv))
    if val is not None and kind == "N":
        sc = abs(rel) <= 0.01
    elif val is not None:
        b = boot(f"boot_authorseeds_{model}.csv", term); s = sd(b)
        if len(b) >= 3 and s is not None:
            lo, hi = val - 1.96 * s, val + 1.96 * s
            sc = (val > 0) and lo > 0
            note = f"reduced bootstrap, authors' seeds, K={len(b)} draws: SD={s:.4f}, est +/- 1.96 SD = [{lo:.3f}, {hi:.3f}]"
            bsum.append({"model": model, "term": term, "estimate": val, "K": len(b), "boot_mean": st.mean(b), "boot_sd": s,
                         "lo_1.96sd": lo, "hi_1.96sd": hi, "perc2.5": pct(b, .025), "perc97.5": pct(b, .975)})
        else:
            note = f"fewer than 3 bootstrap draws with authors' seeds ({len(b)}); same_conclusion null"
    targets.append({"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": dec,
                    "reproduced_value": val, "source_file": f"outputs/{f}", "abs_diff": ad, "rel_diff": rel,
                    "match_to_rounding": m2r, "within_5pct": None if rel is None else abs(rel) <= 0.05,
                    "same_conclusion": sc, "note": note})

def sdboot(model, term): return sd(boot(f"boot_authorseeds_{model}.csv", term))
rob = []; rsum = []
# R_a
for model, term in (("pool_xsec", "cuteth"), ("pool_ldv", "cuteth_lag")):
    b = boot(f"boot_seeds1001_{model}.csv", term); e, _ = est(f"targets_{model}.csv", term)
    s = sd(b); s0 = sdboot(model, term)
    ran = len(b) >= 2 and e is not None
    r = {"id": "R_a", "description": f"Reduced parametric bootstrap with seeds 1001.. instead of 1..K, {model} {term}", "ran": ran,
         "estimate": e, "se_or_ci": None, "p_value": None, "same_direction_and_significance_as_paper": None,
         "source_file": f"outputs/boot_seeds1001_{model}.csv", "note": ""}
    if ran:
        lo, hi = e - 1.96 * s, e + 1.96 * s
        r["se_or_ci"] = f"SD={s:.4f}; est +/- 1.96 SD [{lo:.3f}, {hi:.3f}]; percentile [{pct(b,.025):.3f}, {pct(b,.975):.3f}] (K={len(b)}, descriptive)"
        r["same_direction_and_significance_as_paper"] = (e > 0) and lo > 0
        ratio = (s / s0) if (s0 and s) else None
        r["note"] = f"draw mean {st.mean(b):.4f}; SD ratio seeds1001/seeds1..K = {ratio if ratio is None else round(ratio,3)}; differs by >1.5x: {None if ratio is None else (ratio > 1.5 or ratio < 1/1.5)}"
        rsum.append({"check": "R_a", "model": model, "term": term, "estimate": e, "K": len(b), "sd": s, "lo": lo, "hi": hi, "sd_ratio_vs_authorseeds": ratio})
    else:
        r["note"] = f"not run or fewer than 2 draws ({len(b)})"
    rob.append(r)
# R_b, R_c
for chk, desc in (("Rb", "Edges with |z|>3 on length.norm or elevmean.norm set to NA, refit"), ("Rc", "Penalty sigma2 = 1000 instead of 10, refit")):
    for model, term in (("pool_xsec", "cuteth"), ("pool_ldv", "cuteth_lag")):
        f = f"targets_{chk}_{model}.csv"; e, row = est(f, term); s0 = sdboot(model, term)
        r = {"id": "R_b" if chk == "Rb" else "R_c", "description": f"{desc}; {model} {term}", "ran": e is not None, "estimate": e,
             "se_or_ci": None, "p_value": None, "same_direction_and_significance_as_paper": None, "source_file": f"outputs/{f}", "note": ""}
        if e is not None:
            se = row.get("stdEr_maxLik")
            extra = ""
            if chk == "Rb":
                fl = rd(f"Rb_flagged_edges_{model}.csv"); mn, _ = est(f"targets_{model}.csv", term)
                mrow = rd(f"targets_{model}.csv")
                if fl: extra += f" lattice edges flagged: length {fl[0]['n_flag_length']}, elev {fl[0]['n_flag_elev']}, union {fl[0]['n_flag_union']} of {fl[0]['n_edges_total']};"
                if mrow: extra += f" summed over periods: edges {int(float(mrow[0]['sum_N_edges']))-int(float(row['sum_N_edges']))} and vertices {int(float(mrow[0]['sum_N']))-int(float(row['sum_N']))} fewer than main fit;"
            if s0:
                lo, hi = e - 1.96 * s0, e + 1.96 * s0
                r["se_or_ci"] = f"maxLik stdEr {float(se):.4f} (descriptive); est +/- 1.96 SD_boot(authors' seeds) [{lo:.3f}, {hi:.3f}]"
                r["same_direction_and_significance_as_paper"] = (e > 0) and lo > 0
            else:
                r["se_or_ci"] = f"maxLik stdEr {float(se):.4f} (descriptive)"; extra += " step-6 bootstrap missing, significance null;"
            r["note"] = extra.strip()
            rsum.append({"check": chk, "model": model, "term": term, "estimate": e, "K": None, "sd": s0, "lo": e - 1.96 * s0 if s0 else None,
                         "hi": e + 1.96 * s0 if s0 else None, "sd_ratio_vs_authorseeds": None})
        else:
            r["note"] = "not run (time budget) or failed; see LOG.md"
        rob.append(r)

def wcsv(name, rows):
    if not rows: return
    with open(os.path.join(O, name), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
wcsv("summary_bootstrap_authorseeds.csv", bsum); wcsv("summary_robustness.csv", rsum)

extra = json.load(open(os.path.join(O, "manual_fields.json")))  # class reasoning, bugs, env fixes, uncertainties, time (text written by agent)
allm = all(t["match_to_rounding"] for t in targets); anyn = any(t["reproduced_value"] is None for t in targets)
res = {"paper_id": "17_T1NXVQ", "agent": "B", "run_date_ist": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
       "ran": not all(t["reproduced_value"] is None for t in targets), "could_not_run_reason": extra.get("could_not_run_reason", ""),
       "targets": targets, "robustness": rob, "bugs": extra["bugs"], "env_fixes": extra["env_fixes"],
       "proposed_class": extra["proposed_class"], "class_reason": extra["class_reason"], "confidence": extra["confidence"],
       "confidence_reason": extra["confidence_reason"], "time_minutes": extra["time_minutes"], "uncertainties": extra["uncertainties"],
       "computed_flags": {"all_targets_match_to_rounding": allm, "any_target_missing": anyn,
                          "all_same_conclusion_true": all(t["same_conclusion"] is True for t in targets)}}
json.dump(res, open(os.path.join(P, "results.json"), "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]] for t in targets}))
print(json.dumps([[r["id"], r["description"][-25:], r["ran"], r["estimate"], r["same_direction_and_significance_as_paper"]] for r in rob]))
