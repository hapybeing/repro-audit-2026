"""Records the agent-B check of the six target cells against the publisher PDF text (web_fetch 2026-10-11 ~05:50 IST).
Excerpts are short strings copied from the fetched PDF text."""
import json
chk = {"source": "https://www.tandfonline.com/doi/pdf/10.1080/13501763.2024.2391510 (web_fetch, served via fallback, 2026-10-11 IST)",
 "cells": [
  {"id": "T1", "row": "Challenger * Proximity to next National Election", "excerpt_models_1_to_4": "0.02 *** 0.02 *** 0.02 *** 0.02 *** / (0.00) (0.00) (0.01) (0.00)", "model2_value": 0.02, "stars": "***", "matches_targets_json": True},
  {"id": "T2", "row": "Proximity to next EP-Election", "excerpt_models_1_to_4": "0.01 ** 0.01 *** 0.01 ** 0.01 *** / (0.00) (0.00) (0.00) (0.00)", "model2_value": 0.01, "stars": "***", "matches_targets_json": True},
  {"id": "T3", "row": "Challenger", "excerpt_models_1_to_4": "0.06 *** 0.05 *** 0.04 ** 0.04 ** / (0.01) (0.01) (0.02) (0.02)", "model2_value": 0.05, "stars": "***", "matches_targets_json": True},
  {"id": "T4", "row": "Num. obs.", "excerpt_models_1_to_4": "266,854 266,854 266854 266854", "model2_value": 266854, "matches_targets_json": True},
  {"id": "T5", "row": "Challenger * Austerity Salience (Table 2, Austerity)", "excerpt": "0.04 ** (0.01)", "value": 0.04, "stars": "**", "matches_targets_json": True},
  {"id": "T6", "row": "Challenger * EU Salience (Table 2, European Integration)", "excerpt": "0.02 * (0.01)", "value": 0.02, "stars": "*", "matches_targets_json": True}],
 "context_seen": {"T1_model2_AIC": "738,747.50", "T1_model2_logLik": "-369,309.75", "T2_num_obs": "101077 233056 77276"},
 "result": "All six target cells in the PDF equal targets.json; targets.json values used unchanged."}
json.dump(chk, open("outputs/pdf_cell_check.json", "w"), indent=1)
print("ok")
