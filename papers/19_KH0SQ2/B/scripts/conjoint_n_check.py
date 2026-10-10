# Parses outputs/main_text.log for the residual df of the first UK and FR conjoint models (l.639 res1, l.666 res2) and derives n = df + number of coefficients.
import re, csv, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = open(os.path.join(B, "outputs", "main_text.log")).read().split("\n")
out = []
for label, pat in [("UK conjoint res1 l.639", "> res1 <- lm(Qualified_score ~ Treatment, data = subset(longuk,"), ("FR conjoint res2 l.670", "> res2 <- lm(Qualified_score ~ Treatment, data = subset(longfr,")]:
    i = next(k for k, l in enumerate(L) if l.startswith(pat))
    blk = L[i:i+40]
    c0 = next(k for k, l in enumerate(blk) if l.startswith("Coefficients:"))
    c1 = next(k for k, l in enumerate(blk) if l.startswith("---") and k > c0)
    ncoef = c1 - c0 - 2  # rows between the header line and the signif separator
    for l in blk:
        m = re.search(r"on (\d+) degrees of freedom", l)
        if m: out.append({"model": label, "resid_df": int(m.group(1)), "n_coef": ncoef, "n": int(m.group(1)) + ncoef}); break
with open(os.path.join(B, "outputs", "conjoint_model_n.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["model", "resid_df", "n_coef", "n"]); w.writeheader(); w.writerows(out)
print(out)
