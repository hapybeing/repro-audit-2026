"""Log every scripted route tried to reach the Sage supplementary file of paper 04.
Usage (from repo/): python3 scripts/p04_supplement_attempts.py
Writes papers/04_PSHE5L/data_statement_raw/supplement_access_attempts.json (URL, UTC time, HTTP status, bytes, what came back)."""
import json, datetime, urllib.request, urllib.error, urllib.parse

SUPP = "https://journals.sagepub.com/doi/suppl/10.1177/23780231251317227/suppl_file/sj-docx-1-srd-10.1177_23780231251317227.docx"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
URLS = [
    ("Sage supplementary file (direct)", SUPP),
    ("Sage supplementary listing", "https://journals.sagepub.com/doi/suppl/10.1177/23780231251317227"),
    ("Sage article landing page", "https://journals.sagepub.com/doi/10.1177/23780231251317227"),
    ("DOI resolver", "https://doi.org/10.1177/23780231251317227"),
    ("Sage full-text XML (Crossref text-mining link)", "https://journals.sagepub.com/doi/full-xml/10.1177/23780231251317227"),
    ("Sage PDF (Crossref text-mining link)", "https://journals.sagepub.com/doi/pdf/10.1177/23780231251317227"),
    ("Crossref metadata", "https://api.crossref.org/works/10.1177/23780231251317227"),
    ("Unpaywall", "https://api.unpaywall.org/v2/10.1177/23780231251317227?email=repro-audit-2026@users.noreply.github.com"),
    ("OpenAlex", "https://api.openalex.org/works/doi:10.1177/23780231251317227"),
    ("Semantic Scholar", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1177/23780231251317227?fields=title,openAccessPdf,externalIds"),
    ("Wayback availability of the supplementary file", "http://archive.org/wayback/available?url=" + SUPP.split("//", 1)[1]),
    ("Wayback CDX for the supplementary path", "https://web.archive.org/cdx/search/cdx?url=journals.sagepub.com/doi/suppl/10.1177/23780231251317227*&output=json"),
]


def classify(status, body):
    b = body[:3000].decode("utf-8", "replace")
    if "Just a moment" in b or "challenges.cloudflare.com" in b:
        return "Cloudflare interstitial ('Just a moment...')"
    if status == 200:
        return "response body: " + b[:200].replace("\n", " ")
    return b[:120].replace("\n", " ")


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
    out.append({"route": name, "url": u, "utc": t, "http": st, "bytes": len(body), "what_came_back": classify(st, body)})
    print(name, st, len(body))
json.dump({"script": "scripts/p04_supplement_attempts.py", "attempts": out,
           "not_scripted": ["web_fetch tool (Hark fetch service) on the supplementary URL and the suppl listing: 'page extraction failed' (2026-10-10, about 10:10 UTC)",
                            "figshare API v2 POST /articles/search with resource_doi=10.1177/23780231251317227 and with the article title: 0 results (2026-10-10, about 10:10 UTC)",
                            "Headless browser (Hark browser agent), 2026-10-10 about 10:12 UTC: direct Sage URL showed the Cloudflare interstitial on first load and two reloads (Ray IDs a484d823fd8af4e3, a484d8617b28f4e3); Office Online viewer (view.officeapps.live.com) returned an error; Google Docs viewer (docs.google.com/viewer?url=<supplementary URL>) rendered the full 26-page document, which was read. Notes: supplement_read_2026-10-10.md"]},
          open("papers/04_PSHE5L/data_statement_raw/supplement_access_attempts.json", "w"), indent=1)
