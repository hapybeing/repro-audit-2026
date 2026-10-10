"""Agent B, 12_CYBR7L: code-review check of the location coding (not a pre-registered robustness check).
Counts, for the 1956-2021 data, authors whose Author_based_in_Africa is all blank (mode empty, set to 1 by the notebook),
authors with a tie, and compares the complete-set Africa-based share computed from first-row raw values (as cell 'Table 1')
with the share from the mode-based node attribute. Writes outputs/location_coding_check.json."""
import os, json, pickle
import numpy as np, pandas as pd

P = '/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/12_CYBR7L/B'
RUN = '/workspace/audit_runs/12_CYBR7L/B/run'
df = pd.read_csv(os.path.join(RUN, 'SciSciNet_AfricanPolitics_Data.csv'))
d = df[df['Year'] <= 2021]
g = d.groupby('AuthorID')['Author_based_in_Africa']
all_blank = [a for a, s in g if s.isna().all()]
ties = [a for a, s in g if len(s.mode()) > 1]
loc = g.agg(lambda x: x.mode()).to_dict()
for k, v in loc.items():
    if isinstance(v, (list, np.ndarray)):
        loc[k] = 1.
df2 = d.drop_duplicates(subset='AuthorID', keep='first')
first_row_based = int((df2['Author_based_in_Africa'] == 1).sum())
mode_based = int(sum(1 for a in df2['AuthorID'] if loc.get(a) == 1))
obj = pickle.load(open(os.path.join(RUN, 'audit_table1_objects.pkl'), 'rb'))
top45 = set(obj['df_auth_cit_net_2021_table1'].iloc[:45]['AuthorID'])
G = obj['G_citation'][2021]
res = {
    'n_authors_2021': len(df2),
    'n_authors_all_blank_location': len(all_blank),
    'all_blank_authors_coded_based_by_mode_rule': int(sum(1 for a in all_blank if loc.get(a) == 1)),
    'all_blank_in_network_2021': int(sum(1 for a in all_blank if a in G)),
    'all_blank_in_main_top45': int(sum(1 for a in all_blank if a in top45)),
    'n_authors_tied_location': len(ties),
    'tied_in_main_top45': int(sum(1 for a in ties if a in top45)),
    'complete_set_based_count_first_row_raw': first_row_based,
    'complete_set_based_pct_first_row_raw': 100 * first_row_based / len(df2),
    'complete_set_based_count_mode_rule': mode_based,
    'complete_set_based_pct_mode_rule': 100 * mode_based / len(df2),
}
json.dump(res, open(os.path.join(P, 'outputs', 'location_coding_check.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
