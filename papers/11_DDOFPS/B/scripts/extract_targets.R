# Agent B: extract pre-registered target quantities from the saved session of the authors' run.
# Usage: Rscript extract_targets.R SESSION.RData LABEL OUTDIR
suppressPackageStartupMessages({library(ggplot2); library(ggpubr); library(dplyr)})
a <- commandArgs(trailingOnly = TRUE); load(a[1]); lab <- a[2]; od <- a[3]
rows <- list(); add <- function(q, v) rows[[length(rows) + 1]] <<- data.frame(file_version = lab, quantity = q, value = format(v, digits = 15), stringsAsFactors = FALSE)
# T1
add("T1_sum_df_programas", sum(df$programas)); add("T1_nrow_bd_doxa_programas", nrow(bd_doxa_programas))
for (i in seq_len(nrow(df))) add(paste0("T1_programas_", df$ano[i]), df$programas[i])
# T4
tb <- table(bd_doxa_programas$ano, bd_doxa_programas$APE4)
for (y in rownames(tb)) for (k in colnames(tb)) add(paste0("tab_ano_APE4_", y, "_", k), tb[y, k])
add("T4_obs_2018_Sim", tb["2018", "Sim"]); add("T4_expected_2018_Sim", test$expected["2018", "Sim"])
add("T4_chisq_statistic", unname(test$statistic)); add("T4_chisq_df", unname(test$parameter)); add("T4_chisq_p", test$p.value)
add("APE4_share_overall", sum(tb[, "Sim"]) / sum(tb)); add("APE4_share_2018", tb["2018", "Sim"] / sum(tb["2018", ]))
# T5, T6
tb2 <- table(partidos_sel$numpartido, partidos_sel$APE3)
for (y in rownames(tb2)) for (k in colnames(tb2)) { add(paste0("tab_party_APE3_obs_", y, "_", k), tb2[y, k]); add(paste0("tab_party_APE3_exp_", y, "_", k), test2$expected[y, k]) }
add("T5_obs_13_Sim", tb2["13", "Sim"]); add("T6_expected_13_Sim", test2$expected["13", "Sim"])
add("test2_chisq_statistic", unname(test2$statistic)); add("test2_chisq_p", test2$p.value)
add("parties_in_partidos_sel", paste(sort(unique(partidos_sel$numpartido)), collapse = ";"))
add("n_rows_party45_in_bd", sum(as.character(bd_doxa_programas$numpartido) == "45", na.rm = TRUE))
# T2, T3 (only from candidates file; identical for v1/v2 runs)
p <- sp + stat_cor(aes(color = el)); ld <- layer_data(p, i = length(p$layers))
lv <- levels(teste_2$el)
for (j in seq_len(nrow(ld))) { yr <- lv[ld$group[j]]; add(paste0("statcor_r_", yr), ld$r[j]); add(paste0("statcor_p_", yr), ld$p[j]) }
for (yr in lv) { s <- teste_2[teste_2$el == yr, ]; ct <- cor.test(s$HGPE_total, s$VR_RECEITA_total)
  add(paste0("cortest_r_", yr), unname(ct$estimate)); add(paste0("cortest_p_", yr), ct$p.value); add(paste0("n_teste_2_", yr), nrow(s)) }
add("nrow_teste_2", nrow(teste_2)); add("nrow_teste_1", nrow(teste_1))
out <- do.call(rbind, rows)
write.csv(out, file.path(od, paste0("targets_extracted_", lab, ".csv")), row.names = FALSE)
print(out)
