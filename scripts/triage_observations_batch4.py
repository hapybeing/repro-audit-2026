"""Triage of code observations logged by agents A and B on batch 4 (papers 16-20). Same design and status rule as
scripts/triage_observations_batch3.py (copied from it; only the tables below and the file names differ); batch 1 to 3
files are not touched. Batch 4 agents also logged items under results.json "code_observations_unverified" (20_SINIYU);
those are matched as notes with an asserted quote, like any other note.

Writes:
  batches/batch4_code_observations.csv           one row per distinct code observation (A and B items matched)
  batches/batch4_code_observations_excluded.csv  items agents logged that are NOT code observations, with the reason
  batches/batch4_code_observations_counts.json   counts, all computed from the rows above

Hand-coded here (and only this): the MATCHING TABLE below, a neutral one-line description, the output files each agent
cited, whether PREREG.md pre-flagged the issue, and, where the mechanical rule would allow "verified finding" but the
item cannot be shown to be an unintended behaviour of the code, a written reason that keeps it "unverified agent
observation" (key intent_open). Checked from files: as in the batch 2 script (issue-list entries mapped exactly once,
quotes asserted, PREREG pre-flags asserted, cited files exist, line numbers checked against the deposited code whose
sha256 is in PREREG.md when the scratch copy under /workspace/audit_runs/ is present).

Status rule (CHANGELOG_METHOD #4d, as for batches 1 and 2):
  "verified finding"                  file + line, a demonstrated output change (or data fact) saved in an output file,
                                      AND both agents found it (independently, or, where PREREG.md pre-flagged it, each
                                      agent demonstrated it in its own saved output), AND the behaviour is shown to be
                                      unintended (for example a column that does not exist);
  "unverified agent observation"      any other code / reproducibility observation, including items whose intent is open;
  "out of scope: not reproducibility" text-versus-code descriptions where the code reproduces the reported number.
Usage: python3 scripts/triage_observations_batch4.py
"""
import csv, json, os, re, sys, hashlib
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {"16": "16_QZNVZ0", "17": "17_T1NXVQ", "18": "18_YXC5K5", "19": "19_KH0SQ2", "20": "20_SINIYU"}


def rj(pid, ag):
    return json.load(open(f"{REPO}/papers/{P[pid]}/{ag}/results.json"))


def norm(s):
    return re.sub(r"\s+", " ", s)


def assert_quote(path, quote):
    full = f"{REPO}/{path}"
    txt = open(full, encoding="utf-8").read()
    if path.endswith(".json"):
        try:
            txt = txt + "\n" + json.dumps(json.load(open(full)), ensure_ascii=False)
        except Exception:
            pass
    if norm(quote) not in norm(txt):
        sys.exit(f"QUOTE NOT FOUND in {path}: {quote!r}")
    return path


def rjp(pid, ag):
    return f"papers/{P[pid]}/{ag}/results.json"


