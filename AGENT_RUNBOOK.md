# Agent runbook (read fully before starting)

Repo root: /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo  (call it REPO)
Read REPO/PROTOCOL.md first. Accuracy and honesty beat speed. "I could not determine this" is always acceptable.

## Hard rules
- Never invent, estimate or fill in a number. Every reproduced number must be written to a file by code you ran.
- Never call a paper wrong, flawed or fraudulent. Describe what you observed.
- Public downloads only. No sign-ins, no contacting authors, no posting anything anywhere.
- Do not change the authors' analysis. Only environment fixes (package versions, file paths, missing `library()` for an installed
  package, setting the working directory). Save every change as a unified diff in your `diffs/` folder (`diff -u orig new`).
- Never change a pre-registered check after seeing results. If something cannot be run as written, say so and say why.
- No em dashes in any text you write.

## Environment
- Machine: aarch64 Debian 13, 2 CPUs, 7 GB RAM, shared with other agents. Keep memory use modest; one heavy job at a time.
- Python 3.12 at `python3`. For a clean env: `python3 -m venv RUNDIR/venv` and pip install only what the code needs.
- R: system `Rscript` (Debian R 4.5.x). If `Rscript` is missing, run `bash REPO/scripts/setup_env.sh` first (idempotent; the sandbox can be recycled). For a clean R library per run, set `R_LIBS_USER=RUNDIR/rlib` (mkdir it) and
  install missing packages there with `install.packages(..., repos="https://cloud.r-project.org", lib=Sys.getenv("R_LIBS_USER"))`
  (source builds work; Debian binaries `sudo apt-get install r-cran-<pkg>` are also fine, record them). setup_env.sh installs
  tidyverse, data.table, haven, lme4, readxl, sandwich, lmtest, remotes, sessioninfo. If the authors pin versions (renv.lock,
  sessionInfo, README), try those versions first via `remotes::install_version`.
- Long jobs: use background shell tasks (each foreground command is capped at 120 s; background at 600 s, so split long jobs or
  make them resumable). If the full analysis cannot finish within about 2 hours of compute, classify E with the reason and what did run.
- Downloads: Harvard Dataverse API, e.g. `https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/XXXX`
  (zip of all files) or per file `https://dataverse.harvard.edu/api/access/datafile/<id>`. Send a User-Agent header (curl -A "repro-audit-2026").
  Record sha256 of every downloaded file.

## Directory layout
- Scratch (raw data, venvs, rlib): /workspace/audit_runs/<PID>/<AGENT>/   (AGENT = A or B)
- Saved results: REPO/papers/<PID>/<AGENT>/ containing:
  - `LOG.md`: dated, step-by-step run log in plain language (what you ran, what happened, errors verbatim, decisions).
  - `diffs/`: one .diff per changed file, plus `diffs/README.md` saying why each change was needed.
  - `outputs/`: raw output files produced by the authors' code (tables, logs, figures) and by your check scripts.
  - `scripts/`: your own scripts (robustness checks, extraction of numbers, comparison builder).
  - `environment.txt`: OS (`uname -a`, /etc/os-release), R/Python version, full package versions (sessionInfo / pip freeze), seeds, date (IST).
  - `checksums.sha256`: sha256 of every downloaded file.
  - `results.json`: built BY A SCRIPT (`scripts/build_results.py` or .R) that reads numbers from files in `outputs/`. Schema below.
- AGENT B: you must NOT open, list or read REPO/papers/<PID>/A/ or /workspace/audit_runs/<PID>/A/ or any batch report. Work only from
  the paper, the dataset, PROTOCOL.md, this runbook and REPO/papers/<PID>/PREREG.md.

## results.json schema
```
{
 "paper_id": "<PID>", "agent": "A|B", "run_date_ist": "YYYY-MM-DD",
 "ran": true|false, "could_not_run_reason": "" ,
 "targets": [ {"id": "T1", "description": "...", "paper_value": <number copied from PREREG.md>, "paper_rounding_decimals": <int>,
               "reproduced_value": <number read from an output file or null>, "source_file": "outputs/...",
               "abs_diff": .., "rel_diff": .., "match_to_rounding": true|false|null, "within_5pct": true|false|null,
               "same_conclusion": true|false|null, "note": "" } ],
 "robustness": [ {"id": "R_a|R_b|R_c", "description": "as pre-registered", "ran": true|false, "estimate": <num or null>,
                  "se_or_ci": "...", "p_value": <num or null>, "same_direction_and_significance_as_paper": true|false|null,
                  "source_file": "outputs/...", "note": ""} ],
 "bugs": [ {"file": "...", "line": <int>, "description": "...", "evidence": "..."} ],
 "env_fixes": ["diffs/xxx.diff: reason"],
 "proposed_class": "A|B|C|D|E", "class_reason": "one or two sentences",
 "confidence": "high|medium|low", "confidence_reason": "one line",
 "time_minutes": <wall-clock minutes you spent, from LOG.md timestamps>,
 "uncertainties": ["anything you are unsure about"]
}
```
`paper_value` comes from PREREG.md (copied from the paper there). Everything in `reproduced_value`, `estimate`, `p_value` must be parsed
from files in `outputs/` by the build script, never typed. match_to_rounding: reproduced value rounded to paper_rounding_decimals equals
paper_value. within_5pct: |rel_diff| <= 0.05.

## Classification (PROTOCOL.md section 7), proposed per agent
A exact to rounding (all targets) / B all within 5% and same conclusion / C materials incomplete or unclear / D discrepancy affecting the
conclusion (final D needs both A and B to see it) / E could not run. Robustness does not change the class.

## Code review
Real bugs only: wrong variable, wrong filter, miscoded values, off-by-one merges, etc., with file, line and evidence (the code and the
data fact that shows the problem). Style issues, inefficiency and missing comments are not bugs. If none found, say "none found" and
how much of the code you read.

## Final message back
Reply with: proposed class + one-line reason, confidence + reason, list of targets with paper vs reproduced values (as read from
results.json), robustness outcomes, bugs, env fixes, and every uncertainty. Keep it factual.
