#!/usr/bin/env python3
"""Build results.json for 25_914AN0 agent A. Every reproduced number is read from files in outputs/."""
import csv, json, re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

P = Path("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A")
REPO = P.parents[2]
targets = json.load(open(REPO / "papers/25_914AN0/targets.json"))
tx = {r["id"]: r for r in csv.DictReader(open(P / "outputs/targets_extracted.csv"))}

def fnum(s):
    try: return float(s)
    except (TypeError, ValueError): return None

def rnd(x, d):
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))

out_t = []
for t in targets:
    r = tx.get(t["id"], {})
    v, l, u = fnum(r.get("value")), fnum(r.get("l")), fnum(r.get("u"))
    pv, d = t["paper_value"], t["paper_rounding_decimals"]
    rec = {"id": t["id"], "description": t["description"], "paper_value": pv, "paper_rounding_decimals": d,
           "reproduced_value": v, "source_file": "outputs/targets_extracted.csv (from outputs/mermods.rds; T6 from outputs/war_mod_out.rds)",
           "abs_diff": None, "rel_diff": None, "match_to_rounding": None, "within_5pct": None, "same_conclusion": None, "note": r.get("src", "")}
    if v is not None:
        rec["abs_diff"] = abs(v - pv); rec["rel_diff"] = (v - pv) / abs(pv)
        rec["match_to_rounding"] = rnd(v, d) == pv
        rec["within_5pct"] = abs(rec["rel_diff"]) <= 0.05
        if t["id"] == "T5":
            rec["same_conclusion"] = abs(v - pv) <= 5
            rec["note"] += "; N identical across all 7 FE pop-weights outcomes" if l == u == v else "; N differs across outcomes"
        else:
            sign_ok = (v > 0) if t["id"] == "T2" else (v < 0)
            rec["same_conclusion"] = bool(sign_ok and (l > 0 or u < 0))
            rec["note"] += f"; 95% CI (b +/- 1.96 SE) = [{l:.4f}, {u:.4f}]"
    out_t.append(rec)

bc = list(csv.DictReader(open(P / "outputs/robust_bc.csv")))
ra = {r["outcome"]: r for r in csv.DictReader(open(P / "outputs/ra_summary.csv"))}
def bcrow(check, oc): return next(r for r in bc if r["check"] == check and r["outcome"] == oc)
def tf(s): return {"TRUE": True, "FALSE": False}.get(s)

rob, rob2 = [], []
for oc in ["MIA", "KIA", "Medals", "POW"]:
    a = ra[oc]
    ea = {"id": "R_a" if oc == "MIA" else f"R_a_{oc}", "outcome": oc,
          "description": "Case bootstrap of the FE pop-weights model, set.seed(20261011), K resamples of rows of the estimation sample",
          "ran": True, "estimate": fnum(a["estimate"]),
          "se_or_ci": f"bootstrap SE {float(a['boot_se']):.4f}; percentile 95% CI [{float(a['ci_l']):.4f}, {float(a['ci_u']):.4f}]; K={a['K']}, ok={a['n_ok']}, failed={a['n_failed']}",
          "p_value": fnum(a["p"]), "same_direction_and_significance_as_paper": tf(a["same_dir_sig"]),
          "source_file": "outputs/ra_summary.csv (from outputs/ra_boot.csv)", "note": "p = min(1, 2 x share of draws on the other side of 0)"}
    b = bcrow("R_b", oc)
    eb = {"id": "R_b" if oc == "MIA" else f"R_b_{oc}", "outcome": oc,
          "description": "Drop rows with |z| > 3 on the outcome (unweighted z within the estimation sample), refit same model",
          "ran": True, "estimate": fnum(b["b"]),
          "se_or_ci": f"felm SE {float(b['se']):.4f}; 95% CI [{float(b['l']):.4f}, {float(b['u']):.4f}]; rows dropped {b['dropped']} of {int(b['n'])+int(b['dropped'])}",
          "p_value": fnum(b["p"]), "same_direction_and_significance_as_paper": tf(b["same_dir_sig"]),
          "source_file": "outputs/robust_bc.csv", "note": "no rows with |z|>3 for KIA (outputs/rb_zmax.csv), so identical to baseline" if b["dropped"] == "0" else ""}
    c = bcrow("R_c", oc)
    ec = {"id": "R_c" if oc == "MIA" else f"R_c_{oc}", "outcome": oc,
          "description": "Same model with SE clustered by unit (DIV_ARMY) in lfe::felm; point estimate unchanged by construction",
          "ran": True, "estimate": fnum(c["b"]),
          "se_or_ci": f"clustered SE {float(c['se']):.4f}; 95% CI [{float(c['l']):.4f}, {float(c['u']):.4f}]; clusters {c['clusters']}",
          "p_value": fnum(c["p"]), "same_direction_and_significance_as_paper": tf(c["same_dir_sig"]),
          "source_file": "outputs/robust_bc.csv", "note": ""}
    (rob if oc == "MIA" else rob2).extend([ea, eb, ec])

# time from LOG.md timestamps
stamps = re.findall(r"^- 2026-10-11 (\d\d):(\d\d)", open(P / "LOG.md").read(), flags=re.M)
mins = [int(h) * 60 + int(m) for h, m in stamps]
time_minutes = max(mins) - min(mins) if mins else None

