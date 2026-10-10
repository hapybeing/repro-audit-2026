# Method changelog

## 2026-10-09 #1 (before selection was run; no results existed)
- What: frame restricted to datasets hosted on Harvard Dataverse (dataset DOI prefix 10.7910). candidates.csv now holds only these.
- Why: the Harvard Dataverse search index also lists datasets harvested from other installations (e.g. heiDATA 10.11588, other prefixes).
  Their metadata and files are not served by the Harvard API, so they cannot be screened or downloaded consistently. Found while
  inspecting candidates.csv column headers/prefix counts, before the random draw. 6769 of 8593 frame rows are hosted at Harvard.

## 2026-10-09 #2 (before any paper was selected; no results existed)
- What: (a) when a Dataverse dataset lists no article DOI, the DOI is looked up on Crossref by the article title (cleaned dataset title,
  or a quoted title inside the Dataverse publication citation), restricted to journal articles from 2022-06 on, accepted only if
  normalised title similarity >= 0.90 (difflib). (b) OpenAlex lookups use the `doi:` form; API responses are cached; a lookup that
  fails after retries stops the script instead of being recorded as "ineligible".
- Why: the first screening pass rejected all 147 screened datasets. 123 had no DOI field (journal dataverses often write
  "Forthcoming" with no DOI), and OpenAlex rate-limited (HTTP 429) the rest, which the first script wrongly counted as "not found".
  E1 requires the article to have a DOI, not that Dataverse records it, so the first pass applied E1 too narrowly.

## 2026-10-09 #3 (after selection and pre-registration of batch 1; before any reproduction run)
- What: (a) PROTOCOL.md disappeared from the workspace (sandbox recycle, about 20:30 IST) and was restored verbatim from the
  original text at 21:12 IST. The batch-1 pre-registration agents worked from AGENT_RUNBOOK.md and the brief, which carry the
  same rules; each PREREG.md notes this. (b) The conda R 4.4.3 environment was also lost. Runs now use Debian's system R (4.5.x)
  and Debian CRAN binaries, installed by `scripts/setup_env.sh`, with per-run libraries for anything else.
- Why: the sandbox's local disk is not persistent; installed tooling and one file did not survive. No reproduction had started.
- Note on the selection script: `selection/screening.csv` records E2 via OpenAlex `is_oa` (PROTOCOL says "via Unpaywall";
  OpenAlex open-access status is built on Unpaywall data). Flagged here rather than silently.

