# Summarise R_a bootstrap (outputs/ra_boot.csv) -> outputs/ra_summary.csv; also R_b z diagnostics -> outputs/rb_zmax.csv
source("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A/scripts/robust_common.R")
bt <- fread(file.path(PDIR,"outputs","ra_boot.csv"))
stopifnot(!anyDuplicated(bt[, .(k, outcome)]))
base <- fread(file.path(PDIR,"outputs","robust_bc.csv"))[check=="baseline"]
s <- bt[, { bb <- b[ok]; est <- base[outcome==.BY$outcome, b]
  .(K=max(k), n_ok=sum(ok), n_failed=sum(!ok), estimate=est, boot_se=sd(bb), ci_l=quantile(bb,.025,names=FALSE), ci_u=quantile(bb,.975,names=FALSE),
    p=min(1, 2*mean(if (est<0) bb>=0 else bb<=0))) }, by=outcome]
s[, paper_value := paper[outcome]]; s[, same_dir_sig := sign(estimate)==sign(paper_value) & (ci_l>0 | ci_u<0)]
fwrite(s, file.path(PDIR,"outputs","ra_summary.csv")); print(s)
z <- rbindlist(lapply(names(outs), function(nm){ D <- est_sample(outs[[nm]]); zz <- (D$y-mean(D$y))/sd(D$y); data.table(outcome=nm, n=nrow(D), max_abs_z=max(abs(zz)), n_abs_z_gt3=sum(abs(zz)>3)) }))
fwrite(z, file.path(PDIR,"outputs","rb_zmax.csv")); print(z)
