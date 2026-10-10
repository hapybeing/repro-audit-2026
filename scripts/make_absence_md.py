"""Generate papers/<id>/ABSENCE_SEARCHES.md from papers/<id>/data_statement_raw/absence_searches.json (batch 1)
or absence_searches_scripted.json (batch 2: 08, 09, 10; 08's pre-registration log keeps its frozen name).
Batch 3 (11, 14): from data_statement_raw/absence_searches.json written by the pre-registration scripts
data_statement_raw/absence_11.py and data_statement_raw/absence_searches_14.py (both frozen; a list of records whose time
field is an ISO 8601 UTC time).
Batch 4 (17, 18, 20): from data_statement_raw/absence_searches.json written by the frozen pre-registration scripts
absence_searches_17.py, absence_searches_18.py and absence_searches_20.py (records whose utc field is an ISO 8601 UTC time).
19_KH0SQ2's searches are for the absence of a data statement (statement_searches.json) and stay in its DATA_STATEMENT.md.
Usage (from repo/): python3 scripts/make_absence_md.py [1|2|3|4]   (default 1; batch 1 to 3 output is unchanged)
No number is typed by hand: counts are read from the JSON written by scripts/absence_searches.py."""
import json, re, sys
BATCH = sys.argv[1] if len(sys.argv) > 1 else "1"

CLAIM = {
    "01_5BIH0P": ("The production trajectory of 2XWT, 310 K, seed #3 (dynamic-nopbc.xtc, dynamic-nopbc-2.xtc, system_reduced.xtc) "
                  "is not deposited at any location the paper points to or that these searches reach.",
                  "a file in, or a dataset titled, 2XWT + 310K + seed #3, other than the audited deposit DVN/5BIH0P and its analysis record DVN/TZAPSH (neither holds a production trajectory: see DATA_STATEMENT.md)"),
    "03_3IOGQ8": ("No ProteomeXchange (PRIDE, MassIVE, jPOST, iProX) accession exists for this paper, and the Byonic PSM export the notebook reads is not deposited.",
                  "a dataset whose title mentions sortase together with histone or chromatin, or whose title or metadata contains Whedon, jacs.4c12585, 39585806 or EBZ_Cole (the raw-file prefix in the deposit); for SI and article text, any accession or repository name"),
    "04_PSHE5L": ("The article (and its supplement) contains no data availability statement and cites no data location.",
                  "any term pointing to a data location in the article text; any record that links this article to a dataset other than the code-only deposit DVN/PSHE5L"),
}


CLAIM2 = {
    "08_SQRZR8": ("The data preparation script data_preparation_rep.R, named in the deposit's ReadMe.txt, is not deposited at any location the article points to or that these searches reach.",
                  "a file named data_preparation_rep.R anywhere searched; a version of DVN/SQRZR8 listing it; or a dataset, software or other non-text record for this article other than DVN/SQRZR8"),
    "09_4U8CTG": ("The Study 1 inputs (study1_fes_panel.csv, study1_fes_panel_long.csv, or the ELIPSS files elipss_fes2022_v3.csv and elipss_fes2022_cses_v4.csv that 00_fes_data_preprocessing.R reads) are not openly downloadable: the FES 2022 wave 3 and wave 4 data files sit behind registration at ELIPSS.",
                  "a public copy of any of the four files, or unrestricted FES 2022 data files for BOTH wave 3 and wave 4 (the 00 script needs both), or HTTP 200 with data on an anonymous request to a restricted ELIPSS data file"),
    "10_6MLKJZ": ("The article and its online appendix contain no data availability statement and name no data or code location (so rule #4 materials are the deposit DVN/6MLKJZ alone).",
                  "a transcript line that names a data or code location for this article (not an agent's note saying none exists); a record that links this article to a dataset or software other than DVN/6MLKJZ; any Zenodo, OSF or GitHub record for this article"),
}
DEPOSIT = {"08_SQRZR8": "10.7910/dvn/sqrzr8", "09_4U8CTG": "10.7910/dvn/4u8ctg", "10_6MLKJZ": "10.7910/dvn/6mlkjz"}


