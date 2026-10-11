"""Check every number in a batch report and target table against the files they cite.
Usage (from repo/): python3 scripts/check_report_numbers.py 1  > batches/batch1_number_check.txt

Two layers:
 1. Structured checks: tables and count lines are re-derived from the source CSV/JSON and compared cell by cell.
 2. Generic trace: every remaining number token is looked up in the files cited on its line or in its section heading.
    A decimal matches if some number in a cited file rounds to it at the same number of decimals; an integer must occur
    as a number in a cited file. Integers 0 to 31 are flagged "weak" when only the generic trace supports them, because
    small integers occur in most files by chance.
Batch 5 adds structured checks for the extra blocks of batch5_targets.md (21 SI cells, 23 T6 formulas, 24 target cells,
24 R_a bootstrap recomputed from the per-draw files, 25 table versus prose).
Identifiers (DOIs, URLs, file paths, paper and dataset IDs, target IDs like T4, observation IDs like 05-1) are listed
but not traced as measurements. Exit status 1 if any number is unmatched."""
import csv, glob, json, os, re, sys
from collections import Counter

K = sys.argv[1]
REPORT, TARGETS = f"batches/batch{K}_report.md", f"batches/batch{K}_targets.md"
out, n_fail = [], 0


def say(s=""):
    out.append(s)


