"""Build results.json for 03_3IOGQ8 / Agent A from files in outputs/ and targets.json.
No reproduced number is typed here: reproduced values are read from outputs/ when an output
exists; for this paper the pipeline could not reach any output, so they are null.
Usage: python3 build_results.py <A dir> <paper dir>"""
import json, os, re, sys, datetime

A, P = sys.argv[1], sys.argv[2]
out = os.path.join(A, "outputs")
targets = json.load(open(os.path.join(P, "targets.json")))
partial = open(os.path.join(out, "partial_run_log.txt")).read()
tests = json.load(open(os.path.join(out, "code_review_tests.json")))
inv = open(os.path.join(out, "input_inventory.txt")).read()

# Facts parsed from outputs (used in reasons, not typed)
stop = re.search(r"Rmd line (\d+): Byonic_df <- read.csv\(\"Byonic_results.csv\"\)\n\s+-> (ERROR: [^\n]+)", partial)
stop_line, stop_err = (stop.group(1), stop.group(2)) if stop else (None, None)
byonic_exists = re.search(r"file.exists\('Byonic_results.csv'\)[^:]*: (\w+)", partial).group(1)
n_files = len(re.findall(r"^\d{8} ", inv, flags=re.M))

# The reproduced proteoform csv would be outputs/experiment1_proteoform_df_*.csv; check
repro_csvs = [f for f in os.listdir(out) if f.startswith("experiment1_proteoform_df_")]
assert not repro_csvs, "a reproduced proteoform table exists; extend this script to parse it"

reason = (f"The notebook's only tabular input Byonic_results.csv (PSM export from the commercial Byonic search engine) "
          f"is not in the dataset ({n_files} files: two Thermo RAW files and the Rmd) and no open copy was found; "
          f"execution stops at Rmd line {stop_line} ({stop_err}); file.exists = {byonic_exists}.")
res_t = []
for t in targets:
    res_t.append({"id": t["id"], "description": t["description"], "paper_value": t["paper_value"],
                  "paper_rounding_decimals": int(t.get("paper_rounding_decimals", 0)),
                  "reproduced_value": None, "source_file": None, "abs_diff": None, "rel_diff": None,
                  "match_to_rounding": None, "within_5pct": None, "same_conclusion": None,
                  "note": "Not reproduced: pipeline cannot reach the step that writes experiment1_proteoform_df (missing Byonic_results.csv). "
                          "Published SI value recorded for reference in outputs/si_published_values.json (paper side, not a reproduction)."})
rob_reason = ("Not run: needs scan-level TMT reporter intensities (assigned_fractional_intensity_hits / TMT_single_scan_df) that exist only "
              "inside the pipeline after the Byonic PSM table is read; SI tables hold only per-proteoform summaries (PREREG section 3).")
rob = [{"id": i, "description": d, "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
        "same_direction_and_significance_as_paper": None, "source_file": None, "note": rob_reason}
       for i, d in [("R_a", "Scan-level bootstrap of fc_cum for K9ac K14ac K23ac K27me2, B=2000, seed 20261009, percentile 95% CI"),
                    ("R_b", "Drop the most outlying channel per condition (furthest channel mean from condition mean), 2 vs 2 Welch t-test and fc_cum"),
                    ("R_c", "Replicate-level Welch t-test, one mean log2_cum per channel, n=3 vs 3")]]
t1 = tests["test1_neutral_loss"]; t2 = tests["test2_tmt_correction"]
bugs = [
 {"file": "Byonic_Middle-Down_Processing_Notebook.Rmd", "line": 195,
  "description": "Off-by-one in generate_ions_for_sequence: the Kme3/pST/Ksu neutral-loss ions for fragment i (lines 195-284) are computed from a_mass..z_mass before these are recomputed for fragment i (lines 287-291), i.e. from fragment i-1 of the previous loop iteration (and, for i=1 of each new charge state, from the last fragment of the previous charge state).",
  "evidence": f"outputs/code_review_tests.json test1: authors' function on H3.1 tail with K9me3; b_nl_Kme3 equals previous-fragment b ion minus 59.073499: {t1['code_equals_previous_fragment_minus_loss']}; equals same-fragment minus loss: {t1['code_equals_same_fragment_minus_loss']}; c ions previous-fragment: {t1['c_code_equals_previous_fragment_minus_loss']}; charge 2: {t1['b_charge2_code_equals_previous_fragment_minus_loss']}. Affects fragment-ion matching and so matched intensities (proteoform_intensity, percent_abundance); TMT fold changes are read separately (find_intensities_for_scan) so the direct effect on T3/T4 is expected to be small. Impact on published numbers could not be measured (no data)."},
 {"file": "Byonic_Middle-Down_Processing_Notebook.Rmd", "line": 2662,
  "description": "TMT isotope-impurity correction appears transposed relative to the per-reagent vectors defined at lines 21-27 (comment: c(-2, -1, monoisotopic, +1, +2)): channel X subtracts neighbour intensity times reagent X's own impurity fraction, instead of neighbour reagent's impurity toward X. Probable bug; judged from the code's own stated convention.",
  "evidence": f"outputs/code_review_tests.json test2: authors' expression (Rmd lines {t2['expression_rmd_lines'][0]}-{t2['expression_rmd_lines'][1]}) on a synthetic scan with only reagent 126 (126=1000, its +1 spill 127=76) returns 126_corrected={t2['corrected']['126_corrected']}, 127_corrected={t2['corrected']['127_corrected']}, 128_corrected={t2['corrected']['128_corrected']} instead of 1000/0/0. Affects every log2_cum value and so fc_cum (T1-T4); size of effect on published values not measurable without data."},
 {"file": "Byonic_Middle-Down_Processing_Notebook.Rmd", "line": 1867,
  "description": "Probable wrong argument: extract_intensities(scan_number, PID, ions_list, grouped_list) (line 1383) selects the ion group with .x$PID == PID, but in the 2- and 3-PSM sections it is called with rank_order (1, 2, 3; assigned by row_number() at lines 1466/2337) in the PID position (lines 1867, 1898, 2132, 2404, 2441), whereas the single-PSM section passes PID (lines 1552, 1614).",
  "evidence": "Code only: grouped_ion_intensity_list is grouped by (scan_number, PID) at lines 1478-1479. Unless Byonic PID values coincide with the per-scan rank, these calls return intensities of a different PSM or none. Could not be confirmed against data (Byonic export not available). Affects intensities of multi-PSM scans (proteoform_intensity, percent_abundance), not the single-hit TMT t-test behind T3/T4."},
]
time_minutes = None
log = open(os.path.join(A, "LOG.md")).read()
ts = re.findall(r"\b(\d{2}):(\d{2}) IST", log)
if len(ts) >= 2:
    m = [int(h) * 60 + int(mm) for h, mm in ts]
    time_minutes = max(m) - min(m)
