# Reads the session saved after the authors' script ran and writes the pre-registered target
# quantities to OUTDIR/targets_extracted_<label>.csv (long format: key, value).
# Args: RUNDIR OUTDIR LABEL
suppressPackageStartupMessages({library(tidyverse); library(ggpubr)})
args <- commandArgs(trailingOnly = TRUE)
rundir <- args[1]; outdir <- args[2]; label <- args[3]
load(file.path(rundir, "session_after_script.RData"))
out <- list()
add <- function(k, v) out[[length(out) + 1]] <<- data.frame(key = k, value = as.character(v))

# T1
add("T1_sum_df_programas", sum(df$programas))
add("T1_nrow_bd_doxa_programas", nrow(bd_doxa_programas))
for (i in seq_len(nrow(df))) add(paste0("programs_by_year_", df$ano[i]), df$programas[i])
add("class_numpartido", class(bd_doxa_programas$numpartido)[1])
add("class_ano", class(bd_doxa_programas$ano)[1])

# T2, T3: stat_cor layer of line 219
p219 <- sp + stat_cor(aes(color = el))
ld <- ggplot2::layer_data(p219, i = length(p219$layers))
lev <- levels(teste_2$el)
for (j in seq_len(nrow(ld))) {
  yr <- lev[ld$group[j]]
  add(paste0("statcor_r_", yr), ld$r[j])
  add(paste0("statcor_p_", yr), ld$p[j])
  add(paste0("statcor_n_group_", yr), sum(teste_2$el == yr))
}
for (yr in lev) {
  d <- teste_2[teste_2$el == yr, ]
  ct <- cor.test(d$HGPE_total, d$VR_RECEITA_total)
  add(paste0("cortest_r_", yr), unname(ct$estimate))
  add(paste0("cortest_p_", yr), ct$p.value)
  add(paste0("cortest_n_", yr), nrow(d))
}
add("nrow_teste_2", nrow(teste_2))
add("nrow_bd_doxa_candidatos", nrow(bd_doxa_candidatos))

# T4
tab4 <- table(bd_doxa_programas$ano, bd_doxa_programas$APE4)
for (r in rownames(tab4)) for (c in colnames(tab4)) add(paste0("tab_ano_APE4_", r, "_", c), tab4[r, c])
add("T4_obs_2018_Sim", tab4["2018", "Sim"])
add("T4_exp_2018_Sim", test$expected["2018", "Sim"])
add("chisq_ano_APE4_stat", unname(test$statistic))
add("chisq_ano_APE4_df", unname(test$parameter))
add("chisq_ano_APE4_p", test$p.value)
add("APE4_share_2018", tab4["2018", "Sim"] / sum(tab4["2018", ]))
add("APE4_share_all", sum(tab4[, "Sim"]) / sum(tab4))

# T5, T6
tab5 <- table(partidos_sel$numpartido, partidos_sel$APE3)
for (r in rownames(tab5)) for (c in colnames(tab5)) add(paste0("tab_party_APE3_", r, "_", c), tab5[r, c])
add("T5_obs_13_Sim", tab5["13", "Sim"])
add("T6_exp_13_Sim", test2$expected["13", "Sim"])
add("obs_15_Sim", tab5["15", "Sim"])
add("exp_15_Sim", test2$expected["15", "Sim"])
add("chisq_party_APE3_stat", unname(test2$statistic))
add("chisq_party_APE3_df", unname(test2$parameter))
add("chisq_party_APE3_p", test2$p.value)
add("party_rows_in_partidos_sel", paste(rownames(tab5), collapse = ";"))
add("party45_rows_in_full_data", sum(as.character(bd_doxa_programas$numpartido) == "45", na.rm = TRUE))
add("nrow_partidos_sel", nrow(partidos_sel))

res <- bind_rows(out)
write.csv(res, file.path(outdir, paste0("targets_extracted_", label, ".csv")), row.names = FALSE)
print(res, digits = 15)
