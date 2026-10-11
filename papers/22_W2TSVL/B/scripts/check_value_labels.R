# Code review aid (agent B): value labels and frequencies of the variables the authors recode.
library(haven)
d <- read_dta("/workspace/audit_runs/22_W2TSVL/B/run/OA23 Base UT-TEC.dta")
for (v in c("TratUT2","UT2_1","UT2_2","d1","d3","d12","PartyID","EdadRec","Entidad")) {
  cat("\n==", v, ":", attr(d[[v]], "label"), "\n"); l <- attr(d[[v]], "labels"); if (!is.null(l)) print(l)
  print(table(as.numeric(d[[v]]), useNA = "ifany")) }
cat("\nEdadRec by age range:\n"); print(tapply(as.numeric(d$d2), as.numeric(d$EdadRec), range))
