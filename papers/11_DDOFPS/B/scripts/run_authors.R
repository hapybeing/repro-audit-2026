# Agent B wrapper: run the deposited script unmodified, top to bottom, in RUNDIR.
# Usage: Rscript run_authors.R RUNDIR OUTRDATA
args <- commandArgs(trailingOnly = TRUE)
setwd(args[1])
pdf(file.path(args[1], "Rplots.pdf"))
source("Análise dos Dados Nota Técnica.R", encoding = "latin1", echo = TRUE, max.deparse.length = 300, print.eval = TRUE)
dev.off()
save(df, bd_doxa_programas, bd_doxa_candidatos, test, test2, partidos_sel, teste_1, teste_2, sp, file = args[2])
cat("RUN_COMPLETED\n")
