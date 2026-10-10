"""Triage of code observations logged by agents A and B on batch 3 (papers 11-15). Same design and status rule as
scripts/triage_observations_batch2.py; batch 1 and 2 files are not touched.

Writes:
  batches/batch3_code_observations.csv           one row per distinct code observation (A and B items matched)
  batches/batch3_code_observations_excluded.csv  items agents logged that are NOT code observations, with the reason
  batches/batch3_code_observations_counts.json   counts, all computed from the rows above

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
Usage: python3 scripts/triage_observations_batch3.py
"""
import csv, json, os, re, sys, hashlib
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {"11": "11_DDOFPS", "12": "12_CYBR7L", "13": "13_DX5T9G", "14": "14_CJISMY", "15": "15_1BBC4E"}


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
    # ---------------- 11_DDOFPS ----------------
    dict(id="11-1", pid="11",
         desc="Line 177 filters parties with the entry '\u00b445' (byte 0xB4 before 45), which matches no row, so the 711 programs of party 45 are not in the Figura 5 table. The paper's Figura 5 legend also omits party 45, so the printed T5 and T6 equal the deposited code's output. An exploratory rerun with '45' keeps PT observed above expected.",
         sources=[("note", "A", "papers/11_DDOFPS/A/results.json", "the filter entry with an acute accent before 45 matches 0 rows", "177"),
                  ("note", "B", "papers/11_DDOFPS/B/results.json", "711 rows have numpartido 45 and are left out of Figura 5", "177")],
         file="An\u00e1lise dos Dados Nota T\u00e9cnica.R", outputs={"A": ["A/outputs/party_share_check.csv"], "B": ["B/outputs/robustness.json"]},
         effect="numeric", prereg="Party 45 excluded by the",
         intent_open="intent cannot be established: the paper's Figura 5 legend also omits party 45, so the deposited output is what the paper prints; both agents left intent open",
         codecheck=("/workspace/audit_runs/11_DDOFPS/prereg/deposit/An\u00e1lise dos Dados Nota T\u00e9cnica.R",
                    "a057273fa5ef24c0d5b5d87fa3eae099c48f05d1f16d86d18002700964bb527b", 177, '"\u00b445"', "latin1")),
    dict(id="11-2", pid="11",
         desc="rio::import (readxl) guesses column types from the first rows and sets every value of sequencial_tse and raca_tse to NA; the script never uses these two columns.",
         sources=[("note", "A", "papers/11_DDOFPS/A/results.json", "turns every value of sequencial_tse (6959 values), raca_tse (2800 values) into NA", "")],
         file="An\u00e1lise dos Dados Nota T\u00e9cnica.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/import_coercion_check_v1.csv"]}),
    # ---------------- 12_CYBR7L ----------------
    dict(id="12-1", pid="12",
         desc="Cell 4 (Figure 1) sets df_tmp['Author_based_in_Africa'][mask] = value by chained assignment with warnings silenced; under pandas 3.0.0 (the README version, Copy-on-Write) this does not modify df_tmp, so Figure 1's Africa-based series uses each author's first row. Figure 1 only; no target.",
         sources=[("issue_list", "A", 0)],
         outputs={"A": ["A/outputs/code_checks.json"]}, effect="numeric",
         prereg="updates `df_tmp['Author_based_in_Africa'][mask] = value` by chained assignment",
         note_extra="B did not log it"),
    dict(id="12-2", pid="12",
         desc="Cell 8 computes the complete-set Africa-based shares from each author's first row while the top-5% counts use the mode-based node attribute; with the mode-based value the 2021 complete-set count is 120 instead of 117. Both give 13% at the paper's rounding; top-5% counts and all targets are unchanged.",
         sources=[("note", "A", "papers/12_CYBR7L/A/results.json", "cell 8 complete-set Africa-based counts use each author's first row", "318"),
                  ("note", "B", "papers/12_CYBR7L/B/results.json", "Table 1 complete-set shares use first-row raw location while top-5% counts use mode-based location", "")],
         file="replication_code.ipynb", outputs={"A": ["A/outputs/code_checks.json"], "B": ["B/outputs/location_coding_check.json"]},
         effect="numeric", prereg="percentages in the same cell 8 lines use the raw value in each author's first row",
         intent_open="intent cannot be established: whether the complete-set column should use the first-row or the mode-based location is not stated, and both give the printed share at the paper's rounding; A described it as a design inconsistency"),
    dict(id="12-3", pid="12",
         desc="Authors whose location rows are all blank get an empty mode, which cells 6 and 9 set to 1 (Africa-based), while the appendix says undetermined values were set to missing. One such author in 2010 (not in the top 5%), none in 2021.",
         sources=[("note", "A", "papers/12_CYBR7L/A/results.json", "authors whose location rows are all blank get an empty mode, which cells 6 and 9 set to 1 (Africa-based)", "")],
         file="replication_code.ipynb", outputs={}, effect="none",
         evidence={"A": ["A/outputs/code_checks.json"]},
         prereg="an author whose rows are all blank, where mode is empty) is set to 1",
         note_extra="B checked and found no such author in 2021"),
    # ---------------- 13_DX5T9G ----------------
    dict(id="13-1", pid="13",
         desc="Footnote 20 probit models mod_UK (lines 197-199) and mod_US (lines 201-203) pass weights as subset(...)$w1, but the prepared data has no column w1 (01_Prepare data.R creates only w), so both models are fitted unweighted while the other models use w. A refit shows the WHO coefficient changes (UK 1.468 as deposited vs 1.903 weighted; US 0.556 vs 0.510). Footnote only; no target.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/check_06_w1.csv"], "B": ["B/outputs/code_checks.txt"]}, effect="numeric",
         prereg="weights are passed as `...$w1`",
         codecheck=("/workspace/audit_runs/13_DX5T9G/A/orig_code/06_Estimate Open.R",
                    "2afcfdd41c42765413cb52c38eafe670119695320baf5d6c05a8a3fdb81ee632", 199, "$w1)", "utf-8")),
    dict(id="13-2", pid="13",
         desc="Inside the country loop the counterfactual data for the change-in-probability simulations is tmp_0 <- tmp_1 <- data (combined UK and US data) rather than the country subset used to fit the model, so each country's Figure A4 effects average over both samples' covariates. Small numeric effect in an own-seed rerun; no target.",
         sources=[("issue_list", "B", 1)],
         outputs={"B": ["B/outputs/code_checks.txt"]}, effect="numeric",
         codecheck=("/workspace/audit_runs/13_DX5T9G/A/orig_code/06_Estimate Open.R",
                    "2afcfdd41c42765413cb52c38eafe670119695320baf5d6c05a8a3fdb81ee632", 72, "tmp_0 <- tmp_1 <- data", "utf-8")),
    dict(id="13-3", pid="13",
         desc="01_Prepare data.R draws the 10,000 entropy-balancing target rows uniformly with sample(), so the CCES and BES survey weights stored as w are not used for the targets. Whether this is intended is not stated; impact not tested.",
         sources=[("note", "A", "papers/13_DX5T9G/A/results.json", "the CCES commonweight and BES wt_demog are stored as w but not used", "121; 127; 136; 162"),
                  ("note", "B", "papers/13_DX5T9G/B/results.json", "the 10,000 target-population rows are drawn with sample() without the CCES/BES survey weights", "162")],
         file="code/01_Prepare data.R", outputs={}, effect="none"),
    dict(id="13-4", pid="13",
         desc="runif() for the dummy outcome M is called before set.seed(1230); M only serves as the left-hand side for model.matrix and does not affect the weights.",
         sources=[("note", "A", "papers/13_DX5T9G/A/results.json", "runif() for the dummy M is called before set.seed(1230)", "153-154")],
         file="code/01_Prepare data.R", outputs={}, effect="none"),
    dict(id="13-5", pid="13",
         desc="419 CCES rows with missing ideo5 stay in the target data; model.matrix drops them when sampled, so the effective US target sample is slightly below 10,000. Impact not tested.",
         sources=[("note", "A", "papers/13_DX5T9G/A/results.json", "419 CCES rows with missing ideo5 stay in t_data", "121-126")],
         file="code/01_Prepare data.R", outputs={}, effect="none"),
    dict(id="13-6", pid="13",
         desc="BES LR stays a factor after mapvalues and becomes character when combined with the numeric CCES LR, so the ebalance range conditions on LR are string comparisons for UK target rows. In the run locale they agree with the numeric comparison on all 2139 BES rows; other collation locales were not testable here.",
         sources=[("note", "B", "papers/13_DX5T9G/B/results.json", "BES LR stays a factor after mapvalues and becomes character", "138-142")],
         file="code/01_Prepare data.R", outputs={}, effect="none",
         evidence={"B": ["B/outputs/code_checks.txt"]}),
    dict(id="13-7", pid="13",
         desc="The p-value in 03 uses df = nrow(data) of the combined UK and US data rather than the country N; with N near 1,600 the agent judged it to have no practical effect on the stars.",
         sources=[("note", "B", "papers/13_DX5T9G/B/results.json", "pvalue in 03 uses df = nrow(data) of the combined UK+US data rather than the country N", "")],
         file="code/03_Estimate main models.R", outputs={}, effect="none",
         prereg="where `data` inside `run_models` is the global combined UK+US data frame"),
    # ---------------- 14_CJISMY ----------------
    dict(id="14-1", pid="14",
         desc="full_model_h3_prop_no_outliers (line 180) is specified identically to full_model_h3 (no outlier filter despite the name). It is not printed in any table call, so no table is affected.",
         sources=[("note", "A", "papers/14_CJISMY/A/results.json", "full_model_h3_prop_no_outliers is specified identically to full_model_h3", "180")],
         file="crosssection_linear.R", outputs={}, effect="none"),
    dict(id="14-2", pid="14",
         desc="Text p. 824 says a min-to-max change predicts a 0.2 point increase (Figure 2 left panel); Table 1 Model 1 prints 0.51. The Figure 2 model in the code dichotomises the predictor (line 92), and its Both vs None/Single gap (0.22) is close to the 0.2 in the text. Table 1 reproduces.",
         sources=[("note", "A", "papers/14_CJISMY/A/results.json", "Figure 2 left panel model recodes resource_and_agriculture to 'Both' only when the 2000-2019 mean equals 1", "92"),
                  ("note", "B", "papers/14_CJISMY/B/results.json", "So the 0.2 in the prose is close in size to the Both vs None/Single gap of the dichotomised Figure 2 model", "")],
         file="crosssection_linear.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/figure2_check.csv"], "B": ["B/outputs/figure2_prose_check.csv"]},
         prereg="predicts a 0.2 point increase in the value of disagreement", out_of_scope=True,
         oos_reason="Text versus code description of a figure; the code reproduces the Table 1 numbers."),
    # ---------------- 15_1BBC4E ----------------
    dict(id="15-1", pid="15",
         desc="Comparison.R lines 105, 176 and 183 relabel factor levels by position after as.factor(), so the label-to-variable mapping of Figures 1 and 4 depends on the collation locale. Labels are correct in the run environment (C.UTF-8); B's check shows a mismatch under the C locale. The authors' comment at line 104 notes the level order sometimes switched. Figures only; no target.",
         sources=[("note", "A", "papers/15_1BBC4E/A/results.json", "Comparison.R lines 105, 176 and 183 relabel alphabetically ordered factor levels by position", "105; 176; 183"),
                  ("note", "B", "papers/15_1BBC4E/B/results.json", "Factor levels are relabelled by position after as.factor(), so the label-to-variable mapping depends on the collation locale", "105; 176; 183")],
         file="Scripts/Comparing Indices/Comparison.R", outputs={"B": ["B/outputs/factor_label_locale_check.csv"]}, effect="label",
         evidence={"A": ["A/outputs/label_locale_check.csv"]},
         intent_open="labels are correct in the run of record; a mismatch appears only under another collation locale (an environment dependence), shown by B only; A found the labels correct and did not test another locale; the authors' comment at line 104 acknowledges the level order",
         codecheck=("/workspace/audit_runs/15_1BBC4E/A/deposit/Replication Data/Replication Files. Electoral Autocracy. Hybrid Regimes. Multiparty Autocracy. Same. same but different/Scripts/Comparing Indices/Comparison.R",
                    "ea2802451a965234765d97e7d3159f3a64a26eea1c6b8a035ea427d92c5c521c", 176, 'levels(base$Comparison) <- c("CPR"', "utf-8")),
]

