# Reads outputs/mermods.rds and outputs/war_mod_out.rds; writes outputs/targets_extracted.csv, outputs/mermods_fe_pop.csv, outputs/war_mod_out.csv
.libPaths(c("/workspace/audit_runs/25_914AN0/A/rlib", .libPaths())); suppressMessages(library(data.table))
PDIR <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A"
mm <- readRDS(file.path(PDIR,"outputs","mermods.rds")); setDT(mm)
fe <- mm[model_name=="FE pop weights", .(outcome_name, b, l, u, n, N_DIV_ARMY, N_bxid, N_TID, hausman_p)]
fwrite(fe, file.path(PDIR,"outputs","mermods_fe_pop.csv"))
fwrite(mm[, .(outcome_name, model_name, b, l, u, n)], file.path(PDIR,"outputs","mermods_all_nkvd.csv"))
tg <- list()
add <- function(id, v, l=NA, u=NA, src) tg[[length(tg)+1]] <<- data.table(id=id, value=v, l=l, u=u, src=src)
for (p in list(c("T1","MIA_100"), c("T2","KIA_100"), c("T3","WMED_100"), c("T4","POW_100"))) {
  r <- fe[outcome_name==p[2]]
  if (nrow(r)==1) add(p[1], r$b, r$l, r$u, paste0("mermods FE pop weights ", p[2])) else add(p[1], NA, NA, NA, paste0("missing row ", p[2]))
}
ns <- unique(fe$n); add("T5", if (length(ns)==1) ns else NA, min(fe$n), max(fe$n), "mermods FE pop weights n (min,max across outcomes in l,u)")
f6 <- file.path(PDIR,"outputs","war_mod_out.rds")
if (file.exists(f6)) { w <- readRDS(f6); setDT(w); fwrite(w, file.path(PDIR,"outputs","war_mod_out.csv"))
  r <- w[model_name=="Model 1" & x=="blocking"]; add("T6", r$b, r$l, r$u, paste0("war mod_out Model 1 blocking, outcome ", r$outcome_name, ", n=", r$n))
} else add("T6", NA, NA, NA, "war_mod_out.rds missing")
out <- rbindlist(tg); fwrite(out, file.path(PDIR,"outputs","targets_extracted.csv")); print(out)
