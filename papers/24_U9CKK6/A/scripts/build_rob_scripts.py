#!/usr/bin/env python3
"""Build robustness prep scripts: authors' data-prep lines (from the F1 variant of the run scripts, i.e. text
columns blanked, which no estimation uses) followed by code that saves the estimation samples of the target
models to scratch (sample = rows of model.frame(<saved model>))."""
O = "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A"
S = "/workspace/audit_runs/24_U9CKK6/A"
for tab, models in [("table1", ["cycle_AE_fit2"]), ("table2", ["AUT_sal_model", "EU_sal_model"])]:
    src = open(f"{O}/scripts/run_table{tab[-1]}_f1f2.R").read().split("\n")
    k = next(i for i, x in enumerate(src) if x.startswith("## [ENV FIX] resume"))
    body = src[:k]
    add = ['## ---- agent A robustness prep: save estimation samples ----', 'w <- warnings(); cat("N_WARNINGS", length(w), "\\n"); print(head(w, 5)); print(table(sub("\\x27.*", "", names(w))))', 'suppressMessages(library(lme4))']
    for m in models:
        add += [f'm <- readRDS("{S}/models/{m}.rds")',
                'mf <- model.frame(m); idx <- match(rownames(mf), rownames(EP_eurobar_cent))',
                'stopifnot(!anyNA(idx), nrow(mf) == nobs(m))',
                'vars <- intersect(all.vars(formula(m)), names(EP_eurobar_cent))',
                'smp <- EP_eurobar_cent[idx, vars]',
                f'saveRDS(list(data = smp, formula = formula(m), rows = idx), "{S}/models/sample_{m}.rds")',
                f'cat("SAMPLE {m}", nrow(smp), ncol(smp), "\\n")', 'rm(m, mf, smp); invisible(gc())']
    open(f"{O}/scripts/rob_prep_{tab}.R", "w").write("\n".join(body + add) + "\n")
print("ok")
