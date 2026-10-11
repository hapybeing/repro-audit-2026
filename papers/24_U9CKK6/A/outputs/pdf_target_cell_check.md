# Check of the six target cells against the article PDF (agent A)

Source: https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2391510 , fetched 2026-10-11 ~04:45 IST through the Hark web_fetch tool (text layer of the publisher PDF; curl was not used). Short excerpts of the PDF text layer only:

- Table 1, row "Challenger * Proximity to next National Election": "0.02 *** 0.02 *** 0.02 *** 0.02 ***" / "(0.00) (0.00) (0.01) (0.00)". Model 2 = 0.02 ***, SE 0.00. Matches T1.
- Table 1, row "Proximity to next EP- Election": "0.01 ** 0.01 *** 0.01 ** 0.01 ***" / "(0.00) ...". Model 2 = 0.01 ***. Matches T2.
- Table 1, row "Challenger": "0.06 *** 0.05 *** 0.04 ** 0.04 **" / "(0.01) (0.01) (0.02) (0.02)". Model 2 = 0.05 ***, SE 0.01. Matches T3.
- Table 1, row "Num. obs.": "266,854 266,854 266854 266854". Model 2 = 266,854. Matches T4.
- Table 2, row "Challenger * Austerity Salience 0.04 ** (0.01)" (Austerity column). Matches T5.
- Table 2, row "Challenger * EU Salience 0.02 * (0.01)" (European Integration column). Matches T6.
- No star legend or table note is printed under Table 1 or Table 2 in the PDF text layer (consistent with PREREG.md).

Result: all six cells in targets.json agree with the PDF. targets.json is used unchanged for scoring.
