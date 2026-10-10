# Batch 3 classification decisions (fixed before any batch 3 reproduction run)

Written 2026-10-10 (IST) after the five pre-registrations and before any of the authors' analysis code was run. Frozen with the pre-registrations in batch3_prereg_hashes.txt. Applies PROTOCOL.md section 7 and CHANGELOG_METHOD.md #4, #5 and #6 exactly as in batches 1 and 2. Nothing here changes those rules; it records how they apply to cases the batch 3 pre-registrations raised. All six batch 2 decisions carry over where relevant.

1. Deposited file names that differ from the names the code reads (11_DDOFPS). Pointing the script at the deposited file with the same structure is a path-only environment fix. The main class uses the file PREREG.md names as primary (bd_doxa_programas_HGPE.xlsx). The v2 file is run as a labelled alternative. If v1 and v2 give different target values, both are reported and the class computed on v2 is given as the alternative.

2. Descriptive targets with no printed test (11, 12, 15). A means every target matches at the printed precision. B means a target differs beyond rounding but meets its pre-registered same-conclusion rule. D needs a same-conclusion rule to fail in both agents' clean runs.

3. Unseeded randomness in the authors' code (12_CYBR7L). The class is computed from the pre-registered primary seed run. The spread over seeds 1 to 20 is reported. If the printed value appears for some seeds but not the primary one, the paper is B with a note, not D.

4. Statistic ambiguity (13_DX5T9G: draw mean vs fitted coefficient; 11: p-value wording; 15 T4: two code objects). The first candidate listed in PREREG.md is the pre-registered one and sets the class. Other candidates are reported beside it.

5. Version pins in the authors' readme (14_CJISMY fixest 0.11.1, 13 ebal 0.1-8). Agents try the authors' pinned version first, as stated before any run. If a pin cannot be installed, the current version is used and recorded. A result that differs only because of a version is reported both ways, as for 07 in batch 2.

6. Factor reference level (14_CJISMY T3, T4). The class uses the model exactly as the code builds it. If the baseline is not "Both", T3 and T4 count as not produced as-is, and the relevelled refit gives the alternative class.

7. Robustness checks never change the class (PROTOCOL.md section 7).
