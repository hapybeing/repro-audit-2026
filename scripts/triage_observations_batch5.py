"""Triage of code observations logged by agents A and B on batch 5 (papers 21-25). Same design and status rule as
scripts/triage_observations_batch5.py (copied from it; only the tables below, the file names and one added key differ);
batch 1 to 4 files are not touched. Batch 5 agents also logged items under results.json "code_observations" (22 A,
24 B, 25 A and B) and "uncertainties"; those are matched as notes with an asserted quote, like any other note.
Added key force_unverified: a written reason that keeps an item "unverified agent observation" when the two agents'
saved evidence does not support one description (24-2).

Writes:
  batches/batch5_code_observations.csv           one row per distinct code observation (A and B items matched)
  batches/batch5_code_observations_excluded.csv  items agents logged that are NOT code observations, with the reason
  batches/batch5_code_observations_counts.json   counts, all computed from the rows above

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
Usage: python3 scripts/triage_observations_batch5.py
"""
import csv, json, os, re, sys, hashlib
from collections import Counter, OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {"21": "21_LEFTNE", "22": "22_W2TSVL", "23": "23_FXRNBA", "24": "24_U9CKK6", "25": "25_914AN0"}


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


D21 = ("/workspace/audit_runs/21_LEFTNE/prereg/02- Replication_Appendix.R", "6cab25664aff17d0576e6b72046bfc68f67566b68ec6b35573157d3601694e85")
D22 = ("/workspace/audit_runs/22_W2TSVL/prereg/files/Framing Labor Action_Appendix A1.R", "72d139742fddc0c5449ff441f825454c77f535c696519091268a1290013af223")
D24a = ("/workspace/audit_runs/24_U9CKK6/prereg/dl/6_analysis1.R", "fd9d4d746528fd70865eaa159b0f246ca5f7fb256d032a8034b4c758e98a393e")
D24b = ("/workspace/audit_runs/24_U9CKK6/prereg/dl/9_analysis4.R", "4a6c15513c5a91c3c1f44eeaeb33b026f657cf62d65128d6f87c93933990428d")
D25 = ("/workspace/audit_runs/25_914AN0/prereg/deposit/code/functions.R", "28b5af1bd14d8bba9c907cb500f08c4357d438e2dc455eb21683391b575c5f8e")

