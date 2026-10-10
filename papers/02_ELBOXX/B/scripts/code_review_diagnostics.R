# Code review diagnostics (NOT pre-registered analyses; evidence for the code review only).
# Usage: Rscript code_review_diagnostics.R <scratch dir with data/ and objs/> <REPO B dir>
args <- commandArgs(trailingOnly = TRUE)
S <- args[1]; B <- args[2]
o <- readRDS(file.path(S, "objs", "pathA_fixed_objects.rds")); d <- o$d
sh <- readRDS(file.path(S, "objs", "pathB_objects.rds"))$d
m <- read.csv(file.path(S, "data", "dyadic_mid_4.02.csv"))
sy <- read.csv(file.path(S, "data", "atop5_1sy.csv"))
al <- read.csv(file.path(S, "data", "atop5_1a.csv"))
out <- list(); add <- function(k, v) out[[k]] <<- v

## 1. rebuilt d (Path A, date fix) vs shipped d
d1 <- d[order(d$state, d$year), ]; s1 <- sh[order(sh$state, sh$year), ]
add("rebuilt_dim", paste(dim(d1), collapse = "x")); add("shipped_dim", paste(dim(s1), collapse = "x"))
for (v in names(s1)) add(paste0("identical_col_", v), isTRUE(all.equal(d1[[v]], s1[[v]], check.attributes = FALSE)))

## 2. what `disputes` counts (analysis_data_creation.R lines 81-85)
key <- function(s, y) paste(s, y)
cnt <- function(sel) { t <- table(key(m$stateb[sel], m$strtyr[sel])); t }
dk <- key(d$state, d$year)
c_auth <- as.numeric(table(key(m$stateb, m$strtyr)[m$dyad_rolea == 3])[dk]); c_auth[is.na(c_auth)] <- 0
add("disputes_equals_rows_stateb_focal_dyad_rolea3", all(c_auth == d$disputes))
# same rows expressed from the focal state's own side: focal = statea and focal is dyadic INITIATOR
c_init <- as.numeric(table(key(m$statea, m$strtyr)[m$dyad_rolea == 1])[dk]); c_init[is.na(c_init)] <- 0
add("disputes_equals_rows_focal_is_dyadic_initiator", all(c_init == d$disputes))
# focal state is the dyadic TARGET (what the code comment and paper text describe)
c_targ <- as.numeric(table(key(m$statea, m$strtyr)[m$dyad_rolea == 3])[dk]); c_targ[is.na(c_targ)] <- 0
add("disputes_equals_rows_focal_is_dyadic_target", all(c_targ == d$disputes))
add("n_countryyears_disputes_ne_focal_initiator_count", sum(c_init != d$disputes))
add("n_countryyears_disputes_ne_focal_target_count", sum(c_targ != d$disputes))
add("cor_disputes_with_focal_initiator_count", cor(d$disputes, c_init)); add("cor_disputes_with_focal_target_count", cor(d$disputes, c_targ))
k <- paste(m$disno, m$statea, m$stateb, m$year); rr <- m$dyad_rolea[match(paste(m$disno, m$stateb, m$statea, m$year), k)]
sel3 <- m$dyad_rolea == 3
add("counted_rows_whose_mirror_row_has_focal_as_initiator(dyad_rolea==1)", sum(sel3 & rr == 1))
add("counted_rows_whose_mirror_row_has_focal_as_target(dyad_rolea==3, unmirrored coding)", sum(sel3 & rr == 3))
add("share_rows_dyadic_roles_are_1_or_3_only", mean(m$dyad_rolea %in% c(1, 3)))
add("dataset_is_directed_every_dyad_both_orders", all(paste(m$disno, m$statea, m$stateb, m$year) %in% paste(m$disno, m$stateb, m$statea, m$year)))
# example: MID 2 (USA primary initiator vs UK, 1902-1903)
ex <- m[m$disno == 2, c("disno", "statea", "stateb", "rolea", "roleb", "dyad_rolea", "dyad_roleb", "strtyr", "year", "durindx")]
write.csv(ex, file.path(B, "outputs", "code_review_example_mid2.csv"), row.names = FALSE)
add("disputes_USA_1902", d$disputes[d$state == 2 & d$year == 1902]); add("disputes_UK_1902", d$disputes[d$state == 200 & d$year == 1902])
# multi-year counting: rows matched by strtyr include every dyad-year of a dispute
sel <- m$dyad_rolea == 3
add("rows_counted_total", sum(sel)); add("rows_counted_with_durindx_gt1", sum(sel & m$durindx > 1))
c_targ_once <- as.numeric(table(key(m$statea, m$strtyr)[m$dyad_rolea == 3 & m$year == m$strtyr])[dk]); c_targ_once[is.na(c_targ_once)] <- 0
c_auth_once <- as.numeric(table(key(m$stateb, m$strtyr)[m$dyad_rolea == 3 & m$year == m$strtyr])[dk]); c_auth_once[is.na(c_auth_once)] <- 0
add("max_year_mid", max(m$year)); add("max_year_secret_in_d", max(d$year[d$secret > 0]))
add("max_year_any_alliance_in_sy", max(sy$year))

