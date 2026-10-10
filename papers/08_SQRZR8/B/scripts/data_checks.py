#!/usr/bin/env python3
"""Writes outputs/run_meta.json: row count, complete cases on all Table 3 model variables, missing counts,
and the order of unique(data$condition) (used by the mediation label mapping in main_rep.R lines 194, 273-292)."""
import csv, json, os, datetime, zoneinfo
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f = "/workspace/audit_runs/08_SQRZR8/B/dl/data_cleaned_rep.csv"
covs = "Age Gender Education Ethnicity MonthlyIncome CCPMembership rural OverseaExperience_yes nationalism_nor liberalism_nor vpnsavvy conservation_nor openness_nor conscientiousness_nor neuroticism_nor extraversion_nor agreeableness_nor LifeSat_1".split()
items = "Sadness Anger Fear Disgust DoNotCare Helplessness Secured Happiness Curiosity Surprised Attitude.I_1 Attitude.I_2 Attitude.I_3 Attitude.I_4 Attitude.II_1 Attitude.II_2 Attitude.II_3 Attitude.II_4 Surveillance Censorship".split()
v = covs + items; miss = {c: 0 for c in v}; n = 0; cc = 0; order = []
for r in csv.DictReader(open(f)):
    n += 1; bad = [c for c in v if r[c].strip() in ("", "NA")]
    for c in bad: miss[c] += 1
    cc += not bad
    if r["condition"] not in order: order.append(r["condition"])
json.dump({"run_date_ist": datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d"),
           "nrow_data": n, "complete_cases": cc, "missing_by_variable": miss, "condition_order_first_appearance": order},
          open(os.path.join(B, "outputs", "run_meta.json"), "w"), indent=1)
print(n, cc, order)
