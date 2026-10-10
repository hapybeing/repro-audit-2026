# Compares the main run (edited script) with the unmodified authors' script run after specr 1.0.0 was installed.
import csv, sys
from pathlib import Path
O = Path(__file__).resolve().parents[1] / "outputs"
a = list(csv.DictReader(open(O / "targets_extracted.csv"))); b = list(csv.DictReader(open(O / "targets_extracted_unmodified.csv")))
same_terms = [(x["model"], x["term"]) for x in a] == [(y["model"], y["term"]) for y in b]
d = max(abs(float(x[k]) - float(y[k])) for x, y in zip(a, b) for k in ["estimate", "se_cluster", "p_fixest", "nobs"])
txt = (f"specr 1.0.0 (authors' pin) was installed from CRAN after the main run; the unmodified crosssection_linear.R then ran without error "
       f"(outputs/console_crosssection_linear_unmodified.log). Same {len(a)} model-term rows: {same_terms}; max abs difference in estimate/SE/p/nobs vs the edited-script run: {d}.")
open(O / "specr_check.txt", "w").write(txt + "\n"); print(txt)
