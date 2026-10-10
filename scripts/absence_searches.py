"""Re-runnable searches behind the batch 1 absence claims (01, 03, 04).

Usage: python3 scripts/absence_searches.py 01|03|04   (run from repo/)
Writes papers/<id>/data_statement_raw/absence_searches.json: one record per query with the exact URL,
UTC time, HTTP status, total result count and the hits that could be relevant. Public APIs only, no sign-in.
ABSENCE_SEARCHES.md is generated from that JSON by scripts/make_absence_md.py.
"""
import json, sys, re, io, zipfile, time, datetime, urllib.request, urllib.parse, urllib.error

UA = {"User-Agent": "repro-audit-2026 (github.com/hapybeing/repro-audit-2026)", "Accept": "application/json"}
RECS = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, headers=None, timeout=90, raw=False):
    h = dict(UA); h.update(headers or {})
    t = now()
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)
            b = r.read()
            return t, r.status, (b if raw else b.decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(5); continue
            return t, e.code, b"" if raw else ""
        except Exception as e:  # network error
            if attempt < 2:
                time.sleep(5); continue
            return t, f"error: {type(e).__name__}", b"" if raw else ""


def rec(paper, source, query, url, t, status, total, relevant, note=""):
    RECS.append({"paper": paper, "source": source, "query": query, "url": url, "utc": t, "http": status,
                 "total_results": total, "relevant_hits": relevant, "note": note})
    print(source, "|", query, "|", status, "| total", total, "| relevant", len(relevant) if isinstance(relevant, list) else relevant)


# ---------------------------------------------------------------- 01
def dv_search_all(q, extra):
    """Harvard Dataverse Search API, paged 1000 at a time. Returns (first url, time, status, total, items)."""
    items, start, first = [], 0, None
    while True:
        params = [("q", q), ("per_page", "1000"), ("start", str(start))] + extra
        url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode(params)
        t, st, body = get(url)
        if first is None:
            first = (url, t, st)
        if st != 200:
            return first[0], first[1], st, None, items
        d = json.loads(body)["data"]
        items += d["items"]
        start += 1000
        if start >= d["total_count"]:
            return first[0], first[1], first[2], d["total_count"], items
        time.sleep(1)


def is_target_01(name):
    n = (name or "").lower()
    return "2xwt" in n and "310k" in n.replace(" ", "") and ("seed #3" in n or "seed#3" in n or "seed 3" in n)


def run01():
    P = "01_5BIH0P"
    # A. every .xtc file in the ThermoPCD collection
    url, t, st, tot, items = dv_search_all("fileName:*.xtc", [("type", "file"), ("subtree", "ThermoPCD")])
    rel = [{"file": i["name"], "dataset": i.get("dataset_name"), "dataset_doi": i.get("dataset_persistent_id")}
           for i in items if is_target_01(i.get("dataset_name"))]
    n2 = sum(1 for i in items if "2xwt" in (i.get("dataset_name") or "").lower())
    rec(P, "Harvard Dataverse Search API (collection ThermoPCD)", "fileName:*.xtc, type=file, subtree=ThermoPCD", url, t, st, tot, rel,
        f"{n2} of the returned xtc files belong to datasets whose title contains 2XWT; relevant = title also contains 310K and seed #3")
    # B. the three missing file names, anywhere on Harvard Dataverse
    for fn in ["dynamic-nopbc.xtc", "dynamic-nopbc-2.xtc", "system_reduced.xtc"]:
        url, t, st, tot, items = dv_search_all(f'fileName:"{fn}"', [("type", "file")])
        rel = [{"file": i["name"], "dataset": i.get("dataset_name"), "dataset_doi": i.get("dataset_persistent_id")}
               for i in items if is_target_01(i.get("dataset_name"))]
        rec(P, "Harvard Dataverse Search API (all of Harvard Dataverse)", f'fileName:"{fn}", type=file', url, t, st, tot, rel,
            "relevant = file in a dataset whose title contains 2XWT, 310K and seed #3")
        time.sleep(1)
    # C. 2XWT datasets anywhere on Harvard Dataverse
    url, t, st, tot, items = dv_search_all("title:2XWT", [("type", "dataset")])
    rel = [{"dataset": i["name"], "doi": i.get("global_id")} for i in items if is_target_01(i.get("name"))]
    rec(P, "Harvard Dataverse Search API (all of Harvard Dataverse)", "title:2XWT, type=dataset", url, t, st, tot, rel,
        "relevant = title contains 310K and seed #3 (expected: 5BIH0P and TZAPSH, the audited deposit and its analysis record)")
    # D. other repositories
    for q in ['"2XWT" AND (trajectory OR xtc)', '"ThermoPCD"']:
        url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": "25"})
        t, st, body = get(url)
        hits = json.loads(body)["hits"] if st == 200 else {"hits": [], "total": None}
        rec(P, "Zenodo REST API", q, url, t, st, hits["total"],
            [{"title": h["metadata"]["title"], "doi": h.get("doi")} for h in hits["hits"]])
    for q in ["ThermoPCD", "2XWT"]:
        url = "https://api.datacite.org/dois?" + urllib.parse.urlencode({"query": q, "page[size]": "100"})
        t, st, body = get(url)
        d = json.loads(body) if st == 200 else {"data": [], "meta": {"total": None}}
        non_harvard = [{"doi": x["id"], "title": (x["attributes"]["titles"] or [{}])[0].get("title")}
                       for x in d["data"] if not x["id"].lower().startswith("10.7910/")]
        rec(P, "DataCite REST API (all DataCite repositories)", q, url, t, st, d["meta"].get("total"), non_harvard,
            "relevant = any DOI outside Harvard Dataverse (prefix 10.7910); first 100 results inspected")
    # E. repository words in the article full text (Europe PMC XML, saved locally; not redistributed)
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10950042/fullTextXML"
    t, st, body = get(url, headers={"Accept": "application/xml"})
    terms = ["zenodo", "figshare", "github", "osf.io", "mendeley data", "dryad", "upon request", "on request", "xtc", "dataverse"]
    counts = {k: len(re.findall(re.escape(k), body.lower())) for k in terms} if st == 200 else {}
    rec(P, "Europe PMC full text XML (article text)", "case-insensitive term counts", url, t, st, None, counts,
        "only Harvard Dataverse is named as a data location; see DATA_STATEMENT.md")


# ---------------------------------------------------------------- 03
TERMS03 = ["sortase", "Whedon", "jacs.4c12585", "39585806", "EBZ_Cole", "MS275", "Corin", "middle-down histone",
           "circular engineered sortase", "cW11", "histone H3 chromatin"]
TEXT03 = ["sortase", "whedon", "jacs.4c12585", "39585806", "ebz_cole", "ms275", "corin", "middle-down", "middle down", "cw11"]


def run03(part="all"):
    P = "03_3IOGQ8"
    on = lambda k: part in ("all", k)
    # A. ProteomeXchange PROXI (central; covers PRIDE, MassIVE, jPOST, iProX, PeptideAtlas, Panorama)
    for q in (TERMS03 if on("proxi") else []):
        url = "https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets?" + urllib.parse.urlencode({"search": q, "resultType": "compact", "pageSize": "500"})
        t, st, body = get(url)
        ds = json.loads(body).get("datasets", []) if st == 200 else []
        rec(P, "ProteomeXchange PROXI (ProteomeCentral)", q, url, t, st, len(ds) if st == 200 else None,
            [{"id": d[0], "title": d[1], "repository": d[2]} for d in ds])
        time.sleep(0.5)
    # B. PRIDE Archive v2 and v3 keyword search
    for q in (TERMS03 if on("pride") else []):
        for ver in ["v2", "v3"]:
            url = f"https://www.ebi.ac.uk/pride/ws/archive/{ver}/search/projects?" + urllib.parse.urlencode({"keyword": q, "pageSize": "100"})
            t, st, body = get(url)
            try:
                d = json.loads(body) if st == 200 else []
            except Exception:
                d = []
            if isinstance(d, dict):
                d = d.get("_embedded", {}).get("compactprojects", []) or d.get("content", [])
            hits = [{"id": x.get("accession"), "title": x.get("title")} for x in d] if isinstance(d, list) else []
            rec(P, f"PRIDE Archive API {ver}", q, url, t, st, len(hits) if st == 200 else None, hits)
            time.sleep(0.5)
    # C. MassIVE full public dataset listing, searched locally (title, description, keywords, PI, user)
    if not on("massive"): return run03_rest(P, part)
    url = "https://massive.ucsd.edu/ProteoSAFe/datasets_json.jsp"
    t, st, body = get(url, timeout=110)
    ds = json.loads(body)["datasets"] if st == 200 else []
    for q in TERMS03:
        hits = [{"id": d.get("dataset"), "title": d.get("title")} for d in ds if q.lower() in json.dumps(d).lower()]
        rec(P, "MassIVE public dataset listing (full JSON, searched locally)", q, url, t, st, len(hits), hits,
            f"{len(ds)} MassIVE datasets in the listing")
    return run03_rest(P, part)


def run03_rest(P, part):
    on = lambda k: part in ("all", k)
    pat = re.compile(r"(PXD\d{6}|MSV\d{9}|JPST\d{6}|IPX\d{7}|PRIDE|MassIVE|ProteomeXchange|jPOST|iProX|PeptideAtlas)", re.I)
    if not on("jpost"): return run03_si(P, part, pat)
    # D. jPOST PROXI full listing, searched locally
    url = "https://repository.jpostdb.org/proxi/datasets?resultType=compact"
    t, st, body = get(url, timeout=110)
    ds = json.loads(body) if st == 200 else []
    for q in TERMS03:
        hits = [{"id": [a["value"] for a in d.get("accession", [])], "title": d.get("title")} for d in ds if q.lower() in json.dumps(d).lower()]
        rec(P, "jPOST repository PROXI listing (searched locally)", q, url, t, st, len(hits), hits, f"{len(ds)} jPOST datasets in the listing")
    return run03_si(P, part, pat)


def run03_si(P, part, pat):
    if part not in ("all", "si"): return
    # E. article Supporting Information via Europe PMC (the publisher site returns 403 to scripts)
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11638967/supplementaryFiles"
    import os, hashlib
    si_dir = os.environ.get("SI_DIR")  # optional: folder with the SI members already downloaded from the URL above
    found, members, hashes = {}, [], {}
    if si_dir:
        t, st = now(), "local copy of SI members (live zip download >110 s, see note)"
        blobs = {n: open(os.path.join(si_dir, n), "rb").read() for n in sorted(os.listdir(si_dir)) if n.endswith((".pdf", ".xlsx"))}
    else:
        t, st, body = get(url, headers={"Accept": "application/zip"}, raw=True, timeout=110)
        blobs = {}
        if st == 200:
            z = zipfile.ZipFile(io.BytesIO(body))
            blobs = {n: z.read(n) for n in z.namelist()}
    for n, data in blobs.items():
        members.append(n)
        hashes[n] = hashlib.sha256(data).hexdigest()
        texts = []
        if n.lower().endswith(".xlsx"):
            zz = zipfile.ZipFile(io.BytesIO(data))
            texts = [zz.read(m).decode("utf-8", "replace") for m in zz.namelist() if m.endswith(".xml")]
        elif n.lower().endswith(".pdf"):
            import subprocess, tempfile
            with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
                f.write(data); f.flush()
                texts = [subprocess.run(["pdftotext", f.name, "-"], capture_output=True, text=True).stdout]
        found[n] = sorted(set(m.group(0) for tx in texts for m in pat.finditer(tx)))
    rec(P, "Europe PMC supplementaryFiles (article SI: PDF and XLSX)",
        "regex PXD######|MSV#########|JPST######|IPX#######|PRIDE|MassIVE|ProteomeXchange|jPOST|iProX|PeptideAtlas",
        url, t, st, len(members), {"matches_per_file": found, "sha256": hashes},
        "total_results = SI files searched (PDF text via pdftotext, XLSX via its XML parts); empty list = no match. "
        "When SI_DIR is used, the files are the SI members downloaded from this URL on 2026-10-09 by Agent A; their sha256 equal those recorded in PREREG.md")
    # F. article full text and Europe PMC text-mined accessions
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11638967/fullTextXML"
    t, st, body = get(url, headers={"Accept": "application/xml"})
    hits = sorted(set(m.group(0) for m in pat.finditer(body))) if st == 200 else None
    rec(P, "Europe PMC full text XML (article text)", "same regex as SI", url, t, st, None, hits)
    url = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?" + urllib.parse.urlencode({"articleIds": "PMC:PMC11638967", "type": "Accession Numbers", "format": "JSON"})
    t, st, body = get(url)
    ann = [a["exact"] for x in (json.loads(body) if st == 200 else []) for a in x.get("annotations", [])]
    rec(P, "Europe PMC Annotations API (text-mined accession numbers)", "type=Accession Numbers", url, t, st, len(ann), ann)


# ---------------------------------------------------------------- 04
TEXT04 = ["osf", "10.7910", "dataverse", "github", "zenodo", "icpsr", "figshare", "openicpsr", "replication data",
          "replication code", "replication material", "on request", "upon request", "data availability", "available from"]


def run04():
    P = "04_PSHE5L"
    # A. term counts in the saved Sage full text (local copy; not redistributed)
    path = "papers/04_PSHE5L/data_statement_raw/sage_fulltext_webfetch.md"
    try:
        body = open(path, encoding="utf-8").read().lower()
        counts = {k: len(re.findall(re.escape(k), body)) for k in TEXT04}
        rec(P, "Article full text (Sage HTML, saved copy; sha256 in DATA_STATEMENT.md)", "case-insensitive term counts", path, now(), "local file", None, counts,
            "nonzero counts were each read in context: see DATA_STATEMENT.md (only Sage boilerplate and reference-list entries)")
    except FileNotFoundError:
        rec(P, "Article full text (Sage HTML, saved copy)", "term counts", path, now(), "missing locally", None, {})
    # B. Crossref metadata: relations and links registered by the publisher
    url = "https://api.crossref.org/works/10.1177/23780231251317227"
    t, st, body = get(url)
    m = json.loads(body)["message"] if st == 200 else {}
    rec(P, "Crossref REST API (publisher-registered metadata)", "relation and link fields", url, t, st, None,
        {"relation": m.get("relation"), "link_urls": [l["URL"] for l in m.get("link", [])]})
    # C. DataCite: any dataset that declares this article as related
    for q in ['relatedIdentifiers.relatedIdentifier:"10.1177/23780231251317227"', '"Rural Populism and Tolerance for Political Violence"']:
        url = "https://api.datacite.org/dois?" + urllib.parse.urlencode({"query": q, "page[size]": "100"})
        t, st, body = get(url)
        d = json.loads(body) if st == 200 else {"data": [], "meta": {}}
        rec(P, "DataCite REST API", q, url, t, st, d["meta"].get("total"),
            [{"doi": x["id"], "title": (x["attributes"]["titles"] or [{}])[0].get("title")} for x in d["data"]])
    # D. Zenodo, figshare, Harvard Dataverse, OSF (SHARE) by title
    q = '"Rural Populism"'
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": "25"})
    t, st, body = get(url)
    h = json.loads(body)["hits"] if st == 200 else {"hits": [], "total": None}
    rec(P, "Zenodo REST API", q, url, t, st, h["total"], [{"title": x["metadata"]["title"], "doi": x.get("doi")} for x in h["hits"]])
    url = "https://api.figshare.com/v2/articles/search"
    t = now()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, data=json.dumps({"search_for": '"Rural Populism and Tolerance for Political Violence"'}).encode(),
                                                          headers={**UA, "Content-Type": "application/json"}), timeout=60)
        d = json.loads(r.read()); st = r.status
    except urllib.error.HTTPError as e:
        d, st = [], e.code
    rec(P, "figshare API v2 (POST /articles/search)", '"Rural Populism and Tolerance for Political Violence"', url, t, st, len(d), [x.get("title") for x in d])
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": '"Rural Populism"', "type": "dataset", "per_page": "100"})
    t, st, body = get(url)
    d = json.loads(body)["data"] if st == 200 else {"items": [], "total_count": None}
    rec(P, "Harvard Dataverse Search API", '"Rural Populism", type=dataset', url, t, st, d["total_count"],
        [{"name": x["name"], "doi": x.get("global_id")} for x in d["items"] if "rural populism" in x["name"].lower()],
        "Dataverse search matches words, not the exact phrase; relevant = dataset title contains 'rural populism' (first 100 results inspected)")
    url = "https://share.osf.io/api/v3/index-card-search?" + urllib.parse.urlencode({"cardSearchText": '"Rural Populism"', "page[size]": "50"})
    t, st, body = get(url, headers={"Accept": "application/vnd.api+json"})
    total, titles = None, []
    if st == 200:
        try:
            d = json.loads(body)
            total = d.get("data", {}).get("attributes", {}).get("totalResultCount")
            for inc in d.get("included", []):
                rm = inc.get("attributes", {}).get("resourceMetadata", {})
                for tt in rm.get("title", []) if isinstance(rm, dict) else []:
                    titles.append(tt.get("@value"))
        except Exception as e:
            titles = [f"parse error {e}"]
    titles.append({"mtd4z_in_response": "osf.io/mtd4z" in body})
    rec(P, "OSF / SHARE search API", '"Rural Populism"', url, t, st, total, titles,
        "OSF component mtd4z holds data and code but is not cited by the article; this search shows whether it is indexed")


if __name__ == "__main__":
    which = sys.argv[1]
    pid = {"01": "01_5BIH0P", "03": "03_3IOGQ8", "04": "04_PSHE5L"}[which]
    part = sys.argv[2] if len(sys.argv) > 2 else "all"
    out = f"papers/{pid}/data_statement_raw/absence_searches.json"
    if which == "03":
        run03(part)
        if part != "all":  # chunked run: keep records of the other chunks, replace this chunk's
            import os
            old = json.load(open(out))["records"] if os.path.exists(out) else []
            keep = [r for r in old if r.get("chunk") != part]
            for r in RECS: r["chunk"] = part
            RECS[:0] = keep
    else:
        {"01": run01, "04": run04}[which]()
    json.dump({"script": "scripts/absence_searches.py", "paper": pid, "run_started_utc": RECS[0]["utc"] if RECS else now(),
               "records": RECS}, open(out, "w"), indent=1, ensure_ascii=False)
    print("wrote", out, len(RECS), "records")