## 3. secret alliance count definitions (analysis_data_creation.R lines 32 and 109 count memberships of pubsecr==2 alliances)
ids <- sy[, grep("^atopid", names(sy))]
long <- data.frame(year = rep(sy$year, ncol(ids)), atopid = unlist(ids)); long <- long[!is.na(long$atopid) & long$atopid > 0, ]
long <- merge(long, al[, c("atopid", "pubsecr", "defense")], by = "atopid")
sec <- unique(long[long$pubsecr %in% 2, c("year", "atopid")]); n_distinct <- table(sec$year)
secd <- unique(long[long$pubsecr %in% 2 & long$defense %in% 1, c("year", "atopid")]); n_distinct_def <- table(secd$year)
d$sec_distinct <- as.numeric(n_distinct[as.character(d$year)]); d$sec_distinct[is.na(d$sec_distinct)] <- 0
d$sec_def_distinct <- as.numeric(n_distinct_def[as.character(d$year)]); d$sec_def_distinct[is.na(d$sec_def_distinct)] <- 0
sd_sum <- tapply(d$secret_def, d$year, sum); d$secret_def_memberships <- as.numeric(sd_sum[as.character(d$year)])
yr <- unique(d[, c("year", "secret_alliances", "sec_distinct")])
add("corr_yearly_memberships_vs_distinct_secret_alliances", cor(yr$secret_alliances, yr$sec_distinct))

## 4. diagnostic correlations (cor.test), not pre-registered
pd <- d$pub_def == 1
ct <- function(lbl, x, y) { h <- cor.test(x, y); data.frame(label = lbl, n = length(x), r = unname(h$estimate), ci_lo = h$conf.int[1], ci_hi = h$conf.int[2], p = h$p.value) }
diag <- rbind(
  ct("M2 as coded (reference)", d$secret_alliances[pd], d$disputes[pd]),
  ct("M2 disputes = focal is dyadic target, rows per dyad-year as coded", d$secret_alliances[pd], c_targ[pd]),
  ct("M2 disputes = focal is dyadic target, first dyad-year only", d$secret_alliances[pd], c_targ_once[pd]),
  ct("M2 as coded but first dyad-year only", d$secret_alliances[pd], c_auth_once[pd]),
  ct("M2 x = distinct secret alliances per year", d$sec_distinct[pd], d$disputes[pd]),
  ct("M1 as coded (reference)", d$secret_alliances, d$disputes),
  ct("M1 disputes = focal is dyadic target", d$secret_alliances, c_targ),
  ct("M1 x = defensive secret alliance memberships per year (paper text)", d$secret_def_memberships, d$disputes),
  ct("M1 x = distinct defensive secret alliances per year", d$sec_def_distinct, d$disputes))
yt <- aggregate(cbind(disputes = d$disputes) ~ year, d, sum); yt <- merge(yt, unique(d[, c("year", "secret_alliances")]))
diag <- rbind(diag, ct("M1 at system-year level (yearly sums, paper text 'sum the total number of MIDs in a given year')", yt$secret_alliances, yt$disputes))
write.csv(diag, file.path(B, "outputs", "code_review_diagnostic_correlations.csv"), row.names = FALSE)
facts <- data.frame(key = names(out), value = sapply(out, function(v) paste(v, collapse = ";")))
write.csv(facts, file.path(B, "outputs", "code_review_facts.csv"), row.names = FALSE)
print(facts, row.names = FALSE); print(diag, digits = 6, row.names = FALSE)
