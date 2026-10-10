"""Target table for batch 1: one row per pre-registered target per paper (papers 01-05).
Writes batches/batch1_targets.csv and batches/batch1_targets.md. Every value is read from files:
  paper value, description, location      papers/<pid>/targets.json (frozen; sha256 in batches/batch1_prereg_hashes.txt)
  A value, B value                        papers/<pid>/{A,B}/results.json  (reproduced_value of the run of record)
  01_5BIH0P has no paper target (targets.json is []); its pre-registered internal checks (PREREG.md section 1,
  deposited author output values, NOT paper numbers) are listed in a separate block, with the deposited value parsed
  from PREREG.md and A/B values from results.json (B ids mapped with batches/id_aliases.json).
Match status: value rounded to the paper's reported decimals equals the paper value.
Usage: python3 scripts/make_target_table.py [batch]   (default batch 1; batch 1 output is unchanged by the batch argument)
Batch 2 (papers 06-10): same paper-target table, plus blocks read from files for the alternative readings named in
batches/batch2_class_rules.json (06 coefficient p, 07 current-CRAN fixest run, 10 figure-claim checks FC1 to FC3).
Batch 3 (papers 11-15): same paper-target table plus an A/B agreement column (A and B equal at the paper's reported
rounding, and whether they are equal at full precision), and the 11_DDOFPS v2 programs-file block read from A's
results.json (alternative_v2) and B's results.json (same_conclusion_v2). Batch 1 and 2 outputs are unchanged.
Batch 4 (papers 16-20): same paper-target table and A/B agreement column as batch 3, plus two blocks read from files:
17_T1NXVQ reduced bootstrap (A: papers/17_T1NXVQ/A/outputs/boot_summary.csv and boot_vs_deposited.csv; B:
papers/17_T1NXVQ/B/outputs/summary_bootstrap_authorseeds.csv and compare_boot_vs_deposited.csv), and the 18_YXC5K5
docid-paired rerun R_c (papers/18_YXC5K5/{A,B}/outputs/R_c_targets_extracted.csv). Batch 1 to 3 outputs are unchanged.
"""
import csv, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = int(sys.argv[1]) if len(sys.argv) > 1 else 1
PIDS = {1: ["01_5BIH0P", "02_ELBOXX", "03_3IOGQ8", "04_PSHE5L", "05_FNTC1J"],
        2: ["06_VSV5DM", "07_JH9DBC", "08_SQRZR8", "09_4U8CTG", "10_6MLKJZ"],
        3: ["11_DDOFPS", "12_CYBR7L", "13_DX5T9G", "14_CJISMY", "15_1BBC4E"],
        4: ["16_QZNVZ0", "17_T1NXVQ", "18_YXC5K5", "19_KH0SQ2", "20_SINIYU"]}[BATCH]


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

if BATCH == 1:
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
if BATCH in (3, 4):
    for r in rows:
        a, b, d = r["A_value"], r["B_value"], r["decimals"]
        if a == "" or b == "": r["AB_agree"] = "not both computed"
        elif float(a) == float(b): r["AB_agree"] = "yes (identical at full precision)"
        elif round(float(a), d) == round(float(b), d): r["AB_agree"] = "yes (at reported rounding)"
        else: r["AB_agree"] = "no"
    F = F + ["AB_agree"]
for r in rows:
    for k in F:
        if isinstance(r[k], str) and "\u2014" in r[k]: r[k] = r[k].replace("\u2014", ",")
with open(f"{REPO}/batches/batch{BATCH}_targets.csv", "w", newline="") as f:
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