res = {"paper_id": "03_3IOGQ8", "agent": "A", "run_date_ist": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d"),
       "ran": False, "could_not_run_reason": reason, "targets": res_t, "robustness": rob, "bugs": bugs,
       "env_fixes": ["diffs/01_working_directory.diff: line 10 placeholder 'C:/Users/your_file_path/' replaced by the run directory so setwd() works; only fix needed to reach the missing-input stop at line 498"],
       "proposed_class": "C",
       "class_reason": ("Materials incomplete: the deposited notebook cannot produce Tables S2-S5 because its input, the Byonic PSM export (plus the search FASTA and the "
                        "RAW-to-mzML step), is not deposited, and the Rmd is a template with placeholder paths and experiment aliases. "
                        "Section 7 lists missing files under C; E is for an available pipeline blocked by compute or an uninstallable dependency. PREREG section 2 anticipated E; see uncertainties."),
       "confidence": "medium",
       "confidence_reason": "That nothing can run is verified by script; the C vs E choice is a judgement (PREREG pre-stated E) and bugs 2-3 could not be checked on data.",
       "time_minutes": time_minutes,
       "uncertainties": [
         "C vs E: PREREG section 2 (frozen) pre-states 'propose class E ... noting the underlying reason (C)'. Protocol section 7 wording ('missing files' under C; E 'e.g. exceeds compute, missing system dependency that cannot be installed') fits C better, because the blocking item is an undeposited intermediate data file, not a compute or install limit. Both agree nothing could be reproduced; the batch report should flag this so A and B are compared on the same reading.",
         "A Byonic licence would not suffice on its own: the search FASTA ('histone protein sequences, common contaminants' plus two tail sequences) is not deposited, Byonic version and full settings beyond the Methods paragraph are not given, and MS alias names for the experiment filter are placeholders.",
         "No public PRIDE/MassIVE/ProteomeXchange deposit was found for this paper: none cited in the paper (Europe PMC full text), the bioRxiv preprint text, or the SI PDF; PRIDE keyword search and a web search returned nothing relevant. The dataset description says 'Raw and processed bottom-up and middle-down mass spectrometry data' but only two RAW files and the Rmd are deposited (no processed data, no bottom-up data). An undiscovered deposit cannot be ruled out.",
         "Re-deriving the PSM table with an open search engine was not attempted: it would change the authors' analysis (PREREG section 2 forbids it).",
         "mzR was not installed (not needed to reach the stop point). The two RAW files (about 499 MB) were not downloaded; their MD5s from Dataverse metadata are in checksums.sha256.",
         "Bug 2 (TMT correction) is judged against the impurity convention stated in the Rmd's own comment; if the authors' vectors were meant in the transposed sense the code would be correct. Bug 3 depends on what Byonic's PID column holds.",
         "Not counted as bugs (observations): volcano classification uses 'cum_p_value > 0.5' (line 2999, same for mean and median versions) where 0.05 seems intended, but the case_when order makes the outcome identical; scans with 4-10 PSMs are split out (lines 1703-1744) but never merged into assigned_fractional_intensity_hits, so they are silently dropped; experiment1/2/3 filters all use the same placeholder alias.",
         "T1/T2 note from PREREG: published SI fc values give 156.10% and 110.99% by 100*(2^fc-1) (outputs/si_published_values.json), so the text values 155 and 110 do not equal SI rounded to 0 decimals; irrelevant to the class here since nothing was reproduced."
       ]}
json.dump(res, open(os.path.join(A, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["ran", "proposed_class", "confidence", "time_minutes"]}))
print(reason)