# ---------------------------------------------------------------- helpers
PATH_RE = re.compile(r"(?:[\w.*-]+/)*[\w.*-]+\.(?:md|json|csv|txt|tsv|py|R|r|rds|diff)\b")
URL_RE = re.compile(r"https?://[^\s)|>`]+")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s)|,;`]+")
ALNUM_RE = re.compile(r"\b(?=\w*[A-Za-z])(?=\w*\d)\w+\b")       # T4, SDO2, 5BIH0P, 2XWT, R_a ...
OBS_RE = re.compile(r"\b0[1-9]-\d+\b|(?<![\d-])(?:1\d|2[0-5])-\d+\b(?!-)")  # observation ids 05-1, 10-1 (not inside dates)
PAPER_RE = re.compile(r"(?<![\w.:-])0[1-9](?![\w.-]|:\d)")               # paper labels 01..05 (leading zero)
CHG_RE = re.compile(r"#\d+[a-z]?\b")                               # CHANGELOG refs #4, #4d
LABEL_RE = re.compile(r"(?i)\b(?:batch(?:es)?|revision|section|rule)\s+\d+(?:\s+(?:to|and)\s+\d+)?\b|\bSHA-?256\b")  # document labels, not measurements
DATE_RE = re.compile(r"\b\d{4}-\d\d-\d\d\b")
TIME_RE = re.compile(r"\b\d\d:\d\d(?::\d\d)?\b")
NUM_RE = re.compile(r"(?<![\w.])-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![\w])|(?<![\w.])-?\.\d+")

_cache = {}


def nums_in(path):
    if path not in _cache:
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except (IsADirectoryError, FileNotFoundError):
            txt = ""
        flat = txt if path.endswith((".csv", ".tsv", ".json")) else re.sub(r"(?<=\d),(?=\d{3}\b)", "", txt)
        toks = re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|(?<![\w.])-?\.\d+|(?<=[\w])\d+(?:\.\d+)?", flat)
        vals = set()
        for t in toks:
            try:
                vals.add(float(t))
            except ValueError:
                pass
        _cache[path] = (txt, vals)
    return _cache[path]


def resolve(tok, paper_dir=None):
    cands = [tok, os.path.join("batches", tok)]
    if paper_dir:
        cands += [os.path.join(paper_dir, tok), os.path.join(paper_dir, "A", tok)]
    res = []
    for c in cands:
        g = glob.glob(c)
        if g:
            res += [x for x in g if os.path.isfile(x)]
            break
    return res


def cited_files(line, paper_dir=None):
    files = []
    for tok in PATH_RE.findall(URL_RE.sub(" ", line)):
        files += resolve(tok, paper_dir)
    return files


def matches(numstr, files):
    s = numstr.replace(",", "")
    neg = s.startswith("-")
    core = s.lstrip("-")
    if core.startswith("."):
        core = "0" + core
    v = float(core) * (-1 if neg else 1)
    d = len(core.split(".")[1]) if "." in core else 0
    for f in files:
        txt, vals = nums_in(f)
        if d == 0:
            if v in vals:
                return f
        else:
            for x in vals:
                if abs(round(x, d) - v) < 10 ** (-d - 6) or abs(round(abs(x), d) - abs(v)) < 10 ** (-d - 6) and (x < 0) == (v < 0):
                    return f
    return None


def mask(line):
    """Return (masked line, identifiers found)."""
    ids = []
    for rx in (URL_RE, DOI_RE, PATH_RE, LABEL_RE, OBS_RE, CHG_RE, ALNUM_RE):
        ids += rx.findall(line)
        line = rx.sub(" ", line)
    for m in PAPER_RE.findall(line):
        ids.append(m)
    line = PAPER_RE.sub(" ", line)
    return line, ids


def generic(path, structured_lines, section_rule=None):
    """Trace every number in `path` not covered by structured checks."""
    global n_fail
    lines = open(path, encoding="utf-8").read().split("\n")
    sec_files, paper_dir = [], None
    counts = Counter()
    unmatched, weak, idents = [], [], Counter()
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            sec_files = cited_files(line)
            if section_rule:
                sec_files += section_rule(line)
        if i in structured_lines:
            counts["covered by a structured check"] += len(NUM_RE.findall(mask(line)[0]))
            continue
        pm = re.search(r"papers/((?:0[1-9]|1\d|2[0-5])_[A-Z0-9]{6})", line)
        paper_dir = f"papers/{pm.group(1)}" if pm else None
        files = cited_files(line, paper_dir) + sec_files
        if path == TARGETS:
            pid = re.search(r"\|\s*((?:0[1-9]|1\d|2[0-5])_[A-Z0-9]{6})\s*\|", line)
            if pid:
                files += [f"papers/{pid.group(1)}/targets.json", f"papers/{pid.group(1)}/A/results.json", f"papers/{pid.group(1)}/B/results.json"]
        m, ids = mask(line)
        for x in ids:
            idents[x] += 1
        for dt in DATE_RE.findall(m) + TIME_RE.findall(m):
            hit = next((f for f in files if dt in nums_in(f)[0]), None)
            if hit:
                counts["date/time found in cited file"] += 1
            else:
                unmatched.append((i, dt, "date/time", files)); counts["UNMATCHED"] += 1
        m = TIME_RE.sub(" ", DATE_RE.sub(" ", m))
        for n in NUM_RE.findall(m):
            hit = matches(n, files)
            if hit:
                counts["number found in cited file"] += 1
                core = n.replace(",", "").lstrip("-")
                if "." not in core and float(core) <= 31:
                    weak.append((i, n, hit))
            else:
                unmatched.append((i, n, "number", files)); counts["UNMATCHED"] += 1
    say(f"Generic trace of {path}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for i, n, kind, files in unmatched:
        n_fail += 1
        say(f"  UNMATCHED line {i}: {kind} '{n}' not found in cited files {sorted(set(files)) or '(none cited)'}")
    say(f"  Weak matches (integer 0 to 31 found only by generic trace; line: value -> file): " +
        "; ".join(f"{i}: {n} -> {f}" for i, n, f in weak) if weak else "  Weak matches: none")
    say(f"  Identifiers seen (not measurements): {len(idents)} distinct")


def check(label, got, want):
    global n_fail
    ok = got == want
    if not ok:
        n_fail += 1
    say(f"  [{'OK' if ok else 'MISMATCH'}] {label}: report {got!r} vs source {want!r}")
    return ok


# ---------------------------------------------------------------- structured checks: report
rep = open(REPORT, encoding="utf-8").read().split("\n")
covered = set()
say(f"Number check for batch {K}. Generated by scripts/check_report_numbers.py {K}.")
say("")
say(f"== Structured checks: {REPORT}")
cj = json.load(open(f"batches/batch{K}_counts_rule4.json"))
keymap = {"Main": "counts_main", "Excluding 01": "counts_excluding_no_target", "If the uncited OSF": "counts_if_uncited_OSF_counted",
          "If 02 were judged": "counts_if_02_run_as_is"}
if K != "1":  # batch 2 on: one line per paper alternative, plus all alternatives together (scripts/apply_class_rules.py)
    keymap = {"Main": "counts_main", "All alternatives together": "counts_all_alternatives"}
    keymap.update({f"Alternative for {pid}": f"counts_if_{pid}_alt" for pid in cj.get("alternatives", {})})
for i, line in enumerate(rep, 1):
    for pre, key in keymap.items():
        if line.startswith(f"- {pre}"):
            got = dict(re.findall(r"\b([A-E]) (\d+)\b", line.split(":", 1)[1].split("(")[0]))
            want = {c: str(v) for c, v in cj[key].items() if str(v) != "0" or c in got}
            check(f"line {i} counts '{pre}'", got, {c: want.get(c, "0") for c in got})
            nm = re.search(r"\((\d+) papers\)", line)
            if nm:
                nk = "n_main" if key == "counts_main" else ("n_excluding_no_target" if K == "1" else key.replace("counts_", "n_", 1))
                check(f"line {i} n", int(nm.group(1)), cj[nk])
            covered.add(i)
rr = {r["paper_id"][:2]: r for r in csv.DictReader(open(f"batches/batch{K}_results_rule4.csv"))}
for i, line in enumerate(rep, 1):
    m = re.match(r"\|\s*(0[1-9]|1\d|2[0-5])_\w+ \|.*\| ([A-E]) / ([A-E]) \| ([A-E]) \|", line)
    if m:
        r = rr[m.group(1)]
        check(f"line {i} paper {m.group(1)} classes A/B/rule4", (m.group(2), m.group(3), m.group(4)),
              (r["class_agents_A"], r["class_agents_B"], r["class_rule4"]))
        doi = re.search(r"\[(10\.[^\]]+)\]", line).group(1)
        check(f"line {i} paper {m.group(1)} DOI", doi, r["paper_doi"].replace("https://doi.org/", ""))
        covered.add(i)
oc = json.load(open(f"batches/batch{K}_code_observations_counts.json"))
for i, line in enumerate(rep, 1):
    if re.search(r"\d+ observations: \d+ verified", line):
        a = re.findall(r"(\d+) (observations|verified findings?|unverified agent observations?|out of scope)", line)
        got = {(k if k.endswith("s") or k == "out of scope" else k + "s"): int(v) for v, k in a}
        check(f"line {i} code observation counts", got,
              {"observations": oc["n_observations"], "verified findings": oc["by_status"]["verified finding"],
               "unverified agent observations": oc["by_status"]["unverified agent observation"],
               "out of scope": oc["by_status"]["out of scope: not reproducibility"]})
        covered.add(i)
    if "The 16 marked" in line or re.search(r"The (\d+) marked \"unverified", line):
        n = int(re.search(r"The (\d+) marked", line).group(1))
        check(f"line {i} unverified count", n, oc["by_status"]["unverified agent observation"])
tc = Counter(r["match_status"] for r in csv.DictReader(open(f"batches/batch{K}_targets.csv")) if r["row_type"] == "paper target")
for i, line in enumerate(rep, 1):
    m = re.search(r"(\d+) of (\d+) computable targets", line)
    if m:
        computable = sum(v for k, v in tc.items() if k not in ("no paper target", "not computed by A or B"))
        check(f"line {i} targets matched / computable", (int(m.group(1)), int(m.group(2))),
              (tc["A and B match paper at reported rounding"], computable))
        covered.add(i)
say("")

# ---------------------------------------------------------------- structured checks: targets table
say(f"== Structured checks: {TARGETS}")
tg = open(TARGETS, encoding="utf-8").read().split("\n")
rows = list(csv.DictReader(open(f"batches/batch{K}_targets.csv")))


def fmt(v):
    """make_target_table.py prints values with 6 significant digits (Python 'g' format)."""
    if v in ("", None):
        return ""
    return f"{float(v):.6g}"


key = {(r["paper"], r["target_id"]): r for r in rows}
for i, line in enumerate(tg, 1):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if K in ("3", "4", "5") and len(cells) == 9 and re.match(r"(?:0[1-9]|1\d|2[0-5])_", cells[0]):
        # batch 3 and 4 paper-target rows: Paper | Target | Description | Location | Paper | A | B | Match | A/B agree
        r = key.get((cells[0], cells[1]))
        if r is None:
            check(f"line {i} row {cells[0]} {cells[1]} exists in CSV", False, True); continue
        check(f"line {i} {cells[0]} {cells[1]} paper/A/B/match/AB",
              (cells[4], cells[5], cells[6], cells[7], cells[8]),
              (fmt(r["paper_value"]), fmt(r["A_value"]), fmt(r["B_value"]), r["match_status"], r["AB_agree"]))
        tv = next((t for t in json.load(open(f"papers/{cells[0]}/targets.json")) if t.get("id") == cells[1]), None)
        check(f"line {i} {cells[0]} {cells[1]} paper value vs targets.json", fmt(r["paper_value"]), fmt(tv["paper_value"]) if tv else None)
        continue
    if len(cells) == 9 and re.match(r"(?:0[1-9]|1\d|2[0-5])_", cells[0]):
        r = key.get((cells[0], cells[1]))
        if r is None:
            check(f"line {i} row {cells[0]} {cells[1]} exists in CSV", False, True); continue
        pv = r["paper_value"]
        check(f"line {i} {cells[0]} {cells[1]} paper/A/B/match",
              (cells[4], cells[5], cells[6], cells[8]),
              (fmt(pv) if pv else "", fmt(r["A_value"]), fmt(r["B_value"]), r["match_status"]))
        # the paper value must equal targets.json
        tj = json.load(open(f"papers/{cells[0]}/targets.json"))
        tl = tj if isinstance(tj, list) else tj.get("targets", [])
        tv = next((t for t in tl if t.get("id") == cells[1] or t.get("target_id") == cells[1]), None)
        if tv is not None:
            pvj = tv.get("paper_value", tv.get("value"))
            check(f"line {i} {cells[0]} {cells[1]} paper value vs targets.json", fmt(pv), fmt(pvj))
        covered_t = True
    if len(cells) == 6 and cells[0].startswith(("I1", "I2", "I3")):
        r = next((x for x in rows if x["paper"] == "01_5BIH0P" and x["target_id"].split(" ")[0] == cells[0].split(" ")[0]), None)
        if r:
            check(f"line {i} 01 internal {cells[0].split(' ')[0]} deposited/A/B", (cells[2], cells[3], cells[4]),
                  (fmt(r["paper_value"]), fmt(r["A_value"]), fmt(r["B_value"])))
tcount = {"A and B match paper at reported rounding": None, "no paper target": None, "not computed by A or B": None}
tcount.update({k: None for k in tc})
for i, line in enumerate(tg, 1):
    m = re.match(r"- (.+?): (\d+)$", line.strip())
    if m and m.group(1) in tcount:
        check(f"line {i} count '{m.group(1)}'", int(m.group(2)), tc[m.group(1)])
    m = re.match(r"- A/B agreement (.+?): (\d+)$", line.strip())
    if m and K in ("3", "4", "5"):
        check(f"line {i} count 'A/B agreement {m.group(1)}'", int(m.group(2)),
              sum(1 for r in rows if r["row_type"] == "paper target" and r.get("AB_agree") == m.group(1)))
    m = re.match(r"- paper targets listed: (\d+) across (\d+) papers", line.strip())
    if m:
        listed = [r for r in rows if r["row_type"] == "paper target" and r["target_id"] != "(none)"]
        check(f"line {i} targets listed / papers", (int(m.group(1)), int(m.group(2))), (len(listed), len({r['paper'] for r in listed})))
    m = re.match(r"Internal-check counts: A and B match deposited value at reported rounding: (\d+)", line.strip())
    if m:
        check(f"line {i} internal-check count", int(m.group(1)),
              sum(1 for r in rows if r["paper"] == "01_5BIH0P" and r["row_type"] != "paper target" and r["match_status"].startswith("A and B match")))
# 02 clock table: values from the two as-is CSVs; relative difference recomputed
asisA = list(csv.DictReader(open("papers/02_ELBOXX/A/outputs/targets_pathA_clock2026.csv")))
in_clock = False
for i, line in enumerate(tg, 1):
    if line.startswith("## 02_ELBOXX without the clock fix"):
        in_clock = True; continue
    if in_clock and re.match(r"\| T\d", line):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        p, a, b, rel = float(c[1]), float(c[2]), float(c[3]), float(c[5])
        srcA = matches(c[2], ["papers/02_ELBOXX/A/outputs/targets_pathA_clock2026.csv"])
        srcB = matches(c[3], ["papers/02_ELBOXX/B/outputs/pathA_asis/targets_asis.csv"])
        srcP = matches(c[1], ["papers/02_ELBOXX/targets.json"])
        check(f"line {i} 02 as-is {c[0]} paper/A/B found in source files", (bool(srcP), bool(srcA), bool(srcB)), (True, True, True))
        aval = float(next(x for x in nums_in("papers/02_ELBOXX/A/outputs/targets_pathA_clock2026.csv")[1] if abs(round(x, 6) - a) < 5e-7 or f"{x:.6g}" == c[2]))
        check(f"line {i} 02 as-is {c[0]} relative difference (derived: (A - paper) / paper, 4 decimals)", f"{rel:+.4f}", f"{(aval - p) / p:+.4f}")
if K == "2":
    a06 = "papers/06_VSV5DM/A/outputs/targets_extracted.csv"; b06 = "papers/06_VSV5DM/B/outputs/targets_extracted.csv"
    a07 = "papers/07_JH9DBC/A/outputs/targets_extracted_fixest0142.csv"; b07 = "papers/07_JH9DBC/B/outputs/targets_extracted_fixest_current.csv"
    sec = None
    for i, line in enumerate(tg, 1):
        if line.startswith("## "):
            sec = "06" if line.startswith("## 06_VSV5DM T4") else ("07" if line.startswith("## 07_JH9DBC with current") else ("10" if line.startswith("## 10_6MLKJZ figure-claim") else None))
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if sec == "06" and line.startswith("| AME p") or sec == "06" and line.startswith("| coefficient p"):
            check(f"line {i} 06 T4 reading '{c[0]}' paper/A/B found in source files",
                  (bool(matches(c[1], ["papers/06_VSV5DM/targets.json"])), bool(matches(c[2], [a06])), bool(matches(c[3], [b06]))), (True, True, True))
            covered_t = True
        if sec == "07" and re.match(r"\| T\d", line):
            check(f"line {i} 07 fixest 0.14.2 {c[0]} paper/A/B found in source files",
                  (bool(matches(c[1], ["papers/07_JH9DBC/targets.json"])), bool(matches(c[2], [a07])), bool(matches(c[3], [b07]))), (True, True, True))
            pv, av = float(c[1]), float(c[2])
            check(f"line {i} 07 {c[0]} relative difference (derived from the printed values: (A - paper) / paper, 4 decimals; A printed to 6 significant digits)",
                  c[5], f"{(av - pv) / pv:+.4f}")
        if sec == "10" and re.match(r"\| FC\d", line):
            fa = json.load(open("papers/10_6MLKJZ/A/outputs/figure_claims.json")); fb = json.load(open("papers/10_6MLKJZ/B/outputs/figure_claims.json"))
            want = {"FC1": (f"count {fa['FC1']['count_CI_excludes_0']}, holds {fa['FC1']['same_conclusion']}", f"count {fb['FC1']['count_excluding_0']}, holds {fb['FC1']['same_conclusion']}"),
                    "FC2": (f"holds {fa['FC2']['same_conclusion']}", f"holds {fb['FC2']['same_conclusion']}"),
                    "FC3": (f"strict {fa['FC3']['same_conclusion_strict']}, lenient {fa['FC3']['same_conclusion_lenient']}", f"strict {fb['FC3']['strict_same_conclusion']}, lenient {fb['FC3']['lenient_same_conclusion']}")}[c[0]]
            check(f"line {i} 10 {c[0]} A/B outcome vs figure_claims.json", (c[2], c[3]), want)
if K == "3":
    # 11_DDOFPS v2 programs-file block: values from A's results.json (alternative_v2) and B's same_conclusion_v2
    a11 = json.load(open("papers/11_DDOFPS/A/results.json")); b11 = json.load(open("papers/11_DDOFPS/B/results.json"))
    tj11 = {t["id"]: t for t in json.load(open("papers/11_DDOFPS/targets.json"))}
    av2 = {t["id"]: t for t in a11["alternative_v2"]["targets"]}
    sec = None
    for i, line in enumerate(tg, 1):
        if line.startswith("## "):
            sec = "11v2" if line.startswith("## 11_DDOFPS with the v2") else None
            continue
        if sec == "11v2" and re.match(r"\| T\d", line):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            t = tj11[c[0]]; v = av2[c[0]]["reproduced_value"]
            check(f"line {i} 11 v2 {c[0]} paper/A/match/B", (c[1], c[2], c[3], c[4]),
                  (str(t["paper_value"]), fmt(v), str(round(float(v), t["paper_rounding_decimals"]) == round(float(t["paper_value"]), t["paper_rounding_decimals"])),
                   str(b11["same_conclusion_v2"][c[0]])))
if K == "4":
    # 17_T1NXVQ reduced-bootstrap block and 18_YXC5K5 R_c block: every printed value must be found (at its printed decimals)
    # in the source file named in the block; true/false columns are recomputed from the printed interval.
    f17a, f17b = "papers/17_T1NXVQ/A/outputs/boot_summary.csv", "papers/17_T1NXVQ/B/outputs/summary_bootstrap_authorseeds.csv"
    f18a, f18b = "papers/18_YXC5K5/A/outputs/R_c_targets_extracted.csv", "papers/18_YXC5K5/B/outputs/R_c_targets_extracted.csv"
    tj17 = {t["id"]: t for t in json.load(open("papers/17_T1NXVQ/targets.json"))}
    tj18 = {t["id"]: t for t in json.load(open("papers/18_YXC5K5/targets.json"))}
    a18 = {t["id"]: t for t in json.load(open("papers/18_YXC5K5/A/results.json"))["targets"]}
    sec = None
    for i, line in enumerate(tg, 1):
        if line.startswith("## "):
            sec = "17" if line.startswith("## 17_T1NXVQ reduced") else ("18" if line.startswith("## 18_YXC5K5 docid") else None)
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if sec == "17" and re.match(r"\| T\d", line):
            nums = re.findall(r"-?\d+\.\d+", c[2] + " " + c[4])
            okA = all(matches(x, [f17a]) for x in nums[:2]); okB = all(matches(x, [f17b]) for x in nums[2:])
            check(f"line {i} 17 {c[0]} paper value vs targets.json, A and B interval ends found in source CSVs",
                  (c[1], okA, okB), (str(tj17[c[0]]["paper_value"]), True, True))
            lo_a, hi_a, lo_b, hi_b = map(float, nums)
            check(f"line {i} 17 {c[0]} excludes-0 columns recomputed", (c[3], c[5]), (str(lo_a > 0 or hi_a < 0), str(lo_b > 0 or hi_b < 0)))
        if sec == "17" and line.startswith("Reproduced draws"):
            ma = max(abs(float(r["abs_diff"])) for r in csv.DictReader(open("papers/17_T1NXVQ/A/outputs/boot_vs_deposited.csv")))
            mb = max(abs(float(r["abs_diff"])) for r in csv.DictReader(open("papers/17_T1NXVQ/B/outputs/compare_boot_vs_deposited.csv")))
            na = len(list(csv.DictReader(open("papers/17_T1NXVQ/A/outputs/boot_vs_deposited.csv"))))
            nb = len(list(csv.DictReader(open("papers/17_T1NXVQ/B/outputs/compare_boot_vs_deposited.csv"))))
            got = re.findall(r"(\d+) coefficients? compared, largest absolute difference ([\d.e+-]+)|B (\d+) compared, largest absolute difference ([\d.e+-]+)", line)
            check(f"line {i} 17 draws vs deposited (n and max difference, recomputed)", line.count(f"A {na} coefficients compared, largest absolute difference {ma:.2e}") + line.count(f"B {nb} compared, largest absolute difference {mb:.2e}"), 2)
            covered_t = True
        if sec == "18" and re.match(r"\| T\d", line):
            p_, d_ = tj18[c[0]]["paper_value"], tj18[c[0]]["paper_rounding_decimals"]
            check(f"line {i} 18 R_c {c[0]} paper / as deposited / A / B found in source files",
                  (c[1], fmt(a18[c[0]]["reproduced_value"]) == c[2], bool(matches(c[3], [f18a])), bool(matches(c[4], [f18b]))),
                  (str(p_), True, True, True))
            va, vb = float(c[3]), float(c[4])
            want = "yes, both runs" if round(va, d_) == round(float(p_), d_) and round(vb, d_) == round(float(p_), d_) else "no, both runs"
            check(f"line {i} 18 R_c {c[0]} match column recomputed from printed values", c[5], want)
if K == "5":
    import statistics
    from math import erf, sqrt
    tj21 = {t["id"]: t for t in json.load(open("papers/21_LEFTNE/targets.json"))}
    a5 = json.load(open("papers/21_LEFTNE/A/outputs/si_A5_check.json"))
    b5 = open("papers/21_LEFTNE/B/outputs/si_tableA5_check.txt").read()
    bN = re.search(r"\nN\t(\d+)\t(\d+)\t(\d+)", b5).groups()
    f23a, f23b = "papers/23_FXRNBA/A/outputs/targets_extracted.csv", "papers/23_FXRNBA/B/outputs/targets_extracted.csv"
    tj24 = {t["id"]: t for t in json.load(open("papers/24_U9CKK6/targets.json"))}
    am24 = open("papers/24_U9CKK6/A/outputs/pdf_target_cell_check.md").read()
    bj24 = {c["id"]: c for c in json.load(open("papers/24_U9CKK6/B/outputs/pdf_cell_check.json"))["cells"]}
    est24 = {t["id"]: t for t in json.load(open("papers/24_U9CKK6/A/results.json"))["targets"]}["T1"]["reproduced_value"]
    tj25 = {t["id"]: t for t in json.load(open("papers/25_914AN0/targets.json"))}
    r25 = {ag: {t["id"]: t for t in json.load(open(f"papers/25_914AN0/{ag}/results.json"))["targets"]} for ag in "AB"}

    def q7(x, p):
        x = sorted(x); h = (len(x) - 1) * p; lo = int(h)
        return x[lo] + (h - lo) * (x[min(lo + 1, len(x) - 1)] - x[lo])

    sec = None
    for i, line in enumerate(tg, 1):
        if line.startswith("## "):
            sec = ("21" if line.startswith("## 21_LEFTNE") else "23" if line.startswith("## 23_FXRNBA") else
                   "24c" if line.startswith("## 24_U9CKK6 target cells") else "24r" if line.startswith("## 24_U9CKK6 R_a") else
                   "25" if line.startswith("## 25_914AN0") else None)
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if sec == "21" and re.match(r"\| T[34] ", line):
            tid = c[0][:2]
            want_a = (a5["T3_cell_None_Trump"] + ", N " + a5["N_None"]) if tid == "T3" else (a5["T4_cell_Party_TrumpParty"] + ", N " + a5["N_Party"])
            cell_b = "0.15 *** (0.02)" if tid == "T3" else "0.22 *** (0.05)"
            ok_b = cell_b.split(" (")[0] in b5 and "(" + cell_b.split("(")[1] in b5
            check(f"line {i} 21 {tid} SI cell: targets.json / A re-check / B re-check", (c[1], c[2], c[3]),
                  (str(tj21[tid]["paper_value"]), want_a, f"{cell_b if ok_b else 'not found'}, N {bN[0] if tid == 'T3' else bN[2]}"))
        if sec == "21" and line.startswith("T6 is the only"):
            dg = json.load(open("papers/21_LEFTNE/A/outputs/diagnostics.json"))
            b21 = open("papers/21_LEFTNE/B/outputs/diag_t6_and_samples.txt").read()
            nums = [int(x) for x in re.findall(r"\b(\d{3})\b", line)]
            check(f"line {i} 21 T6 paragraph: 698 and 697 traced", sorted(set(nums)),
                  sorted({int(dg["nobs_mod2"]), int(tj21["T6"]["paper_value"]), int(re.search(r"complier==1 rows: (\d+)", b21).group(1))}))
            covered_t = True
        if sec == "23" and re.match(r"\| \d: ", line):
            check(f"line {i} 23 T6 formula '{c[0][:2]}' A and B values found in source CSVs; rounding column",
                  (bool(matches(c[1], [f23a])), bool(matches(c[2], [f23b])), c[3]),
                  (True, True, "yes" if round(float(c[1]), 1) == 3.6 and round(float(c[2]), 1) == 3.6 else "no"))
        if sec == "24c" and re.match(r"\| T\d ", line):
            tid = c[0]; bv = bj24[tid].get("model2_value", bj24[tid].get("value"))
            check(f"line {i} 24 {tid} cell re-check: targets.json / A / B value / B agrees", (c[1], c[2], c[3], c[4]),
                  (fmt(tj24[tid]["paper_value"]), "yes" if f"Matches {tid}." in am24 else "no", fmt(bv), "yes" if bj24[tid]["matches_targets_json"] else "no"))
        if sec == "24r" and re.match(r"\| [AB] \|", line):
            ag = c[0]
            rr = list(csv.DictReader(open(f"papers/24_U9CKK6/{ag}/outputs/R_a_partial.csv")))
            e = [float(x["estimate"]) for x in rr if x.get("ok", "TRUE") == "TRUE"]
            sd = statistics.stdev(e); lo, hi = q7(e, 0.025), q7(e, 0.975)
            pz = 2 * (1 - 0.5 * (1 + erf(abs(est24 / sd) / sqrt(2))))
            if ag == "A":
                kr = next(csv.DictReader(open("papers/24_U9CKK6/A/outputs/R_a_K.csv"))); t1, K_ = float(kr["t_first_secs"]), int(kr["K"])
            else:
                kb = open("papers/24_U9CKK6/B/outputs/R_a_K.txt").read().split(); t1, K_ = float(kb[kb.index("first_refit_secs") + 1]), int(kb[0])
            want = (f"{t1:.2f}", str(K_), str(len(e)), f"{sd:.6f}", f"[{lo:.6f}, {hi:.6f}]", "yes" if lo > 0 or hi < 0 else "no", f"{pz:.4f}", "yes" if pz < 0.001 else "no")
            check(f"line {i} 24 R_a run {ag} recomputed from R_a_partial.csv and the K file", tuple(c[1:9]), want)
            rj = json.load(open(f"papers/24_U9CKK6/{ag}/results.json"))
            ra = next(x for x in rj["robustness"] if x["id"] == "R_a")
            check(f"line {i} 24 R_a run {ag} normal p equals results.json p_value at 4 decimals", f"{ra['p_value']:.4f}", c[7])
        if sec == "24r" and line.startswith("Both runs fail"):
            covered_t = True
        if sec == "25" and re.match(r"\| T\d ", line):
            tid = c[0]
            prose = float(re.search(r"prose p\. 180 gives (-?[\d.]+)", tj25[tid]["location"]).group(1))
            check(f"line {i} 25 {tid} table / prose / A / B", (c[1], c[2], c[3], c[4]),
                  (str(tj25[tid]["paper_value"]), str(prose), fmt(r25["A"][tid]["reproduced_value"]), fmt(r25["B"][tid]["reproduced_value"])))
say("")

# ---------------------------------------------------------------- generic trace of everything else
say("== Generic trace (numbers not covered above)")
generic(REPORT, covered)
t_struct = {i for i, l in enumerate(tg, 1) if (re.match(r"\| T\d", l) or l.startswith("- ") or l.startswith("Internal-check counts"))}
if K == "4":
    t_struct |= {i for i, l in enumerate(tg, 1) if l.startswith("Reproduced draws against")}
if K == "5":
    t_struct |= {i for i, l in enumerate(tg, 1) if re.match(r"\| (\d: |[AB] \|)", l) or l.startswith("T6 is the only")}
if K == "2":
    t_struct |= {i for i, l in enumerate(tg, 1) if re.match(r"\| (FC\d|AME p|coefficient p)", l)}


def t_sections(h):
    if "01_5BIH0P" in h:
        return ["papers/01_5BIH0P/A/results.json", "papers/01_5BIH0P/B/results.json", f"batches/batch{K}_targets.csv"]
    if "without the clock fix" in h:
        return ["papers/02_ELBOXX/A/outputs/clock_comparison.json"]
    if "Paper targets" in h or "Counts" in h:
        return [f"batches/batch{K}_targets.csv"]
    if h.startswith("## 06_VSV5DM T4"):
        return ["papers/06_VSV5DM/targets.json", "papers/06_VSV5DM/A/outputs/targets_extracted.csv"]
    if h.startswith("## 07_JH9DBC with current"):
        return ["papers/07_JH9DBC/A/outputs/targets_extracted_fixest0142.csv", "papers/07_JH9DBC/A/environment.txt", "papers/07_JH9DBC/B/environment.txt"]
    if h.startswith("## 11_DDOFPS with the v2"):
        return ["papers/11_DDOFPS/A/results.json", "papers/11_DDOFPS/targets.json"]
    if h.startswith("## 17_T1NXVQ reduced"):
        return ["papers/17_T1NXVQ/A/outputs/boot_K.json", "papers/17_T1NXVQ/B/outputs/bootstrap_K.json", "papers/17_T1NXVQ/A/outputs/boot_summary.csv", "papers/17_T1NXVQ/PREREG.md"]
    if h.startswith("## 18_YXC5K5 docid"):
        return ["papers/18_YXC5K5/PREREG.md", "papers/18_YXC5K5/A/outputs/R_c_targets_extracted.csv"]
    if h.startswith("## 21_LEFTNE T6"):
        return ["papers/21_LEFTNE/A/outputs/si_A5_check.json", "papers/21_LEFTNE/targets.json", "papers/21_LEFTNE/A/outputs/diagnostics.json"]
    if h.startswith("## 23_FXRNBA T6"):
        return ["papers/23_FXRNBA/targets.json", "papers/23_FXRNBA/PREREG.md", "papers/23_FXRNBA/A/outputs/targets_extracted.csv"]
    if h.startswith("## 24_U9CKK6 target cells"):
        return ["papers/24_U9CKK6/targets.json", "papers/24_U9CKK6/PREREG.md"]
    if h.startswith("## 24_U9CKK6 R_a"):
        return ["papers/24_U9CKK6/PREREG.md", "papers/24_U9CKK6/A/outputs/R_a_K.csv", "papers/24_U9CKK6/B/outputs/R_a_K.txt", "papers/24_U9CKK6/A/outputs/R_a_partial.csv"]
    if h.startswith("## 25_914AN0"):
        return ["papers/25_914AN0/targets.json"]
    if h.startswith("## 10_6MLKJZ figure-claim"):
        return ["papers/10_6MLKJZ/A/outputs/figure_claims.json", "papers/10_6MLKJZ/PREREG.md"]
    return []


generic(TARGETS, t_struct, t_sections)
say("")
say(f"RESULT: {'PASS' if n_fail == 0 else 'FAIL'} ({n_fail} problems)")
print("\n".join(out))
sys.exit(1 if n_fail else 0)
