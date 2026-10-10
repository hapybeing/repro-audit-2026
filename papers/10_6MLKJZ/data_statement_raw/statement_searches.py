"""Repeatable searches behind the 10_6MLKJZ data-statement finding (CHANGELOG_METHOD #4, #5a).
Usage (from repo/): python3 papers/10_6MLKJZ/data_statement_raw/statement_searches.py
Writes papers/10_6MLKJZ/data_statement_raw/statement_searches.json. Public APIs only, no sign-in.
Hit rule: (1) text search: any case-insensitive match of a term in a transcript of the article or appendix counts as a hit
and is printed with its line; (2) repository search: an item whose title contains 'prioriti' and 'social needs'
(case-insensitive) counts as a relevant hit."""
import json, re, datetime, urllib.request, urllib.parse, urllib.error, os
D = "papers/10_6MLKJZ/data_statement_raw"
UA = {"User-Agent": "repro-audit-2026", "Accept": "application/json"}
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
recs = []
TERMS = ["data availab", "availability", "replication", "dataverse", "osf", "github", "zenodo", "repository", "code", "syntax", "request"]
for f in ["sage_html_structure_and_end_matter.md", "article_pdf_read_notes_2026-10-10.md", "supplement_pdf_transcript_2026-10-10.md"]:
    L = open(os.path.join(D, f), encoding="utf-8").read().split("\n")
    for t in TERMS:
        hits = [(i + 1, l.strip()[:200]) for i, l in enumerate(L) if t in l.lower() and not l.startswith("<!--")]
        recs.append({"source": "local transcript " + f, "query": t, "url": None, "utc": now(), "http": None, "total_results": len(hits), "relevant_hits": hits})
def get(url):
    t = now()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60); return t, r.status, json.loads(r.read())
    except urllib.error.HTTPError as e: return t, e.code, None
    except Exception as e: return t, "error: " + type(e).__name__, None
rel = lambda s: bool(s) and "prioriti" in s.lower() and "social needs" in s.lower()
q = []
for term in ['"10.1177/09520767231210025"', '"Prioritizing Exceptional Social Needs"']:
    u = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": term, "type": "dataset", "per_page": 100})
    t, st, j = get(u); items = (j or {}).get("data", {}).get("items", [])
    recs.append({"source": "Harvard Dataverse search API", "query": term, "url": u, "utc": t, "http": st,
                 "total_results": (j or {}).get("data", {}).get("total_count"), "relevant_hits": [[i.get("global_id"), i.get("name")] for i in items if rel(i.get("name"))]})
    u = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": term, "size": 100})
    t, st, j = get(u); hits = (j or {}).get("hits", {})
    recs.append({"source": "Zenodo records API", "query": term, "url": u, "utc": t, "http": st, "total_results": hits.get("total") if isinstance(hits, dict) else None,
                 "relevant_hits": [[h.get("doi"), h.get("metadata", {}).get("title")] for h in (hits.get("hits", []) if isinstance(hits, dict) else []) if rel(h.get("metadata", {}).get("title"))]})
u = "https://api.osf.io/v2/nodes/?" + urllib.parse.urlencode({"filter[title]": "Prioritizing exceptional social needs"})
t, st, j = get(u)
recs.append({"source": "OSF API v2 public nodes, title filter", "query": "Prioritizing exceptional social needs", "url": u, "utc": t, "http": st,
             "total_results": (j or {}).get("links", {}).get("meta", {}).get("total") if j else None, "relevant_hits": [[n["id"], n["attributes"]["title"]] for n in (j or {}).get("data", []) if rel(n["attributes"]["title"])]})
u = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": "Prioritizing exceptional social needs"})
t, st, j = get(u)
recs.append({"source": "GitHub repository search API", "query": "Prioritizing exceptional social needs", "url": u, "utc": t, "http": st,
             "total_results": (j or {}).get("total_count"), "relevant_hits": [[r["full_name"], r.get("description")] for r in (j or {}).get("items", [])]})
u = "https://api.crossref.org/works/10.1177/09520767231210025"
t, st, j = get(u); m = (j or {}).get("message", {})
recs.append({"source": "Crossref work metadata, 'relation' field", "query": "10.1177/09520767231210025", "url": u, "utc": t, "http": st,
             "total_results": len(m.get("relation", {}) or {}), "relevant_hits": m.get("relation", {})})
json.dump({"script": D + "/statement_searches.py", "searches": recs}, open(os.path.join(D, "statement_searches.json"), "w"), indent=1, ensure_ascii=False)
for r in recs: print(r["source"][:45], "|", r["query"], "|", r["http"], "| total", r["total_results"], "| relevant", r["relevant_hits"] if r["relevant_hits"] else 0)
