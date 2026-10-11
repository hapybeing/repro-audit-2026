# R_b (|z|>3 outlier exclusion on outcome) and R_c (SE clustered by DIV_ARMY). Writes outputs/robust_bc.csv
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A/scripts/robust_common.R")
res <- list()
for (nm in names(outs)) {
  D <- est_sample(outs[[nm]]); n0 <- nrow(D)
  m0 <- fit_fe(D); r0 <- nkvd_row(m0)
  res[[length(res)+1]] <- data.table(check="baseline", outcome=nm, n=n0, dropped=0, b=r0[1], se=r0[2], p=r0[4], clusters=NA_integer_)
  # R_b
  z <- (D$y - mean(D$y)) / sd(D$y); Db <- D[abs(z) <= 3]
  mb <- fit_fe(Db); rb <- nkvd_row(mb)
  res[[length(res)+1]] <- data.table(check="R_b", outcome=nm, n=nrow(Db), dropped=n0-nrow(Db), b=rb[1], se=rb[2], p=rb[4], clusters=NA_integer_)
  # R_c
  fc <- Formula::Formula(y ~  log(NKVD_OO+1) + scale(AGE_1941) + scale(soldiers_dist) + scale(RUS_100) + scale(URBAN_PCT) + scale(POP_DENSITY) + scale(M_10km_ADM3) | DIV_ARMY + TID + bxid | 0 | DIV_ARMY)
  mc <- fit_fe(D, fc); rc <- nkvd_row(mc)
  res[[length(res)+1]] <- data.table(check="R_c", outcome=nm, n=n0, dropped=0, b=rc[1], se=rc[2], p=rc[4], clusters=length(unique(D$DIV_ARMY)))
  message(nm, " done")
}
out <- rbindlist(res); out[, `:=`(l=b-1.96*se, u=b+1.96*se)]
out[, paper_value := paper[outcome]]
out[, same_dir_sig := sign(b)==sign(paper_value) & (l>0 | u<0)]
fwrite(out, file.path(PDIR,"outputs","robust_bc.csv")); print(out)
