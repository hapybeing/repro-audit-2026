"""Write SELECTION.md (repo root): how the 25 papers were drawn. Every number is read or computed from files:
selection/frame_meta.json, selection/frame_raw.csv, candidates.csv, selection/order.csv, selection/screening.csv,
selection/selected.csv, selection/selection_meta.json, CHANGELOG_METHOD.md, scripts/01_build_frame.py,
scripts/02_select.py, batches/batch1_prereg_hashes.txt, papers/0[1-5]*/{A,B}/LOG.md and results.json.
If numpy is importable, the seeded permutation is recomputed and compared with selection/order.csv.
Usage: python3 scripts/selection_summary.py   (use a Python with numpy for the permutation re-check)
"""
import csv, datetime, glob, hashlib, json, os, re
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda p: f"{REPO}/{p}"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


fm = json.load(open(R("selection/frame_meta.json")))
sm = json.load(open(R("selection/selection_meta.json")))
frame = list(csv.DictReader(open(R("selection/frame_raw.csv"))))
cands = list(csv.DictReader(open(R("candidates.csv"))))
order = list(csv.DictReader(open(R("selection/order.csv"))))
scr = list(csv.DictReader(open(R("selection/screening.csv"))))
sel = list(csv.DictReader(open(R("selection/selected.csv"))))
chlog = open(R("CHANGELOG_METHOD.md"), encoding="utf-8").read()
build_src = open(R("scripts/01_build_frame.py"), encoding="utf-8").read()
sel_src = open(R("scripts/02_select.py"), encoding="utf-8").read()

# ---- frame
n_frame_meta = fm["n_datasets"]; n_frame_rows = len(frame)
harvard = [r for r in frame if r["dataset_doi"].startswith("10.7910/")]
m = re.search(r"(\d+) of (\d+) frame rows are hosted at Harvard", chlog)
ch_h, ch_n = int(m.group(1)), int(m.group(2))
prefix = Counter(r["dataset_doi"].split("/")[0] for r in frame)
lang = Counter(r["code_language"] for r in frame)
lang_h = Counter(r["code_language"] for r in harvard)
# query parameters, read from the build script source
base = re.search(r'BASE="([^"]+)"', build_src).group(1)
date_fq = re.search(r"DATE='([^']+)'", build_src).group(1)
q_items = re.search(r"urlencode\((\[.*?\])\)\n", build_src).group(1)
q_desc = f"`{q_items}` (from the build script; `ct` loops over the content types below, `start` pages by 1000)"

# ---- permutation
seed = sm["seed"]
seed_in_src = int(re.search(r"SEED=(\d+)", sel_src).group(1))
perm_line = re.search(r"perm=.*", sel_src).group(0)
sort_line = re.search(r"rows=sorted\(.*", sel_src).group(0)
try:
    import numpy as np
    hs = sorted(harvard, key=lambda r: r["dataset_doi"])
    perm = np.random.default_rng(seed).permutation(len(hs))
    same = [hs[i]["dataset_doi"] for i in perm] == [r["dataset_doi"] for r in order]
    perm_check = (f"Recomputed here with numpy {np.__version__}: sorting the {len(hs)} Harvard-hosted frame rows by DOI and applying "
                  f"`default_rng({seed}).permutation` gives the same order as `selection/order.csv`: **{'yes' if same else 'NO'}**.")
except ImportError:
    perm_check = "Not recomputed in this run (numpy not available to the Python that ran this script)."

# ---- screening
crit = [("E1_article", "E1 article: one peer-reviewed journal article with a DOI, published 2023 to 2026 (OpenAlex)"),
        ("E2_open_text", "E2 article text openly readable (OpenAlex is_oa)"),
        ("E3_no_restricted", "E3 no restricted file in the dataset"),
        ("E4_no_stata_matlab_spss_sas", "E4 no Stata, MATLAB, SPSS or SAS code files"),
        ("E5_size_ok", "E5 total size 5 GB or less"),
        ("E6_licence", "E6 no access-request terms (licence check)")]