ISSUES = [
    # ---------------- 21_LEFTNE ----------------
    dict(id="21-1", pid="21",
         desc="Under the SI Table A3 header (Study 2, NORC), line 87 of 02- Replication_Appendix.R tabulates PARTISANSHIP from df (the Study 1 Qualtrics data) instead of df_TESS, which every other row of the Table A3 block (lines 74 to 93) uses and which has its own PARTISANSHIP column. The printed SI Table A3 partisanship shares (Republican 34.98, Democrat 36.68, Independent 26.10 percent) equal the Study 1 shares of Table A1; the NORC data give Democrat 57.2, Independent 10.7 and Republican 31.9 percent. Descriptive table only; no target or estimate is affected.",
         sources=[("issue_list", "A", 0), ("issue_list", "B", 2)],
         outputs={"A": ["A/outputs/code_review_check.json"], "B": ["B/outputs/diag_code_review.txt", "B/outputs/si_tableA3_partisanship_excerpt.txt"]},
         effect="numeric", codecheck=(D21[0], D21[1], 87, "df %>%", "utf-8")),
    dict(id="21-2", pid="21",
         desc="Two car::recode specifications in 02- Replication_Appendix.R do not match the data levels: line 299 keys income on ' $50,000 - $59,999' with a leading space, so the 68 respondents at that level get NA instead of 6, and line 300 contains \"'Slightly conservative'; = 5;\", so the 58 'Slightly conservative' respondents get NA instead of 5. Those respondents drop out of the Ideology- and Income-controlled models (SI Tables A19 to A21). Shown by agent B's run; agent A's log prints the two lines but A did not test them. No target is affected.",
         sources=[("issue_list", "B", 0), ("issue_list", "B", 1)],
         outputs={"B": ["B/outputs/diag_code_review.txt"]},
         effect="numeric", codecheck=(D21[0], D21[1], 300, "'Slightly conservative'; = 5;", "utf-8")),
    # ---------------- 22_W2TSVL ----------------
    dict(id="22-1", pid="22",
         desc="The Table A4 block of Framing Labor Action_Appendix A1.R (lines 224 to 228) computes group means with mean() on unions, which line 58 makes an ordered factor, so every computed mean is NA with the warning 'argument is not numeric or logical: returning NA'. The Table A4 values are typed as constants at line 234, and those constants equal the group means computed from the data at 2 decimals (all 10 cells in B's check), so no printed number is affected.",
         sources=[("note", "A", "papers/22_W2TSVL/A/results.json", "Table A4 group means of `unions` are computed on an ordered factor, so mean() returns NA with a warning", "224"),
                  ("issue_list", "B", 0)],
         outputs={"A": ["A/outputs/appendix_stdout.txt", "A/outputs/code_observations_check.json"],
                  "B": ["B/outputs/appendix_run_stdout.txt", "B/outputs/appendix_run_stderr.txt", "B/outputs/check_tableA4_means.csv"]},
         effect="numeric", note_extra="PREREG.md noted that the Table A4 values are typed as constants; it did not note that the computed means are NA",
         codecheck=(D22[0], D22[1], 226, "dplyr::summarize(Mean = mean(unions, na.rm=TRUE))", "utf-8")),
    dict(id="22-2", pid="22",
         desc="The education recode at lines 110 to 121 of Framing Labor Action_Appendix A1.R maps d3 codes 1 to 12 and sends every other code to NA, including code 13 ('No tiene estudios', no schooling; 17 respondents) together with code 14 (NS/NC). This affects only the control-variable models (m3, m6, m9, m12) and the balance tables, not T1 to T6.",
         sources=[("note", "A", "papers/22_W2TSVL/A/results.json", "Education recode maps d3 codes 1-12 only; code 13 ('No tiene estudios', no schooling) becomes NA", "110"),
                  ("note", "B", "papers/22_W2TSVL/B/results.json", "Appendix A1.R lines 110-121 map education codes 1 to 12 and send everything else to NA", "110-121")],
         outputs={"A": ["A/outputs/code_observations_check.json"], "B": ["B/outputs/check_value_labels.txt"]},
         effect="row_count", file="Framing Labor Action_Appendix A1.R",
         intent_open="Both agents note that sending code 13 to NA may be a deliberate coding choice; the line does what it is written to do, and its intent cannot be shown from the deposit",
         codecheck=(D22[0], D22[1], 110, "dta$education_levels <- factor(ifelse(dta$d3 == 1", "utf-8")),
    # ---------------- 24_U9CKK6 ----------------
    dict(id="24-1", pid="24",
         desc="The Table 1 texreg call in Scripts/6_analysis1.R (line 410) writes the row 'Year Fixed Effects' = Yes for all four models, but the four Table 1 models (lines 356, 365, 374, 384) enter year as a numeric column, that is one linear year term, while other models in the same script and all Table 2 models use as.factor(year). The linear-year code reproduces the printed Table 1 Model 2 AIC 738747.50 and log likelihood -369309.75 exactly, so the printed numbers are those of the linear-year specification and the row label does not describe it. Refitting with as.factor(year) (R_c) gives T1 0.0174, which also rounds to 0.02 with p below 0.001.",
         sources=[("issue_list", "A", 0),
                  ("note", "B", "papers/24_U9CKK6/B/results.json", "the 'Year Fixed Effects' row label does not describe it", "356; 365; 374; 384; 410")],
         outputs={"A": ["A/outputs/fixef_all_cycle_AE_fit2.csv", "A/outputs/model_gof.csv", "A/outputs/robustness_bc.csv"],
                  "B": ["B/outputs/modelinfo_cycle_AE_fit2.txt", "B/outputs/R_c_factor_year.csv"]},
         effect="label", prereg="Table 1 prints \"Year Fixed Effects: Yes\" for all four models",
         codecheck=(D24a[0], D24a[1], 410, '"Year Fixed Effects" = c("Yes", "Yes", "Yes", "Yes")', "utf-8")),
    dict(id="24-2", pid="24",
         desc="The centering index list 117:118 at line 43 of Scripts/9_analysis4.R is the one used at line 35 of 6_analysis1.R, where column 118 is radical; script 9 adds columns before radical (lines 30 to 32), so 117:118 no longer selects radical. Agent A's saved column list shows that column 118 in script 9 is EU_sal (radical is column 119 of 119); agent B, from code reading with no saved output, names year_mon. Neither radical nor the column actually centred changes a Table 2 model input (EU_sal is re-centred by scale() at line 61 with the same mean), and the Table 2 AIC and log likelihood match, so T5 and T6 are not affected.",
         sources=[("issue_list", "A", 1),
                  ("note", "B", "papers/24_U9CKK6/B/results.json", "selects year_mon instead of radical", "30; 32; 36; 43; 47")],
         outputs={}, effect="none",
         evidence={"A": ["A/outputs/s9_column_index_check.csv", "A/outputs/model_gof.csv"]},
         force_unverified="no change to any model input or output; and the two agents name a different column at position 118 (A's saved column list shows EU_sal; B's year_mon comes from code reading with no saved output), so the evidence does not support one description",
         codecheck=(D24b[0], D24b[1], 43, "117:118", "utf-8")),
    dict(id="24-3", pid="24",
         desc="Lines 132 and 246 of Scripts/6_analysis1.R use variables right and left, which no deposited script creates and which are not columns of EP_debates_07062023.Rdata, so a top-to-bottom run of the script would stop at line 132. These models feed appendix results, not T1 to T6; neither agent ran these lines (the pre-registered target blocks avoid them). This is the basis of the alternative class C for 24_U9CKK6.",
         sources=[("issue_list", "A", 2),
                  ("note", "B", "papers/24_U9CKK6/B/results.json", "Models at lines 132 and 246 use `right` and `left`, which no deposited script creates", "132; 246")],
         outputs={}, effect="none",
         prereg="use variables `right` and `left` that are not created in any deposited script",
         codecheck=(D24a[0], D24a[1], 132, "chall_fact*right", "utf-8")),
    # ---------------- 25_914AN0 ----------------
    dict(id="25-1", pid="25",
         desc="The helper tlagz (functions.R line 102) refers to X_ instead of its argument data; tlagz is defined but not called anywhere in run2_main.R, so no output depends on it.",
         sources=[("note", "A", "papers/25_914AN0/A/results.json", "tlagz (functions.R line 102) refers to X_ instead of its argument data", "102"),
                  ("note", "B", "papers/25_914AN0/B/results.json", "functions.R line 102 (tlagz) refers to X_ instead of its argument data", "102")],
         file="functions.R", outputs={}, effect="none",
         codecheck=(D25[0], D25[1], 102, "X_[", "utf-8")),
    dict(id="25-2", pid="25",
         desc="In ensemble_modz, functions.R lines 256 and 290 assign a column 'Y' while the fixed-effects formula uses 'y'; 'y' already holds the same outcome from the preceding lmer call (lines 240 and 274). Agent A's refit with y set explicitly gives the same MIA coefficient as the authors' object, so no result changes.",
         sources=[("note", "A", "papers/25_914AN0/A/results.json", "functions.R lines 256 and 290 assign column 'Y' but model_fe uses 'y'", "256; 290")],
         file="functions.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/robust_bc.csv", "A/outputs/mermods_fe_pop.csv"]},
         codecheck=(D25[0], D25[1], 256, 'c("Y","weights")', "utf-8")),
    dict(id="25-3", pid="25",
         desc="The article prose (p. 180) gives the NKVD effect on the KIA share as 0.52 and on the medals share as -0.34; the appendix Table A2.3 and the authors' deposited results/tabA2_3.tex give 0.629 and -0.287, which both runs reproduce (T2, T3). The prose values are not produced by the deposited code. MIA, POW and the war-level target agree with the prose.",
         sources=[("note", "A", "papers/25_914AN0/A/results.json", "The prose values are not reproduced by the deposited code", ""),
                  ("note", "B", "papers/25_914AN0/B/results.json", "the code and appendix Table A2.3 give 0.629 and -0.287 (reproduced)", "")],
         file="run2_main.R", outputs={}, effect="none",
         evidence={"A": ["A/outputs/targets_extracted.csv"], "B": ["B/outputs/targets_extracted.csv", "B/outputs/appendix_tabA2_3_excerpt.txt"]},
         out_of_scope=True,
         oos_reason="Article prose versus the appendix table; the code reproduces the table values that are the pre-registered targets (pre-run decision #4), so this is a text-versus-table difference, not a reproducibility failure."),
]

