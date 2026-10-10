# Agent B: pre-registered robustness checks R_a, R_b, R_c (PREREG.md section 3).
args <- commandArgs(TRUE); RUN <- args[1]; OUT <- args[2]; RAW <- args[3]
suppressPackageStartupMessages({library(cregg); library(data.table); library(jsonlite)})
d <- readRDS(file.path(RUN, "pooled_df2.rds"))
feats <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive","Since","Education")
fc1f <- c("Gender","Age","Citizenship","Composition","Unemployment","Supportive")
f8 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Since + Education
f_fig1 <- selected ~ Gender + Age + Citizenship + Composition + Unemployment + Supportive + Citizenship + Since + Education
E1lev <- "2 Adults, 3 Childr."
lab2var <- c("Gender"="Gender","Age"="Age","Nationality"="Citizenship","Household\nComposition"="Composition",
             "Reason for\nUnemployment"="Unemployment","Supportive\nBehavior"="Supportive",
             "Duration of\nUnemployment"="Since","Education\nLevel"="Education")
fixf <- function(x) { x <- as.data.frame(x); x$feature <- as.character(x$feature); lab2var2 <- c(lab2var, setNames(unname(lab2var), unname(lab2var))); stopifnot(all(x$feature %in% names(lab2var2))); x$feature <- unname(lab2var2[x$feature]); x }
mm0 <- fixf(read.csv(file.path(OUT, "cj_marginal_means_grouped_sector.csv")))
e1row <- mm0[mm0$sector == "Private Sector" & mm0$feature == "Composition" & mm0$level == E1lev, ]
ds <- d[d$sector %in% c("Private Sector","Public Sector"), ]
ds$sector <- droplevels(ds$sector)
res <- list()

## R_a: respondent cluster bootstrap
set.seed(20261009); B <- 1000
long <- rbindlist(lapply(feats, function(f) data.table(id = ds$respondentIndex, sector = as.character(ds$sector), lev = paste0(f, "::", as.character(ds[[f]])), y = ds$selected)))
agg <- long[, .(s = sum(y), n = .N), by = .(id, sector, lev)]
levs <- sort(unique(agg$lev)); ids <- unique(ds[, c("respondentIndex","sector")]); ids$sector <- as.character(ids$sector)
idx <- function(sec) ids$respondentIndex[ids$sector == sec]
mats <- lapply(c("Private Sector","Public Sector"), function(sec) {
  a <- agg[sector == sec]; rid <- idx(sec)
  S <- matrix(0, length(rid), length(levs), dimnames = list(rid, levs)); N <- S
  S[cbind(match(a$id, rid), match(a$lev, levs))] <- a$s; N[cbind(match(a$id, rid), match(a$lev, levs))] <- a$n
  list(S = S, N = N, n = length(rid))})
names(mats) <- c("Private Sector","Public Sector")
bmm <- list(); for (sec in names(mats)) bmm[[sec]] <- matrix(NA, B, length(levs), dimnames = list(NULL, levs))
for (b in 1:B) for (sec in names(mats)) {
  m <- mats[[sec]]; w <- tabulate(sample.int(m$n, m$n, replace = TRUE), m$n)
  bmm[[sec]][b, ] <- as.vector(crossprod(w, m$S)) / as.vector(crossprod(w, m$N))
}
orig_unw <- sapply(names(mats), function(sec) colSums(mats[[sec]]$S) / colSums(mats[[sec]]$N))
e1n <- paste0("Composition::", E1lev); e1b <- bmm[["Private Sector"]][, e1n]
dif <- bmm[["Public Sector"]] - bmm[["Private Sector"]]
ci <- t(apply(dif, 2, quantile, c(.025, .975)))
dtab <- data.frame(lev = levs, feature = sub("::.*","",levs), level = sub(".*::","",levs),
                   mmdiff_orig = orig_unw[, "Public Sector"] - orig_unw[, "Private Sector"], lo = ci[,1], hi = ci[,2])
