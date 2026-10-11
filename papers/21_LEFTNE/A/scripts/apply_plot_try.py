"""Allowed plot-only environment fix (PREREG.md section 2): wrap each top-level figure-printing statement that renders a
hrbrthemes::theme_ipsum_rc theme (Roboto Condensed font not available to the R pdf device -> 'invalid font type') in try(print({ ... })) so the render error is caught inside try (a bare try() would return the plot and print it outside try).
No estimation line is touched. Writes patched copies into RUNDIR/data/ and unified diffs into diffs/."""
import subprocess, pathlib
RUN = pathlib.Path("/workspace/audit_runs/21_LEFTNE/A"); DIFFS = pathlib.Path("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/21_LEFTNE/A/diffs")
ranges = {"01- Replication_Text.R": [(71, 77), (155, 162), (201, 207), (229, 238), (274, 274), (336, 336)],
          "02- Replication_Appendix.R": [(334, 340), (353, 359), (395, 395), (416, 418), (428, 430)]}
for fn, rs in ranges.items():
    lines = (RUN / "orig" / fn).read_text().splitlines(keepends=True)
    for a, b in sorted(rs, reverse=True):
        lines[b - 1] = lines[b - 1].rstrip("\n") + "}))  # audit env fix: plot-only, made non-fatal\n"
        lines[a - 1] = "try(print({" + lines[a - 1]
    (RUN / "data" / fn).write_text("".join(lines))
    d = subprocess.run(["diff", "-u", str(RUN / "orig" / fn), str(RUN / "data" / fn)], capture_output=True, text=True).stdout
    (DIFFS / (fn.split("- ")[1].replace(".R", "") + "_plot_try.diff")).write_text(d)
    print(fn, "wrapped", len(rs), "statements")
