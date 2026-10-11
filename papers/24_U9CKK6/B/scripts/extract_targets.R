## Reads saved models (scratch) and writes outputs/targets_extracted.csv. Usage: Rscript extract_targets.R <models_dir> <outputs_dir>
suppressMessages(library(lme4))
a <- commandArgs(TRUE); md <- a[1]; od <- a[2]
spec <- data.frame(id = c("T1","T2","T3","T4","T5","T6"),
  model = c("cycle_AE_fit2","cycle_AE_fit2","cycle_AE_fit2","cycle_AE_fit2","AUT_sal_model","EU_sal_model"),
  term = c("challenge:days_to_nat","days_to_EP","challenge","NOBS","challenge:aut_sal","challenge:EU_sal"))
rows <- list(); cache <- list()
for (i in seq_len(nrow(spec))) {
  f <- file.path(md, paste0(spec$model[i], ".rds"))
  if (!file.exists(f)) { rows[[i]] <- data.frame(id = spec$id[i], model = spec$model[i], term = spec$term[i], estimate = NA, se = NA, t = NA, p_naive = NA, nobs = NA, n_mep = NA, n_party = NA, conv_messages = "model file missing"); next }
  if (is.null(cache[[spec$model[i]]])) cache[[spec$model[i]]] <- readRDS(f)
  m <- cache[[spec$model[i]]]
  fe <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m)))); names(se) <- names(fe)
  ng <- ngrps(m); cm <- m@optinfo$conv$lme4$messages
  cm <- if (is.null(cm)) "none" else paste(cm, collapse = " | ")
  if (spec$term[i] == "NOBS") { est <- nobs(m); s <- NA; tt <- NA; p <- NA } else {
    est <- unname(fe[spec$term[i]]); s <- unname(se[spec$term[i]]); tt <- est / s; p <- 2 * pnorm(-abs(tt)) }
  rows[[i]] <- data.frame(id = spec$id[i], model = spec$model[i], term = spec$term[i], estimate = est, se = s, t = tt,
    p_naive = p, nobs = nobs(m), n_mep = unname(ng["mep_ids"]), n_party = unname(ng["party_id"]), conv_messages = cm)
}
out <- do.call(rbind, rows)
write.csv(out, file.path(od, "targets_extracted.csv"), row.names = FALSE)
## full fixed-effect tables for context (secondary numbers)
for (nm in names(cache)) { m <- cache[[nm]]; fe <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m))))
  write.csv(data.frame(term = names(fe), estimate = fe, se = se, t = fe/se, p_naive = 2*pnorm(-abs(fe/se))),
            file.path(od, paste0("fixef_", nm, ".csv")), row.names = FALSE)
  writeLines(c(paste("nobs", nobs(m)), paste("AIC", AIC(m)), paste("logLik", as.numeric(logLik(m))),
               capture.output(print(ngrps(m))), capture.output(print(VarCorr(m), comp = "Variance")),
               paste("dropped_cols", paste(attr(m@pp$X, "col.dropped"), collapse = ";"))),
             file.path(od, paste0("modelinfo_", nm, ".txt"))) }
print(out)
