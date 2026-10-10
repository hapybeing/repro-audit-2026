"""Triage of code observations logged by agents A and B on batch 1 (papers 01-05).

Writes:
  batches/batch1_code_observations.csv           one row per distinct code observation (A and B items matched)
  batches/batch1_code_observations_excluded.csv  items agents logged that are NOT code observations, with the reason
  batches/batch1_code_observations_counts.json   counts, all computed from the rows above

What is hand-coded here (and only this): the MATCHING TABLE below, i.e. which agent item describes which issue, a neutral
one-line description, the output files each agent cited, and whether PREREG.md pre-flagged the issue. Everything else is
read or checked from files:
  - every entry of each results.json issue list (key "bugs") must be mapped to exactly one row (asserted);
  - file and line for issue-list entries are read from results.json;
  - for items an agent logged outside results.json (code review notes, LOG, diffs README), a verbatim quote is asserted to
    exist in the cited file;
  - PREREG pre-flags are asserted by quoting PREREG.md;
  - cited output files are checked to exist on disk;
  - status is computed by rule (see status()).

Status rule (reviewer's definition):
  "verified finding"                  file + line given, a demonstrated output change saved in an output file, AND both
                                      agents found it independently;
  "unverified agent observation"      anything else that is a code / reproducibility observation;
  "pending re-check"                  05 SDO index item (re-check output: papers/05_FNTC1J/A/outputs/sdo_check.json);
  "out of scope: not reproducibility" measurement-validity or interpretation opinions (code reproduces the reported number;
                                      the claim is about what a variable means or how the text describes it).
Independence = both agents logged it, PREREG.md (which both received) did not pre-flag it, and no recorded exposure of one
agent to the other's files bears on it.
Usage: python3 scripts/triage_observations.py
"""
import json
import csv, json, os, re, sys
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {"01": "01_5BIH0P", "02": "02_ELBOXX", "03": "03_3IOGQ8", "04": "04_PSHE5L", "05": "05_FNTC1J"}


def rj(pid, ag):
    return json.load(open(f"{REPO}/papers/{P[pid]}/{ag}/results.json"))


def norm(s):
    return re.sub(r"\s+", " ", s)


def assert_quote(path, quote):
    full = f"{REPO}/{path}"
    txt = open(full, encoding="utf-8").read()
    if path.endswith(".json"):
        # quotes inside JSON strings may be escaped; compare against decoded text as well
        try:
            txt = txt + "\n" + json.dumps(json.load(open(full)), ensure_ascii=False)
        except Exception:
            pass
    if norm(quote) not in norm(txt):
        sys.exit(f"QUOTE NOT FOUND in {path}: {quote!r}")
    return path


