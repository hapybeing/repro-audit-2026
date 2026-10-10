<!-- status-note:start -->
> **Status note added 2026-10-10, after this run; not part of the agent's record.** This file keeps the agent's run-time wording, which may call an item a "bug". Under CHANGELOG_METHOD.md #4d, the status in `batches/batch1_code_observations.csv` applies. For 02_ELBOXX: out of scope: not reproducibility: 02-1, 02-2, 02-4, 02-5, 02-6, 02-7, 02-8; unverified agent observation: 02-9, 02-10; verified finding: 02-3. Only "verified finding" items are findings; "unverified agent observation" items are unverified and are not claims about the paper. Nothing here says the paper is wrong.
<!-- status-note:end -->

# Code review, 02_ELBOXX, Agent A

Read in full: analysis_data_creation.R (125 lines), replication.R (35 lines), visualization.R (75 lines), README.txt.
Numbers below come from outputs/code_review_facts.csv and outputs/mid_direction_check.csv (scripts/compare_and_review.R,
scripts/check_mid_direction.R).

## Bug found

### B1. `disputes` counts MIDs the country initiated, not MIDs initiated against it
- File: analysis_data_creation.R, lines 81-82 (comment line 84: "Code number of mids this state was target of in this year").
  ```
  mt <- m[m$stateb == t$state & m$strtyr == t$year,]
  mt <- mt[mt$dyad_rolea == 3,]
  ```
- Data facts: dyadic_mid_4.02.csv is directed, every row has a mirror row with statea and stateb swapped
  (share_rows_with_mirror_row = 1). dyad_rolea and dyad_roleb are always opposite (table rolea x roleb: only (1,3) and (3,1)).
  The Dyadic MID 4.01/4.02 codebook (Dyadic MID Codebook V4.0.pdf, Dataverse file 11182353, variable DYAD_ROLEA) codes
  1 = Initiator of dyadic MID, 3 = Target of dyadic MID. The code keeps rows where state A is the target and assigns them to
  state B; in all 5168 such rows dyad_roleb = 1, so state B (the country being coded) is the initiator.
  Example from the data, dispute 2 (1902): row statea = 2 (USA), stateb = 200 (UKG), dyad_rolea = 1 (USA initiates);
  mirror row statea = 200, stateb = 2, dyad_rolea = 3. The code counts the mirror row for country 2 (USA), the initiator.
- Paper text (Wiley HTML): "for each country-year, we calculate the total number of MIDs initiated against that country in the given year".
  The code's own comment says the same. The implemented variable is the opposite side of the dyad.
- Effect (information only, not a pre-registered check): recounting with the country as dyadic target
  (statea == country and dyad_rolea == 3) gives M2 r = 0.1214, 95% CI [0.0900, 0.1526], p = 5.5e-14
  (code version: 0.1628), and M1 r = 0.0462, p = 1.0e-9 (code version 0.0544). Same sign and significance; the
  correlation between the code's count and the target-side count across country-years is 0.29.

## PREREG section 3/4 observations, decisions

1. `pub_def == 1` filter (replication.R line 24). `pub_def` is a count (analysis_data_creation.R line 17 comment
   "num of public defensive alliances"; max 14). The filter keeps 3811 country-years with exactly one public defensive
   alliance and drops 4834 with two or more; the paper's sample is "country-years in which the given country was a member
   of a public defensive alliance". Decision: discrepancy between stated sample and code; whether `== 1` was meant as
   "has one" (a slip) or a deliberate "exactly one" cannot be determined from the materials. Not counted as a bug.
   S1 (pub_def >= 1): r = 0.0972, CI [0.0763, 0.1181], positive and significant.
2. M1 text says "defensive secret alliances" and "sum the total number of MIDs in a given year" (system-year). Code uses
   `secret` (all secret treaties, pubsecr == 2, lines 32 and 109) and correlates at country-year level (N = 17511).
   Decision: text/code mismatch; the reported number matches the code, so the paper reports what the code does, but the
   description differs. Information only: using yearly sum of secret_def gives r = 0.0555; a system-year version
   (209 years, yearly sums of `secret` and `disputes`) gives r = -0.0953. Undeterminable which the authors intended;
   not counted as a bug.
3. Paper says MIDs 5.0; code uses dyadic MID 4.02 (line 70 comment "v 4.02"). Documented in code and README; documentation
   mismatch, not a bug. Dyadic MID 4.02 ends in 2014 (max strtyr 2014), so 2015-2024 country-years have disputes = 0
   by construction (200 of the 3811 M2 rows). S2 (year <= 2014): r = 0.1621, essentially unchanged.
4. `secret_alliances` (lines 107-110) sums `secret` over country-years, so it counts alliance memberships, not alliances
   (differs from the distinct count in 155 years; max ratio 3). Paper says "total number of active secret alliances".
   Documented-choice versus wording mismatch; information only: using distinct secret alliances per year gives
   M2 r = 0.1686. Not counted as a bug.
5. replication.R lines 18-19 comment ("correlation between defensive alliances and concurrent secret alliances") does
   not describe the code; the code matches the paper sentence. Comment-only, not a bug.
6. README names `AJPS_rep.RData` and `codebook.pdf`; Dataverse has `AJPS_analysis_data.RData` and no project codebook.
   Documentation gap (materials slightly incomplete), not a bug; does not block reproduction.

## Other observations
- create_stateyears() depends on the system date (see diffs/README.md); the replication result for test 1 depends on
  the date the code is run. Environment dependency, not a bug in the analysis logic, but the README does not mention it.
- 307 of 11923 ATOP state-year rows do not match a COW state-year and are dropped by the merge (line 64, all.y = TRUE);
  ATOP starts in 1815 and the COW frame in 1816. Consistent with the stated design; not a bug.
- visualization.R line 38: backtick name with a trailing space (`1 `) in recode; tested with dplyr 1.1.4, it still recodes 1 to "Secret Article". Not a bug.
