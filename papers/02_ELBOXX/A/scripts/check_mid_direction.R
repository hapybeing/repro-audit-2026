# Code review check: which side of the dyadic MID does analysis_data_creation.R lines 81-82 count?
# Usage: Rscript check_mid_direction.R <raw_data_dir> <d.rds> <outdir>
args <- commandArgs(trailingOnly = TRUE)
m <- read.csv(file.path(args[1], "dyadic_mid_4.02.csv")); d <- readRDS(args[2]); out <- args[3]
f <- list()
f$rows <- nrow(m)
key_ab <- paste(m$disno, m$statea, m$stateb); key_ba <- paste(m$disno, m$stateb, m$statea)
f$share_rows_with_mirror_row <- mean(key_ab %in% key_ba)
f$rows_statea_lt_stateb <- sum(m$statea < m$stateb)
f$table_dyad_rolea_by_dyad_roleb <- paste(capture.output(print(table(rolea = m$dyad_rolea, roleb = m$dyad_roleb))), collapse = " | ")
sel <- m$dyad_rolea == 3
f$code_selection_rows <- sum(sel)
f$code_selection_dyad_roleb_values <- paste(names(table(m$dyad_roleb[sel])), table(m$dyad_roleb[sel]), sep = ":", collapse = ",")
f$code_selection_sideab_values <- paste(names(table(m$sideab[sel])), table(m$sideab[sel]), sep = ":", collapse = ",")
# example: first rows of a well-known dyad
ex <- m[m$disno == m$disno[1], c("disno", "statea", "stateb", "dyad_rolea", "dyad_roleb", "sideaa", "sideab", "strtyr")]
f$example_first_dispute <- paste(capture.output(print(ex)), collapse = " | ")
# alternative counts per country-year (for information only, NOT a pre-registered check)
cnt <- function(s, y, rows) sum(rows$s == s & rows$y == y)
code_rows <- data.frame(s = m$stateb[sel], y = m$strtyr[sel])                          # as in the code
target_rows <- data.frame(s = m$statea[m$dyad_rolea == 3], y = m$strtyr[m$dyad_rolea == 3])  # state A is target
tab_code <- table(paste(code_rows$s, code_rows$y)); tab_tgt <- table(paste(target_rows$s, target_rows$y))
k <- paste(d$state, d$year)
d$disp_code_recomputed <- as.numeric(ifelse(k %in% names(tab_code), tab_code[k], 0))
d$disp_targeted <- as.numeric(ifelse(k %in% names(tab_tgt), tab_tgt[k], 0))
f$recomputed_code_count_identical_to_d_disputes <- isTRUE(all.equal(d$disp_code_recomputed, d$disputes))
pd <- d[d$pub_def == 1, ]
t2 <- cor.test(pd$secret_alliances, pd$disp_targeted); t1 <- cor.test(d$secret_alliances, d$disp_targeted)
f$info_M2_with_country_as_target_r <- unname(t2$estimate); f$info_M2_with_country_as_target_ci <- paste(signif(t2$conf.int, 6), collapse = ";")
f$info_M2_with_country_as_target_p <- t2$p.value
f$info_M1_with_country_as_target_r <- unname(t1$estimate); f$info_M1_with_country_as_target_p <- t1$p.value
f$cor_code_disputes_vs_targeted_countryyear <- cor(d$disputes, d$disp_targeted)
write.csv(data.frame(fact = names(f), value = sapply(f, as.character)), file.path(out, "mid_direction_check.csv"), row.names = FALSE)
print(data.frame(value = unlist(f)))
