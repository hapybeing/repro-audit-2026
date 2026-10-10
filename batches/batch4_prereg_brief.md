# Batch 4 pre-registration brief (papers 16 to 20)

REPO = /workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo

You write the pre-registration for ONE paper. Read REPO/PROTOCOL.md (sections 5 to 7), REPO/AGENT_RUNBOOK.md, REPO/CHANGELOG_METHOD.md (#4, #5 and #6 apply), REPO/papers/<PID>/META.md, and use REPO/papers/05_FNTC1J/PREREG.md and targets.json as the format model.

Hard rules
- Do NOT run any of the authors' analysis code. You may download the deposit and read files (code, README, codebooks, column headers). Record sha256 of each file you download (scratch: /workspace/audit_runs/<PID>/prereg/).
- Copy every paper value exactly from the paper (open full text, PDF, publisher page, PMC, SSRN, author preprint, or the deposit's own copy). Give table/figure/page location. Never invent or estimate a number. If you cannot read the paper's numbers, say so plainly in PREREG.md.
- Targets: 3 to 6 headline numbers from the abstract's main claim and the table that reports it. Prefer coefficients/estimates, plus N.
- Robustness checks, defined in advance: (a) different seed or bootstrap resample, (b) outlier exclusion (default |z| > 3 on the outcome, or top/bottom 1% where z is meaningless; for binary outcomes apply to the main continuous predictor instead and say so), (c) one alternative reasonable analysis choice. State exactly how each will be run and what counts as "same direction and significance".
- State the conclusion criterion for same_conclusion for each target.
- No em dashes. No sign-ins, no author contact, no posting.
- Do not read any batch report or any other paper's A/ or B/ folders.

Outputs (in REPO/papers/<PID>/)
1. PREREG.md: header with written date (IST) and "before any analysis code was run"; paper citation and the text source you read (URL + sha256 if downloaded); dataset files list (datafile id, URL, bytes, sha256); 1. headline + targets table; inconsistencies noticed (described, not judged); 2. reproduction plan (script order, inputs, where each target comes from, allowed env fixes); 3. robustness checks R_a, R_b, R_c; 4. known risks (missing files, Stata/proprietary deps, long compute).
2. targets.json: list of {id, description, paper_value, paper_rounding_decimals, location}.
3. DATA_STATEMENT.md: rule 4 (CHANGELOG #4). Quote the article's data/code availability statement verbatim with its location, list every location it names, and for each say whether you checked it and whether the files the code reads are there (compare script read calls to files present). If the deposit lacks a file the code reads, log the exact searches you did (query, site, UTC time, result count) in the same file so a reader can repeat them. If no statement exists, say "no data availability statement found" and where you looked.

Final message: PID, targets with paper values and locations, the three checks, the data-statement finding (complete / missing what), and any risk that could make the paper C or E.

Lessons carried from batch 2 (apply before any run)
- For every target, name the exact statistic and code object it maps to. If the paper's text is ambiguous about which statistic it reports (for example which p-value), say so in PREREG.md and list each candidate; the first listed is the pre-registered one.
- Prefer printed table estimates over values quoted only in prose.
- If the paper prints more than one N for the same model, record each with its location.
- If the main text cannot be read, say so in the first paragraph of PREREG.md.
- Do not save near-verbatim transcriptions of article or supplement text; save short excerpts (statement, target rows) only.
- Lessons from batch 3: if the deposited file names differ from the names the code reads, map them explicitly in PREREG.md as a path-only fix and list any alternative file. Flag pinned package versions and say whether the pin is tried first. Estimate peak memory; the shared machine has 7 GB and two agents run each paper, so pre-register a fallback that keeps the authors' estimation lines and seeds unchanged if the full pipeline may exceed about 3 GB.
