# Batch 4 run brief (agents A and B)

REPO = /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo

You are agent <AGENT> for paper <PID>. Read REPO/AGENT_RUNBOOK.md fully and follow it exactly, then REPO/PROTOCOL.md, REPO/papers/<PID>/PREREG.md, REPO/papers/<PID>/targets.json, REPO/papers/<PID>/DATA_STATEMENT.md and REPO/batches/batch4_class_decisions.md.

- The pre-registration was frozen at 2026-10-10 18:46:56 UTC (GitHub issue #3, commit e29c1b6). PREREG.md and targets.json are read-only. Do not edit them. If something cannot be run as written, say so in LOG.md and results.json.
- Agent B: do not open, list or read REPO/papers/<PID>/A/ or /workspace/audit_runs/<PID>/A/ or any batch report or results file. Agent A: do not read B/.
- Do not read any other paper's folders.
- Memory: the machine is shared by up to 8 agents with 7 GB RAM. Run one R process at a time, avoid parallel package compiles (use `Ncpus=1`), and prefer Debian r-cran-* binaries via `sudo apt-get install -y r-cran-<pkg>` when available (record it). If R is missing, run `bash REPO/scripts/setup_env.sh`.
- Follow the PREREG's reproduction plan, allowed env fixes and download notes (for example `?format=original` where PREREG says so). Save every change as a diff.
- Write REPO/papers/<PID>/<AGENT>/ with LOG.md, diffs/, outputs/, scripts/, environment.txt, checksums.sha256, results.json (built by script). For figure-claim checks or other pre-registered checks not in targets.json, write their outcomes to outputs/ by script and summarise them in results.json under "robustness" or "uncertainties" as appropriate, with the source file.
- Code review: real bugs only, with file, line and evidence. Anything you cannot confirm with a run is an "unverified observation".
- No em dashes. No sign-ins, no author contact, no posting. Never call a paper wrong.
- If you loop more than twice on the same failure, stop that step, record it and move on. Keep total wall time under about 2 hours.

Final message: proposed class + reason, confidence, targets paper vs reproduced (as read from results.json), robustness outcomes, code observations, env fixes, uncertainties.
- Python papers (16, 20): use a venv under /workspace/audit_runs/<PID>/<AGENT>/venv; record pip freeze.
- Paper 17 is memory heavy (1.5 to 3 GB per model, more in a bootstrap draw): fit one model per process as PREREG says, and never start a heavy step if `free -g` shows under 3.5 GB available; wait and retry. Respect the PREREG time budget for K.
- Paper 18: run the Rmd exactly as deposited for the main targets; R_c is the pre-registered docid-sorted copy.
- Paper 19: use only the pre-registered driver (adds load() of the deposited .RData) to run the target lines.
- Paper 20: do NOT write replacement code for the missing interp_radar module or for Table 1. Try what the PREREG says, record exactly what fails, and report targets as null where not produced. Use unrar-free for the RAR5 set.
- Do not save full copies of article text; short excerpts only.