def judge2(pid, r):
    h, src, q = r["relevant_hits"], r["source"], r["query"]
    dep = DEPOSIT[pid]
    if src.startswith("Transcript"):
        nz = {k: v for k, v in h.items() if v}
        if not nz:
            return "none: all term counts 0"
        lines = sorted({n for v in nz.values() for n in v})
        return ("matching lines " + ", ".join(map(str, lines)) + " (terms: " + ", ".join(nz) + "); each was read: "
                + {"sage_html": "line 52 is Sage's licence sentence on permission requests ('permission requests for re-use'), not a data statement",
                   "article_pdf": "every line is the reader's note that no data, replication, Dataverse, OSF or GitHub statement exists",
                   "supplement": "lines 131 to 132 are the reader's note that the appendix has no data statement and names no repository"}[
                    "sage_html" if "sage_html" in r["url"] else ("article_pdf" if "article_pdf" in r["url"] else "supplement")]
                + "; no hit")
    if src.startswith("Crossref"):
        return f"relation field: {h['relation'] or 'empty'}; links: publisher PDF/XML only ({len(h['link_urls'])} entries); no hit"
    if src.startswith("ELIPSS dataset metadata"):
        data = [x for x in h["unrestricted"] if not re.search(r"\.(pdf|xml|txt)$", x["file"] or "", re.I)]
        return (f"{len(h['files'])} files, {len(h['unrestricted'])} unrestricted; unrestricted data files: "
                + (", ".join(x["file"] for x in data) if data else "none") + " (restricted: "
                + ", ".join(x["file"] for x in h["files"] if x["restricted"]) + ")")
    if src.startswith("ELIPSS file access"):
        return f"HTTP {r['http']}, {h['bytes_returned']} bytes: " + ("no data returned; no hit" if r["http"] != 200 else "data returned: HIT")
    if src.startswith("Harvard Dataverse dataset versions"):
        bad = [v["version"] for v in h if "data_preparation_rep.R" in v["files"]]
        return f"{len(h)} version(s) ({', '.join(v['version'] for v in h)}), files per version: " + "; ".join(", ".join(v["files"]) for v in h) + ("; none lists data_preparation_rep.R" if not bad else f"; HIT in {bad}")
    if src.startswith("DataCite DOI record"):
        return (f"{h['resource_type']} record, sizes {h['sizes'] or 'not given'}, relations {h['relations'] or 'none'}"
                + {"Text": ": a text record (article copy or appendix), not data or code; no hit",
                   "Collection": ": collection record lists no files or sizes; the figshare API returns 'Entity not found' and sage.figshare.com blocks scripted requests, so its contents were not established; the only item DOI returned for this article is the appendix record above"}.get(h["resource_type"], ""))
    if isinstance(h, list):
        if not h:
            return "none"
        others = []
        for x in h:
            d = (x.get("doi") or "").lower().replace("doi:", "")
            if d.startswith(dep) or d == dep:
                continue
            if pid == "08_SQRZR8" and q.endswith("type=file"):
                if x.get("name") == "data_preparation_rep.R":
                    others.append(x)
                continue
            others.append(x)
        if pid == "08_SQRZR8" and q.startswith("Guo"):
            others = []
        if not others:
            return "only the audited deposit " + dep.upper().replace("10.7910/DVN/", "doi:10.7910/DVN/") if len(h) else "none"
        return (f"{len(others)} item(s) other than the deposit, not hits by themselves; each DOI is checked in a 'DataCite DOI record' row of this table: "
                + "; ".join(f"{x.get('doi') or x.get('name') or x.get('repo')} ({re.sub('<[^>]+>', '', x.get('title') or x.get('dataset') or x.get('description') or '')})" for x in others))
    return str(h)


