# Diffs (12_CYBR7L, agent A)

- `replication_code_audit_cells.diff`: readable cell-source diff between the deposited `replication_code.ipynb` and the run copy `replication_code_audit.ipynb`. Two cells added, both only pickle objects:
  1. inserted after cell 8 (before cell 9): saves `G_citation` (the cell 6 networks) and `author_attributes` to `audit_G_citation_cell6.pkl`. Needed because cell 9 reassigns `G_citation`, and PREREG section 2 and 3 run the boundary scores and robustness checks on the cell 6 `G_citation[2021]`.
  2. appended at the end: saves the post-cell-9 objects to `audit_G_citation_cell9.pkl` (the "added final cell" PREREG names; not used by any check).
- `replication_code_audit.ipynb.diff`: the same change as a raw JSON diff of the notebook files.

No change to any analysis line, file path, package version or backend in the code. `MPLBACKEND=Agg` was set in the shell environment, not in the code.
