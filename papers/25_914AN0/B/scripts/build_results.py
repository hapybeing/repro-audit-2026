#!/usr/bin/env python3
"""Builds results.json for 25_914AN0 agent B from files in outputs/ (no hand-typed reproduced numbers)."""
import csv, json, math, re, os, datetime
B = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B"
O = os.path.join(B, "outputs")
targets = json.load(open(os.path.join(B, "..", "targets.json")))
ext = {r["id"]: r for r in csv.DictReader(open(os.path.join(O, "targets_extracted.csv")))}
def num(x):
    try: return float(x)
    except: return None
crit = {"T1": "neg", "T2": "pos", "T3": "neg", "T4": "neg", "T6": "neg"}
tout = []
for t in targets:
    r = ext.get(t["id"]); v = num(r["value"]) if r else None
    pv = t["paper_value"]; d = t["paper_rounding_decimals"]
    ad = None if v is None else abs(v - pv); rd = None if v is None else (v - pv) / abs(pv)
    mr = None if v is None else (round(v, d) == pv)
    w5 = None if rd is None else abs(rd) <= 0.05
    note = ""
    if t["id"] == "T5":
        sc = None if v is None else abs(v - pv) <= 5
        note = r["quantity"] if r else ""
        src = "outputs/targets_extracted.csv (from outputs/mermods.rds, FE pop weights rows, column n)"
    else:
        l, u = num(r["l"]), num(r["u"])
        sc = (v < 0 and u < 0) if crit[t["id"]] == "neg" else (v > 0 and l > 0)
        note = f"95% CI b +/- 1.96 SE as in the code: ({l:.4f}, {u:.4f}); SE {num(r['se']):.4f}. {r['quantity']}"
        src = "outputs/targets_extracted.csv (from outputs/war_mod_out.rds)" if t["id"] == "T6" else "outputs/targets_extracted.csv (from outputs/mermods.rds)"
    if t["id"] == "T2": note += ". Article prose p. 180 gives 0.52 (second candidate); reproduced value matches the table value 0.629, not the prose value."
    if t["id"] == "T3": note += ". Article prose p. 180 gives -0.34 (second candidate); reproduced value matches the table value -0.287, not the prose value."
    tout.append(dict(id=t["id"], description=t["description"], paper_value=pv, paper_rounding_decimals=d, reproduced_value=v,
                     source_file=src, abs_diff=ad, rel_diff=rd, match_to_rounding=mr, within_5pct=w5, same_conclusion=sc, note=note))

# Robustness
rb = {r["outcome"]: r for r in csv.DictReader(open(os.path.join(O, "rb_rc.csv")))}
sign = {"MIA_100": -1, "KIA_100": 1, "WMED_100": -1, "POW_100": -1}
def q7(xs, p):
    xs = sorted(xs); h = (len(xs) - 1) * p; lo = math.floor(h); return xs[lo] + (h - lo) * (xs[min(lo + 1, len(xs) - 1)] - xs[lo])
boot = list(csv.DictReader(open(os.path.join(O, "ra_boot.csv"))))
ra_summary = []
for col, oc in [("MIA", "MIA_100"), ("KIA", "KIA_100"), ("WMED", "WMED_100"), ("POW", "POW_100")]:
    vals = [num(b[col]) for b in boot if col in b]; ok = [x for x in vals if x is not None and not math.isnan(x)]
    nfail = len(vals) - len(ok); m = sum(ok) / len(ok); se = math.sqrt(sum((x - m) ** 2 for x in ok) / (len(ok) - 1))
    lo, hi = q7(ok, 0.025), q7(ok, 0.975); s = sign[oc]
    other = sum(1 for x in ok if (x > 0 if s < 0 else x < 0)); p = min(1.0, 2 * other / len(ok))
    ra_summary.append(dict(outcome=oc, K_done=len(vals), failed=nfail, orig=num(rb[oc]["b_orig"]), boot_mean=m, boot_se=se, pct_l=lo, pct_u=hi, p=p,
                           same=(hi < 0) if s < 0 else (lo > 0)))
