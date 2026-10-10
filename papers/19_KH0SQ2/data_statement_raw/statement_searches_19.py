"""Repeatable searches for the data/code availability statement of 19_KH0SQ2 (doi 10.1080/13501763.2024.2402864).
Run: python3 statement_searches_19.py  (writes statement_searches.json next to this file). Public endpoints, no sign-in.
Hit rule: a statement counts as found if a source contains a heading or sentence matching
'data availability|availability of data|data and code|replication (data|materials|files)|dataverse|10.7910/DVN/KH0SQ2'."""
import json, re, datetime, urllib.request, subprocess, os
UA = {"User-Agent": "repro-audit-2026"}
PAT = re.compile(r"data availability|availability of data|data and code|replication (data|materials|files)|dataverse|10\.7910/DVN/KH0SQ2", re.I)
OUT = []
import time
def now(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def get(url, ua=UA):
    t = now()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=60); b = r.read(); return t, r.status, b
    except urllib.error.HTTPError as e: return t, e.code, b""
    except Exception as e: return t, "error: " + type(e).__name__, b""
def rec(src, url, t, st, text, note=""):
    hits = sorted(set(m.group(0) for m in PAT.finditer(text))) if text else []
    ctx = [text[max(0, m.start()-120): m.end()+120].replace("\n", " ") for m in PAT.finditer(text)][:5] if text else []
    OUT.append({"source": src, "url": url, "utc": t, "http": st, "bytes": len(text), "pattern_hits": hits, "contexts": ctx, "note": note})
    print(src, st, len(text), hits)
# 1 publisher HTML full text
u = "https://www.tandfonline.com/doi/full/10.1080/13501763.2024.2402864"
t, st, b = get(u, {"User-Agent": "Mozilla/5.0 (repro-audit-2026)"}); txt = b.decode("utf-8", "replace")
rec("T&F full-text HTML (direct curl)", u, t, st, txt, "Cloudflare may return 403; see the web_fetch copy below")
# 1b saved copy of the same page obtained via the agent's web_fetch tool on 2026-10-10 17:2x UTC
p = "/workspace/audit_runs/19_KH0SQ2/prereg/tandf_page.txt"
if os.path.exists(p):
    txt = open(p, encoding="utf-8").read(); rec("T&F full-text HTML (web_fetch copy, scratch tandf_page.txt)", u, "2026-10-10 (fetch time of copy)", 200, txt,
        "sections listed: Abstract, Introduction, ..., Conclusion, Supplemental material, Acknowledgements, Disclosure statement, Additional information, Footnotes, References")
# 2 publisher PDF
u = "https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2402864"
t, st, b = get(u, {"User-Agent": "Mozilla/5.0 (repro-audit-2026)"})
rec("T&F article PDF", u, t, st, "" if not b.startswith(b"%PDF") else "(pdf)", "non-PDF/403 means not readable here")
# 3 Crossref metadata
u = "https://api.crossref.org/works/10.1080/13501763.2024.2402864"
t, st, b = get(u); txt = b.decode("utf-8", "replace"); rec("Crossref works API", u, t, st, txt)
# 4 Online appendix (figshare copy of the T&F supplement)
u = "https://ndownloader.figshare.com/files/49219486"
t, st, b = get(u)
if b.startswith(b"%PDF"):
    open("/tmp/supp19.pdf", "wb").write(b); txt = subprocess.run(["pdftotext", "/tmp/supp19.pdf", "-"], capture_output=True, text=True).stdout
else: txt = ""
rec("Online appendix PDF (figshare 27036622, file 49219486)", u, t, st, txt, "tables in this PDF are images; text layer covers prose only")
# 5 Dataverse record (reverse link)
u = "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/KH0SQ2"
t, st, b = get(u); txt = b.decode("utf-8", "replace"); rec("Dataverse dataset JSON", u, t, st, txt, "reverse link only; not an article statement")
# 6 OSF pre-analysis plan named in footnote 5 (view-only link); file listing via the public OSF API
u = "https://api.osf.io/v2/nodes/6hfnt/files/osfstorage/?view_only=30a3981430324807a3eeddf5eb5686ce"
t, st, b = get(u); txt = b.decode("utf-8", "replace")
names = re.findall(r'"name": ?"([^"]+)"', txt)
OUT.append({"source": "OSF node 6hfnt osfstorage listing (footnote 5 link)", "url": u, "utc": t, "http": st, "bytes": len(txt), "file_names": names, "note": "pre-analysis plan location; checked only for whether data or code files are listed"})
print("OSF", st, names)
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "statement_searches.json"), "w"), indent=1)