ISSUES = [
    # ---------------- 16_QZNVZ0 ----------------
    dict(id="16-1", pid="16",
         desc="The model_3 regressor list in cell 6 of Regression.ipynb has no FA_South, while Models 1, 2 and 4 include it; Table 2 prints no Region = South estimate for Model 3. A's data check shows FA_South takes a single value in the Top10 first-author rows, which would make it collinear with the constant there. No target is affected.",
         sources=[("note", "A", "papers/16_QZNVZ0/A/results.json", "Model 3 omits FA_South from its regressor list (notebook cell 6)", "cell 6"),
                  ("note", "B", "papers/16_QZNVZ0/B/results.json", "Model 3 regressor list has no FA_South (Regression.ipynb cell 6)", "cell 6")],
         file="Regression.ipynb", outputs={}, effect="none",
         evidence={"A": ["A/outputs/code_checks.json"]},
         prereg="the notebook's model_3 regressor list omits `FA_South`"),
    dict(id="16-2", pid="16",
         desc="Model 2 (team-based regressors) keeps the rows with non-missing FA_Ethnicity, the first-author variable, the same row filter as Model 1. Model 2 has 39,690 rows in the run. Impact not tested; no target is affected.",
         sources=[("note", "A", "papers/16_QZNVZ0/A/results.json", "Model 2 row filter uses the first-author FA_Ethnicity variable", "")],
         file="Regression.ipynb", outputs={}, effect="none",
         prereg="Model 2 (team-based) is filtered on non-missing `FA_Ethnicity` (first-author variable)"),
    # ---------------- 18_YXC5K5 ----------------
    dict(id="18-1", pid="18",
         desc="The author benchmark pi (read at line 102, de-duplicated at line 108) keeps the file's unsorted docid order, while every model file and the undergraduate files are sorted by docid; the Hamming loss, F1, recall, precision, AUC and ICC functions pair rows by position, so 588 of 589 rows compare different articles. Pairing by docid (R_c) gives the false positive and false negative counts printed in supplement Table A5 (369 and 150) and a Hamming loss of 0.110 for GPT 4o Few Shot 8 labels, against 0.182 as deposited. The printed Table A1 values are the ones the deposited code gives (T1 to T6 match). The ranking and direction claims hold under both pairings.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/row_pairing_confusion_counts.csv", "A/outputs/targets_extracted.csv", "A/outputs/R_c_targets_extracted.csv"],
                  "B": ["B/outputs/checks.csv", "B/outputs/R_c_targets_extracted.csv"]},
         effect="numeric", prereg="lists its 589 docids in a non-sorted order",
         codecheck=("/workspace/audit_runs/18_YXC5K5/prereg/deposit/Benchmarking_DataAnalysis.Rmd",
                    "520d59d1015f6fe81f0240a8b42fdc714c5496c017bf5d9008a4d2bec126a4f7", 108, "distinct(docid, .keep_all = T)", "utf-8")),
    dict(id="18-2", pid="18",
         desc="undergrads8 (lines 2050 to 2056) and undergrads4 (lines 2058 to 2064), labelled as the undergraduate metrics for Table A1, compute AUC, Recall and F1 from gpt10mat and gpt4mat (GPT 4 Turbo Zero Shot output) instead of the undergraduate matrices; only their Hamming Loss and % 1s use the undergraduate matrices. The Table A1 undergraduate AUC, Recall and F1 therefore equal the GPT 4 Turbo Zero Shot rows. T2 (Hamming Loss) is not affected.",
         sources=[("issue_list", "A", 1), ("issue_list", "B", 1)],
         outputs={"A": ["A/outputs/undergrad_row_check.csv"], "B": ["B/outputs/checks.csv"]},
         effect="numeric", prereg="compute AUC, Recall and F1 from `gpt10mat` / `gpt4mat`",
         codecheck=("/workspace/audit_runs/18_YXC5K5/prereg/deposit/Benchmarking_DataAnalysis.Rmd",
                    "520d59d1015f6fe81f0240a8b42fdc714c5496c017bf5d9008a4d2bec126a4f7", 2051, "calculate_auc(actual_list_10mat, gpt10mat)", "utf-8")),
    # ---------------- 19_KH0SQ2 ----------------
    dict(id="19-1", pid="19",
         desc="Line 835 of main_text_figs_JEPP_FINAL.R (and line 865 for France) converts a column Treatment2 that is not in all_merged.RData and is not created in this script (it is created only in Appendix_plus.R lines 1278 and 1286). Run as deposited, the script stops at line 835 with 'replacement has 0 rows, data has 1734', so the Figure 7 list-experiment section is not produced by the main-text script alone. No target is affected.",
         sources=[("issue_list", "A", 0),
                  ("note", "B", "papers/19_KH0SQ2/B/results.json", "column Treatment2 is not in all_merged.RData and is created only in Appendix_plus.R l.1278/1286", "835")],
         file="main_text_figs_JEPP_FINAL.R",
         outputs={"A": ["A/outputs/main_text_status.txt"], "B": ["B/outputs/main_text_status.txt"]}, effect="runtime_error",
         codecheck=("/workspace/audit_runs/19_KH0SQ2/prereg/deposit/main_text_figs_JEPP_FINAL.R",
                    "4352209547dbc51634b7cc4ace17c21af8e60abd1c39779a27d1c5bd85331301", 835, "subset_uk$Treatment2<-as.factor(subset_uk$Treatment2)", "utf-8")),
    dict(id="19-2", pid="19",
         desc="The article's descriptive sample sizes (UK 1,708, France 969) are not the country counts in all_merged.RData (UK 1734, France 1038); they equal the n of the first UK and France conjoint models in main_text_figs_JEPP_FINAL.R (lines 639 and 670), which may be where they come from. The Table S1 and S10 targets, including their Ns, reproduce.",
         sources=[("note", "A", "papers/19_KH0SQ2/A/results.json", "the paper text gives UK N = 1,708, France N = 969, combined 2677 (not targets)", ""),
                  ("note", "B", "papers/19_KH0SQ2/B/results.json", "This may be where the article's Ns come from (respondents with a conjoint rating), but the article does not say so.", "639; 670")],
         file="main_text_figs_JEPP_FINAL.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/descriptive_country_counts.csv"], "B": ["B/outputs/descriptive_counts.csv", "B/outputs/conjoint_model_n.csv"]},
         out_of_scope=True,
         oos_reason="Text description of sample sizes versus the data's country counts; not a target, and every Table S1 and S10 target reproduces."),
    # ---------------- 20_SINIYU ----------------
    dict(id="20-1", pid="20",
         desc="Line 419 of codes/figure6/O_B_Ku.py sets radar_Z_out to NaN where it exceeds 6000 m; line 420 then tests radar_Z_out > 6000 again to mask obs_mesh_meso, which is False for NaN, so line 420 masks no cell. Whether the 6000 m cut still acts depends on the module interp_radar, which is not deposited. Shown on a toy array only; effect on T1 and T2 not measurable.",
         sources=[("note", "A", "papers/20_SINIYU/A/results.json", "line 420 then tests radar_Z_out>6000. to mask obs_mesh_meso, which is False for NaN, so line 420 masks nothing", "420"),
                  ("note", "B", "papers/20_SINIYU/B/results.json", "line 420 then tests radar_Z_out>6000. to mask obs_mesh_meso, which is False for NaN, so line 420 masks no cells", "419-420")],
         file="codes/figure6/O_B_Ku.py", outputs={}, effect="none",
         evidence={"A": ["A/outputs/code_observation_checks.json"], "B": ["B/outputs/code_observation_demo.json"]},
         prereg="after line 419 those cells are NaN, so line 420 masks nothing",
         codecheck=("/workspace/audit_runs/20_SINIYU/A/run/figure6/O_B_Ku.py",
                    "8f98a5072b1d5e1fb087ecabe3d87a35c7ff754bc4a0e7baefa2fa0744153713", 420, "obs_mesh_meso[radar_Z_out>6000.]=np.nan", "utf-8")),
    dict(id="20-2", pid="20",
         desc="Line 344 of codes/figure6/O_B_Ku.py sets the simulated value to 0 where ZH < 0; line 345 then overwrites it with ZH/Rvar, so the clip has no effect (the same pattern is in 1DVAR.py lines 311 to 312). Values below 18 are set to missing later (line 480), so any effect would act only through the interpolation, which cannot be run. Shown on a toy array or the swath file only; effect on T1 and T2 not measurable.",
         sources=[("note", "A", "papers/20_SINIYU/A/results.json", "line 345 overwrites B_value with raw ZH/Rvar, so the clip has no effect", "344-345"),
                  ("note", "B", "papers/20_SINIYU/B/results.json", "line 345 overwrites B_value with B_ds['ZH']/Rvar, so the clip has no effect", "345")],
         file="codes/figure6/O_B_Ku.py", outputs={}, effect="none",
         evidence={"A": ["A/outputs/code_observation_checks.json"], "B": ["B/outputs/code_observation_demo.json"]},
         codecheck=("/workspace/audit_runs/20_SINIYU/A/run/figure6/O_B_Ku.py",
                    "8f98a5072b1d5e1fb087ecabe3d87a35c7ff754bc4a0e7baefa2fa0744153713", 345, "B_value=B_ds['ZH']/Rvar", "utf-8")),
]

