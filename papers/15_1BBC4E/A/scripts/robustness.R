# Pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3) for 15_1BBC4E.
suppressPackageStartupMessages(library(jsonlite))
OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/A/outputs"
d <- readRDS("/workspace/audit_runs/15_1BBC4E/A/deposit/Replication Data/Replication Files. Electoral Autocracy. Hybrid Regimes. Multiparty Autocracy. Same. same but different/Data/Regimedata/Measures_merged.rds")
v <- c(LIED="RegType_lied_EA", RoW="RegType_RoW_EA", Polity="Politytype_Anocracy", FH="status_fh_PF",
       ARD="HTW_RegType_MP_Autocracy", AoW="RegType_magaloni_EA", CPR="AnckarRegtype_MP_Autocracy")
X <- as.matrix(as.data.frame(d)[, v]); colnames(X) <- names(v); storage.mode(X) <- "double"
cc <- d$Final_Code
summ <- function(m) { u <- m[upper.tri(m)]; i <- which(m == max(u, na.rm=TRUE), arr.ind=TRUE)[1,]
  list(T1=m["ARD","AoW"], T2=m["Polity","CPR"], T3=m["LIED","RoW"], max21=max(u, na.rm=TRUE),
       max_pair=paste(rownames(m)[i[1]], colnames(m)[i[2]], sep="-"), median21=median(u, na.rm=TRUE)) }
full <- cor(X, use="pairwise.complete.obs"); fs <- summ(full)
res <- list(full_sample=fs, na_final_code_rows=sum(is.na(cc)),
            na_final_code_rows_with_ARD_AoW_pair=sum(is.na(cc) & !is.na(X[,"ARD"]) & !is.na(X[,"AoW"])))

## R_a country-cluster bootstrap
set.seed(20261010)
keep <- !is.na(cc)  # rows with missing Final_Code are not a country; they have no non-missing pair (see na_* fields)
idx <- split(which(keep), cc[keep]); K <- length(idx); B <- 1000
bt <- matrix(NA_real_, B, 5, dimnames=list(NULL, c("T1","T2","T3","max21","median21")))
for (b in 1:B) { s <- sample.int(K, K, replace=TRUE); r <- unlist(idx[s], use.names=FALSE)
  m <- suppressWarnings(cor(X[r,], use="pairwise.complete.obs")); z <- summ(m)
  bt[b,] <- c(z$T1, z$T2, z$T3, z$max21, z$median21) }
write.csv(bt, file.path(OUT, "R_a_bootstrap_draws.csv"), row.names=FALSE)
t1 <- bt[,"T1"]; ok <- t1[!is.na(t1)]
q <- unname(quantile(ok, c(.025,.975)))
res$R_a <- list(seed=20261010, B=B, n_clusters=K, estimate=fs$T1, ci_lo=q[1], ci_hi=q[2], boot_se=sd(ok),
  share_T1_ge_0.73=mean(ok >= 0.73), p_value=min(2*mean(ok <= 0), 1), n_undefined=sum(is.na(t1)),
  T2_ci=unname(quantile(bt[,"T2"], c(.025,.975), na.rm=TRUE)), T3_ci=unname(quantile(bt[,"T3"], c(.025,.975), na.rm=TRUE)),
  max21_ci=unname(quantile(bt[,"max21"], c(.025,.975), na.rm=TRUE)), median21_ci=unname(quantile(bt[,"median21"], c(.025,.975), na.rm=TRUE)),
  share_max21_ge_0.73=mean(bt[,"max21"] >= 0.73, na.rm=TRUE))
res$R_a$same <- (fs$T1 > 0) && (q[1] > 0) && (fs$T1 < 0.73)

## R_b influential-country exclusion (leave-one-country-out on T1)
pair <- !is.na(X[,"ARD"]) & !is.na(X[,"AoW"]) & !is.na(cc)
cs <- sort(unique(cc[pair]))
loo <- sapply(cs, function(k) { r <- pair & cc != k; cor(X[r,"ARD"], X[r,"AoW"]) })
infl <- data.frame(Final_Code=cs, T1_without=loo, abs_change=abs(loo - fs$T1))
infl <- infl[order(-infl$abs_change),]
nd <- max(1, ceiling(0.01*length(cs))); drop <- infl$Final_Code[1:nd]
write.csv(infl, file.path(OUT, "R_b_loco_T1.csv"), row.names=FALSE)
nm <- sapply(drop, function(k) { x <- unique(na.omit(c(as.character(d$extended_country_name[cc %in% k]), as.character(d$country_name_lied[cc %in% k])))); paste(x, collapse="/") })
r <- !(cc %in% drop)  # rows with NA Final_Code kept (they enter no pair)
mb <- cor(X[r,], use="pairwise.complete.obs"); sb <- summ(mb)
ct <- cor.test(X[r,"ARD"], X[r,"AoW"])
res$R_b <- list(n_countries_ranked=length(cs), n_dropped=nd, dropped_Final_Code=drop, dropped_names=unname(nm),
  dropped_country_years_all_rows=sum(cc %in% drop), dropped_country_years_with_ARD_AoW_pair=sum(pair & cc %in% drop),
  estimate=unname(ct$estimate), ci_lo=ct$conf.int[1], ci_hi=ct$conf.int[2], p_value=ct$p.value, n=sum(!is.na(X[r,"ARD"]) & !is.na(X[r,"AoW"])),
  T2=sb$T2, T3=sb$T3, max21=sb$max21, max_pair=sb$max_pair, median21=sb$median21)
res$R_b$same <- (ct$estimate > 0) && (ct$conf.int[1] > 0) && (ct$estimate < 0.73)

## R_c listwise common sample
cm <- complete.cases(X); mc <- cor(X[cm,]); sc <- summ(mc); ct2 <- cor.test(X[cm,"ARD"], X[cm,"AoW"])
write.csv(round(mc, 10), file.path(OUT, "R_c_listwise_matrix.csv"))
res$R_c <- list(N=sum(cm), estimate=unname(ct2$estimate), ci_lo=ct2$conf.int[1], ci_hi=ct2$conf.int[2], p_value=ct2$p.value,
  T2=sc$T2, T3=sc$T3, max21=sc$max21, max_pair=sc$max_pair, median21=sc$median21)
res$R_c$same <- (ct2$estimate > 0) && (ct2$conf.int[1] > 0) && (ct2$estimate < 0.73)
write_json(res, file.path(OUT, "robustness.json"), auto_unbox=TRUE, digits=NA, pretty=TRUE)
cat(toJSON(res, auto_unbox=TRUE, digits=6, pretty=TRUE))