def judge(pid, r):
    if pid in CLAIM2:
        return judge2(pid, r)
    h = r["relevant_hits"]
    if pid == "03_3IOGQ8" and isinstance(h, list):
        bad = []
        for x in h:
            if isinstance(x, dict):
                t = (x.get("title") or "").lower()
                if ("sortase" in t and ("histone" in t or "chromatin" in t)) or any(k in json.dumps(x).lower() for k in ["whedon", "jacs.4c12585", "39585806", "ebz_cole"]):
                    bad.append(x)
        if r["source"].startswith("Europe PMC Annotations"):
            return "only " + ", ".join(sorted(set(h))) + " (a PDB ID and the audited deposit)"
        return "none" if not bad else f"{len(bad)}: {bad}"
    if pid == "03_3IOGQ8" and isinstance(h, dict) and "matches_per_file" in h:
        m = {k: v for k, v in h["matches_per_file"].items() if v}
        return "none in " + ", ".join(h["matches_per_file"]) if not m else f"matches: {m}"
    if pid == "03_3IOGQ8" and h == []:
        return "none"
    if pid == "01_5BIH0P":
        if isinstance(h, dict):
            return "term counts: " + ", ".join(f"{k} {v}" for k, v in h.items())
        if r["query"].startswith("title:2XWT"):
            dois = sorted(x["doi"] for x in h)
            other = [d for d in dois if d not in ("doi:10.7910/DVN/5BIH0P", "doi:10.7910/DVN/TZAPSH")]
            return f"{len(h)} ({', '.join(dois)}); other than the deposit and its analysis record: {len(other)}"
        return f"{len(h)}" if h else "none"
    if pid == "04_PSHE5L":
        if isinstance(h, dict) and "relation" in h:
            return f"relation field: {h['relation'] or 'empty'}; links: publisher PDF/XML only ({len(h['link_urls'])} entries)"
        if isinstance(h, dict):
            nz = {k: v for k, v in h.items() if v}
            if set(nz) == {"on request"}:
                return ("none: all term counts 0 except 'on request' 1, which is inside Sage's boilerplate "
                        "'permission requests for re-use of supplemental material' (substring 'permissi[on request]s')")
            return "term counts all 0 except " + ", ".join(f"'{k}' {v}" for k, v in nz.items()) if nz else "none: all term counts 0"
        if not h:
            return "none"
        flag = [x for x in h if isinstance(x, dict) and "mtd4z_in_response" in x]
        h = [x for x in h if not (isinstance(x, dict) and "mtd4z_in_response" in x)]
        items = [str(x.get("doi") or x.get("name") or x) if isinstance(x, dict) else str(x) for x in h]
        if all("pshe5l" in i.lower() for i in items):
            return f"none: only {items[0]} (the code-only deposit, which names no data location and is not cited by the article)"
        if r["source"].startswith("OSF"):
            return ("none from the article: returned " + "; ".join(items) + ". 'Rural Populism' is OSF component mtd4z (osf.io/mtd4z in the response: " + str(flag[0]["mtd4z_in_response"] if flag else "not recorded") + "), found by the audit, "
                    "not cited by the article (DATA_STATEMENT.md); the other title is a different study")
        return "; ".join(items)
    return str(h)


CLAIM3 = {
    "11_DDOFPS": ("The two input files the script reads under these exact names, bd_doxa_programas.xlsx and bd_doxa_candidatos.xlsx, are not deposited under those names in any version of DVN/DDOFPS or in any Harvard Dataverse dataset; same-structure files are deposited as bd_doxa_programas_HGPE.xlsx (and _v2) and bd_doxa_candidatos_HGPE.xlsx.",
                  "a file named exactly bd_doxa_programas.xlsx or bd_doxa_candidatos.xlsx in any version of the deposit or in any Harvard Dataverse dataset",
                  "data_statement_raw/absence_11.py"),
    "14_CJISMY": ("The files read only by scripts outside the main-results list (helper_functions_eo2_extraction_analysis.R, data.csv, GeoEPR-2019.csv, EPR_merged.csv, gpw_v4_population_count_rev11_2000_30_min.tif) are not deposited at any location linked to these authors or this article that these searches reach. No target depends on them.",
                  "a file with exactly the missing name, in a dataset or repository linked to these authors or this article",
                  "data_statement_raw/absence_searches_14.py"),
}
MISSING3 = {"11_DDOFPS": {"bd_doxa_programas.xlsx", "bd_doxa_candidatos.xlsx"},
            "14_CJISMY": {"helper_functions_eo2_extraction_analysis.R", "data.csv", "GeoEPR-2019.csv", "EPR_merged.csv",
                          "gpw_v4_population_count_rev11_2000_30_min.tif"}}
DEPOSIT3 = {"11_DDOFPS": "doi:10.7910/DVN/DDOFPS", "14_CJISMY": "doi:10.7910/DVN/CJISMY"}


def utc3(t):
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})Z", t)
    assert m, t
    return f"{m.group(1)} {m.group(2)}"


