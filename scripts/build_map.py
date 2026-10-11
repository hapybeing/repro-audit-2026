"""Build docs/index.html: a single self-contained interactive map of the 25 audited papers.
Usage (from the repository root): python3 scripts/build_map.py

Inputs (read only, nothing here changes a result):
  final/all25_results.csv   one row per paper (class, alternative, DOI, batch)
  final/all25_counts.json   main counts
  PROTOCOL.md               class definitions (section 7), quoted verbatim
  FINAL_REPORT.md           "Why each class C paper is C" lines, quoted verbatim for C papers
The page has no external JS, CSS, fonts, trackers or analytics. Every text value is inserted with textContent."""
import csv, html, json, re, sys

GH = "https://github.com/hapybeing/repro-audit-2026"
CLS = "ABCDE"
COLORS = {"A": "#1b7f3b", "B": "#7cb342", "C": "#e0a800", "D": "#c62828", "E": "#6a5acd"}
SCOPE = ("n = 25, one repository, mostly political science. No rates. A class C means the paper could not be fully "
         "checked from the materials as deposited, not that it is wrong.")
CREDIT = "Gaurang Kumar (@hapybeing). Analysis run with Hark."

rows = list(csv.DictReader(open("final/all25_results.csv", encoding="utf-8")))
counts = json.load(open("final/all25_counts.json", encoding="utf-8"))
main = counts["counts_main"]
assert counts["n_papers"] == len(rows) == 25, len(rows)
assert {k: sum(r["main_class"] == k for r in rows) for k in CLS} == main, "CSV classes disagree with all25_counts.json"

proto = open("PROTOCOL.md", encoding="utf-8").read()
meaning = {}
for k in CLS:
    m = re.search(rf"^- {k}: (.+)$", proto, re.M)
    assert m, k
    meaning[k] = m.group(1).strip()

rep = open("FINAL_REPORT.md", encoding="utf-8").read()
sec = rep.split("## Why each class C paper is C", 1)[1].split("\n## ", 1)[0]
c_reason = {}
for m in re.finditer(r"^- (\d\d_[A-Z0-9]+) \((.+?)\): (.+)$", sec, re.M):
    c_reason[m.group(1)] = {"type": m.group(2), "text": m.group(3)}
c_ids = [r["id"] for r in rows if r["main_class"] == "C"]
assert sorted(c_reason) == sorted(c_ids), (sorted(c_reason), c_ids)

papers = []
for r in rows:
    k = int(r["batch"])
    prereg = ({"label": "batches/batch1_prereg_hashes.txt (batch 1 had no issue; self-attested local freeze)",
               "url": f"{GH}/blob/main/batches/batch1_prereg_hashes.txt"} if k == 1 else
              {"label": f"issue #{k - 1}", "url": f"{GH}/issues/{k - 1}"})
    p = {
        "id": r["id"], "batch": k, "title": r["title"], "journal": r["journal"], "year": r["year"],
        "cls": r["main_class"], "alt_cls": r["alternative_class"], "alt_reason": r["alternative_reason"],
        "doi": r["paper_doi"], "report": f"{GH}/blob/main/batch{k}_report.md", "prereg": prereg,
    }
    if r["main_class"] == "C":
        p["c_reason"] = c_reason[r["id"]]["type"] + ": " + c_reason[r["id"]]["text"]
    papers.append(p)

for t in [SCOPE, CREDIT] + list(meaning.values()):
    assert "\u2014" not in t

legend = "".join(
    f'<li><span class="dot sm" style="background:{COLORS[k]}"></span><b>{k}</b> ({main[k]}): {html.escape(meaning[k])}</li>'
    for k in CLS)
