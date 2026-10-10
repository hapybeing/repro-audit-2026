<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch1_code_observations.csv` applies. For 04_PSHE5L: out of scope: not reproducibility: 04-3; unverified agent observation: 04-1, 04-2, 04-4. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# Code review, 04_PSHE5L, Agent B

Scope: I read the whole deposited script `Rural Populism - Socius - Public Code.R` (409 lines, sha256 955871dc...), every active and commented line, and checked each active recode against the value frequencies of the public OSF CSV (`Rural_Populism_Dataset.csv`, 1203 rows x 30 columns).

## Bugs (real bugs only)
None found that I can establish as a bug.

## Observations (described, not classified as bugs)

1. Q15 code 8 (line 188, commented out). `Q15` enters the main structural model as an observed covariate (`violence ~ ... + e*Q15`, `polgriev ~ ... + a3*Q15`, `Q15 ~~ cultgriev`, `Q15 ~~ econgriev`). In the public CSV, Q15 takes values 1 to 8 (counts 107, 223, 78, 221, 92, 269, 149, 64). The script's own recode `# rural$Q15[rural$Q15 == 8] <- NA # Liberal 1 - 7 Conservative` (line 188) is commented out, so as deposited the 64 rows with code 8 enter the model with the numeric value 8.
   - Codebook: I found no public codebook for this 2021 survey that labels Q15 values. The same team's OSF component "Survey Experiment" (https://osf.io/dfkzx/) holds `GND_Experiment_Reprex_Data.csv` (https://osf.io/download/jymcr/), whose 1203 rows have the same WTS distribution and identical Q15 frequencies, and whose code `GND_Experiment_Final_Reprex.R` (https://osf.io/download/6aghr/, lines 73-77) maps `Q15 == 8 ~ "Missing"`. Its variable-codes PDF (https://osf.io/download/tnx68/) gives no Q15 value labels. The script's own comment on line 188 also describes the scale as "Liberal 1 - 7 Conservative". So code 8 is very likely a nonresponse code, but no codebook states it; I cannot establish what the authors intended for this paper.
   - What the runs show: with line 188 commented (as deposited) the reproduced standardized coefficients equal the paper's Tables 2-4 to all 3 decimals, and the controls-model scaled chi2 equals the paper's 779.793. With line 188 active (diagnostic) the main-model fit statistics equal the paper's text (chi2 516.954, df 141, CFI .911, TLI .892, SRMR .058, RMSEA .062) but the coefficients do not (c .363 vs .354, a1 .761 vs .718, indirect -.155 vs -.145). In both runs lavaan uses 1203 observations for the main model (FIML), not the paper's 1,139. 1203 - 64 = 1139. I could not determine which data state or run produced which reported number.

2. Nonresponse codes in control dummies (lines 48, 122, 179). `is_college` (QF 6 = "No answer" per the comment on line 43, 14 rows), `is_male` (QC 4, 17 rows) and `is_over65` (QB 12, 14 rows) put nonresponse codes into the 0 category. The comment on lines 118-119 says this is deliberate ("it will be 0 in all these new columns unless you decide to handle it differently"). These affect only the controls model (not the targets). A documented choice, not a bug.

3. Lines 17-20: `mutate(across(all_of(paste0("RAW_Q24", LETTERS[1:9])), as.numeric))` errors on the public CSV because the columns are absent (environment fix 02). The resulting variables are never used later. Not a bug in the authors' original data context.

4. Table 1 (reliability; not a target). The script's `rel(measurement, ...)` output (alpha .784/.703/.787/.799, CR .753/.623/.807/.807, AVE .360/.308/.515/.590 for polgriev/econgriev/cultgriev/violence) does not equal the paper's Table 1 values recorded in PREREG (alpha .771/.720/.856/.891, CR .769/.610/.769/.802, AVE .361/.300/.498/.577). I did not map the paper's row order to factors, and the Q15 recode does not touch the measurement model, so I cannot say where the difference comes from. Context only.