if BATCH == 4:
    agc = Counter(r["AB_agree"] for r in pt)
    md = ["# Batch 4 target table (papers 16_QZNVZ0 to 20_SINIYU)", "",
          "Generated by `scripts/make_target_table.py 4`. Paper values, descriptions and locations come from each paper's frozen "
          "`targets.json` (sha256 in `batches/batch4_prereg_hashes.txt`); A and B values are the `reproduced_value` of each agent's "
          "run of record in `results.json`. Match = the value rounded to the paper's reported decimals equals the paper value. "
          "A/B = whether the two blind runs give the same value. Full-precision values and source files are in `batches/batch4_targets.csv`.", "",
          "## Counts (paper targets)"]
    for k, v in sorted(cnt.items()):
        md.append(f"- {k}: {v}")
    for k, v in sorted(agc.items()):
        md.append(f"- A/B agreement {k}: {v}")
    md += [f"- paper targets listed: {len(pt)} across {len(set(r['paper'] for r in pt))} papers", "",
           "## Paper targets", "",
           "| Paper | Target | Description | Location in paper | Paper | A | B | Match | A/B agree |", "|---|---|---|---|---|---|---|---|---|"]
    for r in pt:
        md.append(f"| {r['paper']} | {r['target_id']} | {esc(r['description'])} | {esc(r['location'])} | {short(r['paper_value'])} | "
                  f"{short(r['A_value'])} | {short(r['B_value'])} | {r['match_status']} | {r['AB_agree']} |")
    # 17: pre-registered reduced bootstrap with the authors' seeds (pre-run decision #3)
    d17 = f"{REPO}/papers/17_T1NXVQ"
    aS = {(r["model"], r["term"]): r for r in csv.DictReader(open(f"{d17}/A/outputs/boot_summary.csv")) if r["seed_set"] == "authorseeds"}
    bS = {(r["model"], r["term"]): r for r in csv.DictReader(open(f"{d17}/B/outputs/summary_bootstrap_authorseeds.csv"))}
    tj17 = {t["id"]: t for t in json.load(open(f"{d17}/targets.json"))}
    spec17 = [("T1", "pool_xsec", "cuteth"), ("T2", "pool_ldv", "cuteth_lag"), ("T3", "pool_ldv", "cshp_lag"), ("T4", "pool_ldv", "abram_sum")]
    aK = json.load(open(f"{d17}/A/outputs/boot_K.json"))["K"]; bK = json.load(open(f"{d17}/B/outputs/bootstrap_K.json"))["K"]
    md += ["", "## 17_T1NXVQ reduced bootstrap with the authors' seeds (pre-run decision #3; significance only, the printed 120-draw intervals are not compared)", "",
           f"Read from `papers/17_T1NXVQ/A/outputs/boot_summary.csv` (K = {aK}, seeds 1 to {aK}) and `papers/17_T1NXVQ/B/outputs/summary_bootstrap_authorseeds.csv` (K = {bK}, seeds 1 to {bK}). "
           "Interval = estimate plus or minus 1.96 times the SD of the K draws (pre-registered rule); significant = the interval excludes 0.", "",
           "| Target | Paper | A interval | A excludes 0 | B interval | B excludes 0 |", "|---|---|---|---|---|---|"]
    for tid, mod, term in spec17:
        a_ = aS[(mod, term)]; b_ = bS[(mod, term)]
        alo, ahi, blo, bhi = (float(a_["ci_lo_1.96sd"]), float(a_["ci_hi_1.96sd"]), float(b_["lo_1.96sd"]), float(b_["hi_1.96sd"]))
        md.append(f"| {tid} | {tj17[tid]['paper_value']} | [{alo:.4f}, {ahi:.4f}] | {alo > 0 or ahi < 0} | [{blo:.4f}, {bhi:.4f}] | {blo > 0 or bhi < 0} |")
    ca = list(csv.DictReader(open(f"{d17}/A/outputs/boot_vs_deposited.csv")))
    cb = list(csv.DictReader(open(f"{d17}/B/outputs/compare_boot_vs_deposited.csv")))
    ma = max(abs(float(r["abs_diff"])) for r in ca); mb = max(abs(float(r["abs_diff"])) for r in cb)
    md += ["", f"Reproduced draws against the same-seed rows of the deposited bootstrap file: A {len(ca)} coefficients compared, largest absolute difference {ma:.2e} "
           f"(`papers/17_T1NXVQ/A/outputs/boot_vs_deposited.csv`); B {len(cb)} compared, largest absolute difference {mb:.2e} (`papers/17_T1NXVQ/B/outputs/compare_boot_vs_deposited.csv`)."]
    # 18: docid-paired rerun R_c (robustness, never sets the class; pre-run decision #4)
    d18 = f"{REPO}/papers/18_YXC5K5"
    ra = {}
    for r in csv.reader(open(f"{d18}/A/outputs/R_c_targets_extracted.csv")):
        ra[(r[0] + "|" + r[1]) if r[0] not in ("n",) else r[1]] = r[2]
    rb = {r[0]: r[1] for r in csv.reader(open(f"{d18}/B/outputs/R_c_targets_extracted.csv"))}
    keys18 = {"T1": "metrics_matrix|GPT 4o 8 Few Shot|HammingLoss", "T2": "undergrads8|Hamming Loss", "T3": "metrics_matrix|GPT 4o 4 Few Shot|HammingLoss",
              "T4": "metrics_matrix|GPT 4o 8 Few Shot|F1", "T5": "metrics_matrix|GPT 4o 8 Few Shot|Mean", "T6": "nrow_pi10mat"}
    tj18 = {t["id"]: t for t in json.load(open(f"{d18}/targets.json"))}
    md += ["", "## 18_YXC5K5 docid-paired rerun R_c (robustness check; the class uses the Rmd as deposited, pre-run decision #4)", "",
           "Read from `papers/18_YXC5K5/A/outputs/R_c_targets_extracted.csv` and `papers/18_YXC5K5/B/outputs/R_c_targets_extracted.csv`: the same extraction on a copy of the Rmd with one added line, `pi = pi %>% arrange(docid)` after line 108.", "",
           "| Target | Paper | A as deposited | A (R_c) | B (R_c) | R_c matches paper at its rounding |", "|---|---|---|---|---|---|"]
    a18 = {t["id"]: t for t in json.load(open(f"{d18}/A/results.json"))["targets"]}
    for tid, k in keys18.items():
        va, vb = float(ra[k]), float(rb[k]); p_ = tj18[tid]["paper_value"]; d_ = tj18[tid]["paper_rounding_decimals"]
        md.append(f"| {tid} | {p_} | {short(a18[tid]['reproduced_value'])} | {short(va)} | {short(vb)} | {'yes, both runs' if rmatch(va, p_, d_) and rmatch(vb, p_, d_) else ('no, both runs' if not rmatch(va, p_, d_) and not rmatch(vb, p_, d_) else 'runs differ')} |")
    md += ["", "20_SINIYU T1 to T6 were not computed: O_B_Ku.py stops at its import of the undeposited module interp_radar, and no deposited code computes Table 1 (papers/20_SINIYU/DATA_STATEMENT.md; pre-run decision #5).", ""]
    text = "\n".join(md)
    assert "\u2014" not in text
    open(f"{REPO}/batches/batch4_targets.md", "w").write(text)
    print(dict(cnt), dict(agc))
    sys.exit(0)

