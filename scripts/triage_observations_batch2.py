"""Triage of code observations logged by agents A and B on batch 2 (papers 06-10). Same design and status rule as
scripts/triage_observations.py (batch 1); batch 1 files are not touched.

Writes:
  batches/batch2_code_observations.csv           one row per distinct code observation (A and B items matched)
  batches/batch2_code_observations_excluded.csv  items agents logged that are NOT code observations, with the reason
  batches/batch2_code_observations_counts.json   counts, all computed from the rows above

Hand-coded here (and only this): the MATCHING TABLE below (which agent item describes which issue), a neutral one-line
description, the output files each agent cited, and whether PREREG.md pre-flagged the issue. Checked from files:
  - every entry of each results.json issue list (key "bugs") is mapped to exactly one row (asserted);
  - file and line for issue-list entries are read from results.json;
  - items logged outside the issue list (results.json uncertainties, LOG.md) have a verbatim quote asserted in the cited file;
  - PREREG pre-flags are asserted by quoting PREREG.md;
  - cited output files are checked to exist on disk;
  - the line numbers of the two verified items are checked against the deposited code whose sha256 is in PREREG.md
    (copies under /workspace/audit_runs/<pid>/A/dl/; skipped with a printed note if that scratch copy is absent).

Status rule (batch 1 rule, CHANGELOG_METHOD #4d):
  "verified finding"                  file + line given, a demonstrated output change (or data fact) saved in an output file,
                                      AND both agents found it: independently, or, where PREREG.md pre-flagged it for code
                                      review, each agent demonstrated it in its own saved output (the #4d proof/demonstration
                                      route used for batch 1 item 05-1);
  "unverified agent observation"      any other code / reproducibility observation;
  "out of scope: not reproducibility" text-versus-code descriptions or interpretation where the code reproduces the
                                      reported number.
Usage: python3 scripts/triage_observations_batch2.py
"""
import csv, json, os, re, sys, hashlib
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {"06": "06_VSV5DM", "07": "07_JH9DBC", "08": "08_SQRZR8", "09": "09_4U8CTG", "10": "10_6MLKJZ"}


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
    # ---------------- 06_VSV5DM ----------------
    dict(id="06-1", pid="06",
         desc="Detailed race and ethnicity chunk: hard-coded freq vector (line 1094) and group labels with n values (line 1095), e.g. 'Black Men (n=42)', 'Black Women (n=52)', differ from table(by_leg$race_gender) in the deposited data (44, 50); freq gives White Women 102 where the data have 101. Labels only; no model estimate or target uses them.",
         sources=[("issue_list", "B", 0),
                  ("note", "A", rjp("06", "A"), "Unverified observation: purled line 1051 hard-codes White Women freq 102", "")],
         outputs={"B": ["B/outputs/group_counts_check.txt", "B/outputs/meansbyraceandgenderandethnicity.doc"]}, effect="label",
         prereg="hard-codes White Women freq 102 while the label says n=101",
         note_extra="A noted only the freq 102 item from PREREG.md and did not check it against the data"),
    dict(id="06-2", pid="06",
         desc="Article text says expected counts hold other covariates at their means; the code's margins() call computes average marginal effects over observed rows. The reported numbers equal the margins() output.",
         sources=[("note", "A", rjp("06", "A"), "the article says expected counts hold covariates at means; margins() computes average marginal effects over observed rows", "")],
         file="Multivariate Analysis.Rmd", line="521", outputs={}, effect="none",
         prereg="hold[ing] all other covariates at their mean observed values", out_of_scope=True,
         oos_reason="Text versus code description of the method; the code reproduces the reported numbers."),
    dict(id="06-3", pid="06",
         desc="Appendix Tables A14/A15 are titled 'Fractional Logit Regression Models'; the chunk that produces them fits betareg on proportions + 0.00001. Not a target.",
         sources=[("note", "A", rjp("06", "A"), "Tables A14/A15 titled 'Fractional Logit' are produced by betareg on proportions + 0.00001", "")],
         file="Multivariate Analysis.Rmd", line="995-1057", outputs={}, effect="none",
         prereg="Fractional Logit Regression Models", out_of_scope=True,
         oos_reason="Naming of a model in a table title versus the code; no reported number is in question."),
    # ---------------- 07_JH9DBC ----------------
    dict(id="07-1", pid="07",
         desc="replication.R lines 199 to 207 compute the supplement's Table A summaries on the 600-row 2015/2018 data (mean Year 2018 = 0.5), while Table A reports N = 900 and Year 2018 mean 0.33, which match the 900-row dataall. Table A is not a target.",
         sources=[("note", "B", rjp("07", "B"), "replication.R lines 199 to 207 compute Table A summaries on the 600-row data", "199-207")],
         file="replication.R", outputs={"B": ["B/outputs/code_checks.txt"]}, effect="numeric",
         prereg="lines 199 to 207 compute the Table A summaries on `data`"),
    # ---------------- 08_SQRZR8 ----------------
    dict(id="08-1", pid="08",
         desc="main_rep.R sets no seed before the mediation bootstrap (Figure 3), so Figure 3 values are not fixed across runs. No target depends on it; Figure 3 was not compared with the paper.",
         sources=[("note", "A", rjp("08", "A"), "Figure 3 (mediation bootstrap) is not seed-fixed in main_rep.R", ""),
                  ("note", "B", rjp("08", "B"), "The mediation block (Figure 3) ran to completion without a seed", "")],
         file="main_rep.R", outputs={}, effect="none",
         prereg="main_rep.R sets no seed, so Figure 3 (mediation bootstrap) is not seed-fixed"),
    dict(id="08-2", pid="08",
         desc="The data preparation script data_preparation_rep.R named in the deposit ReadMe (raw to cleaned data) is not in the deposit, so the raw-to-cleaned step cannot be rerun; the targets use the deposited cleaned file (papers/08_SQRZR8/ABSENCE_SEARCHES.md).",
         sources=[("note", "B", rjp("08", "B"), "Data preparation script data_preparation_rep.R named in ReadMe.txt is not in the deposit", "")],
         file="data_preparation_rep.R (not deposited)", outputs={}, effect="none",
         prereg="lists a code file `data_preparation_rep.R`"),
    # ---------------- 09_4U8CTG ----------------
    dict(id="09-1", pid="09",
         desc="make_mht_table attaches a fixed label vector (Intercept, In-group Government, In-group Parliament, Out-group Government, Placebo) to summary(model)$coefficients[, 4], whose rows follow the treatment factor levels (control, danger_contr, win_govt, win_mainstream, win_parl). In Tables D8 and D9 the rows labelled In-group Government, In-group Parliament and Placebo carry the p-values of Placebo, In-group Government and In-group Parliament; the Out-group Government row is correct. No target is affected.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/mht_label_check.csv"], "B": ["B/outputs/mht_label_check.csv"]}, effect="label",
         prereg="`make_mht_table` attaches a fixed label vector",
         codecheck=("/workspace/audit_runs/09_4U8CTG/A/dl/replication_scripts/02_supplementary_materials.R",
                    "5aabc10f7ca1f830ba7207cfda178381e2d31372d42c159c4f4050474c043ff2", 1729, 'trt_group  <- c("Intercept", "In-group Government", "In-group Parliament",')),
    dict(id="09-2", pid="09",
         desc="Figures D1 and D4: positional x-axis / fill labels are applied to the treatment levels in alphabetical order, so the win_mainstream bar is labelled In-group Parliament and the win_parl bar Out-group Government. Figure labels only.",
         sources=[("issue_list", "B", 1)],
         outputs={"B": ["B/outputs/figure_label_check.csv"]}, effect="label"),
    dict(id="09-3", pid="09",
         desc="Figure D2 legend: recode_treatment() level order with legend labels c('Control','T1a','T1b','T2','Placebo') names win_parl 'T1a' and win_govt 'T1b', whereas Table A4 defines T1a as In-group Government and T1b as In-group Parliament. Figure legend only.",
         sources=[("issue_list", "B", 2)],
         outputs={"B": ["B/outputs/figure_label_check.csv"]}, effect="label"),
    dict(id="09-4", pid="09",
         desc="Table D3 Model 4 (model_4_ez) controls for income and gender only, while Model 3 uses age, gender, education and income; whether this is intended is not stated. It matches the deposited table.",
         sources=[("note", "A", rjp("09", "A"), "model_4_ez (02 line 294) uses controls income + gender only", "294"),
                  ("note", "B", rjp("09", "B"), "Table D3 Model 4 (model_4_ez, 02 line 294) controls for income and gender only", "294")],
         file="replication_scripts/02_supplementary_materials.R", outputs={}, effect="none"),
    dict(id="09-5", pid="09",
         desc="make_comp_plot labels m_check3 with difficulty_labels[seq_len(n unique values)], which is correct only if the observed values are exactly 1..k; not checked.",
         sources=[("note", "B", rjp("09", "B"), "make_comp_plot (02 lines 751-752) labels m_check3", "751-752")],
         file="replication_scripts/02_supplementary_materials.R", outputs={}, effect="none"),
    dict(id="09-6", pid="09",
         desc="Text p. 15 attributes 90% significance of the LREM effect to the controls plus robust SE specification; the reproduced Model 4 LREM p is 0.107 and Model 2 (robust, no controls) p is 0.058.",
         sources=[("note", "A", rjp("09", "A"), "Text p. 15 attributes the 90% significance of the LREM effect to the controls + robust SE specification", "")],
         outputs={}, effect="none",
         prereg="is statistically significant at a 90% confidence level when controlling", out_of_scope=True,
         oos_reason="Text versus table description; the code reproduces the deposited tables."),
    # ---------------- 10_6MLKJZ ----------------
    dict(id="10-1", pid="10",
         desc="left_join(pooled_df2, ebalw) is many-to-many: ebalw comes from match_data at task 1, which has two rows (profiles) per respondent, so each matched respondent's 16 rows become 32 (87936 rows vs 62112 distinct). pooled_df2 feeds Figures 1-4 and A3-A4; respondents with an NA balance covariate keep 16 rows and so get half the weight. De-duplicated reruns change Figure 1 marginal means by at most 0.0009; figure claims FC1 to FC3 unchanged.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/code_check_join_dedup_fig1.csv", "A/outputs/diag_T3_and_join.json"],
                  "B": ["B/outputs/code_check_dedup_fig1_mm.csv", "B/outputs/code_checks.json"]}, effect="numeric",
         codecheck=("/workspace/audit_runs/10_6MLKJZ/A/dl/Prioritzing_Social_Needs/analysis/03_data_prep_and_merge.R",
                    "761610b6a83502f75b550f9c9709f813aab22fb4e4c135c2352618fc28cbeada", 133, "pooled_df2 <- left_join(pooled_df2,")),
    dict(id="10-2", pid="10",
         desc="Line 98 builds nongerman from v184_ger == 'Ja', but among civic respondents with a sector v184_ger is 'Ja' for exactly the 333 public and 'Nein' for exactly the 1285 private respondents, so the variable may code sector rather than nationality. nongerman enters no estimate.",
         sources=[("note", "A", rjp("10", "A"), "Unverified observation: in 03_data_prep_and_merge.R line 98", "98"),
                  ("note", "B", rjp("10", "B"), "03 line 98 names v184_ger == 'Ja' 'nongerman'", "98")],
         file="Prioritzing_Social_Needs/analysis/03_data_prep_and_merge.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/diag_T3_and_join.json"], "B": ["B/outputs/t3_sector_by_v184_ger.csv"]},
         prereg="`v184_ger` is merged and turned into `nongerman` for the balance data only"),
    dict(id="10-3", pid="10",
         desc="The sample cleaning the paper describes (speeders, inconsistent patterns, German nationality only) is not in the deposited R code; the code keeps 2482 general-population respondents where Table 2 reports 1849 (target T3).",
         sources=[("note", "A", rjp("10", "A"), "The data cleaning the paper describes (speeders, inconsistent patterns, German nationality only) is not in the deposited R code", ""),
                  ("note", "B", rjp("10", "B"), "The deposited R code contains no step that removes them", "")],
         outputs={"A": ["A/outputs/sample_sizes.csv"], "B": ["B/outputs/t3_civic_decomposition.csv"]}, effect="row_count",
         prereg="The deposited R code contains no filter on nationality"),
]