# ---------------------------------------------------------------------------------------------------------------------
# Hand-coded matching table. Source kinds:
#   ("issue_list", agent, index)        -> results.json["bugs"][index] (file/line read from there)
#   ("note", agent, path, quote, line)  -> logged outside the issue list; quote asserted; line as the agent gave it (or "")
# outputs: {agent: [paths relative to the paper folder]} that show the effect; effect: type of the demonstrated effect.
# effect types that count as a demonstrated output change: numeric, label, runtime_error, row_count
# ---------------------------------------------------------------------------------------------------------------------
ISSUES = [
    # ---------------- 01_5BIH0P ----------------
    dict(id="01-1", pid="01",
         desc="xvg2csv.py: legend test startswith('@ s') also matches the GROMACS '@ subtitle' line, so the derived CSV header reads 'Time (ps),fter lsq fit to Protein'. Labels only; numeric values unaffected.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/xvg2csv_check.json"], "B": ["B/outputs/xvg_format_check.json"]}, effect="label"),
    dict(id="01-2", pid="01",
         desc="xvg2csv.py: first column header hard-coded 'Time (ps)' while the RMSD .xvg files were made with -tu ns, so deposited RMSD tables label nanoseconds as picoseconds. Labels only.",
         sources=[("issue_list", "A", 1), ("issue_list", "B", 1)],
         outputs={"A": ["A/outputs/xvg2csv_check.json"], "B": ["B/outputs/xvg_format_check.json"]}, effect="label"),
    dict(id="01-3", pid="01",
         desc="xvg2csv.py: no header row is written when the .xvg has no legend lines (gmx rmsf); Dataverse ingest then used the residue 1 row as variable names, so the ingested RMSF table has 673 of 674 residues. A's own check file records the same header line but A did not log it as an issue.",
         sources=[("issue_list", "B", 2)],
         outputs={"B": ["B/outputs/xvg_format_check.json"]}, effect="row_count"),
    dict(id="01-4", pid="01",
         desc="Deposit lacks the production trajectories (.xtc) and the processing steps that made the analysis files; the deposited MD shell script covers only the first 200 ns segment (md_0_10); mmpbsa-1.in matches no deposited result.",
         sources=[("note", "A", "papers/01_5BIH0P/A/LOG.md", "the MD shell script covers only the first 200 ns segment (md_0_10)", ""),
                  ("note", "B", "papers/01_5BIH0P/B/results.json", "the inputs needed to regenerate the 2XWT analyses (production .xtc trajectories) are not deposited", "")],
         file="em-md-nvt-npt-single.sh; deposit as a whole",
         outputs={}, effect="none", prereg="The production trajectory is not in the dataset."),
    # ---------------- 02_ELBOXX ----------------
    dict(id="02-1", pid="02",
         desc="disputes keeps rows with stateb == country and dyad_rolea == 3, so it counts dyadic MIDs the country initiated, while the code comment and paper text say 'initiated against'. Recount with the country as target: M2 r 0.1214 vs 0.1628, same sign and significance.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/mid_direction_check.csv"], "B": ["B/outputs/code_review_diagnostic_correlations.csv"]},
         effect="numeric", out_of_scope=True,
         oos_reason="Reviewer-designated: claim about what the dispute variable measures relative to the text; the deposited code reproduces the reported number. Would otherwise meet all three verification criteria."),
    dict(id="02-2", pid="02",
         desc="Disputes matched on strtyr in a dyad-year file, so a MID lasting k years is counted k times in its start year (B only).",
         sources=[("issue_list", "B", 1)],
         outputs={"B": ["B/outputs/code_review_diagnostic_correlations.csv"]}, effect="numeric", out_of_scope=True,
         oos_reason="Same class as 02-1: a claim about how the dispute variable should be constructed; the code reproduces the reported number. Judgement call by the triage author."),
    dict(id="02-3", pid="02",
         desc="analysis_data_creation.R calls peacesciencer::create_stateyears() with default mry = TRUE, which ends the frame at (current year - 1); run in 2026 the frame gains 195 country-years (N 17706 vs 17511) and M1 (T4, T5) drifts; M2 unchanged. README does not mention it. Both agents handled it as an environment fix (clock set to the authors' run date).",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "create_stateyears() depends on the system date", ""),
                  ("note", "B", "papers/02_ELBOXX/B/diffs/README.md", "`analysis_data_creation.R` line 61 calls `peacesciencer::create_stateyears()`", "61")],
         file="analysis_data_creation.R",
         outputs={"A": ["A/outputs/targets_pathA_clock2026.csv"], "B": ["B/outputs/pathA_asis/targets_asis.csv"]}, effect="numeric"),
    dict(id="02-4", pid="02",
         desc="replication.R keeps pub_def == 1 (exactly one public defensive alliance) while the text describes members of a public defensive alliance (pub_def is a count).",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "`pub_def == 1` filter (replication.R line 24)", "24"),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "code uses pub_def == 1 (replication.R line 24)", "24")],
         file="replication.R", outputs={"B": ["B/outputs/robustness_results.csv"]}, effect="numeric",
         prereg="the code keeps only `pub_def == 1`", out_of_scope=True,
         oos_reason="Text versus code description of the sample; the code reproduces the reported number. Interpretation, not reproducibility."),
    dict(id="02-5", pid="02",
         desc="M1 text says defensive secret alliances summed per system-year; code uses all secret alliances at country-year level.",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "M1 text says \"defensive secret alliances\"", ""),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "M1 text says 'defensive secret alliances'", "")],
         file="analysis_data_creation.R; replication.R", outputs={"B": ["B/outputs/code_review_diagnostic_correlations.csv"]},
         effect="numeric", prereg="Paper text for M1 says", out_of_scope=True,
         oos_reason="Text versus code description of the measure; the code reproduces the reported number."),
    dict(id="02-6", pid="02",
         desc="Paper text names MIDs 5.0; code uses dyadic MID 4.02.",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "Paper says MIDs 5.0; code uses dyadic MID 4.02", ""),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "text says MIDs 5.0, code uses dyadic MID 4.02", "")],
         file="analysis_data_creation.R", outputs={}, effect="none",
         prereg="the code uses dyadic MID 4.02", out_of_scope=True,
         oos_reason="Wording of the paper's data description; no bearing on reproducing the reported numbers."),
    dict(id="02-7", pid="02",
         desc="secret_alliances sums memberships (an alliance with k members counts k times), text says number of secret alliances.",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "`secret_alliances` (lines 107-110) sums `secret`", "107-110"),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "secret_alliances sums memberships", "32; 109")],
         file="analysis_data_creation.R", outputs={"B": ["B/outputs/code_review_diagnostic_correlations.csv"]},
         effect="numeric", prereg="so an alliance with k members is counted k times", out_of_scope=True,
         oos_reason="Measurement choice versus text wording; the code reproduces the reported number."),
    dict(id="02-8", pid="02",
         desc="Country-years after 2014 (MID 4.02 coverage end) get disputes = 0 by zero-filling; a coverage limit rather than observed zeros.",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "so 2015-2024 country-years have disputes = 0", ""),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "zero-filled disputes after 2014", "95-98")],
         file="analysis_data_creation.R", outputs={"B": ["B/outputs/robustness_results.csv"]}, effect="numeric",
         prereg="Dyadic MID 4.02 has no disputes after 2014", out_of_scope=True,
         oos_reason="Data-coverage and measurement question; the code reproduces the reported number."),
    dict(id="02-9", pid="02",
         desc="replication.R comment for test 2 describes a different correlation than the code computes (comment only; code matches the paper).",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "replication.R lines 18-19 comment", "18-19"),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "replication.R comment for test 2 describes a different correlation", "")],
         file="replication.R", outputs={}, effect="none", prereg="replication.R comment for test 2 says"),
    dict(id="02-10", pid="02",
         desc="README names AJPS_rep.RData and codebook.pdf; the deposit has AJPS_analysis_data.RData and no project codebook.",
         sources=[("note", "A", "papers/02_ELBOXX/A/outputs/code_review.md", "README names `AJPS_rep.RData` and `codebook.pdf`", ""),
                  ("note", "B", "papers/02_ELBOXX/B/results.json", "README names AJPS_rep.RData and codebook.pdf", "")],
         file="README.txt", outputs={}, effect="none", prereg="README names the data file `AJPS_rep.RData`"),
    # ---------------- 03_3IOGQ8 ----------------
    dict(id="03-1", pid="03",
         desc="TMT isotope-impurity correction takes each leakage coefficient from the corrected channel's own impurity vector rather than the neighbouring reagent's (judged against the convention in the Rmd's own comment). Shown on a synthetic scan (A) and by parsing the expression (B); not run on study data (input not deposited).",
         sources=[("issue_list", "A", 1), ("issue_list", "B", 0)],
         evidence={"A": ["A/outputs/code_review_tests.json"], "B": ["B/outputs/isotope_correction_mapping.json"]},
         outputs={}, effect="synthetic_only"),
    dict(id="03-2", pid="03",
         desc="generate_ions_for_sequence computes neutral-loss ions for fragment i from the masses of fragment i-1 (off by one). Shown on synthetic input; effect on study data not measurable.",
         sources=[("issue_list", "A", 0)], evidence={"A": ["A/outputs/code_review_tests.json"]}, outputs={}, effect="synthetic_only"),
    dict(id="03-3", pid="03",
         desc="extract_intensities is called with rank_order in the PID argument in the 2- and 3-PSM sections (code reading only).",
         sources=[("issue_list", "A", 2)], outputs={}, effect="none"),
    dict(id="03-4", pid="03",
         desc="Volcano UP/DOWN classification uses cum_p_value > 0.5 where 0.05 seems intended; clause order means no label can change.",
         sources=[("note", "A", "papers/03_3IOGQ8/A/results.json", "volcano classification uses 'cum_p_value > 0.5' (line 2999", "2999"),
                  ("note", "B", "papers/03_3IOGQ8/B/LOG.md", "has `p > 0.5` where 0.05 is likely meant", "")],
         file="Byonic_Middle-Down_Processing_Notebook.Rmd", outputs={}, effect="none"),
    dict(id="03-5", pid="03",
         desc="Scans with 4-10 PSMs are split out but never merged into assigned_fractional_intensity_hits, so they are dropped silently.",
         sources=[("note", "A", "papers/03_3IOGQ8/A/results.json", "scans with 4-10 PSMs are split out (lines 1703-1744)", "1703-1744")],
         file="Byonic_Middle-Down_Processing_Notebook.Rmd", outputs={}, effect="none"),
    dict(id="03-6", pid="03",
         desc="Experiment filters use the template placeholder alias your_ms_experiment_1 for all experiments.",
         sources=[("note", "A", "papers/03_3IOGQ8/A/results.json", "experiment1/2/3 filters all use the same placeholder alias", ""),
                  ("note", "B", "papers/03_3IOGQ8/B/LOG.md", "experiment2/3 filters reuse \"your_ms_experiment_1\"", "")],
         file="Byonic_Middle-Down_Processing_Notebook.Rmd", outputs={}, effect="none", prereg="placeholder experiment aliases"),
    dict(id="03-7", pid="03",
         desc="PEP.2D is joined back from all experiments by scan_number and PID, which could duplicate rows if several MS files share one Byonic export (not checkable without the export).",
         sources=[("note", "B", "papers/03_3IOGQ8/B/results.json", "PEP.2D is joined back from all experiments by scan_number and PID (Rmd ~line 1449)", "~1449")],
         file="Byonic_Middle-Down_Processing_Notebook.Rmd", outputs={}, effect="none"),
    dict(id="03-8", pid="03",
         desc="The notebook's only tabular input, Byonic_results.csv (read at line 498), is not deposited, so the run stops there and no target can be computed (materials gap; class C driver).",
         sources=[("note", "A", "papers/03_3IOGQ8/A/LOG.md", "the only file reads are `read.csv(\"Byonic_results.csv\")` (line 498)", "498"),
                  ("note", "B", "papers/03_3IOGQ8/B/results.json", "Notebook stopped at Rmd line 498", "498")],
         file="Byonic_Middle-Down_Processing_Notebook.Rmd",
         outputs={"A": ["A/outputs/partial_run_log.txt"], "B": ["B/outputs/run_status.json"]}, effect="runtime_error",
         prereg="Reads `Byonic_results.csv` (line 498)"),
    # ---------------- 04_PSHE5L ----------------
    dict(id="04-1", pid="04",
         desc="Q15 code 8 (64 rows) stays in the models as a numeric value above the 1-7 scale because the recode to NA at line 188 is commented out. Published coefficients match only with code 8 kept; published structural fit matches only with code 8 set to NA. A logged it as an issue, B as an observation.",
         sources=[("issue_list", "A", 0),
                  ("note", "B", "papers/04_PSHE5L/B/outputs/code_review.md", "is commented out, so as deposited the 64 rows with code 8 enter the model with the numeric value 8", "188")],
         outputs={"A": ["A/outputs/primary_vs_diagnostic.csv"], "B": ["B/outputs/diag_q15na_structural_stdsol.csv"]},
         effect="numeric", prereg="is commented out (line 188)"),
    dict(id="04-2", pid="04",
         desc="Lines 17-20 convert RAW_Q24* columns that are absent from the public data extract, so the script errors as written; the variables are unused later. Both agents commented the lines out as a pre-registered environment fix.",
         sources=[("note", "A", "papers/04_PSHE5L/A/diffs/README.md", "`02_raw_q24_absent.diff` (lines 17, 19, 20, 22)", "17-22"),
                  ("note", "B", "papers/04_PSHE5L/B/outputs/code_review.md", "errors on the public CSV because the columns are absent", "17-20")],
         file="Rural Populism - Socius - Public Code.R",
         outputs={"A": ["A/outputs/envfix2_error_before_fix.txt"]}, effect="runtime_error",
         prereg="These columns are not in the OSF CSV, so this line will error as written."),
    dict(id="04-3", pid="04",
         desc="Control dummies (college, male, over 65) put nonresponse codes into the 0 category; the script's comment says this is deliberate. Controls model only.",
         sources=[("note", "A", "papers/04_PSHE5L/A/results.json", "Controls-model dummies code non-substantive answers as 0", ""),
                  ("note", "B", "papers/04_PSHE5L/B/outputs/code_review.md", "Nonresponse codes in control dummies (lines 48, 122, 179)", "48; 122; 179")],
         file="Rural Populism - Socius - Public Code.R", outputs={}, effect="none", out_of_scope=True,
         oos_reason="Documented measurement choice for controls; does not bear on reproducing the targets."),
    dict(id="04-4", pid="04",
         desc="Script reads a survey file (line 9) that is not in the Dataverse deposit; both agents used the public OSF extract instead (pre-registered path fix).",
         sources=[("note", "A", "papers/04_PSHE5L/A/diffs/README.md", "`01_data_path.diff` (line 9)", "9"),
                  ("note", "B", "papers/04_PSHE5L/B/diffs/README.md", "`01_data_path.diff` (line 9)", "9")],
         file="Rural Populism - Socius - Public Code.R", outputs={}, effect="none",
         prereg="which is not in the deposit."),
    # ---------------- 05_FNTC1J ----------------
    dict(id="05-1", pid="05",
         desc="SDO_index = rowMeans(starts_with('SDO')) averages six columns (SDO1-4 plus reversed SDO1_r, SDO3_r), so items 1 and 3 cancel and the index equals 4 + (SDO2 + SDO4)/6 on complete rows. Rebuilt 4-item index (R_c): T1 1.3075 vs 1.3004, conclusions unchanged.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/Rc_coefs.csv"], "B": ["B/outputs/Rc_targets.csv"]}, effect="numeric",
         prereg="`starts_with(\"SDO\")` would average six columns", pending=True),
    dict(id="05-2", pid="05",
         desc="Hard-coded removal of row name '1400' as an 'influential outlier' does not match the script's own outlier screens in the deposited data; keeping it gives N 2963 and ORs equal at 2 decimals.",
         sources=[("issue_list", "A", 1), ("issue_list", "B", 1)],
         outputs={"A": ["A/outputs/review_row1400_impact.csv"], "B": ["B/outputs/review_row1400_impact.csv"]}, effect="numeric",
         exposure=("papers/05_FNTC1J/B/LOG.md", "displayed file NAMES that",
                   "Independence not established: B's LOG records that file-change notices showed it the names of A's files; B's review_row1400.R has the same name as A's and was written about two minutes after it (file mtimes).")),
    dict(id="05-3", pid="05",
         desc="Bare dash separator at line 3142 (no '#') is parsed as unary minus joined to the next assignment, so a top-to-bottom run stops ('object count_both_ones not found'); B also logged the follow-on error at line 3149. After all target code.",
         sources=[("issue_list", "A", 2), ("issue_list", "B", 2), ("issue_list", "B", 3)],
         outputs={"A": ["A/outputs/run_main_attempt1_console.txt"], "B": ["B/outputs/errors_main_upto3677.csv"]}, effect="runtime_error"),
    dict(id="05-4", pid="05",
         desc="cor(...$COVID_CTB, ...$misinfo_covid_beliefs) at line 3153 refers to columns that object only gets at line 3207, so the run errors ('x must be numeric'). After all target code.",
         sources=[("issue_list", "A", 3), ("issue_list", "B", 4)],
         outputs={"A": ["A/outputs/run_main_attempt2_console.txt"], "B": ["B/outputs/errors_main_upto3677.csv"]}, effect="runtime_error"),
]