ranks = [int(r["rank"]) for r in scr]
n_elig = sum(r["eligible"] == "True" for r in scr)
fails = {c: Counter(r[c] for r in scr) for c, _ in crit}
only = Counter()
for r in scr:
    f = [c for c, _ in crit if r[c] != "True"]
    if len(f) == 1: only[f[0]] += 1
nfail_dist = Counter(sum(r[c] != "True" for c, _ in crit) for r in scr)
no_doi = sum("no related-publication DOI" in r["reason"] for r in scr)
xref = sum("Crossref title match" in r["reason"] for r in scr)
not_retr = sum("not retrievable" in r["reason"] for r in scr)
subj = Counter(r["subject"].split("; ")[0] for r in sel)
sel_ranks = [int(r["rank"]) for r in sel]
sel_lang = Counter(r["code_language"] for r in sel)

# ---- open data
scr_cols = list(scr[0].keys())
data_cols = [c for c in scr_cols if re.search(r"data", c, re.I) and c not in ("dataset_doi", "dataset_link")]
rep = open(R("batches/batch1_report.md"), encoding="utf-8").read()
osf_line = next(l.strip("- ").strip() for l in rep.splitlines() if l.strip().startswith("- 04: the article has no data statement"))
p04 = next(r for r in sel if r["dataset_doi"].endswith("PSHE5L"))
pre03 = open(R("papers/03_3IOGQ8/PREREG.md"), encoding="utf-8").read()
byonic = "NOT DEPOSITED" in pre03 and "Byonic_results.csv" in pre03
pre01 = open(R("papers/01_5BIH0P/PREREG.md"), encoding="utf-8").read()
traj = "The production trajectory is not in the dataset" in pre01

