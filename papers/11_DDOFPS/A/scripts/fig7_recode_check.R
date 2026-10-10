# Check of script lines 245-251: which values of resultado exist in teste_4 and what eleito becomes.
args <- commandArgs(trailingOnly = TRUE); rundir <- args[1]; outdir <- args[2]
load(file.path(rundir, "session_after_script.RData"))
tb <- as.data.frame(table(resultado = teste_4$resultado, eleito = teste_4$eleito, useNA = "ifany"))
tb <- tb[tb$Freq > 0, ]
write.csv(tb, file.path(outdir, "fig7_recode_check.csv"), row.names = FALSE)
print(tb)