# Items agents logged that are not code observations (kept for transparency; not counted as observations).
EXCLUDED = [
    ("01", "A and B", "400 ns RMSD series starts near 4.48 nm and has a duplicated 200 ns time point", "data-value anomaly in deposited outputs, not a code observation",
     "papers/01_5BIH0P/B/LOG.md", "400 ns RMSD series starts at 4.4786 nm"),
    ("01", "A and B", "Deposited MMPBSA SDs are population (ddof=0) values while PREREG named ddof=1", "convention note; means unaffected; not a code observation",
     "papers/01_5BIH0P/A/results.json", "The deposited SD/SEM in FINAL_RESULTS_MMPBSA.dat are population (ddof=0) values"),
    ("02", "A", "ATOP state-years without a COW match are dropped by the merge", "checked by the agent and recorded as consistent with the design",
     "papers/02_ELBOXX/A/outputs/code_review.md", "Consistent with the stated design; not a bug."),
    ("02", "A", "visualization.R line 38 backtick name with trailing space", "tested by the agent and found to work",
     "papers/02_ELBOXX/A/outputs/code_review.md", "it still recodes 1 to \"Secret Article\""),
    ("03", "B", "parse_position_mass comment says 37, code keeps 36", "judged intended by the agent",
     "papers/03_3IOGQ8/B/LOG.md", "which looks intended"),
    ("04", "A and B", "Table 1 reliability values printed by the script differ from the paper's Table 1", "non-target output discrepancy, not a code observation (no file/line identified)",
     "papers/04_PSHE5L/B/outputs/code_review.md", "does not equal the paper's Table 1 values"),
    ("04", "A", "gt library cannot be installed on this platform (library line commented out)", "environment fix only",
     "papers/04_PSHE5L/A/diffs/README.md", "`03_gt_library.diff` (line 6)"),
    ("05", "A", "Significance stars differ from the paper in 6 table rows; y-standardized and some Table A2 cells differ", "output discrepancies on non-target cells, not code observations",
     "papers/05_FNTC1J/A/results.json", "the stars printed by the authors' own code differ from the paper's"),
    ("05", "A", "utils::View() stubbed for non-interactive Rscript", "environment fix only",
     "papers/05_FNTC1J/A/results.json", "View <- function(...) invisible(NULL)"),
    ("05", "A and B", "Bare dash line at 827 only negates a printed value and does not stop the run", "checked by both agents and found to have no effect",
     "papers/05_FNTC1J/B/outputs/code_review.md", "so it only negates a printed table and does not error"),
    ("05", "B", "CA05 factor coding, SDO reversal (12 - item), outcome dummies, mice receiving id", "checked by the agent and recorded as not code issues",
     "papers/05_FNTC1J/B/outputs/code_review.md", "Checked and not found to be bugs"),
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
                where = os.path.basename(path)
                logged.setdefault(ag, set()).add(f"{where} (code-review note)")
        if it.get("file"): files.append(it["file"])
        # file: first file name (strip agent notes like '(identical ...)')
        fname = ""
        for f in files:
            fname = re.sub(r"\s*\(.*?\)\s*", "", f).strip()
            if fname: break
        line_str = "; ".join(OrderedDict.fromkeys(lines))
        agents = [a for a in "AB" if a in logged]
        # outputs: check existence
        outs = [f"{pdir}/{o}" for ag in it.get("outputs", {}) for o in it["outputs"][ag]]
        missing = [o for o in outs if not os.path.exists(f"{REPO}/{o}")]
        if missing: sys.exit(f"missing output file(s) for {it['id']}: {missing}")
        demo = bool(outs) and it["effect"] in DEMO_EFFECTS
        ev = [f"{pdir}/{o}" for ag in it.get("evidence", {}) for o in it["evidence"][ag]]
        for e in ev:
            if not os.path.exists(f"{REPO}/{e}"): sys.exit(f"missing evidence file {e}")
        # independence
        notes = []
        indep = len(agents) == 2
        if not indep: notes.append("logged by one agent only")
        if it.get("prereg"):
            assert_quote(f"{pdir}/PREREG.md", it["prereg"])
            indep = False
            notes.append("pre-flagged in PREREG.md, which both agents received")
        if it.get("exposure"):
            path, quote, note = it["exposure"]
            assert_quote(path, quote)
            indep = False
            notes.append(note)
        has_fl = bool(fname) and bool(line_str)
        # status
        if it.get("out_of_scope"):
            status = "out of scope: not reproducibility"; reason = it["oos_reason"]
        elif it.get("pending"):
            chk = f"{REPO}/papers/05_FNTC1J/A/outputs/sdo_check.json"
            if os.path.exists(chk) and json.load(open(chk)).get("cancellation"):
                status = "verified finding"
                reason = ("file and line given; cancellation proven algebraically and numerically and SDO coefficient change "
                          "saved in papers/05_FNTC1J/A/outputs/sdo_check.json (CHANGELOG #4d: proof/demonstration substitutes "
                          "for independence, since PREREG pre-flagged it)")
            else:
                status = "pending re-check"
                reason = "re-check output papers/05_FNTC1J/A/outputs/sdo_check.json not yet present"
        elif has_fl and demo and indep:
            status = "verified finding"; reason = "file and line given; output change saved; found independently by A and B"
        else:
            status = "unverified agent observation"
            miss = []
            if not has_fl: miss.append("no file+line")
            if not demo: miss.append("no demonstrated output change on study outputs")
            if not indep: miss.append("not independently found by both agents")
            reason = "; ".join(miss)
        rows.append(OrderedDict(
            obs_id=it["id"], paper=P[pid], agents_logged=" and ".join(agents),
            logged_as_A="; ".join(sorted(logged.get("A", []))) or "not logged",
            logged_as_B="; ".join(sorted(logged.get("B", []))) or "not logged",
            file=fname, line=line_str, description=it["desc"], effect_type=it["effect"],
            demonstrated_output_change="yes" if demo else "no", output_file="; ".join(outs) if demo else "",
            evidence_files_no_output_change="; ".join(ev),
            independently_found_by_both="yes" if indep else "no", independence_note="; ".join(notes),
            status=status, status_reason=reason))
    # every issue-list entry mapped exactly once
    for (pid, ag), d in res.items():
        for i in range(len(d.get("bugs", []))):
            if used[(pid, ag, i)] != 1:
                sys.exit(f"issue-list entry {pid} {ag} [{i}] mapped {used[(pid, ag, i)]} times")
    n_entries = sum(len(d.get("bugs", [])) for d in res.values())
    # wording checks
    blob = json.dumps(rows)
    if re.search(r"\bbugs?\b", blob, re.I): sys.exit("forbidden word in output text")
    if "\u2014" in blob: sys.exit("em dash in output")
    out = f"{REPO}/batches/batch1_code_observations.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    ex_rows = []
    for pid, ag, item, reason, path, quote in EXCLUDED:
        assert_quote(path, quote)
        ex_rows.append(OrderedDict(paper=P[pid], agents=ag, item=item, reason_excluded=reason, source_file=path))
    if re.search(r"\bbugs?\b", json.dumps(ex_rows), re.I): sys.exit("forbidden word in excluded output")
    with open(f"{REPO}/batches/batch1_code_observations_excluded.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(ex_rows[0].keys())); w.writeheader(); w.writerows(ex_rows)
    # counts (computed)
    per = OrderedDict()
    for r in rows:
        per.setdefault(r["paper"], Counter())[r["status"]] += 1
    issue_list_counts = {P[pid]: {ag: len(res[(pid, ag)].get("bugs", [])) for ag in "AB"} for pid in P}
    counts = OrderedDict(
        n_observations=len(rows), n_issue_list_entries_mapped=n_entries,
        issue_list_entries_per_paper=issue_list_counts,
        by_status=dict(Counter(r["status"] for r in rows)),
        by_paper_and_status={k: dict(v) for k, v in per.items()},
        logged_by_both=sum(r["agents_logged"] == "A and B" for r in rows),
        independently_found_by_both=sum(r["independently_found_by_both"] == "yes" for r in rows),
        with_demonstrated_output_change=sum(r["demonstrated_output_change"] == "yes" for r in rows),
        n_excluded_items=len(ex_rows))
    json.dump(counts, open(f"{REPO}/batches/batch1_code_observations_counts.json", "w"), indent=1)
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
