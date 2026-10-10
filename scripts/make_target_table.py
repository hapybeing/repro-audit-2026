"""Target table for batch 1: one row per pre-registered target per paper (papers 01-05).
Writes batches/batch1_targets.csv and batches/batch1_targets.md. Every value is read from files:
  paper value, description, location      papers/<pid>/targets.json (frozen; sha256 in batches/batch1_prereg_hashes.txt)
  A value, B value                        papers/<pid>/{A,B}/results.json  (reproduced_value of the run of record)
  01_5BIH0P has no paper target (targets.json is []); its pre-registered internal checks (PREREG.md section 1,
  deposited author output values, NOT paper numbers) are listed in a separate block, with the deposited value parsed
  from PREREG.md and A/B values from results.json (B ids mapped with batches/id_aliases.json).
Match status: value rounded to the paper's reported decimals equals the paper value.
Usage: python3 scripts/make_target_table.py
"""
import csv, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIDS = ["01_5BIH0P", "02_ELBOXX", "03_3IOGQ8", "04_PSHE5L", "05_FNTC1J"]


def load(p):
    return json.load(open(p)) if os.path.exists(p) else None


def rmatch(v, paper, dec):
    if v is None or paper is None: return None
    return round(float(v), dec) == round(float(paper), dec)


def status(pv, a, b, dec):
    ma, mb = rmatch(a, pv, dec), rmatch(b, pv, dec)
    if a is None and b is None: return "not computed by A or B"
    if ma and mb: return "A and B match paper at reported rounding"
    parts = []
    for ag, v, m in (("A", a, ma), ("B", b, mb)):
        parts.append(f"{ag} not computed" if v is None else (f"{ag} matches" if m else f"{ag} differs from paper"))
    return "; ".join(parts)


def fmt(v):
    if v is None: return ""
    return repr(float(v)) if not float(v).is_integer() else str(int(v)) if abs(v) > 100 else repr(float(v))


rows = []
for pid in PIDS:
    tj = json.load(open(f"{REPO}/papers/{pid}/targets.json"))
    A = load(f"{REPO}/papers/{pid}/A/results.json"); B = load(f"{REPO}/papers/{pid}/B/results.json")
    ta = {t["id"]: t for t in (A or {}).get("targets", [])}
    tb = {t["id"]: t for t in (B or {}).get("targets", [])}
    if not tj:
        rows.append(dict(paper=pid, row_type="paper target", target_id="(none)",
                         description="targets.json is empty: the paper reports no computed number for this dataset (PREREG.md section 1)",
                         location="", paper_value="", decimals="", A_value="", B_value="", A_source="", B_source="",
                         match_status="no paper target"))
        continue
    for t in tj:
        dec = t["paper_rounding_decimals"]
        a = ta.get(t["id"], {}).get("reproduced_value"); b = tb.get(t["id"], {}).get("reproduced_value")
        rows.append(dict(paper=pid, row_type="paper target", target_id=t["id"], description=t["description"],
                         location=t.get("location", ""), paper_value=t["paper_value"], decimals=dec,
                         A_value="" if a is None else a, B_value="" if b is None else b,
                         A_source=ta.get(t["id"], {}).get("source_file") or "", B_source=tb.get(t["id"], {}).get("source_file") or "",
                         match_status=status(t["paper_value"], a, b, dec)))

# 01 internal checks (not paper targets)
pid = "01_5BIH0P"
prereg = open(f"{REPO}/papers/{pid}/PREREG.md", encoding="utf-8").read()
dep = {}
m = re.search(r"- I1: GB .*?Average = (-?[\d.]+)", prereg); dep["I1"] = float(m.group(1))
m = re.search(r"- I2: PB .*?Average = (-?[\d.]+)", prereg); dep["I2"] = float(m.group(1))
m = re.search(r"- I3: GB .VDWAALS = (-?[\d.]+), .EEL = (-?[\d.]+), .EGB = (-?[\d.]+), .ESURF = (-?[\d.]+)", prereg)
dep.update({"I3a": float(m.group(1)), "I3b": float(m.group(2)), "I3c": float(m.group(3)), "I3d": float(m.group(4))})
dep["I1_amber"] = dep["I1"]
alias = json.load(open(f"{REPO}/batches/id_aliases.json"))[pid]
A = load(f"{REPO}/papers/{pid}/A/results.json"); B = load(f"{REPO}/papers/{pid}/B/results.json")
ta = {t["id"]: t for t in A["targets"]}
tb = {c["id"]: c for c in B["internal_checks"]}
for iid, dv in dep.items():
    a = ta.get(iid, {}).get("reproduced_value")
    c = tb.get(alias.get(iid, iid), {})
    b = next((c[k] for k in ("reproduced_value", "recomputed_mean_from_perframe_csv", "recomputed_mean") if k in c), None)
    desc = (c.get("term") or ta.get(iid, {}).get("description") or "")
    rows.append(dict(paper=pid, row_type="internal check (not a paper target)", target_id=f"{iid} (B: {alias.get(iid, iid)})",
                     description=desc, location="FINAL_RESULTS_MMPBSA.dat in the deposit (author output, not in the paper); PREREG.md section 1",
                     paper_value=dv, decimals=2, A_value="" if a is None else a, B_value="" if b is None else b,
                     A_source=ta.get(iid, {}).get("source_file") or "", B_source=c.get("source_file", ""),
                     match_status=status(dv, a, b, 2).replace("paper", "deposited value")))

