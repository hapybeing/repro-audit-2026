"""Agent B: build results.json from files in outputs/ and the frozen targets.json. No hand-typed numbers for
reproduced values: reproduced values are read from outputs/ (none exist, because the run stopped)."""
import json, re, os, datetime
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.dirname(B)
targets = json.load(open(os.path.join(PAPER, "targets.json")))
run = json.load(open(os.path.join(B, "outputs/run_status.json")))
inv = json.load(open(os.path.join(B, "outputs/inputs_and_open_routes.json")))
iso = json.load(open(os.path.join(B, "outputs/isotope_correction_mapping.json")))
si = json.load(open(os.path.join(B, "outputs/si_published_context.json")))
reproduced_file = None  # an authors' experiment1_proteoform_df_*.csv would be read here; none was produced
outs = os.listdir(os.path.join(B, "outputs"))
produced = [f for f in outs if f.startswith("experiment1_proteoform_df_")]
assert not produced, "unexpected authors' output present; extend this script to parse it"
stop = f"Notebook stopped at Rmd line 498 (purled line {run['failing_purled_line']}): `{run['failing_code']}` -> '{run['error_message']}'"
T = []
for t in targets:
    T.append({"id": t["id"], "description": t["description"], "paper_value": t["paper_value"],
              "paper_rounding_decimals": t["paper_rounding_decimals"], "reproduced_value": None, "source_file": "outputs/run_status.json",
              "abs_diff": None, "rel_diff": None, "match_to_rounding": None, "within_5pct": None, "same_conclusion": None,
              "note": "Not computed. " + stop + ". Byonic_results.csv is not in the deposit and no open route was found (outputs/inputs_and_open_routes.json)."})
# Context check that PREREG paper values equal the published SI (not a reproduction)
s3 = si["sheets"]["TableS5_DMSO_MS275_quantifiabl"]["K9ac_K14ac_K23ac_K27me2"]; s4 = si["sheets"]["TableS4_DMSO_Corin_quantifiable"]["K9ac_K14ac_K23ac_K27me2"]
T[2]["note"] += f" Published SI value read by script equals paper_value: {s3['cumulative_log2-fold_change'] == T[2]['paper_value']}."
T[3]["note"] += f" Published SI value read by script equals paper_value: {s4['cumulative_log2-fold_change'] == T[3]['paper_value']}."
T[4]["note"] += f" Published SI Table S3 data rows counted by script: {si['sheets']['TableS3_DMSO_MS275_proteoforms']['n_data_rows']}."
T[0]["note"] += f" For context, 100*(2^fc-1) on the published SI value = {s3['pct_increase_100x(2^fc-1)']:.2f} (floor {int(s3['pct_increase_100x(2^fc-1)'])})."
T[1]["note"] += f" For context, 100*(2^fc-1) on the published SI value = {s4['pct_increase_100x(2^fc-1)']:.2f} (floor {int(s4['pct_increase_100x(2^fc-1)'])})."
why_rob = "Not run: needs scan-level TMT reporter intensities (assigned_fractional_intensity_hits) created by the pipeline after Rmd line 498; the pipeline cannot pass line 498 because Byonic_results.csv is not deposited. SI tables hold only per-proteoform summaries."
R = [{"id": i, "description": d, "ran": False, "estimate": None, "se_or_ci": "", "p_value": None,
      "same_direction_and_significance_as_paper": None, "source_file": "outputs/run_status.json", "note": why_rob}
     for i, d in [("R_a", "Scan-level bootstrap of fc_cum for K9ac K14ac K23ac K27me2, B=2000, seed 20261009, percentile 95% CI"),
                  ("R_b", "Drop the most outlying channel per condition (by channel mean log2_cum), Welch t-test on 2 vs 2 channels"),
                  ("R_c", "Replicate-level Welch t-test on per-channel means (n=3 vs n=3)")]]