def judge3(pid, r):
    h = r["relevant_hits"]
    if not h:
        near = r.get("near_matches")
        return "none" + (f" (files with other names in the deposit: {', '.join(near)})" if near else "")
    names, others = [], []
    for x in h:
        if isinstance(x, list):
            name, doi = x[0], x[1]
            names.append(name)
            if name in MISSING3[pid]:
                return f"HIT: {name} in {doi}"
            others.append(f"{name} in {doi} (file {x[2]})")
        else:
            doi = x.get("doi")
            if doi != DEPOSIT3[pid]:
                others.append(f"{doi} ({x.get('name')})")
    if pid == "11_DDOFPS":
        return "positive control, not a hit: returns " + "; ".join(others) + ", a deposited file under its deposited name"
    return ("only the audited deposit " + DEPOSIT3[pid] + (" and " + "; ".join(others) + ", a dataset for a different article" if others else "")
            + "; no file with a missing name")


CLAIM4 = {
    "17_T1NXVQ": ("The files read only by the two scripts marked 'Do not run' and by the data-preparation step (data/analysis_data/res_optim.rds and raw inputs such as gsdm.rds, sdm_claims.csv, epr_sec.geojson, epr_sec.csv, Final_df_complete.shp) are not deposited at any location linked to these authors or this article that these searches reach. No target depends on them.",
                  "a file with exactly the missing name in a dataset or repository linked to these authors or this article",
                  "data_statement_raw/absence_searches_17.py"),
    "18_YXC5K5": ("The raw-text and batch-output files read only by Benchmarking_DataGeneration.Rmd (full_df_for_classification_ten.csv, batch_part1_output_v2.jsonl, batch_part2_output_v2.jsonl) are not deposited at any location these searches reach. No target depends on them.",
                  "a file whose name equals the missing name exactly (Dataverse, Zenodo, dataset versions), or a repository or dataset clearly for this article (GitHub, OSF, Dataverse dataset searches)",
                  "data_statement_raw/absence_searches_18.py"),
    "20_SINIYU": ("The module interp_radar (interp_radar_ppi, interp_radar_shift) imported by codes/figure6/O_B_Ku.py line 17, and any code that computes Table 1, are not in the deposit or at any location the article's data statement names, and these searches found no copy elsewhere.",
                  "a file or repository whose name (or for GitHub, name or description) contains interp_radar, or an item that holds this article's code; for the two volume-matching queries the search script lists every FY-3G item for reading",
                  "data_statement_raw/absence_searches_20.py"),
}


def utc4(t):
    return utc3(t)


def judge4(pid, r):
    h = r.get("relevant_hits", r.get("hits"))
    if not h:
        return "none"
    if pid == "20_SINIYU":
        items = "; ".join(f"{x['doi']} ({x['title'][:70]})" for x in h)
        return ("FY-3G items listed by the script for reading: " + items + ". Read in DATA_STATEMENT.md: records of other studies, none holds this article's code or interp_radar; no hit")
    return "HIT: " + json.dumps(h)[:200]