if BATCH == 3:
    agc = Counter(r["AB_agree"] for r in pt)
    md = ["# Batch 3 target table (papers 11_DDOFPS to 15_1BBC4E)", "",
          "Generated by `scripts/make_target_table.py 3`. Paper values, descriptions and locations come from each paper's frozen "
          "`targets.json` (sha256 in `batches/batch3_prereg_hashes.txt`); A and B values are the `reproduced_value` of each agent's "
          "run of record in `results.json`. Match = the value rounded to the paper's reported decimals equals the paper value. "
          "A/B = whether the two blind runs give the same value. Full-precision values and source files are in `batches/batch3_targets.csv`.", "",
          "## Counts (paper targets)"]
    for k, v in sorted(cnt.items()):
        md.append(f"- {k}: {v}")
    for k, v in sorted(agc.items()):
        md.append(f"- A/B agreement {k}: {v}")
    md += [f"- paper targets listed: {len(pt)} across {len(set(r['paper'] for r in pt))} papers", "",
           "## Paper targets", "",
           "| Paper | Target | Description | Location in paper | Paper | A | B | Match | A/B agree |", "|---|---|---|---|---|---|---|---|---|"]
    for r in pt:
        md.append(f"| {r['paper']} | {r['target_id']} | {esc(r['description'])} | {esc(r['location'])} | {short(r['paper_value'])} | "
                  f"{short(r['A_value'])} | {short(r['B_value'])} | {r['match_status']} | {r['AB_agree']} |")
    A11 = json.load(open(f"{REPO}/papers/11_DDOFPS/A/results.json"))
    B11 = json.load(open(f"{REPO}/papers/11_DDOFPS/B/results.json"))
    tj11 = {t["id"]: t for t in json.load(open(f"{REPO}/papers/11_DDOFPS/targets.json"))}
    md += ["", "## 11_DDOFPS with the v2 programs file (pre-run decision #1; alternative reading in batches/batch3_class_rules.json)", "",
           "Read from `papers/11_DDOFPS/A/results.json` (`alternative_v2`) and `papers/11_DDOFPS/B/results.json` (`same_conclusion_v2`).", "",
           "| Target | Paper | A (v2) | Match at paper rounding (A) | B same conclusion (v2) |", "|---|---|---|---|---|"]
    for t in A11["alternative_v2"]["targets"]:
        p_ = tj11[t["id"]]["paper_value"]; d_ = tj11[t["id"]]["paper_rounding_decimals"]
        md.append(f"| {t['id']} | {p_} | {short(t['reproduced_value'])} | {rmatch(t['reproduced_value'], p_, d_)} | {B11['same_conclusion_v2'].get(t['id'])} |")
    md.append("")
    text = "\n".join(md)
    assert "\u2014" not in text
    open(f"{REPO}/batches/batch3_targets.md", "w").write(text)
    print(dict(cnt), dict(agc))
    sys.exit(0)

