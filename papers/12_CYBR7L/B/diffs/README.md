# Diffs (agent B, 12_CYBR7L)

- replication_code_audit.ipynb.diff: raw JSON diff of the deposited notebook against the run copy.
- replication_code_audit_cells.diff: the same change shown as concatenated cell source, easier to read.

Why: PREREG section 2 asks for the 2021 and 2010 networks to be pickled so the boundary scores and robustness checks run on the same `G_citation` objects as Table 1. Two cells were added that only call `pickle.dump`:
1. right after the Table 1 cell (saves `G_citation`, the 2021 `authorities` dict and the 2021 `df_auth_cit_net` used for Table 1). It is placed there, not at the very end, because the Table 2 cell rebuilds `G_citation` with isolated nodes, so a final cell would hold different networks than Table 1 used.
2. at the end (saves the Table 2 networks).
No computation, package version or path was changed. No other environment fix was needed (README versions installed and ran without error).
