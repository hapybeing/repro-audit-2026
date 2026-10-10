"""Prepend a dated status note to every batch K agent log and code-review file, and to superseded batch files,
so that unverified agent observations are marked as unverified wherever they appear.
Usage (from repo/): python3 scripts/mark_unverified.py 1 [YYYY-MM-DD]   (date in the note; default 2026-10-10, as written for batches 1 to 3)
Reads batches/batch{K}_code_observations.csv. Idempotent: an existing note (between the markers) is replaced.
The agents' own text below the note is not changed."""
import csv, glob, os, sys, re

K = sys.argv[1]
DATE = sys.argv[2] if len(sys.argv) > 2 else "2026-10-10"
START, END = "<!-- status-note:start -->", "<!-- status-note:end -->"
obs = list(csv.DictReader(open(f"batches/batch{K}_code_observations.csv")))


def note_for(paper):
    rows = [o for o in obs if o["paper"] == paper]
    by = {}
    for o in rows:
        by.setdefault(o["status"], []).append(o["obs_id"])
    parts = [f"{s}: {', '.join(ids)}" for s, ids in sorted(by.items())]
    return (f"{START}\n> **Status note added {DATE}, after this run; not part of the agent's record.** "
            f"This file keeps the agent's run-time wording, which may call an item a \"bug\". Under CHANGELOG_METHOD.md #4d, the status in "
            f"`batches/batch{K}_code_observations.csv` applies. For {paper}: " + ("; ".join(parts) if parts else "no code observations") +
            ". Only \"verified finding\" items are findings; \"unverified agent observation\" items are unverified and are not claims about the paper. "
            f"Nothing here says the paper is wrong.\n{END}\n\n")


def apply(path, note):
    s = open(path, encoding="utf-8").read()
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n\n", "", s, flags=re.S)
    open(path, "w", encoding="utf-8").write(note + s)
    print("noted", path)


papers = sorted({o["paper"] for o in obs})
for p in papers:
    n = note_for(p)
    for f in sorted(glob.glob(f"papers/{p}/[AB]/LOG.md") + glob.glob(f"papers/{p}/[AB]/outputs/code_review.md")):
        apply(f, n)

n_unv = sum(1 for o in obs if o["status"] == "unverified agent observation")
sup = (f"{START}\n> **Status note added {DATE}: superseded.** This is an earlier version kept for the record. Current results: "
       f"`batches/batch{K}_report.md`. Items this file calls \"bugs\" are now \"code observations\" with a status in "
       f"`batches/batch{K}_code_observations.csv` (CHANGELOG_METHOD.md #4d); {n_unv} of them are unverified agent observations, not findings, "
       f"including the 03 isotope-correction item. Nothing here says any paper is wrong.\n{END}\n\n")
for f in [f"batches/batch{K}_report_v1.md", f"batches/batch{K}_table.md"]:
    if os.path.exists(f):
        apply(f, sup)