EXCLUDED = [
    ("21", "A and B", "Figure statements wrapped in try() (A) or the default graphics device set to cairo PNG (B) after 'invalid font type' from hrbrthemes Roboto Condensed", "plot-only environment fix allowed by PREREG.md; no estimation line changed",
     "papers/21_LEFTNE/A/results.json", "PREREG-listed plot-only fix; no estimation line changed"),
    ("21", "B", "Figure B4 statements wrapped in try() after 'unused argument (connect.lines = FALSE)' under ggeffects 2.2.1", "figure-only environment fix allowed by PREREG.md",
     "papers/21_LEFTNE/B/results.json", "unused argument (connect.lines = FALSE)"),
    ("21", "A and B", "Current CRAN packages used (lavaan 0.7.3, mediation 4.5.1 and others); none pinned by the authors", "package-version environment note; lavaan 0.6.19 gives identical T1 and T2",
     "papers/21_LEFTNE/A/results.json", "lavaan 0.6.19 (system Debian) gives identical T1/T2"),
    ("21", "A and B", "T6, the Table 3 N: 698 in both runs and in the authors' printed log against 697 printed; CES2020.RDS holds 698 compliers", "target mismatch; the basis of class C, reported in the report and batch5_targets.md, not a code observation",
     "papers/21_LEFTNE/A/results.json", "the deposited CES2020.RDS has 698 compliers with complete data, so the code cannot give 697"),
    ("21", "A and B", "SI Table A8: the printed values equal the lavaan SEM indirect effects (T1 and T2 models), not the output of the deposited mediate() code under the Table A8 header, whose ACMEs equal the 3-arm SEM of R_c", "printed non-target table (candidate 2 for T1 and T2, which does not set the class); reported in the per-paper section of the batch report, not a code observation",
     "papers/21_LEFTNE/A/results.json", "So Table A8 appears to come from the lavaan model rather than the A8 code block"),
    ("21", "B", "SI Table A5 'Gender-Edu' intercept prints 0.12; the run's export_summs shows 0.13", "printed non-target number, not a code observation",
     "papers/21_LEFTNE/B/results.json", "SI Table A5 'Gender-Edu' intercept prints 0.12 in the SI"),
    ("21", "A", "Sandbox restarted during A's package installs", "process note; the install resumed and every reported number comes from a completed process",
     "papers/21_LEFTNE/A/LOG.md", "Sandbox restarted at about 21:12 UTC"),
    ("22", "A and B", "Absolute Windows data path at line 14 replaced by the relative file name; install.packages() lines commented out; browseURL() made a no-op", "pre-registered environment fixes (pre-run decision #3)",
     "papers/22_W2TSVL/A/results.json", "absolute Windows data path at line 14 replaced by the relative file name"),
    ("22", "A and B", "The batch brief names line 15 for the path; the path is on line 14 of both scripts", "note on the audit's brief, not a code observation",
     "papers/22_W2TSVL/A/results.json", "Batch brief mentions 'path line 15' for paper 22"),
    ("22", "A and B", "Weighted-model Ns 975 and 962 (Tables A1 and A2, column 2) differ from the unweighted Ns; MASS::polr reports the sum of the weights as N", "printed non-target numbers reproduced by the code, not a code observation",
     "papers/22_W2TSVL/B/results.json", "MASS::polr reports the sum of the weights Ponderador as N"),
    ("22", "B", "Text p. 1261 prints a union-influence mean of 3.17; the data give 3.1773; and the text says 1,010 respondents where the data file has 1011 rows", "printed non-target numbers, not a code observation",
     "papers/22_W2TSVL/B/results.json", "so the printed 3.17 reads as truncated"),
    ("22", "A and B", "Figure code at lines 212 and 252 of the main script passes an undefined color positionally in aes(); it ran without error in both runs", "figure code with no observed effect in either run; not a code observation",
     "papers/22_W2TSVL/A/results.json", "passes an undefined `color` positionally"),
    ("22", "B", "An ls of the paper folder showed that a folder named A exists; nothing in it was opened", "process note on blinding",
     "papers/22_W2TSVL/B/results.json", "showed that a folder named A exists; nothing in it was opened or read"),
    ("23", "A and B", "No author file edited; folder layout, ?format=original downloads and LC_ALL=C.UTF-8 only", "pre-registered environment fixes (pre-run decision #3)",
     "papers/23_FXRNBA/A/results.json", "Dataverse ?format=original CSVs used"),
    ("23", "A and B", "Supplementary Information (Tables B1 to B14) not compared: it could not be opened during pre-registration", "materials-access limitation, reported in Limitations",
     "papers/23_FXRNBA/A/results.json", "could not be opened during pre-registration (captcha)"),
    ("23", "A and B", "The step that built the merged station-day CSVs from raw sources is not deposited", "data-statement finding (pre-run decision #7); no target depends on it",
     "papers/23_FXRNBA/A/results.json", "The upstream build of the merged station-day CSVs from raw sources is not deposited"),
    ("23", "A", "The sandbox restarted once during A's full run, which was rerun from scratch", "process note; subset and full runs gave identical target numbers",
     "papers/23_FXRNBA/A/results.json", "The sandbox restarted once mid-run"),
    ("23", "A and B", "Exploratory, not pre-registered: listwise deletion over Model 3 variables only gives the same 7163 rows (PREREG inconsistency 1)", "exploratory check (CHANGELOG_METHOD.md #4e), not a code observation",
     "papers/23_FXRNBA/A/results.json", "PREREG inconsistency 1 has no effect on this deposit"),
    ("24", "A and B", "Only the pre-registered target blocks of 6_analysis1.R (lines 1 to 53 and 346 to 416) and 9_analysis4.R (lines 1 to 123) were run, unchanged, with saveRDS after each model", "pre-registered environment fix (pre-run decision #2); alternative class C shown in batches/batch5_class_rules.json",
     "papers/24_U9CKK6/B/results.json", "ran 6_analysis1.R lines 1-53 and 346-416 verbatim (class decision 2)"),
    ("24", "A and B", "Pre-registered memory fallbacks F1 (blank unused text columns after load) and F2 (save, remove and rebuild the table from saved models): A for Table 1 and Table 2; B for Table 1 Model 4 only", "pre-registered environment fix (pre-run decision #3); no estimation line, sample filter or seed changed",
     "papers/24_U9CKK6/A/results.json", "pre-registered memory fallback F1"),
    ("24", "A and B", "parlgov CSVs (script 4) and the Eurobarometer .dta (script 10) are not deposited", "data-statement finding (pre-run decision #7), recorded in DATA_STATEMENT.md and ABSENCE_SEARCHES.md; no target needs them",
     "papers/24_U9CKK6/A/results.json", "parlgov CSVs for script 4 and the Eurobarometer .dta for script 10 are absent from the deposit"),
    ("24", "A and B", "R_a bootstrap size differs between runs (A K = 115, B K = 178) because the pre-registered timing rule uses each run's first refit time", "pre-registered timing rule; both runs reported in the batch report",
     "papers/24_U9CKK6/B/results.json", "K rule = 178 (first refit 20.21 s)"),
    ("24", "B", "B's bootstrap was stopped by its wall-time deadline after 166 draws and resumed from the saved draws to K = 178", "process note; the pre-generated draws were not changed",
     "papers/24_U9CKK6/B/results.json", "The bootstrap was stopped once by the wall-time deadline at 166 draws"),
    ("24", "A", "The sandbox restarted during A's bootstrap; the remaining draws ran after the restart with the same saved draws", "process note; every reported number comes from a completed process",
     "papers/24_U9CKK6/A/results.json", "measured before a sandbox restart"),
    ("24", "A", "Saved models (11 to 29 MB each) are kept in scratch, not in outputs/", "storage note; sha256 in A's LOG.md",
     "papers/24_U9CKK6/A/results.json", "Saved models (11 to 29 MB each)"),
    ("25", "A and B", "lfe 3.1.1 instead of pinned 3.0-0 and a newer data.table than pinned 1.15.4 (the pinned versions do not compile under R 4.5); V8 built with a static library for SUNGEO", "pre-registered package fallbacks (pre-run decision #3)",
     "papers/25_914AN0/A/results.json", "lfe 3.1.1 instead of pinned 3.0-0"),
    ("25", "A and B", "mc.cores wrapped in max(1, ...) at functions.R line 306", "pre-registered environment fix (pre-run decision #3)",
     "papers/25_914AN0/A/results.json", "mc.cores = max(1, ...) at functions.R line 306"),
    ("25", "A and B", "Random-effects results (Table A2.4 and two Hausman p cells of Table A2.3, not targets) differ from the deposited tables in A's staged run and in B's first staged run, and match them in B's second staged run. B shows the cause: the staged route loads X_s with readRDS, which returns a data.table without column over-allocation, and ensemble_modz (functions.R lines 240, 256, 274, 290) assigns the weights column by reference inside the data= argument, so the pop-weights lmer fit silently keeps the old weights; with data.table::setalloccol(X_s), the state the authors' one-session run has after line 58, the tables match", "behaviour of the audit's staged run, not of the deposited one-session pipeline; reported in the batch report; the fixed-effects targets are identical in every run",
     "papers/25_914AN0/B/results.json", "When X_s is a data.table without column over-allocation (e.g. loaded with readRDS)"),
    ("25", "A", "The authors' results/ files were briefly extracted into the run folder and removed before the model stage ran", "process note; the regenerated files compared carry run-date times",
     "papers/25_914AN0/A/results.json", "briefly extracted into RUNDIR/Replication_IO/results/ by my mistake"),
    ("25", "A", "Three errors in A's own robustness scripts were found and fixed before the final outputs", "note on the audit's scripts, not on the authors' code",
     "papers/25_914AN0/A/results.json", "Three errors in my own robustness scripts were found and fixed"),
    ("25", "A", "Figure 1 was not regenerated in A's staged run", "figure not a target",
     "papers/25_914AN0/A/results.json", "Figure 1 png was not regenerated"),
    ("25", "B", "A short concurrent R process ran while B's bootstrap was running", "process note",
     "papers/25_914AN0/B/results.json", "A short concurrent R process (environment listing) ran briefly"),
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
        if it.get("force_unverified"):
            status = "unverified agent observation"; reason = it["force_unverified"]
        elif it.get("out_of_scope"):
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
    with open(f"{REPO}/batches/batch5_code_observations.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    ex_rows = []
    for pid, ag, item, reason, path, quote in EXCLUDED:
        assert_quote(path, quote)
        ex_rows.append(OrderedDict(paper=P[pid], agents=ag, item=item, reason_excluded=reason, source_file=path))
    if re.search(r"\bbugs?\b", json.dumps(ex_rows), re.I): sys.exit("forbidden word in excluded output")
    if "\u2014" in json.dumps(ex_rows): sys.exit("em dash in excluded output")
    with open(f"{REPO}/batches/batch5_code_observations_excluded.csv", "w", newline="") as f:
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
    json.dump(counts, open(f"{REPO}/batches/batch5_code_observations_counts.json", "w"), indent=1)
    print(json.dumps(counts, indent=1))
    for r in rows: print(r["obs_id"], r["status"], "|", r["status_reason"])


if __name__ == "__main__":
    main()
