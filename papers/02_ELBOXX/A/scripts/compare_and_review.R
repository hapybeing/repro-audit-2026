# Compare rebuilt d (Path A) with shipped d (Path B), and compute data facts used in code review.
# Usage: Rscript compare_and_review.R <objs_dir> <outdir> <raw_data_dir>
args <- commandArgs(trailingOnly = TRUE); o <- args[1]; out <- args[2]; raw <- args[3]
sh <- readRDS(file.path(o, "d_shipped.rds"))
fa <- readRDS(file.path(o, "d_pathA_faketime20250506.rds"))
cl <- readRDS(file.path(o, "d_pathA_clock2026.rds"))
key <- function(x) x[order(x$state, x$year), ]
cmp <- function(a, b, lab) { a <- key(a); b <- key(b); rownames(a) <- rownames(b) <- NULL
  data.frame(comparison = lab, nrow_a = nrow(a), nrow_b = nrow(b), same_colnames = identical(sort(names(a)), sort(names(b))),
    column = names(b), identical_values = sapply(names(b), function(v) if (nrow(a) == nrow(b) && v %in% names(a)) isTRUE(all.equal(a[[v]], b[[v]], check.attributes = FALSE)) else NA)) }
res <- rbind(cmp(fa, sh, "pathA_faketime20250506_vs_shipped"), cmp(cl, sh, "pathA_clock2026_vs_shipped"))
write.csv(res, file.path(out, "compare_d_rebuilt_vs_shipped.csv"), row.names = FALSE)
extra <- cl[!(paste(cl$state, cl$year) %in% paste(sh$state, sh$year)), ]
d <- fa
facts <- list(
  clock2026_extra_rows = nrow(extra), clock2026_extra_years = paste(unique(extra$year), collapse = ","),
  clock2026_extra_rows_pub_def_eq1 = sum(extra$pub_def == 1), clock2026_extra_rows_disputes_sum = sum(extra$disputes),
  rows_pub_def_eq1 = sum(d$pub_def == 1), rows_pub_def_ge1 = sum(d$pub_def >= 1), max_pub_def = max(d$pub_def),
  max_year_with_disputes_gt0 = max(d$year[d$disputes > 0]), max_year_with_secret_gt0 = max(d$year[d$secret > 0]),
  max_year_secret_alliances_gt0 = max(d$year[d$secret_alliances > 0]),
  pubdef1_rows_year_gt2014 = sum(d$pub_def == 1 & d$year > 2014),
  cor_M1_using_secret_def_sum = NA)
# yearly sum of secret_def (paper text says "defensive secret alliances") for a note, not a target
sd_year <- aggregate(secret_def ~ year, d, sum); names(sd_year)[2] <- "secret_def_year"
dd <- merge(d, sd_year, by = "year")
facts$cor_M1_using_secret_def_sum <- unname(cor(dd$secret_def_year, dd$disputes))
# system-year level version of M1 (paper text "sum the total number of MIDs in a given year")
sy <- aggregate(cbind(disputes, secret) ~ year, d, sum)
facts$cor_M1_system_year_level <- cor(sy$secret, sy$disputes); facts$n_system_years <- nrow(sy)
# membership vs distinct alliances: count distinct secret alliances active per year from raw ATOP
a <- read.csv(file.path(raw, "atop5_1a.csv")); s <- read.csv(file.path(raw, "atop5_1sy.csv"))
ids <- s[, grep("^atopid", names(s))]
long <- data.frame(year = rep(s$year, ncol(ids)), atopid = as.vector(as.matrix(ids)))
long <- unique(long[!is.na(long$atopid) & long$atopid > 0, ])
long$secret <- a$pubsecr[match(long$atopid, a$atopid)] == 2
dist <- aggregate(secret ~ year, long, sum); names(dist)[2] <- "distinct_secret"
chk <- merge(unique(d[, c("year", "secret_alliances")]), dist, by = "year")
facts$years_where_secret_alliances_ne_distinct_count <- sum(chk$secret_alliances != chk$distinct_secret)
facts$max_ratio_memberships_to_distinct <- max(chk$secret_alliances[chk$distinct_secret > 0] / chk$distinct_secret[chk$distinct_secret > 0])
pd <- merge(d[d$pub_def == 1, ], dist, by = "year", all.x = TRUE); pd$distinct_secret[is.na(pd$distinct_secret)] <- 0
facts$cor_M2_using_distinct_secret_count <- cor(pd$distinct_secret, pd$disputes)
m <- read.csv(file.path(raw, "dyadic_mid_4.02.csv"))
facts$mid402_max_strtyr <- max(m$strtyr); facts$mid402_dyad_rolea_values <- paste(sort(unique(m$dyad_rolea)), collapse = ",")
facts$mid402_rows_rolea3 <- sum(m$dyad_rolea == 3)
facts$atop_sy_rows <- nrow(s); facts$atop_sy_years <- paste(range(s$year), collapse = "-")
facts$atop_a_pubsecr_values <- paste(names(table(a$pubsecr, useNA = "ifany")), table(a$pubsecr, useNA = "ifany"), sep = ":", collapse = ",")
facts$atop_a_defense_NA <- sum(is.na(a$defense))
# rows of sy that fail to merge with peacesciencer state-years (lost by all.y=TRUE)
facts$atop_sy_rows_in_d <- sum(paste(s$state, s$year) %in% paste(d$state, d$year))
write.csv(data.frame(fact = names(facts), value = sapply(facts, as.character)), file.path(out, "code_review_facts.csv"), row.names = FALSE)
print(res[!res$identical_values %in% TRUE, ]); print(data.frame(value = unlist(facts)))
