"""Re-runnable searches for files read by 18_YXC5K5's deposited code but absent from the deposit.
Usage (from repo/): python3 papers/18_YXC5K5/data_statement_raw/absence_searches_18.py
Writes papers/18_YXC5K5/data_statement_raw/absence_searches.json. Public APIs only, no sign-in.
Hit rule: a result counts as a hit only if it is a file whose name equals the missing file name exactly
(Dataverse, Zenodo) or a repository/dataset clearly by the same author for this article (GitHub, OSF, Dataverse dataset search)."""
import json, time, datetime, urllib.request, urllib.parse, urllib.error, os
UA = {"User-Agent": "repro-audit-2026", "Accept": "application/json"}
RECS = []
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "absence_searches.json")
MISSING = ["full_df_for_classification_ten.csv", "batch_part1_output_v2.jsonl", "batch_part2_output_v2.jsonl"]
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def get(url):
    t = now()
    for a in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
            return t, r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and a < 2: time.sleep(5); continue
            return t, e.code, ""
        except Exception as e:
            if a < 2: time.sleep(5); continue
            return t, "error: " + type(e).__name__, ""
def rec(source, query, url, t, st, total, hits, note=""):
    RECS.append(dict(source=source, query=query, url=url, utc=t, http=st, total_results=total, hits=hits, note=note))
    print(source, "|", query, "|", st, "| total", total, "| hits", len(hits))
for fn in MISSING:
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": f'fileName:"{fn}"', "type": "file", "per_page": "100"})
    t, st, b = get(url); tot, hits = None, []
    if st == 200:
        d = json.loads(b)["data"]; tot = d["total_count"]
        hits = [{"file": i["name"], "dataset_doi": i.get("dataset_persistent_id")} for i in d["items"] if i["name"] == fn]
    rec("Harvard Dataverse Search API (files, all collections)", f'fileName:"{fn}"', url, t, st, tot, hits)
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": f'filename:{fn}', "size": "25"})
    t, st, b = get(url); tot, hits = None, []
    if st == 200:
        d = json.loads(b); tot = d["hits"]["total"]
        for r in d["hits"]["hits"]:
            for f in r.get("files", []):
                if f.get("key") == fn: hits.append({"record": r.get("links", {}).get("self_html"), "file": fn})
    rec("Zenodo records API", f'filename:{fn}', url, t, st, tot, hits)
# all versions of the deposit
url = "https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/YXC5K5"
t, st, b = get(url); tot, hits = None, []
if st == 200:
    vs = json.loads(b)["data"]; tot = len(vs)
    for v in vs:
        names = [f["dataFile"]["filename"] for f in v.get("files", [])]
        hits += [{"version": f'{v.get("versionNumber")}.{v.get("versionMinorNumber")}', "file": n} for n in names if n in MISSING]
rec("Harvard Dataverse dataset versions (YXC5K5)", "all versions, file lists", url, t, st, tot, hits, "total_results = number of versions")
# datasets by the author / title on Dataverse
for q in ['"Benchmarking AI and Human Text Classifications"', 'authorName:"Tripp, Alexander"']:
    url = "https://dataverse.harvard.edu/api/search?" + urllib.parse.urlencode({"q": q, "type": "dataset", "per_page": "100"})
    t, st, b = get(url); tot, hits = None, []
    if st == 200:
        d = json.loads(b)["data"]; tot = d["total_count"]
        hits = [{"dataset": i.get("name"), "doi": i.get("global_id")} for i in d["items"] if i.get("global_id") != "doi:10.7910/DVN/YXC5K5" and "benchmark" in (i.get("name") or "").lower()]
        note_titles = [i.get("name") for i in d["items"]]
    rec("Harvard Dataverse Search API (datasets)", q, url, t, st, tot, hits, "hit = a dataset other than the audited deposit whose title contains 'benchmark'; all titles returned: " + json.dumps(note_titles if st == 200 else []))
# GitHub repository search (unauthenticated)
for q in ["Benchmarking AI human text classifications newspaper frames", "Tripp LLM newspaper frames Spanish immigration"]:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": q})
    t, st, b = get(url); tot, hits = None, []
    if st == 200:
        d = json.loads(b); tot = d["total_count"]; hits = [{"repo": i["html_url"], "desc": i.get("description")} for i in d["items"]]
    rec("GitHub repository search API", q, url, t, st, tot, hits, "hits listed for hand inspection")
# OSF nodes by title
url = "https://api.osf.io/v2/nodes/?" + urllib.parse.urlencode({"filter[title]": "Benchmarking AI"})
t, st, b = get(url); tot, hits = None, []
if st == 200:
    d = json.loads(b); tot = d["links"]["meta"]["total"] if "meta" in d["links"] else d.get("meta", {}).get("total")
    hits = [{"node": i["links"]["html"], "title": i["attributes"]["title"]} for i in d["data"] if "newspaper" in i["attributes"]["title"].lower() or "llm" in i["attributes"]["title"].lower()]
rec("OSF nodes API", 'filter[title]="Benchmarking AI"', url, t, st, tot, hits, "hits = titles mentioning newspaper or LLM")
json.dump(RECS, open(OUT, "w"), indent=1)
