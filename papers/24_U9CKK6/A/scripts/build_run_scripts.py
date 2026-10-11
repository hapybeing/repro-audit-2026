#!/usr/bin/env python3
"""Build the run scripts for 24_U9CKK6 agent A from the authors' deposited scripts.
Authors' lines are copied verbatim (pre-registered ranges). Added lines are environment fixes only:
prelude (.libPaths, setwd), saveRDS of each target-block model to scratch, skip-if-saved wrapper for
resume after a sandbox restart, and (variant f1f2 only) PREREG fallback F1 (blank the two unused
speech-text columns after load) and F2 (rm + gc after each saveRDS, combined texreg from RDS files).
Writes: scripts/run_table1_<variant>.R, scripts/run_table2_<variant>.R, scripts/texreg_table1_from_rds.R,
scripts/texreg_table2_from_rds.R, and ranges/ files with the verbatim line ranges for the byte-identity check."""
import os, re, sys
S = "/workspace/audit_runs/24_U9CKK6/A"
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A"
DL = f"{S}/dl"
MOD = f"{S}/models"
s6 = open(f"{DL}/6_analysis1.R", encoding="utf-8").read().split("\n")
s9 = open(f"{DL}/9_analysis4.R", encoding="utf-8").read().split("\n")
L = lambda src, a, b: src[a-1:b]  # 1-based inclusive

prelude = [
 "## [ENV FIX] per-run library, working directory, model save folder (agent A)",
 f'.libPaths(c("{S}/rlib", .libPaths()))',
 f'setwd("{S}/run")',
  'cat("START", format(Sys.time()), "\\n")',
]
F1 = ["## [ENV FIX F1] blank unused speech-text columns 4 and 6 (positions kept)",
      "EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_"]

def wrap_models(block, names, variant):
    """Wrap each `name <- lmer(` ... up to and incl. `texreg(name)` in a skip-if-saved block, add saveRDS (+rm/gc for F2)."""
    out, i = [], 0
    while i < len(block):
        line = block[i]
        m = re.match(r"^(\w+) <- lmer\(", line)
        if m and m.group(1) in names:
            nm = m.group(1)
            # find the texreg(nm) line
            j = i
            while block[j].strip() != f"texreg({nm})":
                j += 1
            f = f'"{MOD}/{nm}.rds"'  # literal: the authors' rm(list=setdiff(ls(), ...)) at line 41 would delete a variable
            out.append(f"## [ENV FIX] resume: skip if saved")
            out.append(f"if (!file.exists({f})) {{ t0 <- Sys.time()")
            out.extend(block[i:j+1])
            out.append(f'saveRDS({nm}, {f}); cat("SAVED {nm}", format(Sys.time()), format(Sys.time()-t0), "\\n")')
            if variant == "f1f2":
                out.append(f"rm({nm}); invisible(gc())  ## [ENV FIX F2]")
            out.append("}")
            i = j + 1
        else:
            out.append(line); i += 1
    return out

def build(variant):
    # Table 1: lines 1-53 and 346-416 of 6_analysis1.R
    a = L(s6, 1, 53); b = L(s6, 346, 416)
    if variant == "f1f2":
        k = a.index('load("Data/EP_debates_07062023.Rdata")')
        a = a[:k+1] + F1 + a[k+1:]
    names1 = ["cycle_AE", "cycle_AE_fit2", "cycle_AE_fit3", "cycle_AE_fit_group"]
    b = wrap_models(b, names1, variant)
    if variant == "f1f2":
        # final combined texreg is built from RDS in texreg_table1_from_rds.R
        k = next(i for i, x in enumerate(b) if x.startswith("texreg(list("))
        b = b[:k] + ["## [ENV FIX F2] combined texreg moved to scripts/texreg_table1_from_rds.R", "if (FALSE) {"] + b[k:] + ["}"]
    t1 = prelude + a + b + ['cat("END", format(Sys.time()), "\\n")']
    # Table 2: lines 1-123 of 9_analysis4.R
    c = L(s9, 1, 123)
    if variant == "f1f2":
        k = c.index('load("Data/EP_debates_07062023.Rdata")')
        c = c[:k+1] + F1 + c[k+1:]
    names2 = ["AUT_sal_model", "Immi_sal_model", "EU_sal_model"]
    c = wrap_models(c, names2, variant)
    if variant == "f1f2":
        k = next(i for i, x in enumerate(c) if x.startswith("texreg(list("))
        c = c[:k] + ["## [ENV FIX F2] combined texreg moved to scripts/texreg_table2_from_rds.R", "if (FALSE) {"] + c[k:] + ["}"]
    t2 = prelude + c + ['cat("END", format(Sys.time()), "\\n")']
    open(f"{O}/scripts/run_table1_{variant}.R", "w").write("\n".join(t1) + "\n")
    open(f"{O}/scripts/run_table2_{variant}.R", "w").write("\n".join(t2) + "\n")

def texreg_from_rds(src, start_pat, names, out):
    k = next(i for i, x in enumerate(src) if x.startswith(start_pat))
    j = k
    while not src[j].strip().startswith("caption"):
        j += 1
    lines = prelude + ["library(lme4)", "library(texreg)"] + \
        [f'{n} <- readRDS("{MOD}/{n}.rds")' for n in names] + src[k:j+1] + \
        ['cat("END", format(Sys.time()), "\\n")']
    open(out, "w").write("\n".join(lines) + "\n")

for v in ["plain", "f1f2"]:
    build(v)
texreg_from_rds(L(s6, 346, 416), "texreg(list(", ["cycle_AE", "cycle_AE_fit2", "cycle_AE_fit3", "cycle_AE_fit_group"], f"{O}/scripts/texreg_table1_from_rds.R")
texreg_from_rds(L(s9, 1, 123), "texreg(list(", ["AUT_sal_model", "Immi_sal_model", "EU_sal_model"], f"{O}/scripts/texreg_table2_from_rds.R")
# verbatim ranges for the byte-identity check
os.makedirs(f"{S}/ranges", exist_ok=True)
open(f"{S}/ranges/6_analysis1_L1-53_L346-416.R", "w").write("\n".join(L(s6,1,53)+L(s6,346,416)) + "\n")
open(f"{S}/ranges/9_analysis4_L1-123.R", "w").write("\n".join(L(s9,1,123)) + "\n")
print("ok")
