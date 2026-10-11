"""Builds LOG.md from the timestamped run-log entries (written during the run by scripts/logit.sh to
/workspace/audit_runs/21_LEFTNE/A/log_entries.md) plus a fixed header."""
import pathlib
A = pathlib.Path("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A")
entries = pathlib.Path("/workspace/audit_runs/21_LEFTNE/A/log_entries.md").read_text()
hdr = """# LOG: 21_LEFTNE, agent A

Paper: DeMora et al. (2025), BJPolS 55 e175, doi 10.1017/S0007123425101166. Dataset doi 10.7910/DVN/LEFTNE (v1.0).
Scratch: /workspace/audit_runs/21_LEFTNE/A/ (raw downloads, data/, orig/, rlib/, si/). Times are IST; tool output times in UTC are marked UTC.
Brief: batches/batch5_run_brief.md with AGENT=A, PID=21_LEFTNE. PREREG.md and targets.json were read only, not edited.
Did not read any B/ folder, other papers' folders, or batch reports.

## Run log
"""
(A / "LOG.md").write_text(hdr + entries)
print("LOG.md written,", entries.count("\n- "), "entries")
