## Agent B: extract target quantities from the authors' saved estimates.
## Run with working directory = RUNDIR (replication/). Writes to OUT dir given as arg 1.
args <- commandArgs(trailingOnly = TRUE)
out_dir <- args[1]
load("output/Estimates-Main.Rdata")
rows <- list(
  list(id="T1", country="UK", el=2, X1='2:I(T_who == "WHO")TRUE'),
  list(id="T2", country="UK", el=2, X1='2:I(T_who == "WHO.Ratified")TRUE'),
  list(id="T3", country="US", el=1, X1='2:I(T_who == "WHO")TRUE'),
  list(id="T4", country="US", el=1, X1='2:I(T_who == "WHO.Ratified")TRUE'))
res <- do.call(rbind, lapply(rows, function(r) {
  co <- store_estimates[[r$el]]$Coefficients
  x <- co[as.character(co$X1) == r$X1 & co$Subset == 1, ]
  stopifnot(nrow(x) == 1, x$Data == r$el)
  data.frame(id=r$id, country=r$country, X1=r$X1, Mean=x$Mean, SD=x$SD, pvalue=x$pvalue, N=x$N)
}))
## T5/T6: N of main-model rows
nuk <- unique(store_estimates[[2]]$Coefficients$N[store_estimates[[2]]$Coefficients$Subset == 1])
nus <- unique(store_estimates[[1]]$Coefficients$N[store_estimates[[1]]$Coefficients$Subset == 1])
stopifnot(length(nuk) == 1, length(nus) == 1)
res <- rbind(res, data.frame(id=c("T5","T6"), country=c("UK","US"), X1="N", Mean=c(nuk, nus), SD=NA, pvalue=NA, N=c(nuk, nus)))
write.csv(res, file.path(out_dir, "targets_extracted.csv"), row.names=FALSE)
## Full main-model coefficient tables for context
for (el in 1:2) {
  co <- store_estimates[[el]]$Coefficients
  write.csv(co[co$Subset == 1, ], file.path(out_dir, paste0("main_model_coefficients_", c("US","UK")[el], ".csv")), row.names=FALSE)
}
print(res, digits=6)
