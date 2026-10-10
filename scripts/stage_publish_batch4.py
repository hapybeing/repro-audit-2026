"""Stage batch 4 files from the working repo into a git clone, applying the publication exclusions.
Usage (from repo/): python3 scripts/stage_publish_batch4.py <clone_dir> [--dry]
Writes batches/batch4_publish_exclusions.tsv (path, bytes, reason) in the working repo first, then copies every
included file into the clone (same relative path), plus the top-level copies batch4_report.md and batch4_targets.md.
Rules (as for batch 3): R data objects and session images derived from the third-party deposit are excluded
(regenerable with the agents' scripts); full or patched copies of the authors' code are excluded (licence varies; the
change is in diffs/); article full-text copies and images would be excluded; any file over 10 MB is excluded."""
import os, shutil, sys

CLONE = sys.argv[1]
DRY = "--dry" in sys.argv
MAXB = 10 * 1024 * 1024
PIDS = ["16_QZNVZ0", "17_T1NXVQ", "18_YXC5K5", "19_KH0SQ2", "20_SINIYU"]
AUTHOR_COPIES = {
    "scripts/regression_verbatim_orig.py": "full copy of the authors' notebook cells as a script (licence varies); the run is described in diffs/",
    "scripts/regression_verbatim.py": "full copy of the authors' notebook cells with the audit's appended output-only block (licence varies); the change is in diffs/",
    "scripts/analysis_pool_orig.R": "full copy of the authors' script (licence varies); the change is in diffs/",
    "scripts/analysis_pool_A.R": "full patched copy of the authors' script (licence varies); the change is in diffs/",
    "scripts/Benchmarking_DataAnalysis_Rc.Rmd": "full modified copy of the authors' R Markdown file for R_c (licence varies); the change is in diffs/",
    "outputs/analysis_main.R": "full copy of the authors' R Markdown code, extracted with knitr::purl (licence varies)",
    "outputs/analysis_Rc.R": "full modified copy of the authors' R Markdown code, extracted with knitr::purl (licence varies); the change is in diffs/",
    "outputs/analysis_purled.R": "full copy of the authors' R Markdown code, extracted with knitr::purl (licence varies)",
    "outputs/analysis_Rc_purled.R": "full modified copy of the authors' R Markdown code, extracted with knitr::purl (licence varies); the change is in diffs/",
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
for pid in ("17_T1NXVQ", "18_YXC5K5", "20_SINIYU"):
    p = f"papers/{pid}/ABSENCE_SEARCHES.md"
    inc.append((p, os.path.getsize(p), None))
for f in ["batch4_class_rules.json", "batch4_code_observations.csv", "batch4_code_observations_counts.json",
          "batch4_code_observations_excluded.csv", "batch4_counts_rule4.json", "batch4_link_check.txt", "batch4_number_check.txt",
          "batch4_prereg_hash_check.txt", "batch4_publish_exclusions.tsv", "batch4_report.md", "batch4_results.csv",
          "batch4_results_counts.json", "batch4_results_rule4.csv", "batch4_run_brief.md", "batch4_run_timing.txt",
          "batch4_targets.csv", "batch4_targets.md"]:
    inc.append((f"batches/{f}", None, None))
for f in ["make_tables.py", "make_target_table.py", "make_absence_md.py", "check_report_numbers.py", "mark_unverified.py",
          "triage_observations_batch4.py", "run_timing.py", "stage_publish_batch4.py"]:
    inc.append((f"scripts/{f}", None, None))
exc.append(("papers/16_QZNVZ0 to 20_SINIYU: deposit copies, author scripts, venvs and run folders", 0,
            "never placed in the repo: kept in the agents' scratch folders outside the repository (sha256 of deposit files in each PREREG.md and checksums.sha256)"))
with open("batches/batch4_publish_exclusions.tsv", "w") as fh:
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
    shutil.copy2("batches/batch4_report.md", os.path.join(CLONE, "batch4_report.md"))
    shutil.copy2("batches/batch4_targets.md", os.path.join(CLONE, "batch4_targets.md"))
print(f"included {len(inc)} files, {sum(os.path.getsize(p) for p, _, _ in inc)} bytes; excluded {len(exc)} entries")
for p, sz, why in exc:
    print("EXCLUDED", p, sz, why)