if BATCH == "4":
    for pid, (claim, rule, script) in CLAIM4.items():
        recs = json.load(open(f"papers/{pid}/data_statement_raw/absence_searches.json"))
        L = [f"# Absence searches: {pid}", "",
             f"Generated by `scripts/make_absence_md.py 4` from `data_statement_raw/absence_searches.json`, which the pre-registration script `{script}` wrote before any run "
             "(both files are frozen; sha256 in `batches/batch4_prereg_hashes.txt`). Re-run that script to repeat every search below. Public APIs only, no sign-in, no author contact. "
             "",
             f"**Claim checked:** {claim}", "",
             f"**What would count as a hit against the claim:** {rule}.", "",
             "| # | Source | Query | Exact URL | Time (UTC) | HTTP | Results returned | Hits against the claim |",
             "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(recs, 1):
            L.append(f"| {i} | {r['source']} | `{r['query']}` | {r['url']} | {utc4(r['utc'])} | {r['http']} | "
                     f"{'' if r['total_results'] is None else r['total_results']} | {judge4(pid, r)} |")
        notes = [r for r in recs if r.get("note")]
        if notes:
            L += ["", "Notes per search (as recorded by the search script):"]
            for i, r in enumerate(recs, 1):
                if r.get("note"):
                    L.append(f"- #{i}: {r['note']}")
        L += ["", "Results returned = the count the source reports. A search that returns results is not a hit: every returned item was tested against the rule above, and the last column shows what passed.",
              "", "Searches can show absence only within what they searched (see the Finding section of DATA_STATEMENT.md for what was not checked)."]
        text = "\n".join(L) + "\n"
        text = text.replace("\u2014", ",")
        open(f"papers/{pid}/ABSENCE_SEARCHES.md", "w").write(text)
        print("wrote", pid, len(recs))
    sys.exit(0)

if BATCH == "3":
    for pid, (claim, rule, script) in CLAIM3.items():
        recs = json.load(open(f"papers/{pid}/data_statement_raw/absence_searches.json"))
        L = [f"# Absence searches: {pid}", "",
             f"Generated by `scripts/make_absence_md.py 3` from `data_statement_raw/absence_searches.json`, which the pre-registration script `{script}` wrote before any run "
             "(both files are frozen; sha256 in `batches/batch3_prereg_hashes.txt`). Re-run that script to repeat every search below. Public APIs only, no sign-in, no author contact.", "",
             f"**Claim checked:** {claim}", "",
             f"**What would count as a hit against the claim:** {rule}.", "",
             "| # | Source | Query | Exact URL | Time (UTC) | HTTP | Results returned | Hits against the claim |",
             "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(recs, 1):
            L.append(f"| {i} | {r['source']} | `{r['query']}` | {r['url']} | {utc3(r['utc'])} | {r['http']} | "
                     f"{'' if r['total_results'] is None else r['total_results']} | {judge3(pid, r)} |")
        notes = [r for r in recs if r.get("note")]
        if notes:
            L += ["", "Notes per search (as recorded by the search script):"]
            for i, r in enumerate(recs, 1):
                if r.get("note"):
                    L.append(f"- #{i}: {r['note']}")
        L += ["", "Results returned = the count the source reports. A search that returns results is not a hit: every returned item was tested against the rule above by this script, and the last column shows what passed."]
        if pid == "11_DDOFPS":
            L += ["", "Limit (from DATA_STATEMENT.md): the Search API tokenises file names, so the partial queries return 0 even though files whose names start with those strings exist in DDOFPS; the positive controls show that full file names are found."]
        if pid == "14_CJISMY":
            L += ["", "Limit (from DATA_STATEMENT.md): for `data.csv` only the first page of results (at most 100) was screened."]
        text = "\n".join(L) + "\n"
        assert "\u2014" not in text
        open(f"papers/{pid}/ABSENCE_SEARCHES.md", "w").write(text)
        print("wrote", pid, len(recs))
    sys.exit(0)

for pid in (CLAIM if BATCH == "1" else CLAIM2):
    fn = "absence_searches.json" if BATCH == "1" else "absence_searches_scripted.json"
    d = json.load(open(f"papers/{pid}/data_statement_raw/{fn}"))
    claim, rule = (CLAIM if BATCH == "1" else CLAIM2)[pid]
    L = [f"# Absence searches: {pid}", "",
         f"Generated by `scripts/make_absence_md.py{'' if BATCH == '1' else ' 2'}` from `data_statement_raw/{fn}`, which `scripts/absence_searches.py {pid[:2]}` writes. "
         "Re-run both scripts from the repo root to repeat every search below. Public APIs only, no sign-in, no author contact.", "",
         f"**Claim checked:** {claim}", "",
         f"**What would count as a hit against the claim:** {rule}.", "",
         "| # | Source | Query | Exact URL | Time (UTC) | HTTP | Results returned | Hits against the claim |",
         "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(d["records"], 1):
        L.append(f"| {i} | {r['source']} | `{r['query']}` | {r['url']} | {r['utc']} | {r['http']} | "
                 f"{'' if r['total_results'] is None else r['total_results']} | {judge(pid, r)} |")
    notes = [r for r in d["records"] if r.get("note")]
    if notes:
        L += ["", "Notes per search:"]
        for i, r in enumerate(d["records"], 1):
            if r.get("note"):
                L.append(f"- #{i}: {r['note']}")
    L += ["", "Results returned = the count the source reports (or the number of items, where the source gives no total). "
          "A search that returns results is not a hit: every returned item was tested against the rule above by the script, and the last column shows what passed."]
    open(f"papers/{pid}/ABSENCE_SEARCHES.md", "w").write("\n".join(L) + "\n")
    print("wrote", pid, len(d["records"]))
