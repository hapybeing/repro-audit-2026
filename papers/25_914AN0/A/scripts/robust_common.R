# Shared setup for pre-registered robustness checks (PREREG.md section 3). Uses X_s from S1a.
lib <- "/workspace/audit_runs/25_914AN0/A/rlib"; .libPaths(c(lib, .libPaths()))
suppressMessages({library(data.table); library(lfe); library(Formula)})
RUNDIR <- "/workspace/audit_runs/25_914AN0/A"; PDIR <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A"
X_s <- readRDS(file.path(RUNDIR,"inter","s1a.rds"))$X_s
# Authors' formula, run2_main.R line 65 (copied verbatim)
model_fe <- Formula::Formula(y ~  log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) | DIV_ARMY + TID + bxid )
outs <- c(MIA="MIA_100", KIA="KIA_100", Medals="WMED_100", POW="POW_100")
paper <- c(MIA=-1.432, KIA=0.629, Medals=-0.287, POW=-0.176)
needed <- c("NKVD_OO","AGE_1941","soldiers_dist","RUS_100","URBAN_PCT","POP_DENSITY","M_10km_ADM3","DIV_ARMY","TID","bxid","N_SOLDIERS")
est_sample <- function(yv){ D <- as.data.table(X_s)[, c(yv, needed), with=FALSE]; D <- D[complete.cases(D)]; D[, y := get(yv)]; D }
fit_fe <- function(D, f=model_fe){ m <- lfe::felm(f, data=D, weights=D$N_SOLDIERS, exactDOF=TRUE); m }
# felm default SE: IID without a cluster part, cluster-robust when the formula has a cluster part
nkvd_row <- function(m){ ct <- summary(m)$coefficients; ct[grep("NKVD", rownames(ct)), ] }
