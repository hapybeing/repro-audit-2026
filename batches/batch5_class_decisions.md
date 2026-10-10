# Batch 5 classification decisions (fixed before any batch 5 reproduction run)

Written 2026-10-11 (IST) after the five pre-registrations and before any of the authors' analysis code was run. Frozen with the pre-registrations in batch5_prereg_hashes.txt. Applies PROTOCOL.md section 7 and CHANGELOG_METHOD.md #4, #5 and #6 exactly as in batches 1 to 4. Nothing here changes those rules; it records how they apply to cases the batch 5 pre-registrations raised. The batch 2 to 4 decisions carry over where relevant.

1. Statistic and model ambiguity. Where PREREG.md lists more than one candidate statistic, model or formula for a target (21 T1/T2 SEM versus bootstrapped mediation; 23 T2 p-value, T5 statistic and T6 formula; 24 texreg Wald p versus Satterthwaite p; 22 Wald versus likelihood-ratio p), the first candidate listed sets the class. The other candidates are reported beside it.

2. Running only the target blocks. Running the authors' own lines for the pre-registered target blocks unchanged, in a fresh session, instead of the whole script (24 script 6 lines 1-53 and 346-416 and script 9 lines 1-123; 25 run2_main.R lines 43-157 and 1310-1408), is an environment fix. A failure in a part of a script that produces no target (24 undefined `right`/`left` at line 132; 22 figure code) is reported as a code observation and does not change the class.

3. Environment fixes named in PREREG.md are accepted as environment fixes: absolute paths and `install.packages()` lines (22), `browseURL()` made a no-op (22), `mc.cores` raised to at least 1 (25), Dataverse `?format=original` downloads (22, 23), blanking unused speech-text columns after loading and saving models to disk to fit in memory (24 F1/F2) as long as no estimation line, sample filter or seed changes, and package version fallbacks listed in PREREG.md (21 lavaan, 23 fixest and kableExtra, 25 lfe, fixest, lme4, SUNGEO). Pinned or dated versions are tried first.

4. Target values read from a secondary copy. 24's targets come from a browser transcription of the publisher's table pop-up and PDF viewer, and 21's supplement targets T3/T4 from text extracted from a .doc file. Each agent re-checks those cells against the paper itself before scoring and logs the check. If a cell differs, the paper's own printed value is used and the change is recorded in the report; the frozen targets.json is not edited. 25's targets come from the authors' appendix PDF hosted on the author's site, which matches the deposited .tex tables; differences from the article's prose (25 T2, T3) are reported and do not change the class.

5. Prose-only targets (23 T5, T6; 25 article prose values). A prose-only value reproduced to its printed rounding counts as matched. A formula not shown by the authors (23 T6) is scored with the first pre-registered formula.

6. Year specification (24). The class uses the deposited code (`year` as a numeric linear term). The factor-year model is robustness check R_c and never changes the class, but its outcome is reported beside the class.

7. Missing files that no target needs (24 parlgov CSVs and the Eurobarometer file for scripts 4 and 10; 23 the undeposited raw-data build step) are listed in the report as data-statement findings and do not change the class. A target that cannot be produced because a file or module is missing from the deposit and every location the data statement names counts as not produced (CHANGELOG #4, C).

8. A target that cannot be produced because no package version can run on this machine, after the listed fallbacks, is E for that target (21 lavaan, as in batch 3).

9. Sample-size-only or p-only mismatches follow CHANGELOG #6 (C, not D). Robustness checks never change the class (PROTOCOL.md section 7).
