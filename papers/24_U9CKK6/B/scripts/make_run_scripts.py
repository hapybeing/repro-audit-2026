"""Build run scripts from the authors' line ranges (verbatim) plus env-fix lines only.
Usage: python3 make_run_scripts.py <dl_dir> <out_dir>
Writes: run_table1.R, run_table2.R (plain, saveRDS only) and *_F1F2.R variants (pre-registered memory fallback),
and verbatim range files *_ranges_verbatim.R for byte-identity diffs."""
import sys, re, os
dl, out = sys.argv[1], sys.argv[2]
def lines(f): return open(os.path.join(dl, f), encoding="utf-8").read().split("\n")
s6, s9 = lines("6_analysis1.R"), lines("9_analysis4.R")
t1 = s6[0:53] + s6[345:416]          # lines 1-53, 346-416
t2 = s9[0:123]                        # lines 1-123
models1 = ["cycle_AE", "cycle_AE_fit2", "cycle_AE_fit3", "cycle_AE_fit_group"]
models2 = ["AUT_sal_model", "Immi_sal_model", "EU_sal_model"]
def build(src, models, f1, f2):
    o = ["## ENV: run with working directory = RUNDIR (set by the caller). Lines below are the authors' unless marked ## ENV.",
         "cat('START', format(Sys.time()), '\\n')"]
    i = 0; final_texreg_idx = None
    while i < len(src):
        ln = src[i]
        # F2: skip the authors' combined texreg call here; rebuild from RDS at end (same call text)
        if f2 and ln.startswith("texreg(list("):
            j = i
            while not src[j].rstrip().endswith('")') or "caption" not in src[j]: j += 1
            final_texreg = src[i:j+1]; i = j + 1; continue
        m0 = re.match(r"^(\w+) <- lmer\(", ln)
        if f2 and m0 and m0.group(1) in models:
            o.append(f"if (!file.exists(\"models/{m0.group(1)}.rds\")) {{ ## ENV F2 resume after sandbox restart")
        o.append(ln)
        if f1 and ln.startswith("load(\"Data/EP_debates_07062023.Rdata\")"):
            o.append("EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_ ## ENV F1 (pre-registered memory fallback)")
        m = re.match(r"^(\w+) <- lmer\(", ln)
        if m and m.group(1) in models:
            # find end of this lmer call (line containing Nelder_Mead"))
            while "Nelder_Mead\"))" not in src[i]:
                i += 1; o.append(src[i])
            nm = m.group(1)
            o.append(f"saveRDS({nm}, \"models/{nm}.rds\"); cat('SAVED {nm}', format(Sys.time()), '\\n') ## ENV save model")
            if f2:
                o.append(f"rm({nm}); invisible(gc()) ## ENV F2")
                o.append("} ## ENV F2 resume")
        if f2 and re.match(r"^texreg\((\w+)\)$", ln) and re.match(r"^texreg\((\w+)\)$", ln).group(1) in models:
            # authors' print of a single model: needs the object; reload briefly
            nm = re.match(r"^texreg\((\w+)\)$", ln).group(1)
            o[-1] = f"{nm} <- readRDS(\"models/{nm}.rds\"); texreg({nm}); rm({nm}); invisible(gc()) ## ENV F2 (authors' line: texreg({nm}))"
        i += 1
    if f2:
        o.append("## ENV F2: rebuild the authors' combined table from saved models; call text unchanged")
        o.append("rm(EP_eurobar_cent); invisible(gc())")
        for nm in models: o.append(f"{nm} <- readRDS(\"models/{nm}.rds\")")
        o += final_texreg
    o.append("cat('END', format(Sys.time()), '\\n')")
    return "\n".join(o) + "\n"
for name, src, models in [("run_table1", t1, models1), ("run_table2", t2, models2)]:
    open(os.path.join(out, name + "_ranges_verbatim.R"), "w").write("\n".join(src) + "\n")
    open(os.path.join(out, name + ".R"), "w").write(build(src, models, False, False))
    open(os.path.join(out, name + "_F1F2.R"), "w").write(build(src, models, True, True))
print("ok")