all_match = all(t["match_to_rounding"] for t in out_t)
res = {
 "paper_id": "25_914AN0", "agent": "A", "run_date_ist": "2026-10-11",
 "ran": True, "could_not_run_reason": "",
 "targets": out_t,
 "robustness": rob + rob2,
 "bugs": [],
 "code_observations": [
   "None found as bugs. Read all code the target blocks execute: functions.R lines 1-116 and 228-336, run2_main.R lines 1-160 and 1300-1410.",
   "functions.R lines 256 and 290 assign column 'Y' but model_fe uses 'y'; 'y' already holds the same outcome from the preceding lmer call (lines 240, 274). Verified by run: my refit with y set explicitly gives the same MIA coefficient as mermods (outputs/robust_bc.csv baseline vs outputs/mermods_fe_pop.csv). No effect on results.",
   "Unverified observation: tlagz (functions.R line 102) refers to X_ instead of its argument data; tlagz is not called anywhere in run2_main.R."
 ],
 "env_fixes": [
   "diffs/functions.R.diff: mc.cores = max(1, ...) at functions.R line 306 (0.5 on 2 CPUs is rejected by mclapply); pre-registered",
   "Staged run of the target blocks only (S1a, S1b, S4) via scripts/s1a_prep.R, s1b_models.R, s4_war.R that eval the authors' lines verbatim; pre-registered (diffs/README.md)",
   "lfe 3.1.1 instead of pinned 3.0-0 (3.0-0 fails to compile under R 4.5: removed Calloc/Free API); PREREG fallback",
   "data.table 1.18.6.1 instead of pinned 1.15.4 (1.15.4 fails to compile under R 4.5: removed Realloc API); PREREG fallback (current CRAN)",
   "V8 installed from CRAN with DOWNLOAD_STATIC_LIBV8=1 so that the pinned SUNGEO 1.3.0 could install (its dependency rmapshaper needs V8; Debian r-cran-v8 not installable)",
   "Pins installed as stated: fixest 0.12.0, lme4 1.1-35.3, SUNGEO 1.3.0, robustlmm 3.3-1, Matching 4.10-14, optimx 2023-10.21, dplyr 1.1.4 (Debian binary). R 4.5.0 (authors 4.4.1); Matrix 1.7-3 (authors 1.6-5)"
 ],
 "proposed_class": "A" if all_match else "see targets",
 "class_reason": ("All six targets (T1-T6) reproduce to the paper's printed rounding from the authors' unchanged code, with environment fixes only; the regenerated Tables A2.3 (estimate rows) and A6.17 are identical to the authors' deposited output." if all_match else "Not all targets matched to rounding; see targets."),
 "confidence": "medium",
 "confidence_reason": "Script-matched targets with pinned fixest and lme4, but two pins needed fallbacks (lfe, data.table) and the random-effects models (Table A2.4, Hausman p) differ from the authors' output; agent B comparison pending.",
 "time_minutes": time_minutes,
 "uncertainties": [
   "Article prose p. 180 gives KIA +0.52 and Medals -0.34; targets use the appendix Table A2.3 values (0.629, -0.287), which this run reproduces. The prose values are not reproduced by the deposited code (reported, not class-relevant per batch5_class_decisions.md item 4).",
   "Random-effects (lme4) estimates differ from the authors' Table A2.4 for all 7 outcomes (outputs/texdiff_tabA2_4.txt; e.g. Medals RE -0.361 authors vs 0.412 here), and so do two Hausman p cells in Table A2.3 (outputs/texdiff_tabA2_3.txt). Not targets. Likely environment drift (lme4 pinned 1.1-35.3, but R 4.5 / Matrix 1.7-3 vs authors' R 4.4.1 / Matrix 1.6-5, Nelder_Mead optimizer); not verified.",
   "Figure 1 png was not regenerated: my staged eval(parse()) does not auto-print the ggplot object. Not a target.",
   "During setup the authors' results/ files were briefly extracted into RUNDIR/Replication_IO/results/ by my mistake; they were removed (verified byte-identical first) before S1b ran. S1a reads nothing from results/. The regenerated .tex files compared here all carry run-date mtimes.",
   "Three errors in my own robustness scripts were found and fixed before final outputs (logged in LOG.md): IID SE reported for R_c on the first pass, a stale CSV after a parse error, and the R_a sample lacking non-MIA outcome columns (failed file kept as outputs/ra_boot_failed_run1.csv). The R_a timing projection was redone after the fix.",
   "Robustness, MIA (primary) keeps sign and significance in R_a, R_b and R_c. Secondary outcomes: R_a percentile CIs include 0 for KIA and Medals; R_b makes Medals not significant at 5%; R_c (unit-clustered SE) makes KIA, Medals and POW not significant at 5%. Robustness does not change the class."
 ]
}
json.dump(res, open(P / "results.json", "w"), indent=1)
print(json.dumps({t["id"]: [t["paper_value"], t["reproduced_value"], t["match_to_rounding"], t["same_conclusion"]] for t in out_t}, indent=0))
print("class", res["proposed_class"], "time", time_minutes)
