"""Parse the authors' printed output (outputs/text_log.txt, outputs/appendix_log.txt) for the printed values of each
target and the Table A8 mediate ACMEs. Writes outputs/log_crosscheck.json and outputs/tableA8_mediate.csv."""
import re, json, csv
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/outputs/"
tx = open(O + "text_log.txt").read(); ap = open(O + "appendix_log.txt").read()
res = {}
blocks = [m.start() for m in re.finditer(r"Defined Parameters:", tx)]
for i, (tid, b) in enumerate(zip(["T1", "T2"], blocks)):
    m = re.search(r"indirTRUMPangr\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", tx[b:b + 2000])
    res[tid] = {"printed_est": float(m.group(1)), "printed_se": float(m.group(2)), "printed_p": float(m.group(4)), "source": "outputs/text_log.txt lavaan summary Defined Parameters block %d" % (i + 1)}
    for lab in ["indrCLINTONngr", "indirTRUMPhope", "indirCLINTONhp"]:
        m = re.search(lab + r"\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", tx[b:b + 2000])
        res[tid + "_" + lab] = {"printed_est": float(m.group(1)), "printed_p": float(m.group(4))}
e = tx.index("> export_summs(mod2)")
seg = tx[e:e + 2500]
m = re.search(r"TREATMENTTreatment of Women\s+(-?[\d.]+)\s*(\**)\s*\n\s*\(([\d.]+)\)", seg)
res["T5"] = {"printed_est": float(m.group(1)), "printed_stars": m.group(2), "printed_se": float(m.group(3)), "source": "outputs/text_log.txt export_summs(mod2)"}
res["T6"] = {"printed_N": int(re.search(r"\bN\s+(\d+)", seg).group(1)), "source": "outputs/text_log.txt export_summs(mod2)"}
a = ap.index('model.names = c("None"'); seg = ap[a:ap.index("Column names", a)]
# Table A5 export_summs output wraps labels; take the TREATMENTTrump row (first numeric cell = None) and the Trump:party row (Party column).
m = re.search(r"TREATMEN\s+(0\.\d+)\s*(\**)\s+(\S+)\s*(\**)\s+[^\n]*\n\s*TTrump\s*\n\s*\(([\d.]+)\)", seg)
res["T3"] = {"printed_est": float(m.group(1)), "printed_stars": m.group(2), "printed_se": float(m.group(5)), "source": "outputs/appendix_log.txt export_summs Table A5 column None"}
m = re.search(r"TREATMEN\s+(0\.\d+)\s*(\**)\s+(-?0\.\d+)\s*\n\s*TTrump:p[\s\S]*?\n\s*\(([\d.]+)\)", seg)
res["T4"] = {"printed_est": float(m.group(1)), "printed_stars": m.group(2), "printed_se": float(m.group(4)), "source": "outputs/appendix_log.txt export_summs Table A5 column Party"}
nrow = re.search(r"\n\s*N\s+(\d+)\s+(\d+)\s+(\d+)", seg)
res["A5_N_None_Balanced_Party"] = [int(nrow.group(i)) for i in (1, 2, 3)]
# Table A8: first four mediate summaries after '## STUDY 1--' section: Study1 Clinton, Study1 Trump, Study2 Clinton, Study2 Trump
s = ap.index("set.seed(20241130)")
acme = re.findall(r"\nACME\s+(-?[\d.e-]+)\s+(-?[\d.e-]+)\s+(-?[\d.e-]+)\s+(<?[\d.e-]+)", ap[s:])[:4]
labels = ["Study 1 Clinton", "Study 1 Trump", "Study 2 Clinton", "Study 2 Trump"]
paper = {"Study 1 Clinton": (0.002, 0.475), "Study 1 Trump": (0.017, 0.004), "Study 2 Clinton": (-0.000, 0.982), "Study 2 Trump": (0.080, 0.000)}
with open(O + "tableA8_mediate.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["row", "acme", "ci90_low", "ci90_high", "p_value_printed", "paper_acme_SI_A8", "paper_p_SI_A8"])
    for lab, r in zip(labels, acme):
        w.writerow([lab, r[0], r[1], r[2], r[3], paper[lab][0], paper[lab][1]])
        res["A8_" + lab] = {"acme": float(r[0]), "p_printed": r[3], "paper_acme": paper[lab][0], "paper_p": paper[lab][1]}
json.dump(res, open(O + "log_crosscheck.json", "w"), indent=1); print(json.dumps(res, indent=1))
