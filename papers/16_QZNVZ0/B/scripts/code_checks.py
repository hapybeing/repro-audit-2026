# Context counts for code-review observations (no model change). Reads the deposited CSV.
import pandas as pd, sys
df = pd.read_csv(sys.argv[1], index_col=0, usecols=[0,1] + [], nrows=0)  # header probe
hdr = pd.read_csv(sys.argv[1], nrows=0).columns.tolist()
df = pd.read_csv(sys.argv[1], index_col=0, usecols=[hdr[0], 'FA_Ethnicity', 'FA_South', 'Top10_Inst', 'Top50_Inst'])
m = df['FA_Ethnicity'].notna()
out = {'rows': len(df), 'FA_Ethnicity_nonmissing': int(m.sum()),
       'top10_rows_FA_Ethnicity_nonmissing': int((m & df['Top10_Inst']).sum()),
       'top10_FA_South_eq1': int((m & df['Top10_Inst'] & (df['FA_South'] == 1)).sum()),
       'top10_FA_South_missing': int((m & df['Top10_Inst'] & df['FA_South'].isna()).sum()),
       'top50_FA_South_eq1': int((m & df['Top50_Inst'] & (df['FA_South'] == 1)).sum())}
pd.Series(out).to_csv(sys.argv[2] + '/outputs/code_check_counts.csv', header=['value'])
print(out)