if BATCH == 2:
    def rcsv(path):
        return list(csv.DictReader(open(f"{REPO}/{path}")))

    md = ["# Batch 2 target table (papers 06_VSV5DM to 10_6MLKJZ)", "",
          "Generated by `scripts/make_target_table.py 2`. Paper values, descriptions and locations come from each paper's frozen "
          "`targets.json` (sha256 in `batches/batch2_prereg_hashes.txt`); A and B values are the `reproduced_value` of each agent's "
          "run of record in `results.json`. Match = the value rounded to the paper's reported decimals equals the paper value. "
          "Full-precision values and source files are in `batches/batch2_targets.csv`.", "",
          "## Counts (paper targets)"]
    for k, v in sorted(cnt.items()):
        md.append(f"- {k}: {v}")
    md += [f"- paper targets listed: {len(pt)} across {len(set(r['paper'] for r in pt))} papers", "",
           "## Paper targets", "",
           "| Paper | Target | Description | Location in paper | Paper | A | B | Match |", "|---|---|---|---|---|---|---|---|"]
    for r in pt:
        md.append(f"| {r['paper']} | {r['target_id']} | {esc(r['description'])} | {esc(r['location'])} | {short(r['paper_value'])} | "
                  f"{short(r['A_value'])} | {short(r['B_value'])} | {r['match_status']} |")
    # 06: T4 under the alternative reading (coefficient p instead of the pre-registered AME p)
    pv06 = {t["id"]: t for t in json.load(open(f"{REPO}/papers/06_VSV5DM/targets.json"))}["T4"]
    a06 = {(r["quantity"], r["term"]): r for r in rcsv("papers/06_VSV5DM/A/outputs/targets_extracted.csv")}
    b06 = {r["level"]: r for r in rcsv("papers/06_VSV5DM/B/outputs/targets_extracted.csv")}
    aa, ac = float(a06[("AME", "rpgDemocratic White Women")]["p"]), float(a06[("coef", "rpgDemocratic White Women")]["p"])
    ba, bc = float(b06["Democratic White Women"]["AME_p"]), float(b06["Democratic White Women"]["coef_p"])
    md += ["", "## 06_VSV5DM T4 under two readings of the text's 'p = .054'", "",
           "Read from `papers/06_VSV5DM/A/outputs/targets_extracted.csv` and `papers/06_VSV5DM/B/outputs/targets_extracted.csv`. "
           "The pre-registered quantity is the delta-method AME p; the alternative is the quasi-Poisson coefficient p for the same group.", "",
           "| Reading | Paper | A | B | Match at paper rounding |", "|---|---|---|---|---|",
           f"| AME p (pre-registered) | {pv06['paper_value']} | {aa:.6g} | {ba:.6g} | {status(pv06['paper_value'], aa, ba, 3)} |",
           f"| coefficient p (alternative) | {pv06['paper_value']} | {ac:.6g} | {bc:.6g} | {status(pv06['paper_value'], ac, bc, 3)} |"]
    # 07: current CRAN fixest 0.14.2 run (alternative class B)
    tj07 = {t["id"]: t for t in json.load(open(f"{REPO}/papers/07_JH9DBC/targets.json"))}
    a07r = {r["model"]: r for r in rcsv("papers/07_JH9DBC/A/outputs/targets_extracted_fixest0142.csv")}
    b07 = {r["model"]: r for r in rcsv("papers/07_JH9DBC/B/outputs/targets_extracted_fixest_current.csv")}
    spec07 = [("T1", "model1B", "estimate"), ("T2", "model2B", "estimate"), ("T3", "model3B", "estimate"),
              ("T4", "model1B", "nobs"), ("T5", "model2G", "estimate"), ("T6", "model2G", "nobs")]
    md += ["", "## 07_JH9DBC with current CRAN fixest 0.14.2 (the run of record uses fixest 0.12.1; CHANGELOG_METHOD.md #6b)", "",
           "Read from `papers/07_JH9DBC/A/outputs/targets_extracted_fixest0142.csv` and `papers/07_JH9DBC/B/outputs/targets_extracted_fixest_current.csv`.", "",
           "| Target | Paper | A (0.14.2) | B (0.14.2) | Match at paper rounding | Relative difference (A) |", "|---|---|---|---|---|---|"]
    for tid, mod, col in spec07:
        p_ = tj07[tid]["paper_value"]; d_ = tj07[tid]["paper_rounding_decimals"]
        va = float(a07r[mod][col]); vb = float(b07[mod][col])
        md.append(f"| {tid} | {p_} | {short(va)} | {short(vb)} | {status(p_, va, vb, d_)} | {(va - p_) / p_:+.4f} |")
    # 10: figure-claim checks (pre-registered conclusion tests, not numeric targets)
    fa = json.load(open(f"{REPO}/papers/10_6MLKJZ/A/outputs/figure_claims.json"))
    fb = json.load(open(f"{REPO}/papers/10_6MLKJZ/B/outputs/figure_claims.json"))
    md += ["", "## 10_6MLKJZ figure-claim checks FC1 to FC3 (pre-registered in PREREG.md; not numeric targets)", "",
           "Read from `papers/10_6MLKJZ/A/outputs/figure_claims.json` and `papers/10_6MLKJZ/B/outputs/figure_claims.json`.", "",
           "| Check | Paper claim | A | B |", "|---|---|---|---|",
           f"| FC1 | no public-private difference significant (count of FC1 levels with CI excluding 0: 0) | count {fa['FC1']['count_CI_excludes_0']}, holds {fa['FC1']['same_conclusion']} | count {fb['FC1']['count_excluding_0']}, holds {fb['FC1']['same_conclusion']} |",
           f"| FC2 | need-deservingness (Composition) has the largest range in both sectors | holds {fa['FC2']['same_conclusion']} | holds {fb['FC2']['same_conclusion']} |",
           f"| FC3 | Syria below and Germany above 0.5 in both sectors | strict {fa['FC3']['same_conclusion_strict']}, lenient {fa['FC3']['same_conclusion_lenient']} | strict {fb['FC3']['strict_same_conclusion']}, lenient {fb['FC3']['lenient_same_conclusion']} |"]
    md += ["", "09_4U8CTG T5 and T6 (Study 1) were not computed: their inputs sit behind ELIPSS registration (papers/09_4U8CTG/DATA_STATEMENT.md; pre-run decision #2).", ""]
    text = "\n".join(md)
    assert "\u2014" not in text
    open(f"{REPO}/batches/batch2_targets.md", "w").write(text)
    print(dict(cnt))
    sys.exit(0)
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
