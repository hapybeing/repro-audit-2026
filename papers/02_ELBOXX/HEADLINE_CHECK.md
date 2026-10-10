# HEADLINE_CHECK: 02_ELBOXX (reviewer point 1)

Written 2026-10-10 (IST), Agent A, in response to an external reviewer. Does not change PREREG.md, targets.json, results or the class.

## Source read
- Journal full text (HTML), open access CC BY 4.0: https://onlinelibrary.wiley.com/doi/full/10.1111/ajps.12997 (read 2026-10-10 via a fetch fallback; the page has no page numbers, so locations below are given by section and paragraph; journal pages 1062-1076).
- OpenAlex record W4411519861 (https://api.openalex.org/works/doi:10.1111/ajps.12997): is_oa true, oa_status hybrid, publishedVersion, licence cc-by; only OA location is the Wiley pdfdirect link (Cloudflare-blocked for the audit, see PREREG.md section 0).
- The CI brackets in both empirical sentences are rendered as math and are dropped in the HTML text; the quotes below show them as "[CI not rendered in HTML text]".
- Quotes are verbatim except that the original's em dash characters are written as "[em dash]" (repo style rule).

## Verdict
The correlation targeted in PREREG (M2, T1 to T3) is a **supporting exhibit, not the paper's headline claim**. The abstract states only theoretical results from a formal model and reports no number. M2 is, however, the paper's only empirical evidence for the last sentence of the abstract and is stated as a finding in the introduction, so it is the closest empirical counterpart to the headline, and the authors themselves describe it as consistent with, not confirmatory of, the model. The M1 correlation (T4, T5) is likewise a supporting exhibit. PREREG.md section 1 already says the paper "is primarily a formal (game-theoretic) model" and that the abstract's claim is theoretical; this check confirms that reading from the journal text.

## Quotes with location

1. Abstract (full paragraph, last two sentences): the headline claim is about a formal model, no data.
   > "To develop this argument, we analyze a formal model in which states may enter into secret or public alliance agreements. We find that the possibility of secret alliances has general effects on deterrence[em dash]possibly undermining the deterrent value of concurrent public alliances."

2. Introduction, paragraph beginning "We also derive a number of results tying secret alliances to conflict" (last sentences): the only place outside the Discussion where the empirical test is mentioned, stated as a finding.
   > "Thus, the model implies a correlation between secret alliances and conflict. This is consistent with previous work and we show this correlation holds specifically for secret defensive alliances. Most interestingly, we find that the existence of secret alliances also undermines the deterrent value of concurrent public alliances. If public alliances remained deterrent in a world of secret alliances, then states could profitably deviate from forming a secret alliance to forming a public one. Using data on alliances and military disputes, we find that when secret alliances are prevalent, concurrent public alliances are less deterrent."

3. Connections to the Literature, first sentence: the authors name the contribution as theoretical.
   > "Our primary contribution is to advance a novel theoretical explanation for secret alliances."

4. Discussion, subsection "Secret alliances and conflict", first paragraph: the empirical tests are framed as consistency checks of implications.
   > "These results make predictions about the empirical relationship between alliances and the onset of conflict. We now discuss two of the implications of these propositions and show they are consistent with patterns in the data."

5. Same subsection, M1 (T4, T5), end of the third paragraph (begins "To evaluate this implication"):
   > "Consistent with our theory, we find a positive and statistically significant relationship between these two variables, with an estimated correlation coefficient of .05441 and a confidence interval of [CI not rendered in HTML text]."

6. Same subsection, fifth paragraph (begins "In contrast, our theoretical argument"): the system-level correlation is all the theory claims.
   > "As such, our theory does not generate a causal claim about the relationship between secret alliances and war. Rather, it simply points to a system-level correlation, which we have found."

7. Same subsection, M2 (T1 to T3, the PREREG main result), sample definition (seventh paragraph, begins "To assess this correlation") and result (eighth paragraph, begins "Consistent with our expectation"):
   > "Our unit of analysis is the country-year, and we restrict our sample to country-years in which the given country was a member of a public defensive alliance according to ATOP."

   > "Consistent with our expectation, we find a positive and statistically significant correlation, with an estimated correlation coefficient of .1628, and 95% confidence interval of [CI not rendered in HTML text]. This correlation is consistent with the implications of our theory, which predict an association between the total number of secret alliances and the deterrent value of concurrent public defensive alliances."

8. Same (eighth) paragraph: the authors' own weighting of M2.
   > "To be clear, we do not argue that this relationship is causal. To the contrary, our model suggests that the relationship is _not_ causal."

   > "Thus, while this does not provide confirmatory evidence of our model, this pattern is consistent with the predictions of our theory. Further, we believe that this empirical pattern is not straightforward to explain without the guidance of our theoretical arguments."

9. Robustness section (first sentence): "robustness" in the paper refers to model extensions, not to the correlations.
   > "We now briefly discuss the robustness of our findings to several extensions of the model."

## Implication for the audit (judgement, not a result)
- The reproduction targets are correctly the paper's only quantitative empirical claims, but a failure or fragility of M2 would weaken a supporting, explicitly non-confirmatory exhibit, not the paper's main (theoretical) contribution. This is worth one line in the batch report next to the class and the R_b outcome.
- PREREG wording "Main result (M2, the empirical counterpart of the abstract's ... claim)" is consistent with this check and is not edited.
