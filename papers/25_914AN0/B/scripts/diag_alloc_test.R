suppressMessages({library(data.table); library(dplyr); library(lme4); library(lfe)})
source("code/functions.R")
model_fe <- Formula::Formula(y ~  log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) | DIV_ARMY + TID + bxid )
model_re <- as.formula(y ~ log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) + (1|DIV_ARMY)+(1|TID)+(1|bxid))
for (alloc in c(FALSE, TRUE)) {
 X_s <- readRDS("/workspace/audit_runs/25_914AN0/B/inter/s1a.rds")$X_s; if (alloc) setalloccol(X_s)
 m <- ensemble_modz(X_s=X_s, yvarz=c("KIA_100","WMED_100"), model_re=model_re, model_fe=model_fe)
 cat("alloc =", alloc, "\n"); print(m[, .(outcome_name, model_name, b)])
}
