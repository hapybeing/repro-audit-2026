"""Log every scripted route tried to reach the Sage supplementary ZIP of paper 06 (sj-zip-2-prq-10.1177_10659129241301785.zip,
533.77 KB per the Sage article page), which the article's "Supplemental material ... available online" points to.
Usage (from repo/): python3 scripts/p06_supplement_attempts.py
Writes papers/06_VSV5DM/data_statement_raw/supplement_access_attempts.json (URL, UTC time, HTTP status, bytes, what came back).
If any route returns a ZIP, its sha256 and member list are recorded and the bytes are saved OUTSIDE the repository
(/workspace/audit_runs/06_VSV5DM/supplement/); third-party files are not committed."""
import json, datetime, hashlib, io, os, zipfile, urllib.request, urllib.error, urllib.parse

DOI = "10.1177/10659129241301785"
NAME = "sj-zip-2-prq-10.1177_10659129241301785.zip"
DL = "https://journals.sagepub.com/action/downloadSupplement?doi=10.1177%2F10659129241301785&file=" + NAME
SUPP = "https://journals.sagepub.com/doi/suppl/10.1177/10659129241301785/suppl_file/" + NAME
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
URLS = [
    ("Sage downloadSupplement URL (as linked on the article page)", DL),
    ("Sage suppl_file URL", SUPP),
    ("Sage supplementary listing", "https://journals.sagepub.com/doi/suppl/" + DOI),
    ("Sage article landing page", "https://journals.sagepub.com/doi/full/" + DOI),
    ("DOI resolver", "https://doi.org/" + DOI),
    ("Crossref metadata (relation and links)", "https://api.crossref.org/works/" + DOI),
    ("DataCite: records declaring the article as related (Sage figshare supplements are registered there)",
     "https://api.datacite.org/dois?" + urllib.parse.urlencode({"query": f'relatedIdentifiers.relatedIdentifier:"{DOI}"', "page[size]": "100"})),
    ("DataCite: title search", "https://api.datacite.org/dois?" + urllib.parse.urlencode({"query": '"Leadership in a Pandemic"', "page[size]": "100"})),
    ("Unpaywall", "https://api.unpaywall.org/v2/" + DOI + "?email=repro-audit-2026@users.noreply.github.com"),
    ("Wayback availability of the downloadSupplement URL", "http://archive.org/wayback/available?url=" + urllib.parse.quote(DL.split("//", 1)[1], safe="")),
    ("Wayback availability of the suppl_file URL", "http://archive.org/wayback/available?url=" + SUPP.split("//", 1)[1]),
    ("Wayback CDX for the article's suppl path", "https://web.archive.org/cdx/search/cdx?url=journals.sagepub.com/doi/suppl/10.1177/10659129241301785*&output=json"),
]


def classify(status, body):
    if body[:2] == b"PK":
        return "ZIP archive"
    b = body[:3000].decode("utf-8", "replace")
    if "Just a moment" in b or "challenges.cloudflare.com" in b or "cf-chl" in b:
        return "Cloudflare interstitial"
    if status == 200:
        return "response body: " + b[:240].replace("\n", " ")
    return b[:160].replace("\n", " ")


out = []
for name, u in URLS:
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60)
        body, st = r.read(), r.status
    except urllib.error.HTTPError as e:
        body, st = e.read(), e.code
    except Exception as e:
        body, st = b"", f"error: {type(e).__name__}"
    row = {"route": name, "url": u, "utc": t, "http": st, "bytes": len(body), "what_came_back": classify(st, body)}
    if body[:2] == b"PK":
        row["sha256"] = hashlib.sha256(body).hexdigest()
        row["members"] = zipfile.ZipFile(io.BytesIO(body)).namelist()
        os.makedirs("/workspace/audit_runs/06_VSV5DM/supplement", exist_ok=True)
        open(f"/workspace/audit_runs/06_VSV5DM/supplement/{NAME}", "wb").write(body)
    if "datacite" in u and st == 200:
        d = json.loads(body)
        row["datacite_total"] = d["meta"].get("total")
        row["datacite_dois"] = [x["id"] for x in d["data"]]
    out.append(row)
    print(name, st, len(body), row["what_came_back"][:80])
json.dump({"script": "scripts/p06_supplement_attempts.py", "target_file": NAME, "attempts": out,
           "earlier_attempts_not_scripted_here": [
               "2026-10-10 about 12:24 UTC, curl with a browser User-Agent on the downloadSupplement URL: HTTP 403, 5884-byte Cloudflare page (DATA_STATEMENT.md)",
               "2026-10-10 about 12:18 to 12:22 UTC, Hark browser agent: downloadSupplement URL (3 navigations) and suppl_file URL (1 navigation) timed out; clicking the ZIP link on the article page 3 times produced no download (DATA_STATEMENT.md)",
               "2026-10-10 earlier, Google Docs viewer, DOI resolver and r.jina.ai proxy: Cloudflare or Sage 'cookieAbsent' interstitial (DATA_STATEMENT.md)",
               "2026-10-10, figshare API v2 POST /articles/search for '\"Leadership in a Pandemic\"': no record for this article (agent console, not saved)"]},
          open("papers/06_VSV5DM/data_statement_raw/supplement_access_attempts.json", "w"), indent=1)