EXCLUDED = [
    ("16", "A and B", "Notebook cells run verbatim as a script with an appended output-only extraction block", "environment fix (pre-registered route); no author line changed",
     "papers/16_QZNVZ0/B/results.json", "the 13 notebook cells were run verbatim as a script"),
    ("16", "A and B", "Current pandas 3.0.6, numpy 2.5.3 and statsmodels 0.15.0 used; the authors recorded no versions", "package-version environment note; B shows every coefficient equals the authors' saved notebook output",
     "papers/16_QZNVZ0/B/results.json", "Packages are current releases"),
    ("16", "A and B", "Table 2 prints 68,558 as the Model 2 N; the run and the authors' saved notebook output give 39,690 (PREREG inconsistency 1)", "printed non-target number; reported in the per-paper section of the batch report, not a code observation",
     "papers/16_QZNVZ0/A/results.json", "Model 2 N in this run is 39690"),
    ("16", "A", "Model 2 Team_Other and Team_South t values versus the single printed t -2.7 (PREREG inconsistency 2)", "printed non-target number, not a code observation",
     "papers/16_QZNVZ0/A/results.json", "Model 2 Team_Other t -0.37 and Team_South t -2.65"),
    ("16", "A", "Significance stars on five non-target cells differ from the run's p-values (PREREG inconsistency 3)", "difference in significance marks only on non-target cells, not a code observation",
     "papers/16_QZNVZ0/A/results.json", "Stars vs this run (nonrobust p)"),
    ("16", "A and B", "Code that builds the regression table from the raw Web of Science records is not deposited", "materials scope note recorded in DATA_STATEMENT.md; the targets depend only on the deposited table",
     "papers/16_QZNVZ0/A/results.json", "The regression table cannot be rebuilt from raw Web of Science records"),
    ("16", "A and B", "Runs killed for memory (exit 137) on the shared machine before a run completed", "process note; no reported number comes from a killed run",
     "papers/16_QZNVZ0/A/results.json", "Runs were OOM-killed twice (exit 137)"),
    ("17", "A and B", "library(rgeos) and library(rgdal) removed; archived versions fail to build", "pre-registered environment fix (E3); not on the Table 1 path",
     "papers/17_T1NXVQ/A/results.json", "library(rgeos)/library(rgdal) removed"),
    ("17", "A and B", "Pinned igraph 1.4.1 and reticulate 1.28 unusable; Debian igraph 2.1.4 and reticulate 1.41.0.1 used", "package-version environment note; reproduced bootstrap draws equal the deposited draws for the same seeds",
     "papers/17_T1NXVQ/B/results.json", "pinned igraph 1.4.1 failed to compile"),
    ("17", "A and B", "Reduced bootstrap (A: K = 4, B: K = 3) instead of 120 draws", "pre-registered timing rule and pre-run decision #3; alternative class E shown in batches/batch4_class_rules.json",
     "papers/17_T1NXVQ/A/results.json", "Reduced bootstrap: K = 4 draws per seed set"),
    ("17", "A and B", "Sandbox restarted twice during each run", "process note; every reported number comes from a process that completed",
     "papers/17_T1NXVQ/B/results.json", "The sandbox restarted twice during the run"),
    ("17", "B", "maxLik::stdEr returned NA in B's extraction of the two main fits", "extraction note on the audit's script; not used for any target",
     "papers/17_T1NXVQ/B/results.json", "maxLik::stdEr returned NA in the extraction"),
    ("17", "A", "The Gaussian penalty also applies to the constant", "design remark on the estimator (the agent wrote 'design'), not a reproducibility or code observation",
     "papers/17_T1NXVQ/A/results.json", "the Gaussian penalty sum(beta^2)/(2*sigma2) also applies to the Constant"),
    ("17", "B", "Workspace change notices showed some A file names to B", "process note on blinding; no A file was opened",
     "papers/17_T1NXVQ/B/results.json", "Process note: the workspace tool echoed names"),
    ("18", "A and B", "Script's undergraduate '% 1s' is 9.72 (as a share 0.0972) where Table A1 prints 9.68", "printed non-target number, not a code observation",
     "papers/18_YXC5K5/A/results.json", "Table A1 prints 9.68 for Undergraduate Coders 8"),
    ("18", "A and B", "Docid-paired undergraduate false positives 256 versus 254 printed in Table A6", "Table A6 comes from Benchmarking_Supplementary.Rmd, which was not run; not a target",
     "papers/18_YXC5K5/A/results.json", "undergraduate FP is 256 vs 254 printed in Table A6"),
    ("18", "B", "Main run killed twice for memory while rendering a plot; the third identical attempt finished", "process note; no code changed between attempts",
     "papers/18_YXC5K5/B/results.json", "The main run was killed twice by the shared machine's memory pressure"),
    ("18", "B", "Theme5 and Theme6 label naming (PREREG inconsistency 3)", "affects per-label plots only, not the pooled targets; not checked further",
     "papers/18_YXC5K5/B/results.json", "Label naming of Theme5/Theme6"),
    ("19", "A and B", "Session driver adds load() of the deposited .RData before Appendix_plus.R lines 892 to 958", "pre-registered environment fix (pre-run decision #2); alternative class C shown in batches/batch4_class_rules.json",
     "papers/19_KH0SQ2/A/results.json", "diffs/Appendix_plus_driver_load.diff: pre-registered driver adds load"),
    ("19", "B", "res1 is reassigned at line 639 of the main-text script, so the cross-check used lines 1 to 364", "note on the audit's cross-check, not a code observation",
     "papers/19_KH0SQ2/B/results.json", "Also res1 (l.325) is reassigned at l.639"),
    ("19", "B", "Workspace change notices showed some A file names to B", "process note on blinding; no A file was opened",
     "papers/19_KH0SQ2/B/results.json", "Tool-generated workspace change notices displayed filenames"),
    ("20", "A and B", "Module interp_radar imported by O_B_Ku.py line 17 is not deposited; no deposited code computes Table 1", "missing material, the basis of class C (pre-run decision #5), recorded in DATA_STATEMENT.md and ABSENCE_SEARCHES.md; not a code observation",
     "papers/20_SINIYU/B/results.json", "No deposited code computes Table 1"),
    ("20", "B", "plt.style.use(['science','no-latex']) raises OSError with SciencePlots 2.2.2 unless scienceplots is imported first", "environment observation (the agent's own label); not reached because line 17 fails first",
     "papers/20_SINIYU/B/results.json", "environment observation, not a bug"),
    ("20", "A and B", "Path-only symlinks for FY3G_PMR.HDF, gep00/postvar.nc and gep00/swath_spaceborn.nc", "pre-registered path-only environment fix (pre-run decision #1)",
     "papers/20_SINIYU/B/results.json", "path-only symlinks"),
]