EXCLUDED = [
    ("06", "A", "Hard-coded group sizes at the top of the Rmd (335/101/114/104 and 242/91/38/63/108/101)", "checked by the agent against the data and found consistent",
     "papers/06_VSV5DM/A/results.json", "match the data, outputs/group_size_check.txt"),
    ("07", "A and B", "sjPlot get_model_data row 7 pick in the Figure B placebo loop (line 438)", "checked by both agents and found to extract the intended term",
     "papers/07_JH9DBC/B/results.json", "so the placebo loop extracts the intended term in this environment"),
    ("07", "A and B", "lme4 convergence warning printed during the run", "checked by both agents: comes from figure-only refits, no saved model carries it",
     "papers/07_JH9DBC/A/results.json", "so it comes from a refit inside bootMer or the placebo loop"),
    ("07", "A and B", "fixest 0.13.0 and later change the default vcov and drop singleton fixed effects (T4 600 vs 586)", "package-version environment issue (CHANGELOG_METHOD #6b), not a code observation",
     "papers/07_JH9DBC/A/results.json", "fixest >= 0.13.0 changed the default vcov to iid"),
    ("07", "B", "14 of 307 districts have one row in the 2015/2018 data", "data feature behind the version dependence; the agent did not identify a code issue",
     "papers/07_JH9DBC/B/results.json", "Not confirmed as a coding issue; it is what makes T4 version-dependent."),
    ("08", "A", "Hard-coded Figure 3 labels Result 1..8", "checked by the agent and found consistent with the data order",
     "papers/08_SQRZR8/A/LOG.md", "in this data file for all 8 arms. No issue."),
    ("08", "A and B", "Table 3 note prints N = 4,057 while every model uses 4,507 rows", "target discrepancy (T6), handled in the class (CHANGELOG_METHOD #6a), not a code observation",
     "papers/08_SQRZR8/B/results.json", "the 4,057 in the Table 3 note cannot arise from listwise deletion"),
    ("09", "A and B", "TinyTeX install-and-stop block (lines 108 to 117) skipped", "environment fix only",
     "papers/09_4U8CTG/A/results.json", "tinytex::tinytex_root() errors on the system TeX Live"),
    ("09", "A", "source(echo = FALSE) leaves sink() tables empty", "execution mode of the runner, not the authors' code",
     "papers/09_4U8CTG/A/results.json", "This concerns how 02 is invoked, not the authors' analysis."),
    ("10", "B", "Figure 1 formula lists Citizenship twice (04 line 31)", "checked by the agent: cregg output has no duplicate level",
     "papers/10_6MLKJZ/B/LOG.md", "cregg output has 32 levels per sector, no duplicate"),
    ("10", "A and B", "Code reads data_uhh.csv / data_hsvn.csv, deposit has upper-case names", "environment fix only (case-sensitive file system)",
     "papers/10_6MLKJZ/A/results.json", "code reads data_uhh.csv / data_hsvn.csv, deposit has data_UHH.csv / data_HSVN.csv"),
    ("10", "A and B", "cjoint 2.1.3 fails in read.qualtrics; 2.1.0 used", "package-version environment fix",
     "papers/10_6MLKJZ/B/results.json", "cjoint 2.1.3 (current CRAN) fails in read.qualtrics"),
    ("10", "A", "Figure 2 / 4 axis limits could drop CI ends", "checked by the agent: no CI end outside the limits",
     "papers/10_6MLKJZ/A/results.json", "No CI end fell outside the Figure 2 / 4 axis limits"),
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
            path, sha, ln, text = it["codecheck"]
            if os.path.exists(path):
                if hashlib.sha256(open(path, "rb").read()).hexdigest() != sha: sys.exit(f"{it['id']}: deposited file hash differs")
                got = open(path, encoding="utf-8").read().split("\n")[ln - 1]
                if text not in got: sys.exit(f"{it['id']}: line {ln} of deposited file is {got!r}")
                notes.append(f"line {ln} checked against the deposited file (sha256 {sha[:12]}..., as in PREREG.md)")
            else:
                print(f"note: {path} absent; line check for {it['id']} skipped")
        has_fl = bool(fname) and bool(line_str)
        if it.get("out_of_scope"):
            status = "out of scope: not reproducibility"; reason = it["oos_reason"]
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
    with open(f"{REPO}/batches/batch2_code_observations.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    ex_rows = []
    for pid, ag, item, reason, path, quote in EXCLUDED:
        assert_quote(path, quote)
        ex_rows.append(OrderedDict(paper=P[pid], agents=ag, item=item, reason_excluded=reason, source_file=path))
    if re.search(r"\bbugs?\b", json.dumps(ex_rows), re.I): sys.exit("forbidden word in excluded output")
    if "\u2014" in json.dumps(ex_rows): sys.exit("em dash in excluded output")
    with open(f"{REPO}/batches/batch2_code_observations_excluded.csv", "w", newline="") as f:
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
    json.dump(counts, open(f"{REPO}/batches/batch2_code_observations_counts.json", "w"), indent=1)
    print(json.dumps(counts, indent=1))
    for r in rows: print(r["obs_id"], r["status"], "|", r["status_reason"])


if __name__ == "__main__":
    main()