count_line = ", ".join(f"{k} {main[k]}" for k in CLS)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:">
<title>Reproducibility audit of 25 papers: interactive map</title>
<meta name="description" content="Pre-registered reproducibility audit of 25 random Harvard Dataverse papers, re-run by two blind AI agents. One dot per paper.">
<style>
:root{{--bg:#fafaf7;--fg:#1d1d1b;--mut:#5b5b57;--line:#ddd9cf;--card:#fff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151513;--fg:#ecebe6;--mut:#a9a8a1;--line:#34332e;--card:#1f1f1c}}}}
*{{box-sizing:border-box}}
body{{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg)}}
main{{max-width:880px;margin:0 auto;padding:20px 16px 120px}}
h1{{font-size:1.45rem;line-height:1.25;margin:.2em 0 .4em}}
h2{{font-size:1.05rem;margin:1.6em 0 .5em}}
p{{margin:.5em 0}}
a{{color:inherit}}
.scope{{border-left:4px solid {COLORS['C']};background:var(--card);padding:10px 12px;border-radius:6px}}
.counts{{font-size:1.1rem;font-weight:600}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}}
.controls button{{font:inherit;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}}
.controls button[aria-pressed=true]{{border-color:var(--fg);font-weight:600}}
.group{{display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid var(--line);flex-wrap:wrap}}
.glabel{{width:92px;flex:none;font-size:.9rem;color:var(--mut)}}
.dots{{display:flex;gap:10px;flex-wrap:wrap}}
.dot{{width:44px;height:44px;border-radius:50%;border:2px solid transparent;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:.8rem;cursor:pointer;padding:0;text-shadow:0 0 2px rgba(0,0,0,.6)}}
.dot:focus-visible,.dot.sel{{outline:3px solid var(--fg);outline-offset:2px}}
.dot.sm{{width:14px;height:14px;cursor:default;vertical-align:middle;margin-right:6px}}
ul.legend{{list-style:none;padding:0;margin:0}}
ul.legend li{{margin:.35em 0}}
#detail{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-top:14px}}
#detail h3{{margin:.1em 0 .4em;font-size:1.05rem;line-height:1.3}}
#detail dl{{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}}
#detail dt{{color:var(--mut);font-size:.9rem}}
#detail dd{{margin:0;overflow-wrap:anywhere}}
.hint{{color:var(--mut)}}
footer{{margin-top:2em;color:var(--mut);font-size:.9rem}}
@media (max-width:520px){{.glabel{{width:100%}}#detail dl{{grid-template-columns:1fr}}#detail dt{{margin-top:6px}}}}
</style>
</head>
<body>
<main>
<h1>Reproducibility audit of 25 Harvard Dataverse papers</h1>
<p>Each paper was re-run from the authors' deposited materials by two blind AI agent runs against pre-registered targets, then classified A to E. One dot per paper; tap a dot for details.</p>
<p class="scope" id="scope">{html.escape(SCOPE)}</p>
<p class="counts" id="counts">Main counts: {count_line}</p>
<h2>Classes (PROTOCOL.md section 7)</h2>
<ul class="legend">{legend}</ul>
<h2>Papers</h2>
<div class="controls" role="group" aria-label="Group dots by">
<span class="hint">Group by:</span>
<button type="button" id="by-batch" aria-pressed="true">Batch</button>
<button type="button" id="by-class" aria-pressed="false">Class</button>
</div>
<div id="map"></div>
<section id="detail" aria-live="polite"><p class="hint">Tap a dot to see the paper, its class, its alternative reading and its links.</p></section>
<footer>
<p>Full results: <a href="{GH}">repository</a> and <a href="{GH}/blob/main/FINAL_REPORT.md">FINAL_REPORT.md</a>. Data for this page: final/all25_results.csv and final/all25_counts.json, built by scripts/build_map.py.</p>
<p>{html.escape(CREDIT)}</p>
</footer>
</main>
<script>
const P={json.dumps(papers, ensure_ascii=False)};
const COL={json.dumps(COLORS)};
const M=document.getElementById('map'),D=document.getElementById('detail');
let mode='batch',sel=null;
function el(t,a,txt){{const e=document.createElement(t);if(a)for(const k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e}}
function link(u,txt){{const a=el('a',{{href:u,rel:'noopener noreferrer'}},txt);return a}}
function render(){{
  M.textContent='';
  const keys=mode==='batch'?[1,2,3,4,5]:['A','B','C','D','E'];
  for(const k of keys){{
    const ps=P.filter(p=>mode==='batch'?p.batch===k:p.cls===k);
    const g=el('div',{{class:'group'}});
    g.appendChild(el('div',{{class:'glabel'}},mode==='batch'?('Batch '+k+' ('+String((k-1)*5+1).padStart(2,'0')+' to '+String(k*5).padStart(2,'0')+')'):('Class '+k+' ('+ps.length+')')));
    const ds=el('div',{{class:'dots'}});
    for(const p of ps){{
      const b=el('button',{{type:'button',class:'dot'+(sel===p.id?' sel':''),style:'background:'+COL[p.cls],'aria-label':p.id+', class '+p.cls+': '+p.title}},p.id.slice(0,2));
      b.addEventListener('click',()=>show(p));
      ds.appendChild(b);
    }}
    if(!ps.length)ds.appendChild(el('span',{{class:'hint'}},'none'));
    g.appendChild(ds);M.appendChild(g);
  }}
}}
function row(dl,k,v){{dl.appendChild(el('dt',null,k));const dd=el('dd');if(typeof v==='string')dd.textContent=v;else dd.appendChild(v);dl.appendChild(dd)}}
function show(p){{
  sel=p.id;render();D.textContent='';
  D.appendChild(el('h3',null,p.title));
  const dl=el('dl');
  row(dl,'Paper',p.id+' (batch '+p.batch+')');
  row(dl,'Journal',p.journal);
  row(dl,'Year',p.year);
  row(dl,'Main class',p.cls);
  row(dl,'Alternative reading',p.alt_cls+': '+p.alt_reason);
  if(p.c_reason)row(dl,'Why C (FINAL_REPORT.md)',p.c_reason);
  row(dl,'Batch report',link(p.report,'batch'+p.batch+'_report.md'));
  row(dl,'Pre-registration',link(p.prereg.url,p.prereg.label));
  row(dl,'Paper DOI',link(p.doi,p.doi.replace('https://doi.org/','')));
  D.appendChild(dl);
  if(window.matchMedia('(max-width:700px)').matches)D.scrollIntoView({{behavior:'smooth',block:'start'}});
}}
function setMode(m){{mode=m;document.getElementById('by-batch').setAttribute('aria-pressed',m==='batch');document.getElementById('by-class').setAttribute('aria-pressed',m==='class');render()}}
document.getElementById('by-batch').addEventListener('click',()=>setMode('batch'));
document.getElementById('by-class').addEventListener('click',()=>setMode('class'));
render();
</script>
</body>
</html>
"""
assert "\u2014" not in page, "em dash in page"
for bad in ("http://", "googleapis", "gtag", "analytics", "<link ", "src=\"http"):
    assert bad not in page, bad
import os
os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w", encoding="utf-8").write(page)
open("docs/.nojekyll", "w").write("")
print(f"docs/index.html written: {len(papers)} papers, main counts {count_line}, {len(page)} bytes")
