"""Build the final all-25 synthesis (v1.0) from the published batch files.
Usage (from the repository root): python3 scripts/make_final.py
Reads only committed files: selection/selected.csv, batches/batch{1..5}_results_rule4.csv, batch{k}_results.csv,
batch{k}_counts_rule4.json, batch{k}_class_rules.json, batch{k}_targets.csv, batch{k}_code_observations.csv,
batch{k}_report.md, CHANGELOG_METHOD.md, PROTOCOL.md, SELECTION.md.
Writes final/all25_results.csv, final/all25_counts.json, final/FINAL_REPORT.md and a byte-identical copy FINAL_REPORT.md.
Counts only: no percentages or rates anywhere (n = 25)."""
import csv, json, os, re, shutil
from collections import Counter, OrderedDict

B = range(1, 6)
CLS = "ABCDE"
GH = "https://github.com/hapybeing/repro-audit-2026"
os.makedirs("final", exist_ok=True)


def rcsv(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def cnt(vals):
    c = Counter(vals)
    return OrderedDict((k, c.get(k, 0)) for k in CLS)


def rounds_equal(a, b, dec):
    try:
        return round(float(a), int(dec)) == round(float(b), int(dec))
    except (TypeError, ValueError):
        return False


# ------------------------------------------------------------------ selection metadata
sel = {}
for r in rcsv("selection/selected.csv"):
    if r["eligible"] == "True":
        sel[int(r["audit_pos"])] = r

# ------------------------------------------------------------------ freeze references (parsed from batch reports)
freeze = {}
t1 = open("batches/batch1_report.md", encoding="utf-8").read()
m = re.search(r"frozen locally at (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)", t1)
freeze[1] = f"self-attested local freeze {m.group(1)} (batches/batch1_prereg_hashes.txt); first published with the results"
for k in range(2, 6):
    t = open(f"batches/batch{k}_report.md", encoding="utf-8").read()
    m = re.search(r"frozen at (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)", t)
    c = re.search(r"commit ([0-9a-f]{7})", t)
    i = re.search(r"issues/(\d+)", t)
    freeze[k] = f"issue #{i.group(1)}, commit {c.group(1)}, frozen {m.group(1)}"

# ------------------------------------------------------------------ per paper
rows, alt_rows, verified = [], [], []
agree_class = agree_all = lead_differs = 0
tgt_total = tgt_match = tgt_computed = tgt_differs = tgt_notcomp = 0
rob = Counter()
rob_ab_diff = 0
obs_status = Counter()
alt_by_batch = {}
for k in B:
    r4 = rcsv(f"batches/batch{k}_results_rule4.csv")
    res = {r["paper_id"]: r for r in rcsv(f"batches/batch{k}_results.csv")}
    rules = json.load(open(f"batches/batch{k}_class_rules.json", encoding="utf-8"))
    tg = rcsv(f"batches/batch{k}_targets.csv")
    ob = rcsv(f"batches/batch{k}_code_observations.csv")
    for o in ob:
        obs_status[o["status"]] += 1
    rob_ab_diff += sum("robustness conclusion differs" in r["ab_flags"] for r in res.values())
    for j, r in enumerate(r4):
        pid = r["paper_id"]
        pos = int(pid[:2])
        s = sel[pos]
        rule = rules[pid]
        main = r["class_rule4"]
        alt = rule["alt_class"]
        if alt == "no computational target":
            alt = "excluded (no computational target)"
        alt_label = rule["alt_label"]
        # targets
        mine = [t for t in tg if t["paper"] == pid and t["row_type"] == "paper target" and t["match_status"] != "no paper target"]
        n_t = len(mine)
        n_m = sum(t["match_status"].startswith("A and B match paper") for t in mine)
        n_c = sum(t["match_status"] != "not computed by A or B" for t in mine)
        n_d = sum(t["match_status"].startswith("A differs") for t in mine)
        tgt_total += n_t; tgt_match += n_m; tgt_computed += n_c; tgt_differs += n_d; tgt_notcomp += n_t - n_c
        # A/B agreement on every target both computed
        ab_ok = True
        for t in mine:
            if t["match_status"] == "not computed by A or B":
                continue
            if "AB_agree" in t:
                ab_ok &= t["AB_agree"].startswith("yes")
            else:
                ab_ok &= rounds_equal(t["A_value"], t["B_value"], t["decimals"] or 0) or t["A_value"] == t["B_value"]
        ca, cb = res[pid]["class_A"], res[pid]["class_B"]
        same_class = ca == cb
        agree_class += same_class
        agree_all += same_class and ab_ok
        lead_differs += same_class and ca != main
        # robustness: agent A, the three pre-registered primary checks
        rr = {}
        for part in r["robustness_A"].split(";"):
            if ":" in part:
                key, val = [x.strip() for x in part.split(":", 1)]
                if key in ("R_a", "R_b", "R_c"):
                    rr[key] = val
        for key in ("R_a", "R_b", "R_c"):
            rob[rr.get(key, "missing")] += 1
        nver = sum(o["paper"] == pid and o["status"] == "verified finding" for o in ob)
        for o in ob:
            if o["paper"] == pid and o["status"] == "verified finding":
                d = o["description"]
                if re.search(r"[Nn]o target|After all target code|no printed number is affected|Labels only", d):
                    touch = "touches no target"
                elif re.search(r"\bT\d\b", d):
                    touch = "mentions a target (see batch report)"
                else:
                    touch = "target effect not stated in the observation record"
                verified.append({"batch": k, "obs_id": o["obs_id"], "paper": pid, "file": o["file"], "line": o["line"],
                                 "effect_type": o["effect_type"], "touch": touch, "description": d})
        rows.append(OrderedDict([
            ("id", pid), ("batch", k), ("title", s["paper_title"]), ("journal", s["journal"]), ("year", s["pub_year"]),
            ("language", s["code_language"]), ("main_class", main), ("alternative_class", alt),
            ("alternative_reason", alt_label), ("targets_matched_both_agents", n_m), ("targets_total", n_t),
            ("targets_computed", n_c), ("agent_class_A", ca), ("agent_class_B", cb),
            ("ab_agree_class", "yes" if same_class else "no"),
            ("ab_agree_every_computed_target", "yes" if ab_ok else "no"),
            ("lead_class_differs_from_agents", "yes" if (same_class and ca != main) else "no"),
            ("robustness_primary_A", "; ".join(f"{x} {rr.get(x, 'missing')}" for x in ("R_a", "R_b", "R_c"))),
            ("verified_code_observations", nver), ("prereg_freeze", freeze[k]),
            ("paper_doi", r["paper_doi"]), ("dataset_doi", r["dataset_doi"]),
        ]))
        alt_by_batch.setdefault(k, []).append((main, alt))

with open("final/all25_results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ------------------------------------------------------------------ counts
main_counts = cnt(r["main_class"] for r in rows)
alt_eff = [r["alternative_class"] for r in rows]
all_alt_n24 = cnt(a for a in alt_eff if a in CLS)
all_alt_n25 = cnt((a if a in CLS else r["main_class"]) for a, r in zip(alt_eff, rows))
per_batch = OrderedDict()
for k in B:
    per_batch[f"batch{k}"] = OrderedDict([
        ("main", cnt(r["main_class"] for r in rows if r["batch"] == k)),
        ("all_alternatives", cnt((r["alternative_class"] if r["alternative_class"] in CLS else None) for r in rows if r["batch"] == k)),
        ("source", f"batches/batch{k}_counts_rule4.json")])
lang = Counter(r["language"] for r in rows)
counts = OrderedDict([
    ("_note", "Generated by scripts/make_final.py from the batch files. Counts only; no percentages or rates (n = 25)."),
    ("n_papers", len(rows)),
    ("counts_main", main_counts),
    ("counts_main_excluding_no_target", cnt(r["main_class"] for r in rows if not r["alternative_class"].startswith("excluded"))),
    ("n_main_excluding_no_target", sum(not r["alternative_class"].startswith("excluded") for r in rows)),
    ("counts_all_alternatives", all_alt_n24),
    ("n_all_alternatives", sum(all_alt_n24.values())),
    ("counts_all_alternatives_note", "every paper at its alternative reading at once; 01_5BIH0P's alternative is exclusion (no computational target), so n = 24"),
    ("counts_all_alternatives_keeping_01_as_C", all_alt_n25),
    ("n_all_alternatives_keeping_01_as_C", sum(all_alt_n25.values())),
    ("papers_with_class_changing_alternative", sum(r["alternative_class"] in CLS and r["alternative_class"] != r["main_class"] for r in rows)),
    ("per_batch", per_batch),
    ("ab_agree_on_class", agree_class),
    ("ab_agree_on_class_and_every_computed_target", agree_all),
    ("papers_with_at_least_one_computed_target", sum(r["targets_computed"] > 0 for r in rows)),
    ("lead_final_class_differs_from_joint_agent_proposal", lead_differs),
    ("targets_total", tgt_total),
    ("targets_computed_by_both", tgt_computed),
    ("targets_matched_by_both", tgt_match),
    ("targets_computed_not_matching", tgt_differs),
    ("targets_not_computed", tgt_notcomp),
    ("code_observations_total", sum(obs_status.values())),
    ("code_observations_verified", obs_status["verified finding"]),
    ("code_observations_unverified", obs_status["unverified agent observation"]),
    ("code_observations_out_of_scope", obs_status["out of scope: not reproducibility"]),
    ("verified_observations_touching_no_target", sum(v["touch"] == "touches no target" for v in verified)),
    ("robustness_primary_checks_agent_A", OrderedDict([("kept_direction_and_significance", rob["same"]),
                                                       ("did_not_keep", rob["differs"]), ("not_run", rob["not run"]),
                                                       ("not_applicable", rob["n/a"]), ("missing", rob["missing"])])),
    ("robustness_conclusions_differing_between_agents", rob_ab_diff),
    ("papers_by_language", OrderedDict(sorted(lang.items(), key=lambda x: x[0], reverse=True))),
])
json.dump(counts, open("final/all25_counts.json", "w", encoding="utf-8"), indent=1)

# ------------------------------------------------------------------ C reasons (each anchored to a quote in its source)
C_REASONS = [
    ("01_5BIH0P", "no computational target", "the paper reports no computed number for this deposit, and the production trajectory the deposit's analyses read is not in the collection",
     "batches/batch1_report.md", "The production trajectory the deposit's analyses read is not in the collection"),
    ("03_3IOGQ8", "missing data location", "the PSM export the notebook reads is not deposited at any location found",
     "batches/batch1_report.md", "The PSM export the code reads is not deposited at any location found."),
    ("04_PSHE5L", "missing data location", "the article has no data statement and cites no external location; the deposit is one R script (data found by the audit on an uncited OSF page)",
     "batches/batch1_report.md", "the article has no data statement and cites no external location; the deposit is one R script."),
    ("06_VSV5DM", "p-only mismatch", "every estimate matches; the pre-registered AME p-value does not reproduce the printed value, in the same 0.05 to 0.10 band",
     "batches/batch2_report.md", "T4, the p-value of the T1 effect, was pre-registered as the delta-method AME p"),
    ("08_SQRZR8", "N-only mismatch", "all five Table 3 coefficients match; the code cannot produce the printed N in the Table 3 note",
     "batches/batch2_report.md", "every model in both runs uses 4507 rows"),
    ("09_4U8CTG", "data behind registration", "Study 2 targets match; the Study 1 inputs sit behind ELIPSS registration, so Study 1 targets were not run",
     "batches/batch2_report.md", "Study 1 targets T5 and T6 were not run: their inputs sit behind ELIPSS registration"),
    ("10_6MLKJZ", "undocumented sample step", "the deposited code gives a larger general-population total than printed and has no step that removes the extra respondents",
     "batches/batch2_report.md", "the deposited code has no step that removes the extra respondents"),
    ("20_SINIYU", "missing code", "the one script that computes a paper number imports a module that is not deposited, and no deposited code computes Table 1",
     "batches/batch4_report.md", "because the module interp_radar is not deposited"),
    ("21_LEFTNE", "N-only mismatch", "every estimate target matches; the Table 3 N reproduces one row larger than printed, as the deposited data hold",
     "batches/batch5_report.md", "T6, the Table 3 N, is 698 in both runs"),
]
c_ids = [r["id"] for r in rows if r["main_class"] == "C"]
assert [x[0] for x in C_REASONS] == c_ids, (c_ids, [x[0] for x in C_REASONS])
for pid, cat, _, src, q in C_REASONS:
    assert q in open(src, encoding="utf-8").read(), (pid, q)
c_cat = Counter(x[1] for x in C_REASONS)

# ------------------------------------------------------------------ method changes (anchored to CHANGELOG headings)
chg = open("CHANGELOG_METHOD.md", encoding="utf-8").read()
heads = re.findall(r"^## (\d{4}-\d\d-\d\d) #(\d+) \((.+?)\)$", chg, re.M)
SUMMARY = {
    "1": "frame restricted to datasets hosted on Harvard Dataverse (DOI prefix 10.7910)",
    "2": "article DOIs looked up on Crossref by title when Dataverse lists none; failed lookups stop the script instead of counting as ineligible",
    "3": "PROTOCOL.md restored verbatim after a sandbox recycle; runs moved to Debian system R",
    "4": "materials rule (deposit plus locations the article's own data statement names); no-computational-target label; clock deviations; verified versus unverified code observations; exploratory checks labelled",
    "5": "scripted absence searches; number checks; status notes on agent logs; pre-registration hashes pushed before runs from batch 2 on",
    "6": "N-only or p-only mismatch with every estimate matching is C, not D (6a); fixest 0.12.1 accepted as an environment fix for 07_JH9DBC (6b); setup script fix (6c)",
}
assert [h[1] for h in heads] == list(SUMMARY), heads

nonmatch = []
for k in B:
    for t in rcsv(f"batches/batch{k}_targets.csv"):
        if t["row_type"] == "paper target" and t["match_status"].startswith("A differs"):
            nonmatch.append(f"{t['paper']} {t['target_id']}")
counts["c_reason_types"] = OrderedDict(sorted(c_cat.items()))
counts["computed_targets_not_matching"] = nonmatch
json.dump(counts, open("final/all25_counts.json", "w", encoding="utf-8"), indent=1)

# ------------------------------------------------------------------ report
L = []
a = L.append
mc = main_counts
fmt = lambda c: ", ".join(f"{k} {c[k]}" for k in CLS)
a("# Reproducibility audit of 25 papers: final report (v1.0)")
a("")
a("Audit by Gaurang Kumar (@hapybeing). Analysis carried out with Hark. Generated by `scripts/make_final.py` from the published batch files; "
  "every number is checked against its source file by `scripts/check_final_numbers.py` (`final/FINAL_number_check.txt`). Counts only: n = 25 is small, so no rates are given.")
a("")
a("## Summary")
a(f"Twenty-five papers were drawn at random from 2023 to 2026 Harvard Dataverse deposits that contain R or Python code (SELECTION.md), and each was re-run from the authors' deposited materials by two blind agent runs against pre-registered targets. "
  f"Main counts: {fmt(mc)} (n = {len(rows)}; final/all25_counts.json). "
  f"With every paper's alternative reading at once: {fmt(all_alt_n24)} (n = {sum(all_alt_n24.values())}, one paper's alternative being exclusion; final/all25_counts.json). "
  f"Both agent runs proposed the same class for {agree_class} of {len(rows)} papers and agreed on every target value both computed in {agree_all} ({counts['papers_with_at_least_one_computed_target']} papers had at least one computed target; final/all25_counts.json). "
  f"Of {tgt_total} pre-registered targets, {tgt_computed} could be computed and {tgt_match} matched the paper at its printed rounding in both runs (final/all25_counts.json). "
  f"No paper is class D under the main reading. Class C means a paper could not be fully checked from the materials as deposited; it does not mean the paper is wrong.")
a("")
a("## What the classes mean (PROTOCOL.md section 7)")
proto = open("PROTOCOL.md", encoding="utf-8").read()
for k in CLS:
    m = re.search(rf"^- {k}: (.+)$", proto, re.M)
    a(f"- {k}: {m.group(1)}")
a("- Robustness outcomes are reported separately and never change the class. The materials rule (CHANGELOG_METHOD.md #4): the deposit plus every location the article's own data statement names; locations the audit found itself give only an alternative class.")
a("")
a("## How the papers were drawn (SELECTION.md)")
selmd = open("SELECTION.md", encoding="utf-8").read()
fr = re.search(r"Frame size: \*\*(\d+)\*\*", selmd).group(1)
hv = re.search(r"Harvard-hosted subset .*?\*\*(\d+)\*\*", selmd).group(1)
sc = re.search(r"\*\*(\d+)\*\* datasets screened", selmd).group(1)
a(f"- Frame: every Harvard Dataverse dataset released 2023-01-01 to 2026-12-31 with at least one R or Python code file, {fr} datasets, of which {hv} are hosted at Harvard (SELECTION.md).")
a("- Random order: Harvard-hosted rows sorted by dataset DOI and permuted with numpy `default_rng(20261009)`; seed 20261009 (SELECTION.md).")
a(f"- Screening in random order until 25 were eligible: {sc} screened (SELECTION.md). Eligibility E1 to E6: one peer-reviewed journal article with a DOI published 2023 to 2026, openly readable article text, no restricted files, no Stata, MATLAB, SPSS or SAS code, at most 5 GB, licence allows use (PROTOCOL.md section 3).")
a("- Data presence was not an eligibility criterion, so the sample is papers whose Dataverse deposit contains R or Python code, not papers with open data and code (SELECTION.md).")
a("")
a("## Method")
a("- Two agent runs per paper: agent A and a blind agent B in a separate folder, given only the paper DOI, dataset DOI and PREREG.md. Both use the same underlying model family, so they are not independent human replications (PROTOCOL.md).")
a("- Pre-registration: targets copied from each paper and three robustness checks were frozen and hashed before any run. Batch 1 was frozen locally and first published with its results (self-attested); batches 2 to 5 were pushed and announced in GitHub issues #1 to #4 before any run (CHANGELOG_METHOD.md).")
a("- Three pre-registered robustness checks per paper: (a) another seed or bootstrap resample, (b) excluding extreme outliers, (c) one alternative reasonable analysis choice (PROTOCOL.md).")
a("- Code review: only observations with file and line, a saved output change or data fact, and detection by both agents count as verified; the rest are unverified agent observations and are not findings (CHANGELOG_METHOD.md #4d).")
a("- Classes were set by the lead from saved outputs after both agents reported, using pre-run class decisions for each batch; every alternative reading is reported.")
a("")
a("## Results (final/all25_results.csv)")
a("Targets: matched by both agents out of all pre-registered targets for that paper. A/B agree: same class proposed and every target value both computed agrees.")
a("")
a("| Paper | Batch | Title (journal, year) | Lang. | Class | Alternative | Targets matched / total | A/B agree | Verified obs. | Pre-registration freeze |")
a("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    agree = "yes" if (r["ab_agree_class"] == "yes" and r["ab_agree_every_computed_target"] == "yes") else "no"
    alt = r["alternative_class"] if r["alternative_class"] != r["main_class"] else "none"
    fz = re.sub(r", frozen .*$", "", r["prereg_freeze"]) if r["batch"] > 1 else "self-attested local freeze"
    a(f"| {r['id']} | {r['batch']} | {r['title']} ({r['journal']}, {r['year']}) | {r['language']} | {r['main_class']} | {alt} | "
      f"{r['targets_matched_both_agents']} / {r['targets_total']} | {agree} | {r['verified_code_observations']} | {fz} |")
a("")
a("Counts by batch (main; all alternatives at once), from final/all25_counts.json:")
for k in B:
    pb = per_batch[f"batch{k}"]
    a(f"- Batch {k}: main {fmt(pb['main'])}; all alternatives {fmt(pb['all_alternatives'])} (batches/batch{k}_counts_rule4.json, final/all25_counts.json)")
a(f"- Main counts excluding 01_5BIH0P (no computational target): {fmt(counts['counts_main_excluding_no_target'])} (n = {counts['n_main_excluding_no_target']}; final/all25_counts.json)")
a(f"- All alternatives at once but keeping 01_5BIH0P as C: {fmt(all_alt_n25)} (n = {sum(all_alt_n25.values())}; final/all25_counts.json)")
a(f"- Papers by code language: " + ", ".join(f"{k} {v}" for k, v in counts["papers_by_language"].items()) + " (final/all25_counts.json)")
a("")
a("## Why each class C paper is C")
a("One line per paper, from its batch report. Reason types: " + ", ".join(f"{k} {v}" for k, v in sorted(c_cat.items())) + " (final/all25_counts.json).")
a("")
for pid, cat, txt, src, _ in C_REASONS:
    a(f"- {pid} ({cat}): {txt} ({src}).")
a("")
a("## Alternatives (final/all25_results.csv)")
a(f"{counts['papers_with_class_changing_alternative']} papers have an alternative reading that changes the class, and 01_5BIH0P's alternative is exclusion (final/all25_counts.json).")
a("")
a("| Paper | Main | Alternative | Reading |")
a("|---|---|---|---|")
for r in rows:
    if r["alternative_class"] != r["main_class"]:
        a(f"| {r['id']} | {r['main_class']} | {r['alternative_class']} | {r['alternative_reason']} |")
a("")
a("## Agreement between the two runs (final/all25_counts.json)")
a(f"- Same class proposed by both agents: {agree_class} of {len(rows)} papers. Same class and every target value both computed agrees: {agree_all} of {len(rows)}; {counts['papers_with_at_least_one_computed_target']} papers had at least one computed target (final/all25_counts.json).")
a(f"- The lead's final class differs from the joint agent proposal in {lead_differs} papers: " + " and ".join(f"{r['id']} (agents {r['agent_class_A']}, final {r['main_class']})" for r in rows if r["lead_class_differs_from_agents"] == "yes") + "; 04_PSHE5L under the materials rule (CHANGELOG_METHOD.md #4), 08_SQRZR8 under CHANGELOG_METHOD.md #6a (final/all25_results.csv).")
a(f"- Robustness conclusions that differ between agents on a check both ran: {rob_ab_diff} (final/all25_counts.json, from the ab_flags column of batches/batch1_results.csv to batches/batch5_results.csv).")
a("")
a("## Targets (final/all25_counts.json)")
a(f"- {tgt_total} pre-registered targets in total; {tgt_computed} computed by both agents; {tgt_match} matched the paper at its printed rounding in both runs; {tgt_differs} computed but not matching; {tgt_notcomp} not computed (final/all25_counts.json).")
a("- The computed targets that do not match: " + ", ".join(nonmatch) + " (batches/batch2_targets.csv, batches/batch5_targets.csv); details in each batch's targets table.")
a("")
a("## Robustness summary (final/all25_counts.json)")
rp = counts["robustness_primary_checks_agent_A"]
a(f"- Agent A's three pre-registered primary checks over 25 papers: kept the paper's direction and significance {rp['kept_direction_and_significance']}, did not keep {rp['did_not_keep']}, not run {rp['not_run']}, not applicable {rp['not_applicable']} (final/all25_counts.json, from the robustness_A column of batches/batch1_results_rule4.csv to batches/batch5_results_rule4.csv).")
a("- Checks are not run where no target could be computed (03_3IOGQ8, 20_SINIYU) and not applicable where the paper has no computational target (01_5BIH0P). Secondary quantities and per-check values are in each batch report; robustness never changes a class.")
a("")
a("## Verified code observations")
a(f"{obs_status['verified finding']} verified, {obs_status['unverified agent observation']} unverified agent observations (not findings), {obs_status['out of scope: not reproducibility']} out of scope, {sum(obs_status.values())} logged in total (final/all25_counts.json). The target column below is read from each observation record by keyword; 'touches no target' applies to {counts['verified_observations_touching_no_target']} of them (final/all25_counts.json).")
a("")
a("| Obs. | Paper | File | Line | Target | Note |")
a("|---|---|---|---|---|---|")
SHORT = {
    "01-1": "CSV header parser also matches the GROMACS subtitle line; labels only",
    "01-2": "first column labelled picoseconds for tables made in nanoseconds; labels only",
    "02-3": "state-year frame ends at the current year minus 1, so results drift with the run date",
    "05-1": "SDO index averages items with their reversed copies, so items 1 and 3 cancel",
    "05-3": "bare dash separator stops a top-to-bottom run, after all target code",
    "05-4": "correlation refers to columns created later in the script, after all target code",
    "09-1": "fixed label vector puts other rows' p-values on three rows of supplement Tables D8 and D9",
    "10-1": "many-to-many join of balancing weights duplicates matched respondents' rows",
    "13-1": "footnote 20 probit models pass a weight column that does not exist, so they run unweighted",
    "18-1": "benchmark rows paired by position although files are in different docid orders",
    "18-2": "undergraduate AUC, recall and F1 computed from GPT 4 Turbo matrices",
    "19-1": "main-text script uses a column created only in the appendix script",
    "21-1": "Study 2 table tabulates partisanship from the Study 1 data",
    "22-1": "group means computed on an ordered factor return NA; typed constants shown instead, equal to the data",
    "24-1": "Table 1 says year fixed effects while its models use a linear year term",
}
assert set(SHORT) == {v["obs_id"] for v in verified}, sorted(v["obs_id"] for v in verified)
for v in verified:
    a(f"| {v['obs_id']} | {v['paper']} | `{v['file']}` | {v['line']} | {v['touch']} | {SHORT[v['obs_id']]} |")
a("")
a("Full descriptions and evidence files: batches/batch1_code_observations.csv to batches/batch5_code_observations.csv.")
a("")
a("## Method changes (CHANGELOG_METHOD.md)")
for d, n, when in heads:
    a(f"- {d}, #{n} ({when}): {SUMMARY[n]}.")
a("")
a("## Limitations")
a(f"- Small sample: n = {len(rows)} papers from one repository (Harvard Dataverse), and only deposits with R or Python code. The counts support no rate claims about any journal, field or repository (final/all25_counts.json).")
a("- Agent runs, not human replications: A and B share no context but use the same underlying model family, so they can share blind spots (PROTOCOL.md).")
a("- Version substitutions: runs used R 4.5 and, where no versions were pinned, current package releases. Some pinned packages did not build or load, so pre-registered fallbacks or system versions were used (14_CJISMY, 17_T1NXVQ, 25_914AN0), and for 07_JH9DBC the package version of record was chosen after seeing current-version output (batches/batch2_report.md, batches/batch3_report.md, batches/batch4_report.md, batches/batch5_report.md).")
a("- Reduced bootstraps: 17_T1NXVQ significance uses a pre-registered reduced bootstrap with the authors' seeds instead of the full bootstrap (batches/batch4_report.md).")
a("- Target-blocks-only runs and fallbacks: 24_U9CKK6 and 25_914AN0 ran only the target blocks; 13_DX5T9G used a pre-registered fallback after running out of memory; 19_KH0SQ2 used a pre-registered session driver (batches/batch3_report.md, batches/batch4_report.md, batches/batch5_report.md). 24_U9CKK6, 13_DX5T9G and 19_KH0SQ2 each have an alternative class; 25_914AN0 has no alternative class for its targets (batches/batch5_report.md).")
a("- Sandbox restarts interrupted some runs in batches 4 and 5, and a sandbox recycle before the batch 1 runs removed the R environment and PROTOCOL.md, which was restored verbatim (CHANGELOG_METHOD.md #3). Every reported number comes from a process that completed (batches/batch4_report.md, batches/batch5_report.md).")
a("- Batch 1 pre-registration ordering is self-attested: hashes were frozen locally before the runs but first published with the results (CHANGELOG_METHOD.md #5e).")
a("- Post-results reading: CHANGELOG_METHOD.md #6a (an N-only or p-only mismatch with every estimate matching is C, not D) was written after the batch 2 results; counts are shown both ways in batches/batch2_counts_rule4.json, and it also sets the main class of 21_LEFTNE in batch 5, where it was a pre-run decision.")
a("- Some paper values were read from supplements through viewers or screenshots because publishers block scripted downloads; each case is in its batch report. Absence searches show absence only within what they searched.")
a("- No author was contacted. A class C or an alternative C or E means the paper could not be fully checked from the materials as deposited under that reading; it is not a judgement of the research.")
a("- Batch 2 freeze file check in the public repository: CHANGELOG_METHOD.md was extended with a later entry after the batch 2 results (the frozen text is still the unchanged start of the file), and the third-party page images and texts listed in batches/batch2_publish_exclusions.tsv are kept out of the public repository, so those files cannot be re-hashed here. Batches 3 to 5 re-hash fully. Details: final/FINAL_prereg_hash_check.txt.")
a("")
a("## Links")
for k in B:
    a(f"- Batch {k} report: {GH}/blob/main/batches/batch{k}_report.md")
for i in range(1, 5):
    a(f"- Pre-registration freeze for batch {i + 1}: {GH}/issues/{i}")
a(f"- Repository: {GH}")
a("- v1.0 snapshot of this repository: see README.md (Google Drive link with size and SHA-256) and https://github.com/hapybeing/repro-audit-2026/releases/tag/v1.0")
a("")
a("Credit: Gaurang Kumar (@hapybeing). Analysis carried out with Hark.")
rep = "\n".join(L) + "\n"
assert "\u2014" not in rep and "%" not in rep.replace("within 5%", ""), "em dash or percent sign in report (the only allowed one is the 5% tolerance in the class B definition)"
open("final/FINAL_REPORT.md", "w", encoding="utf-8").write(rep)
shutil.copyfile("final/FINAL_REPORT.md", "FINAL_REPORT.md")
print("main", dict(main_counts), "all_alt", dict(all_alt_n24), "agree", agree_class, agree_all, "targets", tgt_match, tgt_total)
