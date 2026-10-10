# Builds Model 1 and Model 4 design matrices exactly as in Regression.ipynb cells 4 and 7 (same columns, same
# row filters, missing='drop'), restricted to the rows results_1/results_4 used (outputs/model*_row_labels.csv).
# Saves npz to scratch for the robustness scripts. usecols only to keep memory modest on a shared machine.
import pandas as pd, numpy as np, sys, os
O = sys.argv[1]; S = sys.argv[2]
X1 = ['Const','FA_Female','FA_European','FA_Asian','FA_Slavic','FA_Hispanic/Latino','FA_African','FA_Jewish','FA_Other','FA_South',
      'Mixed_Gender','Cross_Ethnic','Cross_Regional','International','Cited_Outgroup',
      'Team_Size','Cited_References','FA_Author_Reputation','FA_Author_Publication','Article_Age','Journal_Prestige','FA_Affliation_Weight']+['T'+str(i) for i in range(1,50)]
X4 = ['Const','FA_Female','FA_European','FA_Asian','FA_Slavic','FA_Hispanic/Latino','FA_African','FA_Jewish','FA_Other','FA_South',
      'Mixed_Gender','Cross_Ethnic','Cross_Regional','International','Cited_Outgroup',
      'Team_Size','Cited_References','Article_Age','Journal_Prestige','FA_Author_Publication','FA_Author_Reputation','FA_Affliation_Weight']+['T'+str(i) for i in range(1,50)]
hdr = pd.read_csv(os.path.join(S,'regression_table_anonymous_final.csv'), nrows=0).columns.tolist()
use = [hdr[0]] + sorted(set(X1+X4+['FA_Ethnicity','Citations_Received','Top50_Inst']))
df = pd.read_csv(os.path.join(S,'regression_table_anonymous_final.csv'), index_col=0, usecols=use)
for k, cols, lab in [(1, X1, 'model1_row_labels.csv'), (4, X4, 'model4_row_labels.csv')]:
    rows = pd.read_csv(os.path.join(O,'outputs',lab))['row_label'].values
    sub = df.loc[rows]
    y = np.log10(sub['Citations_Received'].values.astype(float)+1)
    X = sub[cols].values.astype(float)
    assert not np.isnan(X).any() and not np.isnan(y).any()
    np.savez(os.path.join(S,'design_m%d.npz'%k), X=X, y=y, count=sub['Citations_Received'].values.astype(float), cols=np.array(cols))
    print(k, X.shape)
