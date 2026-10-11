"""Stage batch 5 files from the working repo into a git clone, applying the publication exclusions.
Usage (from repo/): python3 scripts/stage_publish_batch5.py <clone_dir> [--dry]
Writes batches/batch5_publish_exclusions.tsv (path, bytes, reason) in the working repo first, then copies every
included file into the clone (same relative path), plus the top-level copies batch5_report.md and batch5_targets.md.
Copied from the batch 4 staging script. Two additions for batch 5, in the same spirit: figure PDFs written by the
authors' plotting code are treated like png images, and the HTML tables that 23_FXRNBA's code writes with kableExtra
are excluded because each embeds third-party JavaScript (jQuery and others) and they are regenerable.
Rules (as for batch 3): R data objects and session images derived from the third-party deposit are excluded
(regenerable with the agents' scripts); full or patched copies of the authors' code are excluded (licence varies; the
change is in diffs/); article full-text copies and images would be excluded; any file over 10 MB is excluded."""
import os, shutil, sys

CLONE = sys.argv[1]
DRY = "--dry" in sys.argv
MAXB = 10 * 1024 * 1024
PIDS = ["21_LEFTNE", "22_W2TSVL", "23_FXRNBA", "24_U9CKK6", "25_914AN0"]
COPY = "full copy of the authors' target-block lines with the audit's environment lines added (licence varies); the change is in diffs/"
AUTHOR_COPIES = {
    "scripts/run_table1_plain.R": COPY, "scripts/run_table1_f1f2.R": COPY, "scripts/run_table2_plain.R": COPY,
    "scripts/run_table2_f1f2.R": COPY, "scripts/run_table1.R": COPY, "scripts/run_table1_F1F2.R": COPY,
    "scripts/run_table2.R": COPY, "scripts/run_table2_F1F2.R": COPY,
    "scripts/run_table1_ranges_verbatim.R": "full copy of the authors' target-block lines (licence varies); the run is described in diffs/",
    "scripts/run_table2_ranges_verbatim.R": "full copy of the authors' target-block lines (licence varies); the run is described in diffs/",
    "scripts/texreg_table1_from_rds.R": "copy of the authors' texreg call run on saved models (licence varies); the change is in diffs/",
    "scripts/texreg_table2_from_rds.R": "copy of the authors' texreg call run on saved models (licence varies); the change is in diffs/",
}


def rule(p):
    b = os.path.basename(p)
    rel = "/".join(p.split("/")[3:]) if p.startswith("papers/") else p  # path inside A/ or B/
    if b.endswith((".rds", ".RData", ".rda", ".dta", ".nc", ".HDF", ".HDF4")):
        return "R data object, session image or dataset derived from the third-party deposit (regenerable with the agent's scripts)"
    if rel in AUTHOR_COPIES:
        return AUTHOR_COPIES[rel]
    if b.endswith((".png", ".jpg", ".jpeg")) or "pdftotext" in b or "fulltext" in b.lower():
        return "image or article full-text copy"
    if b.endswith(".pdf"):
        return "figure image written by the authors' plotting code (regenerable)"
    if b.endswith(".html"):
        return "table written as HTML by the authors' code with embedded third-party JavaScript (jQuery and others); regenerable with the agent's scripts"
    if "__pycache__" in p:
        return "build artefact"
    if os.path.getsize(p) > MAXB:
        return "over 10 MB"
    return None


inc, exc = [], []
for pid in PIDS:
    for ag in "AB":
        for r, _, fs in os.walk(f"papers/{pid}/{ag}"):
            for f in sorted(fs):
                p = os.path.join(r, f)
                why = rule(p)
                (exc if why else inc).append((p, os.path.getsize(p), why))
for pid in ("24_U9CKK6",):
    p = f"papers/{pid}/ABSENCE_SEARCHES.md"
    inc.append((p, os.path.getsize(p), None))
for f in ["batch5_class_rules.json", "batch5_code_observations.csv", "batch5_code_observations_counts.json",
          "batch5_code_observations_excluded.csv", "batch5_counts_rule4.json", "batch5_link_check.txt", "batch5_number_check.txt",
          "batch5_prereg_hash_check.txt", "batch5_publish_exclusions.tsv", "batch5_report.md", "batch5_results.csv",
          "batch5_results_counts.json", "batch5_results_rule4.csv", "batch5_run_brief.md", "batch5_run_timing.txt",
          "batch5_targets.csv", "batch5_targets.md"]:
    inc.append((f"batches/{f}", None, None))
for f in ["make_target_table.py", "make_absence_md.py", "check_report_numbers.py",
          "triage_observations_batch5.py", "run_timing.py", "stage_publish_batch5.py"]:
    inc.append((f"scripts/{f}", None, None))
exc.append(("papers/21_LEFTNE to 25_914AN0: deposit copies, author scripts, venvs and run folders", 0,
            "never placed in the repo: kept in the agents' scratch folders outside the repository (sha256 of deposit files in each PREREG.md and checksums.sha256)"))
with open("batches/batch5_publish_exclusions.tsv", "w") as fh:
    fh.write("path\treason\n")
    for p, sz, why in exc:
        fh.write(f"{p}\t{why}" + (f" ({sz} bytes)" if sz else "") + "\n")
big = [p for p, sz, _ in inc if os.path.getsize(p) > MAXB]
assert not big, big
if not DRY:
    for p, _, _ in inc:
        d = os.path.join(CLONE, p)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(p, d)
    shutil.copy2("batches/batch5_report.md", os.path.join(CLONE, "batch5_report.md"))
    shutil.copy2("batches/batch5_targets.md", os.path.join(CLONE, "batch5_targets.md"))
print(f"included {len(inc)} files, {sum(os.path.getsize(p) for p, _, _ in inc)} bytes; excluded {len(exc)} entries")
for p, sz, why in exc:
    print("EXCLUDED", p, sz, why)