diff_terms = [t for t in iso["terms"] if t["differs"]]
ex = iso["terms"][0]
bugs = [{"file": "Byonic_Middle-Down_Processing_Notebook.Rmd", "line": iso["rmd_line_of_block_start"],
         "description": "TMT isotope-impurity correction takes each leakage coefficient from the corrected channel's own impurity vector instead of from the neighbouring reagent's vector, so most cross-talk terms use the wrong coefficient (e.g. reagent 126's +1 leak of 0.076 is subtracted from channel 126 using the 127 intensity, while nothing is subtracted from 127 for 126's leak).",
         "evidence": f"Rmd lines {iso['rmd_line_of_block_start']}-{iso['rmd_line_of_block_start']+23}: `126_corrected` = 126_intensity*TMT126[3] - (127_intensity*TMT126[4] + ...); vectors defined at lines 22-27 with comment 'reference c(-2, -1, monoisotopic, +1, +2)'. Script 05 finds {len(diff_terms)} of {iso['n_terms']} subtraction terms differ from the standard first-order mapping (coefficient of reagent j at offset k-j). Impact on the targets cannot be quantified without the input data; all coefficients are <= 0.076. Caveat: assumes the vectors are per-reagent isotope distributions (as the Rmd comment and the usual TMT certificate of analysis convention state). See outputs/isotope_correction_mapping.json."}]
log = open(os.path.join(B, "LOG.md")).read()
times = re.findall(r"^- (\d\d):(\d\d) ", log, re.M)
mins = (int(times[-1][0]) * 60 + int(times[-1][1])) - (int(times[0][0]) * 60 + int(times[0][1]))
res = {"paper_id": "03_3IOGQ8", "agent": "B", "run_date_ist": "2026-10-09", "ran": False,
       "could_not_run_reason": stop + ". The Byonic PSM export (output of commercial Byonic software) is not in the Dataverse deposit (files: " + ", ".join(f["name"] for f in inv["deposit_files"]) + "), nor is the search FASTA; no PRIDE/MassIVE/ProteomeXchange deposit or other open source exists (paper, preprint and SI cite only the Dataverse DOI).",
       "targets": T, "robustness": R, "bugs": bugs,
       "env_fixes": ["diffs/notebook_envfix.Rmd.diff: working directory placeholder 'C:/Users/your_file_path/' replaced by the scratch run folder; library(mzR) commented out because mzR is not installed and is first used at line 671, after the stopping point at line 498 (no effect on any value)."],
       "proposed_class": "C",
       "class_reason": "Materials incomplete: the notebook's only tabular input (Byonic_results.csv) and the search FASTA are not deposited, though the dataset description promises processed data, so no target can be computed. PREREG's pre-set rule suggested E; under PROTOCOL section 7 the cause is missing files (C), with commercial Byonic as a secondary barrier.",
       "confidence": "medium",
       "confidence_reason": "Facts (missing input, no open route, stop at line 498) were verified by script; the C versus E boundary is a judgement and differs from PREREG's suggested E.",
       "time_minutes": mins,
       "uncertainties": [
         "Class C vs E is a judgement: PROTOCOL's E examples are compute or system dependencies; here the blocker is an undeposited intermediate file that only commercial software (Byonic, plus an undeposited FASTA) can regenerate. PREREG section 2 pre-set E.",
         "Repository search covered PRIDE, ProteomeXchange (PROXI keyword search) and the MassIVE public listing, plus paper, preprint and SI text; jPOST, iProX and Panorama Public were not searched separately (ProteomeXchange indexes them).",
         "RAW files were not downloaded (no open route uses them without the Byonic export), so their integrity was not checked beyond Dataverse md5 metadata.",
         "The isotope-correction finding assumes the TMT1xx vectors are per-reagent isotope distributions; the reporter ions actually read are the ETD reporters (114-119 m/z, TMT_ETD_mz_values), for which manufacturer HCD-reporter impurity values may not map one-to-one. Its numerical effect is unknown.",
         "PEP.2D is joined back from all experiments by scan_number and PID (Rmd ~line 1449); if several MS files share one Byonic export this could duplicate rows. Could not be checked without the export; not listed as a bug.",
         "The SI zip from Europe PMC had a different sha256 from the one in PREREG, but the xlsx and PDF inside are byte-identical to PREREG's.",
         "Paper text values 155 % and 110 % differ from 100*(2^fc-1) on the published SI values (156.10 %, 110.99 %); consistent with truncation (noted in PREREG)."]}
json.dump(res, open(os.path.join(B, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["ran", "proposed_class", "confidence", "time_minutes"]}), [t["note"][-90:] for t in T])