FIELDS = ["obs_id", "paper", "agents_logged", "logged_as_A", "logged_as_B", "file", "line", "description",
          "effect_type", "demonstrated_output_change", "output_file", "evidence_files_no_output_change",
          "independently_found_by_both", "independence_note", "status", "status_reason"]
DEMO_EFFECTS = {"numeric", "label", "runtime_error", "row_count"}


def main():
    res = {(pid, ag): rj(pid, ag) for pid in P for ag in "AB"}
    used = Counter()
    rows = []
    for it in ISSUES:
        pid = it["pid"]; pdir = f"papers/{P[pid]}"
        files, lines, logged = [], [], OrderedDict()
        for src in it["sources"]:
            if src[0] == "issue_list":
                _, ag, i = src
                b = res[(pid, ag)]["bugs"][i]
                used[(pid, ag, i)] += 1
                files.append(b["file"]); lines.append(str(b["line"]))
                logged.setdefault(ag, set()).add("results.json issue list")
            else:
                _, ag, path, quote, line = src
                assert_quote(path, quote)
                if line: lines.append(line)
                logged.setdefault(ag, set()).add(f"{os.path.basename(path)} (note)")
        if it.get("file"): files.append(it["file"])
        if it.get("line"): lines.append(it["line"])
        fname = next((re.sub(r"\s*\(.*?\)\s*", "", f).strip() for f in files if re.sub(r"\s*\(.*?\)\s*", "", f).strip()), "")
        line_str = "; ".join(OrderedDict.fromkeys(lines))
        agents = [a for a in "AB" if a in logged]
        outs = {ag: [f"{pdir}/{o}" for o in it.get("outputs", {}).get(ag, [])] for ag in "AB"}
        allouts = outs["A"] + outs["B"]
        missing = [o for o in allouts if not os.path.exists(f"{REPO}/{o}")]
        if missing: sys.exit(f"missing output file(s) for {it['id']}: {missing}")
        demo = bool(allouts) and it["effect"] in DEMO_EFFECTS
        demo_both = demo and bool(outs["A"]) and bool(outs["B"])
        ev = [f"{pdir}/{o}" for ag in it.get("evidence", {}) for o in it["evidence"][ag]]
        for e in ev:
            if not os.path.exists(f"{REPO}/{e}"): sys.exit(f"missing evidence file {e}")
        notes = []
        both = len(agents) == 2
        indep = both
        if not both: notes.append("logged by one agent only")
        if it.get("note_extra"): notes.append(it["note_extra"])
        if it.get("prereg"):
            assert_quote(f"{pdir}/PREREG.md", it["prereg"])
            indep = False
            notes.append("pre-flagged in PREREG.md, which both agents received")
        if it.get("codecheck"):
            path, sha, ln, text, enc = it["codecheck"]
            if os.path.exists(path):
                if hashlib.sha256(open(path, "rb").read()).hexdigest() != sha: sys.exit(f"{it['id']}: deposited file hash differs")
                got = open(path, encoding=enc).read().split("\n")[ln - 1]
                if text not in got: sys.exit(f"{it['id']}: line {ln} of deposited file is {got!r}")
                notes.append(f"line {ln} checked against the deposited file (sha256 {sha[:12]}..., as in PREREG.md)")
            else:
                print(f"note: {path} absent; line check for {it['id']} skipped")
        has_fl = bool(fname) and bool(line_str)
        if it.get("out_of_scope"):
            status = "out of scope: not reproducibility"; reason = it["oos_reason"]
        elif it.get("intent_open") and has_fl and demo and both:
            status = "unverified agent observation"; reason = it["intent_open"]
        elif has_fl and demo and indep:
            status = "verified finding"; reason = "file and line given; output change saved; found independently by A and B"
        elif has_fl and demo_both and both:
            status = "verified finding"
            reason = ("file and line given; pre-flagged in PREREG.md for code review, and each agent demonstrated it in its own "
                      "saved output (CHANGELOG_METHOD #4d proof/demonstration route, as batch 1 item 05-1)")
        else:
            status = "unverified agent observation"
            miss = []
            if not has_fl: miss.append("no file+line")
            if not demo: miss.append("no demonstrated output change on study outputs")
            if not both: miss.append("found by one agent only")
            elif not indep and not demo_both: miss.append("not independently found by both agents")
            reason = "; ".join(miss)
        rows.append(OrderedDict(
            obs_id=it["id"], paper=P[pid], agents_logged=" and ".join(agents),
            logged_as_A="; ".join(sorted(logged.get("A", []))) or "not logged",
            logged_as_B="; ".join(sorted(logged.get("B", []))) or "not logged",
            file=fname, line=line_str, description=it["desc"], effect_type=it["effect"],
            demonstrated_output_change="yes" if demo else "no", output_file="; ".join(allouts) if demo else "",
            evidence_files_no_output_change="; ".join(ev),
            independently_found_by_both="yes" if indep else "no", independence_note="; ".join(notes),
            status=status, status_reason=reason))
    for (pid, ag), d in res.items():
        for i in range(len(d.get("bugs", []))):
            if used[(pid, ag, i)] != 1:
                sys.exit(f"issue-list entry {pid} {ag} [{i}] mapped {used[(pid, ag, i)]} times")
    n_entries = sum(len(d.get("bugs", [])) for d in res.values())
    blob = json.dumps(rows)
    if re.search(r"\bbugs?\b", blob, re.I): sys.exit("forbidden word in output text")
    if "\u2014" in blob: sys.exit("em dash in output")
    with open(f"{REPO}/batches/batch4_code_observations.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    ex_rows = []
    for pid, ag, item, reason, path, quote in EXCLUDED:
        assert_quote(path, quote)
        ex_rows.append(OrderedDict(paper=P[pid], agents=ag, item=item, reason_excluded=reason, source_file=path))
    if re.search(r"\bbugs?\b", json.dumps(ex_rows), re.I): sys.exit("forbidden word in excluded output")
    if "\u2014" in json.dumps(ex_rows): sys.exit("em dash in excluded output")
    with open(f"{REPO}/batches/batch4_code_observations_excluded.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(ex_rows[0].keys())); w.writeheader(); w.writerows(ex_rows)
    per = OrderedDict()
    for r in rows:
        per.setdefault(r["paper"], Counter())[r["status"]] += 1
    counts = OrderedDict(
        n_observations=len(rows), n_issue_list_entries_mapped=n_entries,
        issue_list_entries_per_paper={P[pid]: {ag: len(res[(pid, ag)].get("bugs", [])) for ag in "AB"} for pid in P},
        by_status=dict(Counter(r["status"] for r in rows)),
        by_paper_and_status={k: dict(v) for k, v in per.items()},
        logged_by_both=sum(r["agents_logged"] == "A and B" for r in rows),
        independently_found_by_both=sum(r["independently_found_by_both"] == "yes" for r in rows),
        with_demonstrated_output_change=sum(r["demonstrated_output_change"] == "yes" for r in rows),
        n_excluded_items=len(ex_rows))
    json.dump(counts, open(f"{REPO}/batches/batch4_code_observations_counts.json", "w"), indent=1)
    print(json.dumps(counts, indent=1))
    for r in rows: print(r["obs_id"], r["status"], "|", r["status_reason"])


if __name__ == "__main__":
    main()
