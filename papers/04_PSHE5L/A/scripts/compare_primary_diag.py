"""Side-by-side table: primary run (as deposited, Q15 code 8 kept) vs DIAGNOSTIC run (authors' line 188 re-enabled).
Reads outputs/*.csv written by run_and_extract.R. Paper context values (fit, n) are copied from PREREG.md section 1/2."""
import csv, json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
def rd(p): return list(csv.DictReader(open(os.path.join(OUT, p))))
def fit(p): return {r["measure"]: float(r["value"]) for r in rd(p)}
def std(p):
    d = {}
    for r in rd(p):
        key = (r["lhs"], r["op"], r["rhs"] if r["op"] != ":=" else "")
        d[key] = (float(r["est.std"]), float(r["pvalue"]) if r["pvalue"] not in ("", "NA") else None)
    return d
def pe(p):
    d = {}
    for r in rd(p):
        key = (r["lhs"], r["op"], r["rhs"] if r["op"] != ":=" else "")
        d[key] = float(r["pvalue"]) if r["pvalue"] not in ("", "NA") else None
    return d
keys = {"T1": ("violence", "~", "polgriev"), "T2": ("violence", "~", "econgriev"), "T3": ("polgriev", "~", "econgriev"),
        "T4": ("indirect1_econgriev", ":=", ""), "T5": ("total_effect_econgriev", ":=", "")}
paper = {"T1": (-0.202, 0.006), "T2": (0.354, 0.005), "T3": (0.718, 0.000), "T4": (-0.145, 0.028), "T5": (0.208, 0.020)}
paper_fit = {"chisq.scaled": 516.954, "df.scaled": 141, "cfi.robust": 0.911, "tli.robust": 0.892, "srmr": 0.058, "rmsea.robust": 0.062, "nobs": 1139}
paper_ctrl = {"chisq.scaled": 779.793, "df.scaled": 201, "nobs": 998}
rows = []
runs = {"primary": "structural", "diagnostic_q15_8_as_NA": "diag_q15na"}
S = {k: std(v + "_stdsol.csv") for k, v in runs.items()}
P = {k: pe(v + "_pe.csv") for k, v in runs.items()}
F = {k: fit(v + "_fit.csv") for k, v in runs.items()}
C = {k: fit(v + "_ctrl_fit.csv") for k, v in runs.items()}
for t, k in keys.items():
    r = {"item": t, "paper": paper[t][0], "paper_p": paper[t][1]}
    for run in runs:
        r[run] = round(S[run][k][0], 6); r[run + "_rounded3"] = round(S[run][k][0], 3)
        r[run + "_p_std"] = S[run][k][1]; r[run + "_p_unstd_summary"] = P[run][k]
    rows.append(r)
for m, v in paper_fit.items():
    r = {"item": "structural_fit:" + m, "paper": v, "paper_p": None}
    for run in runs: r[run] = round(F[run][m], 6); r[run + "_rounded3"] = round(F[run][m], 3)
    rows.append(r)
for m, v in paper_ctrl.items():
    r = {"item": "controls_model_fit:" + m, "paper": v, "paper_p": None}
    for run in runs: r[run] = round(C[run][m], 6); r[run + "_rounded3"] = round(C[run][m], 3)
    rows.append(r)
cols = sorted({c for r in rows for c in r}, key=lambda c: (c != "item", c != "paper", c != "paper_p", c))
with open(os.path.join(OUT, "primary_vs_diagnostic.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows]
json.dump(rows, open(os.path.join(OUT, "primary_vs_diagnostic.json"), "w"), indent=1)
for r in rows: print(r["item"], r["paper"], r["primary_rounded3"], r["diagnostic_q15_8_as_NA_rounded3"])