# ---- pre-registration timing
hl = open(R("batches/batch1_prereg_hashes.txt")).read().splitlines()
frozen = re.search(r"frozen (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", hl[0]).group(1)
frozen_utc = datetime.datetime.strptime(frozen, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
hash_rows = []
for l in hl[2:]:
    if not l.strip(): continue
    h, p = l.split(None, 1)
    hash_rows.append((p.strip(), h, sha(R(p.strip())) == h))
tline = re.compile(r"^(?:#+\s*)?(?:-\s*)?(?:\*\*)?(?:(2026-\d\d-\d\d)\s+)?(\d{1,2}):(\d{2})\b")
log_rows = []
for f in sorted(glob.glob(R("papers/0[1-5]_*/[AB]/LOG.md"))):
    pdir = os.path.dirname(f)
    rd = json.load(open(f"{pdir}/results.json")).get("run_date_ist")
    times = []
    cur = rd  # current date: run_date_ist until a date heading (e.g. "## 2026-10-10") changes it
    for line in open(f, encoding="utf-8"):
        hd = re.match(r"^#+.*?(2026-\d\d-\d\d)", line.strip())
        if hd: cur = hd.group(1)
        mm = tline.match(line.strip())
        if mm:
            d = mm.group(1) or cur
            times.append(datetime.datetime.strptime(f"{d} {mm.group(2)}:{mm.group(3)}", "%Y-%m-%d %H:%M").replace(tzinfo=IST))
    files = [p for p in glob.glob(pdir + "/**/*", recursive=True) if os.path.isfile(p)]
    mt = min(os.path.getmtime(p) for p in files)
    log_rows.append((os.path.relpath(pdir, REPO), min(times), datetime.datetime.fromtimestamp(mt, datetime.timezone.utc)))
first_log = min(r[1] for r in log_rows)
first_mtime = min(r[2] for r in log_rows)
sel_run = sm["run_utc"]
prot = re.search(r"#3 \((.*?)\)", chlog).group(1)
prot_restore = re.search(r"restored verbatim from the\s+original text at ([\d:]+ IST)", chlog).group(1)

# ---- file hashes
git_present = any(os.path.exists(os.path.join(d, ".git")) for d in [REPO, os.path.dirname(REPO), os.path.dirname(os.path.dirname(REPO))])
hash_files = sorted(glob.glob(R("scripts/*"))) + [R(p) for p in ("PROTOCOL.md", "CHANGELOG_METHOD.md", "AGENT_RUNBOOK.md",
    "candidates.csv", "selection/frame_raw.csv", "selection/frame_meta.json", "selection/order.csv", "selection/screening.csv",
    "selection/selected.csv", "selection/selection_meta.json", "batches/batch1_prereg_hashes.txt")]


def ist(dt):
    return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M IST")


def utc(dt):
    return dt.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


L = []
A = L.append
A("# How the papers were selected")
A("")
A("Generated by `scripts/selection_summary.py` from the files named in each section. Every number below is read or computed "
  "from those files; nothing is typed by hand. Counts only, no percentages.")
A("")
A("## 1. Sampling frame")
A(f"- Frame size: **{n_frame_meta}** datasets (`selection/frame_meta.json` n_datasets; `selection/frame_raw.csv` has {n_frame_rows} rows).")
A(f"- Code language in the frame (Dataverse file content type): " + ", ".join(f"{k} {v}" for k, v in sorted(lang.items())) + ".")
A(f"- Harvard-hosted subset (dataset DOI prefix 10.7910), applied before the random draw (CHANGELOG_METHOD.md #1): **{len(harvard)}** "
  f"datasets counted here; CHANGELOG #1 states {ch_h} of {ch_n}; `candidates.csv` has {len(cands)} rows and `selection/order.csv` {len(order)} rows. "
  f"Other prefixes in the frame: {n_frame_rows - len(harvard)} rows across {len(prefix) - 1} prefixes (records harvested from other repositories, "
  "whose files the Harvard API does not serve).")
A(f"- Harvard subset by code language: " + ", ".join(f"{k} {v}" for k, v in sorted(lang_h.items())) + ".")
A("")
A("## 2. How the frame was drawn")
A(f"- Source: Harvard Dataverse public Search API `{base}` (no sign-in), script `scripts/01_build_frame.py`.")
A(f"- One query per code content type, paged 1000 at a time: {q_desc}.")
A(f"- Date filter: `{date_fq}` (Dataverse dateSort, i.e. release date).")
A("- Content types counted as code: " + ", ".join(f"`{k}` ({v})" for k, v in fm["content_types"].items()) + ".")
A("- A dataset enters the frame if at least one of its files has one of these content types. File hits are grouped to datasets by persistent id.")
A(f"- Frame build time recorded in `frame_meta.json`: {fm['built_utc']}.")
A("")
A("## 3. Random order")
A(f"- Seed: **{seed}** (`selection/selection_meta.json`; `scripts/02_select.py` has SEED={seed_in_src}).")
A(f"- Method: Harvard-hosted rows sorted by dataset DOI (`{sort_line.strip()}`), then `{perm_line.strip()}`; the permuted order is written to `selection/order.csv` before screening.")
A(f"- {perm_check}")
A("")
A("## 4. Screening")
A(f"- Screened in random order until 25 eligible: **{len(scr)}** datasets screened (ranks {min(ranks)} to {max(ranks)} of {len(order)}; "
  f"selection_meta n_screened {sm['n_screened']}), **{n_elig}** eligible, {len(scr) - n_elig} not eligible. Selected: {len(sel)} "
  f"(ranks {min(sel_ranks)} to {max(sel_ranks)}).")
A(f"- Screening run time recorded in `selection_meta.json`: {sel_run}.")
A("")
A("| Criterion (column in selection/screening.csv) | Pass | Fail | Failed only this criterion |")
A("|---|---|---|---|")
for c, d in crit:
    A(f"| {d} (`{c}`) | {fails[c].get('True', 0)} | {sum(v for k, v in fails[c].items() if k != 'True')} | {only[c]} |")
A("")
A("- Number of criteria failed per screened dataset: " + ", ".join(f"{k} failed: {v}" for k, v in sorted(nfail_dist.items())) + ".")
A(f"- Paper DOI found by Crossref title match (CHANGELOG #2): {xref} screened datasets; no related-publication DOI found: {no_doi}; "
  f"dataset metadata not retrievable: {not_retr}.")
A(f"- Selected code language: " + ", ".join(f"{k} {v}" for k, v in sorted(sel_lang.items())) + ".")
A(f"- Field rule (at least 3 subjects): primary subjects of the 25 selected: " + ", ".join(f"{k} {v}" for k, v in sorted(subj.items()))
  + f". {len(subj)} subjects, so {'no replacement was needed' if len(subj) >= 3 else 'replacement was needed'}.")
A("")
A("## 5. What \"open code and data\" meant in practice")
A("- The frame filter required only that a dataset contain at least one R or Python code file (by Dataverse content type). "
  "It did not check for data files.")
A(f"- Eligibility criteria E1 to E6 (`selection/screening.csv` columns: {', '.join(c for c, _ in crit)}) contain no data-presence "
  f"criterion. Columns mentioning data, other than the DOI and link: {len(data_cols)}. E3 checks that no file is restricted, not that data are present.")
A("- So the presence of the data needed to reproduce the paper was **not** an eligibility criterion. It was assessed only during the audit, "
  "where it can lead to class C.")
A(f"- Batch 1 shows the consequence: 04_PSHE5L's deposit is {int(p04['total_bytes'])} bytes titled \"{p04['title'][:22]}...\" and the batch report "
  f"(revision 3) records: \"{osf_line}\". 03_3IOGQ8's notebook input `Byonic_results.csv` is recorded as not deposited in its PREREG.md: {'yes' if byonic else 'no'}. "
  f"01_5BIH0P's production trajectory is recorded as not in the dataset in its PREREG.md: {'yes' if traj else 'no'}.")
A("- Any description of the sample as \"papers with open data and code\" should read \"papers whose Dataverse deposit contains R or Python code\".")
A("")
A("## 6. Pre-registration came before the runs")
A(f"- Batch 1 PREREG.md and targets.json frozen: **{utc(frozen_utc)}** = {ist(frozen_utc)} (`batches/batch1_prereg_hashes.txt`).")
A(f"- Those files still match the frozen sha256 today: {sum(ok for _, _, ok in hash_rows)} of {len(hash_rows)}.")
A(f"- Selection run (`selection_meta.json` run_utc): {sel_run}, before the freeze.")
A("")
A("| Agent folder | Earliest LOG.md timestamp (start of the agent's work) | Earliest file modification time in the folder | After freeze? |")
A("|---|---|---|---|")
for p, t, mt in log_rows:
    A(f"| {p} | {ist(t)} ({utc(t)}) | {utc(mt)} | {'yes' if (t > frozen_utc and mt > frozen_utc) else 'NO'} |")
A("")
A(f"- Earliest agent LOG entry across batch 1: {ist(first_log)}; earliest file in any agent folder: {utc(first_mtime)}; freeze: {utc(frozen_utc)}. "
  "LOG times are minute-resolution IST as written by the agents (date from results.json run_date_ist where a line gives only a time); "
  "file modification times come from the file system and can be reset by copies, so they are a secondary check.")
A(f"- Caveat recorded in CHANGELOG_METHOD.md #3 ({prot}): PROTOCOL.md was lost from the workspace and restored verbatim at {prot_restore}, "
  "after the freeze; the pre-registration agents worked from AGENT_RUNBOOK.md and their brief.")
A("")
A("## 7. Script and file hashes")
A(f"- Git repository present: {'yes' if git_present else 'no (no .git directory in the repo or its parents), so sha256 file hashes are given instead'}.")
A("- sha256 at the time this file was generated (this script hashes itself as it is on disk):")
A("")
A("| File | sha256 |")
A("|---|---|")
for p in hash_files:
    if os.path.isfile(p):
        A(f"| {os.path.relpath(p, REPO)} | `{sha(p)}` |")
A("")
A(f"Generated {datetime.datetime.now(IST).strftime('%Y-%m-%d %H:%M IST')}.")
text = "\n".join(L) + "\n"
assert "\u2014" not in text and "%" not in text, "em dash or percent sign in output"
open(R("SELECTION.md"), "w").write(text)
print(text)