## 2026-10-10 #4 (after batch 1 results; prompted by external review)
- What: (a) Materials rule for classification: the deposit PLUS every location the article's own data/code statement points to. Locations we find ourselves (e.g. an uncited OSF copy) do not count toward the class; the class they would give is reported as an alternative. Applied to all batch 1 papers via `batches/batch1_class_rules.json` and `scripts/apply_class_rules.py` (evidence: `papers/*/DATA_STATEMENT.md`). Effect: 04 moves from A to C (article cites no data location; data found by us on OSF). No other class changes.
  (b) Papers whose article reports no computed result for the deposited material are labelled "no computational target" and counts are reported with and without them (01).
  (c) A clock or date change needed for exact match is logged as a deviation and the as-is class is reported alongside (02: A with authors' run date, B as-is).
  (d) Code issues are called "code observations". Only those with file + line, a demonstrated output change saved to a file, and independent detection or a proof/demonstration are "verified"; the rest are "unverified agent observations" and stay out of public summaries. Measurement-validity opinions are out of scope. (`batches/batch1_code_observations.csv`)
  (e) Exploratory, NOT pre-registered checks are allowed only when clearly labelled, and never change a class.
  (f) The sample is described as "papers whose Dataverse deposit contains R or Python code", not "open data and code": data presence was never an eligibility criterion (see SELECTION.md).
- Why: an external reviewer found the data rule was applied inconsistently (followed 04 to OSF but not 01/03), and asked for clearer separation of verified findings, deviations and exploratory analysis. Decision on (a) by Gaurang Kumar, 2026-10-10.
- Rerun: no re-execution needed; all batch 1 classes recomputed by script from saved outputs under the new rule. Applies to all later batches.

## 2026-10-10 #5 (after batch 1 results; pre-publication hardening, no class or count changed)
- What: (a) Absence claims ("file X is not deposited", "no accession exists", "no data statement") must be backed by a scripted, repeatable search log: exact query, URL, UTC time, HTTP status and result count, plus the rule for what would count as a hit (`scripts/absence_searches.py`, `scripts/make_absence_md.py`, output `papers/<id>/ABSENCE_SEARCHES.md`). Applied to batch 1 papers 01, 03 and 04 on 2026-10-10; all three absence findings held.
  (b) Paper 04's Sage supplementary file, unread in revision 2, was read on 2026-10-10 through the Google Docs viewer (direct download blocked by Cloudflare; routes logged in `papers/04_PSHE5L/data_statement_raw/supplement_access_attempts.json`). It names no data location, so rule #4 still gives C. `scripts/apply_class_rules.py 1` was re-run: classes and `batch1_counts_rule4.json` are unchanged (counts file byte-identical to revision 2). One wording change in `batch1_class_rules.json`: the 03 alternative label "no external location exists" became "no external data location found", because a search can show absence only within what it searched.
  (c) Every number in a batch report and target table is checked against the files it cites by `scripts/check_report_numbers.py` (output `batches/batch<k>_number_check.txt`) before publication.
  (d) Agent logs and code-review files carry a dated status note (`scripts/mark_unverified.py`) pointing to the observation status in `batches/batch<k>_code_observations.csv`; the agents' own text is unchanged.
  (e) From batch 2 onward, PREREG.md and targets.json hashes are pushed to the public repository before any reproduction run starts. For batch 1 they were frozen locally before the runs but first published on 2026-10-10 together with the results, so the ordering is self-attested.
- Why: hardening before public posting; a hostile reviewer must be able to repeat each absence search and trace each number.
- Rerun: no re-execution of any paper; (a) to (d) are documentation and checks. (e) applies to later batches only.

## 2026-10-10 #6 (after batch 2 results; class readings set by the lead after both blind agents reported)
- What: (a) A target mismatch that is only in a printed sample size, or only in a p-value whose conclusion bucket is unchanged, while every estimate target matches, is classed C ("code cannot produce the reported table", PROTOCOL.md section 7), not D. PROTOCOL.md section 7 defines D as a discrepancy that affects the conclusion; a printed N the code cannot produce, with identical estimates, does not change any conclusion. Applied to 08_SQRZR8: T1 to T5 (all Table 3 coefficients) match to 3 decimals in both runs, T6 is 4507 rows in both runs against the 4,057 printed in the Table 3 note. Both agents had proposed D by reading T6's pre-registered criterion literally. The same reading covers 06_VSV5DM (T4: AME p 0.0569 against the printed .054, same 0.05 to 0.10 band), where both agents had already proposed C. Counts are shown both ways in `batches/batch2_counts_rule4.json`: main (08 as C) and `counts_if_08_SQRZR8_alt` (08 as D). No batch 1 paper is affected: every computed batch 1 target matches the paper at its rounding (15 of 15, `batches/batch1_targets.csv`), so no batch 1 class rests on an N-only or p-only mismatch; paper 04's printed n (1,139 against 1203 in the run) is not a pre-registered target. `batch1_counts_rule4.json` is byte-identical after re-running `scripts/apply_class_rules.py 1`.
  (b) 07_JH9DBC: fixest 0.12.1 (the CRAN release current when the deposited code was written) is accepted as an allowed package-version environment fix (AGENT_RUNBOOK.md, Environment). It was chosen after seeing the output of current CRAN fixest 0.14.2, which gives identical coefficients but drops 14 singleton districts (Table B N 586 against 600) and uses IID standard errors by default. Both runs are kept (`papers/07_JH9DBC/A/outputs/`, `papers/07_JH9DBC/B/outputs/`; side by side in `batches/batch2_targets.md`). Main class A (0.12.1); alternative class B (0.14.2, all targets within 5%).
  (c) Environment only: `scripts/setup_env.sh` listed r-cran-fixest, which has no Debian trixie package, so the whole apt-get line failed and fell back to a shorter list. Missing or failed optional packages are now skipped and logged, and apt waits for another agent's dpkg lock. No analysis or class is affected; batch 2 agents installed fixest from CRAN into per-run libraries.
- Why: (a) and (b) are readings of PROTOCOL.md section 7 and the runbook's environment rule for cases the batch 2 pre-run decisions (`batches/batch2_class_decisions.md`) did not cover. They were made after results were known, so each is reported with its alternative count.
- Rerun: no re-execution of any paper; classes recomputed by `scripts/apply_class_rules.py 2` from saved outputs and `batches/batch2_class_rules.json`.