dtab$excl0 <- dtab$lo > 0 | dtab$hi < 0
write.csv(dtab, file.path(OUT, "robustness_R_a_mmdiff_ci.csv"), row.names = FALSE)
pa <- min(1, 2 * min(mean(e1b <= 0.5), mean(e1b >= 0.5)))
qa <- unname(quantile(e1b, c(.025, .975)))
res$R_a <- list(estimate = e1row$estimate, unweighted_mean_check = unname(orig_unw[e1n, "Private Sector"]),
  ci_lower = qa[1], ci_upper = qa[2], boot_se = sd(e1b), p_value = pa, B = B, seed = 20261009,
  n_resp = sapply(mats, `[[`, "n"),
  same = e1row$estimate > 0.5 && qa[1] > 0.5, fc1_count = sum(dtab$excl0[dtab$feature %in% fc1f]),
  fc1_levels = dtab$lev[dtab$excl0 & dtab$feature %in% fc1f], other_levels_excl0 = dtab$lev[dtab$excl0 & !dtab$feature %in% fc1f])

## R_b: drop top/bottom 1% of survey duration within each sample
files <- c(rh = "data_rh.csv", uhh = "data_UHH.csv", hsvn = "data_HSVN.csv", civic = "data_civic.csv")
dur <- rbindlist(lapply(names(files), function(s) { r <- fread(file.path(RAW, files[s]), data.table = TRUE, select = c("ResponseId","Duration (in seconds)"), colClasses = "character")
  data.table(sam = s, respondentIndex = r$ResponseId, dur = suppressWarnings(as.numeric(r[["Duration (in seconds)"]])))}))
dur <- dur[!is.na(dur)]
d$sam <- sub("\n.*", "", as.character(d$Sample))
resp <- unique(data.table(sam = d$sam, respondentIndex = d$respondentIndex))
rj <- merge(resp, dur, by = c("sam","respondentIndex"), all.x = TRUE)
drop_ids <- c(); dropped <- list()
for (s in unique(rj$sam)) { z <- rj[sam == s]; q <- quantile(z$dur, c(.01, .99), type = 7, na.rm = TRUE)
  dr <- z$respondentIndex[!is.na(z$dur) & (z$dur < q[1] | z$dur > q[2])]; drop_ids <- c(drop_ids, dr)
  dropped[[s]] <- list(n_resp = nrow(z), n_no_duration = sum(is.na(z$dur)), p01 = unname(q[1]), p99 = unname(q[2]), dropped = length(dr)) }
dr2 <- d[!d$respondentIndex %in% drop_ids, ]
mmb <- fixf(cj(data = dr2, formula = f_fig1, estimate = "mm", by = ~ sector, id = ~ respondentIndex))
mdb <- fixf(cj(data = dr2, formula = f8, estimate = "mm_diff", by = ~ sector, id = ~ respondentIndex))
write.csv(as.data.frame(mmb), file.path(OUT, "robustness_R_b_fig1_mm.csv"), row.names = FALSE)
write.csv(as.data.frame(mdb), file.path(OUT, "robustness_R_b_fig2_mmdiff.csv"), row.names = FALSE)
eb <- mmb[mmb$sector == "Private Sector" & mmb$feature == "Composition" & mmb$level == E1lev, ]
mdb$excl0 <- mdb$lower > 0 | mdb$upper < 0
res$R_b <- list(estimate = eb$estimate, se = eb$std.error, ci_lower = eb$lower, ci_upper = eb$upper,
  p_value = 2 * pnorm(-abs((eb$estimate - 0.5) / eb$std.error)), same = eb$estimate > 0.5 && eb$lower > 0.5,
  fc1_count = sum(mdb$excl0[mdb$feature %in% fc1f]), fc1_levels = paste(mdb$feature, mdb$level)[mdb$excl0 & mdb$feature %in% fc1f],
  dropped_per_sample = dropped, total_dropped = length(drop_ids))

## R_c: AMCEs and omnibus test
am <- fixf(cj(ds, f8, estimate = "amce", by = ~ sector, id = ~ respondentIndex))
write.csv(as.data.frame(am), file.path(OUT, "robustness_R_c_amce.csv"), row.names = FALSE)
ec <- am[am$sector == "Private Sector" & am$feature == "Composition" & am$level == E1lev, ]
av <- cj_anova(ds, f8, by = ~ sector)
capture.output(print(av), file = file.path(OUT, "robustness_R_c_anova.txt"))
res$R_c <- list(estimate = ec$estimate, se = ec$std.error, ci_lower = ec$lower, ci_upper = ec$upper, p_value = ec$p,
  baseline = levels(ds$Composition)[1], same = ec$estimate > 0 && ec$p < 0.05,
  anova_F = av$F[2], anova_p = av[["Pr(>F)"]][2], anova_same_as_paper = av[["Pr(>F)"]][2] >= 0.05)
write_json(res, file.path(OUT, "robustness.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA)
cat(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = 6))
