## Extract target and context numbers from the saved lmer models (agent A, 24_U9CKK6).
## Inference as pre-registered: naive normal p = 2*pnorm(-|est/SE|) (texreg default for lmerMod).
.libPaths(c("/workspace/audit_runs/24_U9CKK6/A/rlib", .libPaths()))
suppressMessages(library(lme4))
MOD <- "/workspace/audit_runs/24_U9CKK6/A/models"
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/24_U9CKK6/A/outputs"
want <- list(
  cycle_AE = c("challenge","days_to_EP","days_to_nat","challenge:days_to_EP","challenge:days_to_nat","lrgen_scale"),
  cycle_AE_fit2 = c("challenge","days_to_EP","days_to_nat","challenge:days_to_EP","challenge:days_to_nat","lrgen_scale","EP_Coa"),
  cycle_AE_fit3 = c("challenge","days_to_EP","days_to_nat","challenge:days_to_EP","challenge:days_to_nat","lrgen_scale","EP_Coa","nat_opp"),
  cycle_AE_fit_group = c("challenge","days_to_EP","days_to_nat","challenge:days_to_EP","challenge:days_to_nat","lrgen_scale"),
  AUT_sal_model = c("challenge","aut_sal","challenge:aut_sal","lrgen_scale","EP_Coa","nat_opp"),
  Immi_sal_model = c("challenge","immi_sal","challenge:immi_sal","lrgen_scale","EP_Coa","nat_opp"),
  EU_sal_model = c("challenge","EU_sal","challenge:EU_sal","lrgen_scale","EP_Coa","nat_opp"))
rows <- list(); gof <- list()
for (nm in names(want)) {
  f <- file.path(MOD, paste0(nm, ".rds"))
  if (!file.exists(f)) { cat("missing", nm, "\n"); next }
  m <- readRDS(f)
  fe <- fixef(m); se <- sqrt(diag(as.matrix(vcov(m)))); names(se) <- names(fe)
  msg <- paste(m@optinfo$conv$lme4$messages, collapse = " | ")
  for (t in want[[nm]]) {
    est <- unname(fe[t]); s <- unname(se[t]); z <- est / s
    rows[[length(rows)+1]] <- data.frame(model = nm, term = t, estimate = est, se = s, t_value = z,
      p_naive = 2 * pnorm(-abs(z)), estimate_round2 = round(est, 2), se_round2 = round(s, 2),
      nobs = nobs(m), conv_messages = msg, stringsAsFactors = FALSE)
  }
  ng <- ngrps(m); vc <- as.data.frame(VarCorr(m))
  gof[[length(gof)+1]] <- data.frame(model = nm, nobs = nobs(m), n_mep_ids = unname(ng["mep_ids"]),
    n_party_id = unname(ng["party_id"]), AIC = AIC(m), BIC = BIC(m), logLik = as.numeric(logLik(m)),
    var_mep = vc$vcov[vc$grp == "mep_ids"], var_party = vc$vcov[vc$grp == "party_id"],
    var_resid = vc$vcov[vc$grp == "Residual"], REML = isREML(m), n_fixef = length(fe),
    dropped_cols = paste(attr(getME(m, "X"), "col.dropped"), collapse = ";"),
    conv_messages = msg, optimizer = m@optinfo$optimizer, stringsAsFactors = FALSE)
  write.csv(data.frame(term = names(fe), estimate = unname(fe), se = unname(se)),
            file.path(OUT, paste0("fixef_all_", nm, ".csv")), row.names = FALSE)
  rm(m); invisible(gc())
}
write.csv(do.call(rbind, rows), file.path(OUT, "targets_extracted.csv"), row.names = FALSE)
write.csv(do.call(rbind, gof), file.path(OUT, "model_gof.csv"), row.names = FALSE)
cat("done\n")
