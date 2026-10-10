# Reproducibility audit — Sage supplementary PDF blocked (Cloudflare)

## Task
Read Sage supplementary PDF for DOI 10.1177/13540688251366827 ("Guilty by association: Party effects of corruption-related prosecutions", M. Ang, Party Politics, published 13 Aug 2025), transcribe Tables B and G exactly, and check the /doi/full/ article + Table 2 visibility. Read-only, no sign-in.

## Result: BLOCKED — could not read any Sage content

Every path into journals.sagepub.com returned a Cloudflare "Just a moment... / Performing security verification" interstitial (full-page, not a Turnstile widget). The solve_captcha tool refused every attempt, reporting "no solvable captcha detected" — it only handles reCAPTCHA/hCaptcha/Turnstile/GeeTest/v3, and this interstitial is a full-page browser-IP check it cannot clear.

### Sage URLs attempted (all returned the same Cloudflare interstitial)
- https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F13540688251366827&file=sj-pdf-1-ppq-10.1177_13540688251366827.pdf
  — the exact supplementary PDF URL from the task.
- https://journals.sagepub.com/doi/full/10.1177/13540688251366827
- https://journals.sagepub.com/doi/pdf/10.1177/13540688251366827
- https://journals.sagepub.com/doi/10.1177/13540688251366827 (via doi.org resolver)
- https://journals.sagepub.com/doi/abs/10.1177/13540688251366827
- https://journals.sagepub.com/doi/10.1177/13540688251366827?download=true
- https://doi.org/10.1177/13540688251366827 (redirects back to Sage → CF)
- solve_captcha called 3 times on different Sage URLs; every time returned "no solvable captcha detected".
- reload (ignore_cache=true) called twice on the supplementary URL — stayed on "Just a moment...".

**Conclusion on Sage**: the full article, the supplementary PDF, and every Sage endpoint for this DOI are equally gated by a Cloudflare interstitial that this browser's solver cannot clear. I cannot determine whether Table 2 of the full article is visible, because the /doi/full/ page itself never loads.

### Mirrors and alternative sources attempted
- **Google Scholar** — lists the article (title "Guilty by association: Party effects of corruption-related prosecutions", M Ang, Party Politics 2025) but only links back to journals.sagepub.com/doi/abs/… (which is CF-blocked). No PDF mirror attached.
- **Semantic Scholar** — the exact DOI query returned only unrelated Sage supplements; a title search returned "No Papers Found".
- **Internet Archive / Wayback Machine** — no snapshots in 2025 or 2026 for:
  - https://journals.sagepub.com/action/downloadSupplement?...1366827
  - https://journals.sagepub.com/doi/10.1177/13540688251366827
  - https://journals.sagepub.com/doi/full/10.1177/13540688251366827
  All three return "The Wayback Machine has not archived that URL."
- **CiteDrive** (https://www.citedrive.com/en/discovery/guilty-by-association-party-effects-of-corruption-related-prosecutions/) — landing page loaded and has a "Show PDF" button, but clicking it opens a full-screen Google interstitial ad that covers the entire page; no PDF text is extractable. The page offers no supplementary-material viewer separately.
- **metatoc.com** — timed out on connection twice (ERR_CONNECTION_TIMED_OUT / no response within 10s).
- **ai.updf.cn** — ERR_TIMED_OUT.
- **DuckDuckGo search for the exact supplement filename** `sj-pdf-1-ppq-10.1177_13540688251366827.pdf` — top hit was scholar.archive.org/work/ubc6sjqh6bcxtanao3ja4ufmo4, but that work is `sj-pdf-1-ppq-10.1177_13540688221097082` (different DOI, different article). Other hits were other journal supplements (13540688211059800, 13540688241249035, 87552930251346786). **No mirror of the 1366827 supplement exists in the index.**
- **ResearchGate / Academia.edu** — only older unrelated "Guilty by association" papers (Saibaba, P.K. Vijayan, group-based collective guilt), not Ang 2025.
- **Author replication packages** — searched OSF, GitHub, Harvard Dataverse, and general web for Milena Ang replication materials tied to this paper. No package surfaced. The "Criminal Contagion" / "Contagio criminal" PDFs on Redalyc / SciELO / politicaygobierno.cide.edu (https://scielo.org.mx/pdf/pyg/v27n2/1665-2037-pyg-27-02-ePYG1280-en.pdf) are the **Spanish-language predecessor article** in Política y Gobierno, not the 2025 Party Politics supplementary material.

### A draft that is NOT a substitute
- https://ijlinz.es/wp-content/uploads/2019/03/Ang_Guilty_by_Association_draft.pdf
  This is Ang's 2019 working draft ("The spillover effects of corruption-related prosecutions...") hosted by the Institute for the Study of Latin American Development. It is an **earlier pre-publication draft**, not the published article and not the supplementary PDF. Its coefficient values, model specifications, and standard errors can differ from the published Tables B and G (the task explicitly requires the published Sage supplementary values for the reproducibility audit). **I did not use it as a substitute.**

## What I could NOT deliver
1. Table B ("Year 2018 x Indicted" row for Models 1–4, Observations, FE district / FE party group counts) — could not open the supplementary PDF.
2. Table G ("Indicted x Year 2018" row for Models 1G–4G, Observations, group counts) — could not open the supplementary PDF.
3. Whether the Sage /doi/full/ page renders the full article text and Table 2 without signing in — the /doi/full/ page itself is behind the same Cloudflare interstitial, so visibility could not be assessed.
4. Screenshots of Tables B, G, or Table 2 — none could be captured because the pages never rendered.

## Why retries won't help
Cloudflare "Just a moment..." interstitials bind to the browser's IP/session; repeating the same navigation from this agent returns the same interstitial. The captcha solver explicitly does not handle full-page CF interstitials. A different browser/IP (or the user solving the CF check themselves, or an institutional/library proxy) would be required to reach Sage.

## Suggested next steps for the parent
- Open the supplementary PDF URL from a browser that passes Sage's Cloudflare check (e.g., the user's own browser, or a library/proxy session), and either (a) paste the transcribed values back into the audit, or (b) provide a working alternate URL so the agent can re-run.
- If the user has a copy of the supplementary PDF locally, a file upload path could be opened.
- Do NOT use the ijlinz.es 2019 draft or the Redalyc/SciELO "Criminal Contagion" PDF in place of the published supplementary — they are not the same artifact.

Run concluded: 2026-10-10, Asia/Kolkata. AGENT=B, PID=07_JH9DBC.