EXCLUDED = [
    ("11", "A and B", "Script reads bd_doxa_programas.xlsx / bd_doxa_candidatos.xlsx; the deposit has the _HGPE names", "environment fix (pre-registered path-only fix, pre-run decision #1); alternative class shown in batches/batch3_class_rules.json",
     "papers/11_DDOFPS/B/results.json", "copied under script names (pre-registered path fix)"),
    ("11", "A and B", "theme_ipsum_tw() not exported by current hrbrthemes", "package-version environment fix (Figura 1 styling, no target)",
     "papers/11_DDOFPS/A/results.json", "since 0.9.3 and 0.8.7 do not export theme_ipsum_tw()"),
    ("11", "A and B", "Script sourced with encoding latin1", "environment fix only",
     "papers/11_DDOFPS/B/results.json", "Script sourced with encoding = 'latin1'"),
    ("11", "A", "CRAN ggplot2 4.0.3 masks system ggplot2 3.5.1", "package-version environment note",
     "papers/11_DDOFPS/A/results.json", "CRAN ggplot2 4.0.3 was pulled into the per-run library"),
    ("11", "A and B", "Paper note 9 prints an expected 2018 APE4 count of 16; the code gives 16.87", "secondary number in the text, not a target and not a code observation",
     "papers/11_DDOFPS/B/results.json", "Paper note 9 expected 2018 APE4 count 16 vs code 16.87"),
    ("11", "A and B", "Figura 4 wording 'p-valor > 0,001' versus the code's p far below 0.001", "pre-registered reading of the paper's wording (PREREG T4 criterion), not a code observation",
     "papers/11_DDOFPS/A/results.json", "the code gives p far below 0.001 (pre-registered reading (1))"),
    ("12", "A and B", "nx.hits is unseeded (svds start vector)", "handled by pre-run decision #3 and R_a (20 seeds give the same top-5% set), not a code observation",
     "papers/12_CYBR7L/A/results.json", "R_a: all 20 seeds and the primary seed give the identical 2021 top-5% set"),
    ("12", "A and B", "Python 3.12.15 used instead of README Python 3.14.2", "environment note; all five README package versions installed exactly",
     "papers/12_CYBR7L/B/results.json", "Python 3.12.15 used instead of README 3.14.2"),
    ("12", "A and B", "Pickle cell placed after cell 8 rather than only at the end", "protocol note on the audit's save-only cells, not the authors' code",
     "papers/12_CYBR7L/A/results.json", "Cell 9 reassigns G_citation (graphs with isolated nodes)"),
    ("12", "A", "Text p. 708 says 42 percent where Table 2 prints 40.7 (run gives 40.74)", "text versus table difference noted in PREREG.md, not a target and not a code observation",
     "papers/12_CYBR7L/A/results.json", "Paper text p. 708 says 42 percent"),
    ("13", "A and B", "Full 03 script killed for running out of memory; pre-registered fallback used", "environment limit and labelled deviation (alternative class E in batches/batch3_class_rules.json), not a code observation",
     "papers/13_DX5T9G/B/results.json", "the unchanged full 03 was OOM-killed at 3.3 GB RSS"),
    ("13", "A and B", "registerDoMC cores 7 to 1", "environment fix allowed by PREREG.md",
     "papers/13_DX5T9G/A/results.json", "registerDoMC cores 7 to 1"),
    ("13", "B", "logr 1.4.0 warning hook crashed read.dta13; authors' logr 1.3.3 used", "package-version environment fix",
     "papers/13_DX5T9G/B/results.json", "logr 1.3.3 (authors' version) instead of 1.4.0"),
    ("13", "A and B", "Regenerated Table 2 prints stars on three non-target cells that the printed table shows without stars or with a different mark (PREREG inconsistency 6)", "difference in significance marks only; values match; recorded under Limitations, not a code observation",
     "papers/13_DX5T9G/A/results.json", "PREREG inconsistency 6"),
    ("13", "B", "First fallback launch issued twice; the duplicate failed at once", "process note, no reported number comes from it",
     "papers/13_DX5T9G/B/results.json", "The tool issued the first fallback launch twice"),
    ("14", "A", "Categorical H1 variable aggregated with Mode(); ties broken by first occurrence (line 26)", "checked by the agent and found consistent with the paper's 'nominal by mode' rule (pre-flagged in PREREG.md)",
     "papers/14_CJISMY/A/results.json", "Design choice consistent with the paper's 'nominal by mode' rule"),
    ("14", "A and B", "library(specr) / library(broom.mixed) commented out", "environment fix; B ran the unmodified script after installing specr 1.0.0 with identical results",
     "papers/14_CJISMY/B/results.json", "the unmodified crosssection_linear.R then ran without error"),
    ("14", "A and B", "dplyr 1.0.9 / vctrs 0.5.1 pins could not be loaded; system versions used", "package-version environment note",
     "papers/14_CJISMY/B/results.json", "dplyr 1.0.9 / vctrs 0.5.1 pins were not usable together with the system tidyverse stack"),
    ("15", "A and B", "Prose values '.63' and '.39' versus Table 3 0.636 and median 0.398", "text versus table rounding, Table 3 reproduces; not a code observation",
     "papers/15_1BBC4E/B/results.json", "the prose '.39' looks truncated (not a target)"),
    ("15", "B", "Dataverse API reports version 1.1 where PREREG.md says 1.0", "metadata note; all 49 files byte-identical to the PREREG sha256 list",
     "papers/15_1BBC4E/B/results.json", "All 49 files are byte-identical to the PREREG sha256 list"),
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
    with open(f"{REPO}/batches/batch3_code_observations.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    ex_rows = []
    for pid, ag, item, reason, path, quote in EXCLUDED:
        assert_quote(path, quote)
        ex_rows.append(OrderedDict(paper=P[pid], agents=ag, item=item, reason_excluded=reason, source_file=path))
    if re.search(r"\bbugs?\b", json.dumps(ex_rows), re.I): sys.exit("forbidden word in excluded output")
    if "\u2014" in json.dumps(ex_rows): sys.exit("em dash in excluded output")
    with open(f"{REPO}/batches/batch3_code_observations_excluded.csv", "w", newline="") as f:
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
    json.dump(counts, open(f"{REPO}/batches/batch3_code_observations_counts.json", "w"), indent=1)
    print(json.dumps(counts, indent=1))
    for r in rows: print(r["obs_id"], r["status"], "|", r["status_reason"])


if __name__ == "__main__":
    main()
