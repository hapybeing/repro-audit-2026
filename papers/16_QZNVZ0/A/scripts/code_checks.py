"""Data facts behind the code-review notes and PREREG inconsistencies (agent A). Run from the data directory.
Writes outputs/code_checks.json. Read-only descriptive counts; no model is changed."""
import os, json
import numpy as np
import pandas as pd

OUT = os.environ.get("AUDIT_OUT", "outputs")
rt = pd.read_csv('regression_table_anonymous_final.csv', index_col=0, low_memory=False)
fa = ~pd.isna(rt['FA_Ethnicity'])
out = {}
out['n_rows_csv'] = int(len(rt))
out['n_nonmissing_FA_Ethnicity'] = int(fa.sum())
out['Const_unique_values'] = sorted(map(float, rt['Const'].dropna().unique()))
out['Top_Inst_dtypes'] = {c: str(rt[c].dtype) for c in rt.columns if c.endswith('_Inst')}
# Model 3 omits FA_South: how does FA_South vary in the Top10 sample?
m3 = fa & rt['Top10_Inst']
out['model3_rows_before_drop'] = int(m3.sum())
out['FA_South_value_counts_in_Top10_FA_rows'] = {str(k): int(v) for k, v in rt.loc[m3, 'FA_South'].value_counts(dropna=False).items()}
m4 = fa & rt['Top50_Inst']
out['FA_South_value_counts_in_Top50_FA_rows'] = {str(k): int(v) for k, v in rt.loc[m4, 'FA_South'].value_counts(dropna=False).items()}
# Model 2 (team) vs Model 1 (FA): where do the dropped rows come from?
team_cols = ['Team_Female', 'Team_European', 'Team_Asian', 'Team_Slavic', 'Team_Hispanic/Latino', 'Team_African',
             'Team_Jewish', 'Team_Other', 'Team_South', 'Team_Author_Reputation', 'Team_Author_Publication',
             'Team_Affliation_Weight']
out['missing_counts_team_cols_in_FA_rows'] = {c: int(rt.loc[fa, c].isna().sum()) for c in team_cols}
fa_cols = ['FA_Female', 'FA_European', 'FA_South', 'FA_Author_Reputation', 'FA_Author_Publication',
           'FA_Affliation_Weight', 'Cited_Outgroup', 'Journal_Prestige']
out['missing_counts_FA_cols_in_FA_rows'] = {c: int(rt.loc[fa, c].isna().sum()) for c in fa_cols}
json.dump(out, open(os.path.join(OUT, 'code_checks.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
