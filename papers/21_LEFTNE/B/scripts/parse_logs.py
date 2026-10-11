"""Parses the authors' printed logs: lavaan Defined Parameters (text_log.txt), Table 3 export_summs (text_log.txt),
Table A5 export_summs and Table A8 mediate ACMEs (appendix_log.txt). Writes outputs/printed_log_values.json."""
import re, json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
txt = open(os.path.join(OUT, "text_log.txt")).read()
app = open(os.path.join(OUT, "appendix_log.txt")).read()
res = {}
blocks = re.findall(r"Defined Parameters:\n(.*?)\n\n", txt, re.S)
for study, b in zip(["study1", "study2"], blocks):
    d = {}
    for line in b.splitlines()[1:]:
        p = line.split()
        d[p[0]] = {"est": float(p[1]), "se": float(p[2]), "z": float(p[3]), "p": float(p[4])}
    res["lavaan_" + study] = d
m = re.search(r"> export_summs\(mod2\)(.*?)Column names", txt, re.S).group(1)
res["table3_printed"] = {
    "treatment_of_women": re.search(r"TREATMENTTreatment of Women\s+([-\d.]+)\s*(\**)", m).groups(),
    "N": int(re.search(r"\n\s+N\s+(\d+)", m).group(1))}
acme = re.findall(r"\nACME\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", app)
labels = ["A8_study1_Clinton", "A8_study1_Trump", "A8_study2_Clinton", "A8_study2_Trump"]
res["tableA8_mediate"] = {l: {"acme": float(a[0]), "ci90_lo": float(a[1]), "ci90_hi": float(a[2]), "p_printed": a[3]} for l, a in zip(labels, acme[:4])}
n = re.findall(r"Sample Size Used: (\d+)", app)[:4]
for l, k in zip(labels, n): res["tableA8_mediate"][l]["n"] = int(k)
a5 = re.search(r"> export_summs\(anger1, anger2, anger3, anger4.*?\n(.*?)\n> ", app, re.S).group(1)
res["tableA5_printed_excerpt"] = a5[:6000]
json.dump(res, open(os.path.join(OUT, "printed_log_values.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "tableA5_printed_excerpt"}, indent=1))
