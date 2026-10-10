"""Pre-registration absence searches for 17_T1NXVQ (written before any analysis code was run).
Claim: files read by deposited scripts but missing from DVN/T1NXVQ (res_optim.rds, read only by the two *_notrun.R
scripts and data_prep/prepare_networks.R; data-prep inputs gsdm.rds, sdm_claims.csv, epr_sec.geojson/.csv, census
Final_df_complete) are not deposited at a location linked to these authors or this article that these searches reach.
Hit rule: a file with exactly the missing name in a dataset or repository linked to these authors or this article.
Usage (from repo/): python3 papers/17_T1NXVQ/data_statement_raw/absence_searches_17.py
Writes papers/17_T1NXVQ/data_statement_raw/absence_searches.json. Public APIs only, no sign-in."""
import json, time, datetime, urllib.request, urllib.parse, urllib.error, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "absence_searches.json")
UA = {"User-Agent": "repro-audit-2026", "Accept": "application/json"}
MISSING = ["res_optim.rds", "gsdm.rds", "sdm_claims.csv", "epr_sec.geojson", "epr_sec.csv", "Final_df_complete.shp"]
RECS = []
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def get(url):
    t = now()
    for a in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
            return t, r.status, json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and a < 2: time.sleep(5); continue
            return t, e.code, None
        except Exception as e:
            if a < 2: time.sleep(5); continue
            return t, "error: " + type(e).__name__, None
def rec(source, query, url, t, st, total, hits, note=""):
    RECS.append(dict(paper="17_T1NXVQ", source=source, query=query, url=url, utc=t, http=st,
                     total_results=total, relevant_hits=hits, note=note))
    print(source, "|", query, "|", st, "| total", total, "| hits", len(hits))
DV = "https://dataverse.harvard.edu/api/search?"
for fn in MISSING:
    url = DV + urllib.parse.urlencode([("q", f'fileName:"{fn}"'), ("type", "file"), ("per_page", "100")])
    t, st, d = get(url)
    items = d["data"]["items"] if d else []
    hits = [{"file": i["name"], "dataset": i.get("dataset_name"), "doi": i.get("dataset_persistent_id")}
            for i in items if i.get("name") == fn]
    rec("Harvard Dataverse Search API", f'fileName:"{fn}" type=file', url, t, st, d["data"]["total_count"] if d else None, hits,
        "hits = exact file name; dataset names listed for inspection: " + "; ".join(sorted({str(h['dataset']) for h in hits}))[:500])
for au in ["Müller-Crepon", "Muller-Crepon", "Schvitz"]:
    url = DV + urllib.parse.urlencode([("q", f'authorName:"{au}"'), ("type", "dataset"), ("per_page", "100")])
    t, st, d = get(url)
    items = d["data"]["items"] if d else []
    rec("Harvard Dataverse Search API", f'authorName:"{au}" type=dataset', url, t, st, d["data"]["total_count"] if d else None, [],
        "datasets returned (inspect for a second deposit of this article): " + " | ".join(f"{i.get('global_id')} {i.get('name')}" for i in items)[:1500])
url = "https://api.github.com/users/carl-mc/repos?per_page=100"
t, st, d = get(url)
names = [r["name"] for r in d] if d else []
rec("GitHub REST API (unauthenticated)", "repositories of user carl-mc (named in article footnote 4)", url, t, st, len(names), [], "repos: " + ", ".join(names))
for repo in [n for n in names if n.lower() in ("pspm", "spatiallattice") or any(k in n.lower() for k in ("border", "nation", "shaping", "replication"))]:
    meta_t, meta_st, meta = get(f"https://api.github.com/repos/carl-mc/{repo}")
    br = meta.get("default_branch", "master") if meta else "master"
    url = f"https://api.github.com/repos/carl-mc/{repo}/git/trees/{br}?recursive=1"
    t, st, d = get(url)
    paths = [x["path"] for x in d.get("tree", [])] if d else []
    hits = [p for p in paths if os.path.basename(p) in MISSING]
    rec("GitHub REST API (unauthenticated)", f"full file tree of carl-mc/{repo} ({br})", url, t, st, len(paths), hits)
url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": "Shaping states into nations"})
t, st, d = get(url)
items = d.get("items", []) if d else []
rec("GitHub repository search API (unauthenticated)", "Shaping states into nations", url, t, st, d.get("total_count") if d else None, [],
    "repos returned: " + ", ".join(i["full_name"] for i in items[:20]))
json.dump(RECS, open(OUT, "w"), indent=1, ensure_ascii=False)