with open(os.path.join(O, "ra_summary.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(ra_summary[0].keys())); w.writeheader(); w.writerows(ra_summary)
ras = {r["outcome"]: r for r in ra_summary}
def fmt(x): return f"{x:.4f}"
others = lambda fn: "; ".join(fn(oc) for oc in ["KIA_100", "WMED_100", "POW_100"])
mia = ras["MIA_100"]
rob = [
 dict(id="R_a", description="Case bootstrap of the FE pop-weights model on the 15142-row estimation sample, set.seed(20261011), K=500 (time rule met), NKVD coefficient for MIA (primary); KIA, Medals, POW from the same resamples",
      ran=True, estimate=mia["orig"], se_or_ci=f"bootstrap SE {fmt(mia['boot_se'])}; percentile 95% CI ({fmt(mia['pct_l'])}, {fmt(mia['pct_u'])}); K={mia['K_done']}, failed refits {mia['failed']}",
      p_value=mia["p"], same_direction_and_significance_as_paper=mia["same"], source_file="outputs/ra_boot.csv; outputs/ra_summary.csv",
      note="Secondary outcomes: " + others(lambda oc: f"{oc} b={fmt(ras[oc]['orig'])}, boot SE {fmt(ras[oc]['boot_se'])}, CI ({fmt(ras[oc]['pct_l'])}, {fmt(ras[oc]['pct_u'])}), p={ras[oc]['p']:.3f}, same={ras[oc]['same']}")),
]
r = rb["MIA_100"]
rob.append(dict(id="R_b", description="Drop rows with |z|>3 on the outcome (unweighted z within the estimation sample), refit FE pop-weights model; MIA primary",
      ran=True, estimate=num(r["rb_b"]), se_or_ci=f"felm SE {fmt(num(r['rb_se']))}; 95% CI ({fmt(num(r['rb_l']))}, {fmt(num(r['rb_u']))}); rows dropped {r['rb_dropped']}, n={r['rb_n']}",
      p_value=num(r["rb_p"]), same_direction_and_significance_as_paper=(num(r["rb_u"]) < 0), source_file="outputs/rb_rc.csv",
      note="Secondary outcomes: " + others(lambda oc: f"{oc} b={fmt(num(rb[oc]['rb_b']))}, CI ({fmt(num(rb[oc]['rb_l']))}, {fmt(num(rb[oc]['rb_u']))}), p={num(rb[oc]['rb_p']):.4f}, dropped {rb[oc]['rb_dropped']}, same={(num(rb[oc]['rb_u'])<0) if sign[oc]<0 else (num(rb[oc]['rb_l'])>0)}")))
rob.append(dict(id="R_c", description="Same FE pop-weights model with SE clustered by unit (DIV_ARMY), felm cluster part; MIA primary",
      ran=True, estimate=num(r["rc_b"]), se_or_ci=f"clustered SE {fmt(num(r['rc_se']))}; 95% CI ({fmt(num(r['rc_l']))}, {fmt(num(r['rc_u']))}); clusters {r['rc_nclust']}",
      p_value=num(r["rc_p"]), same_direction_and_significance_as_paper=(num(r["rc_u"]) < 0), source_file="outputs/rb_rc.csv",
      note="Secondary outcomes: " + others(lambda oc: f"{oc} clustered SE {fmt(num(rb[oc]['rc_se']))}, CI ({fmt(num(rb[oc]['rc_l']))}, {fmt(num(rb[oc]['rc_u']))}), p={num(rb[oc]['rc_p']):.4f}, same={(num(rb[oc]['rc_u'])<0) if sign[oc]<0 else (num(rb[oc]['rc_l'])>0)}")))

# time from LOG.md timestamps
log = open(os.path.join(B, "LOG.md")).read()
ts = re.findall(r"^- (\d{2}):(\d{2})", log, re.M); mins = [int(h) * 60 + int(m) for h, m in ts]
tm = max(mins) - min(mins) if mins else None

all_match = all(t["match_to_rounding"] for t in tout)
all5 = all(t["within_5pct"] and t["same_conclusion"] for t in tout)
cls = "A" if all_match else ("B" if all5 else "C")
res = dict(paper_id="25_914AN0", agent="B", run_date_ist=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
  ran=True, could_not_run_reason="", targets=tout, robustness=rob,
  bugs=[],
  code_observations=[
   "Verified by run, not a bug in the deposited one-session pipeline: functions.R ensemble_modz (lines 240, 256, 274, 290) assigns the weights column by reference inside the data= argument and passes weights=X_s$weights. When X_s is a data.table without column over-allocation (e.g. loaded with readRDS), the 'RE pop weights' lmer fit silently uses the stale weights column (1) and equals the unweighted fit. In my first staged run this changed Table A2.4 and the Hausman p row of Table A2.3 but not the FE targets. With setalloccol(X_s), which restores the state line 58 produces in one session, Tables A2.3 and A2.4 match the deposited .tex exactly (outputs/diff_tabA2_*.txt, outputs/s1b_run1_noalloc/, scripts/diag_alloc_test.R).",
   "Unverified observation: functions.R line 102 (tlagz) refers to X_ instead of its argument data; tlagz is defined but never called in run2_main.R, so no output depends on it.",
   "Code read: run2_main.R lines 43-157 and 1310-1408, functions.R lines 1-95 and 228-336 (preprocez, phtest_felm, ensemble_modz, betamat). No real bug found in the target blocks."],
  env_fixes=["diffs/functions_R_mc_cores.diff: mc.cores=0.5 on 2 CPUs is rejected by mclapply; wrapped in max(1, ...) as PREREG allows",
             "Staged run of the pre-registered blocks (S1a, S1b, S4) via scripts/s1a_prep.R, s1b_models.R, s4_war.R that evaluate the authors' line ranges verbatim; s1b adds data.table::setalloccol(X_s) after loading the saved X_s (see LOG.md 07:58-08:02)",
             "Package fallbacks: lfe 3.0-0 failed to compile under R 4.5 (Calloc removed), used lfe 3.1.1; data.table 1.15.4 failed (Calloc), used Debian 1.17.0; V8 (SUNGEO dependency chain) built with DOWNLOAD_STATIC_LIBV8=1 after apt r-cran-v8 failed. Pinned fixest 0.12.0, lme4 1.1-35.3, SUNGEO 1.3.0, robustlmm 3.3-1, Matching 4.10-14, optimx 2023-10.21, dplyr 1.1.4 installed/used."],
  proposed_class=cls,
  class_reason="All six targets (T1-T6) reproduced to the printed rounding by the authors' code; regenerated Tables A2.3, A2.4, A1.2, A6.16 and A6.17 equal the authors' deposited .tex files apart from the header lines." if cls == "A" else "See targets.",
  confidence="high", confidence_reason="Exact matches by script with pinned fixest/lme4; lfe and data.table were fallback versions but outputs equal the deposited tables; A/B agreement not yet known to me.",
  time_minutes=tm,
  uncertainties=[
   "Article prose p. 180 gives KIA 0.52 and Medals -0.34; the code and appendix Table A2.3 give 0.629 and -0.287 (reproduced). Not a target mismatch under batch5 decision 4, reported only.",
   "My first staged S1b run produced different RE (non-target) results because readRDS drops data.table over-allocation; fixed in my stage script with setalloccol. The PREREG statement that both routes give the same objects does not hold without that step for the RE models.",
   "Target cells checked against the author-hosted appendix PDF (sha256 c9ad51f6..., same as PREREG); excerpts in outputs/appendix_tabA2_3_excerpt.txt and outputs/appendix_tabA6_17_excerpt.txt. All six printed values agree with targets.json.",
   "Only the pre-registered target blocks were run; placebo simulations, matching, sequential-g and other appendix analyses were not run.",
   "A short concurrent R process (environment listing) ran briefly while the bootstrap was running."])
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["proposed_class", "time_minutes"]}), [(t["id"], t["paper_value"], t["reproduced_value"], t["match_to_rounding"]) for t in tout])
