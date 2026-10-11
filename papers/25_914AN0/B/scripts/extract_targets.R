# Reads outputs/mermods.rds and outputs/war_mod_out.rds, writes outputs/targets_extracted.csv and outputs/fe_pop_rows.csv
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/B/outputs"
library(data.table)
rows <- list()
if (file.exists(file.path(OUT,"mermods.rds"))) {
  m <- as.data.table(readRDS(file.path(OUT,"mermods.rds")))
  fe <- m[model_name=="FE pop weights", .(outcome_name, b, l, u, se=(u-b)/1.96, n, N_DIV_ARMY, N_bxid, N_TID, hausman_p)]
  fwrite(fe, file.path(OUT,"fe_pop_rows.csv"))
  map <- c(T1="MIA_100", T2="KIA_100", T3="WMED_100", T4="POW_100")
  for (t in names(map)) { r <- fe[outcome_name==map[[t]]]
    rows[[t]] <- if (nrow(r)) data.table(id=t, quantity=paste0("b ", map[[t]]), value=r$b, l=r$l, u=r$u, se=r$se) else data.table(id=t, quantity=map[[t]], value=NA_real_, l=NA_real_, u=NA_real_, se=NA_real_) }
  nn <- unique(fe$n)
  rows[["T5"]] <- data.table(id="T5", quantity=paste0("n FE pop weights (unique values across outcomes: ", paste(nn, collapse="/"), ")"), value=if(length(nn)) fe[outcome_name=="MIA_100", n] else NA_real_, l=NA_real_, u=NA_real_, se=NA_real_)
}
if (file.exists(file.path(OUT,"war_mod_out.rds"))) {
  w <- as.data.table(readRDS(file.path(OUT,"war_mod_out.rds")))
  r <- w[model_name=="Model 1" & x=="blocking"]
  rows[["T6"]] <- data.table(id="T6", quantity=paste0("b blocking, Model 1, outcome ", r$outcome_name, ", n=", r$n), value=r$b, l=r$l, u=r$u, se=(r$u-r$b)/1.96)
}
res <- rbindlist(rows); fwrite(res, file.path(OUT,"targets_extracted.csv")); print(res, digits=10)