F = ["paper", "row_type", "target_id", "description", "location", "paper_value", "decimals", "A_value", "B_value",
     "A_source", "B_source", "match_status"]
for r in rows:
    for k in F:
        if isinstance(r[k], str) and "\u2014" in r[k]: r[k] = r[k].replace("\u2014", ",")
with open(f"{REPO}/batches/batch1_targets.csv", "w", newline="") as f:
    w = csv.DictWriter(f, F); w.writeheader(); w.writerows(rows)

from collections import Counter
pt = [r for r in rows if r["row_type"] == "paper target"]
cnt = Counter(r["match_status"] for r in pt)
ic = Counter(r["match_status"] for r in rows if r["row_type"] != "paper target")


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def short(v):
    if v == "" or v is None: return ""
    try:
        x = float(v)
    except Exception:
        return str(v)
    return f"{x:.6g}" if not x.is_integer() else str(int(x))


md = ["# Batch 1 target table (papers 01 to 05)", "",
      "Generated by `scripts/make_target_table.py`. Paper values, descriptions and locations come from each paper's frozen "
      "`targets.json`; A and B values are the `reproduced_value` of each agent's run of record in `results.json`. "
      "Match = the value rounded to the paper's reported decimals equals the paper value. Full-precision values and source "
      "files are in `batches/batch1_targets.csv`.", "",
      "## Counts (paper targets)"]
for k, v in sorted(cnt.items()):
    md.append(f"- {k}: {v}")
md += [f"- paper targets listed: {sum(r['target_id'] != '(none)' for r in pt)} across {len(set(r['paper'] for r in pt if r['target_id'] != '(none)'))} papers with targets", "",
       "## Paper targets", "",
       "| Paper | Target | Description | Location in paper | Paper | A | B | Match |", "|---|---|---|---|---|---|---|---|"]
for r in pt:
    md.append(f"| {r['paper']} | {r['target_id']} | {esc(r['description'])} | {esc(r['location'])} | {short(r['paper_value'])} | "
              f"{short(r['A_value'])} | {short(r['B_value'])} | {r['match_status']} |")
md += ["", "## 01_5BIH0P internal checks (deposited author outputs, not paper numbers; do not count toward the class)", "",
       "| Check | Term | Deposited value | A | B | Match |", "|---|---|---|---|---|---|"]
for r in rows:
    if r["row_type"] != "paper target":
        md.append(f"| {r['target_id']} | {esc(r['description'])} | {short(r['paper_value'])} | {short(r['A_value'])} | {short(r['B_value'])} | {r['match_status']} |")
md += ["", "Internal-check counts: " + "; ".join(f"{k}: {v}" for k, v in sorted(ic.items())), ""]

# 02: the run of record sets the clock to the authors' run date (environment fix). Show the as-is (2026 clock) values too.
pv = {t["id"]: t for t in json.load(open(f"{REPO}/papers/02_ELBOXX/targets.json"))}
a26 = {r["test"]: r for r in csv.DictReader(open(f"{REPO}/papers/02_ELBOXX/A/outputs/targets_pathA_clock2026.csv"))}
b26 = {r["test"]: r for r in csv.DictReader(open(f"{REPO}/papers/02_ELBOXX/B/outputs/pathA_asis/targets_asis.csv"))}
spec = [("T1", "M2_test2_pubdef1", "M2", "r", "r"), ("T2", "M2_test2_pubdef1", "M2", "ci_low", "ci_lo"),
        ("T3", "M2_test2_pubdef1", "M2", "ci_high", "ci_hi"), ("T4", "M1_test1_all", "M1", "r", "r"),
        ("T5", "M1_test1_all", "M1", "ci_low", "ci_lo")]
md += ["## 02_ELBOXX without the clock fix (authors' code run as-is with a 2026 system clock)", "",
       "Read from `papers/02_ELBOXX/A/outputs/targets_pathA_clock2026.csv` and `papers/02_ELBOXX/B/outputs/pathA_asis/targets_asis.csv`.", "",
       "| Target | Paper | A as-is | B as-is | Match at paper rounding | Relative difference (A) |", "|---|---|---|---|---|---|"]
for tid, ta_, tb_, ca, cb in spec:
    p_ = pv[tid]["paper_value"]; d_ = pv[tid]["paper_rounding_decimals"]
    va = float(a26[ta_][ca]); vb = float(b26[tb_][cb])
    st = status(p_, va, vb, d_)
    md.append(f"| {tid} | {p_} | {va:.6g} | {vb:.6g} | {st} | {(va - p_) / p_:+.4f} |")
md.append("")
text = "\n".join(md)
assert "\u2014" not in text
open(f"{REPO}/batches/batch1_targets.md", "w").write(text)
print(dict(cnt), dict(ic))
