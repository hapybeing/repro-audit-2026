OUT <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/19_KH0SQ2/B/outputs"
# main_objs.rds is written by evaluating lines 1-364 of the deposited main_text_figs_JEPP_FINAL.R in run_main/ (res1 at l.325 is overwritten at l.639 in a whole run)
o <- readRDS("/workspace/audit_runs/19_KH0SQ2/B/main_objs.rds"); a <- readRDS(file.path(OUT, "S1_S10_models.rds"))
d <- data.frame(object=c("res1 (UK, l.325)","res1b (FR, l.363)"), term="TreatmentQuota",
  estimate=c(coef(o$res1)["TreatmentQuota"], coef(o$res1b)["TreatmentQuota"]),
  se=c(summary(o$res1)$coefficients["TreatmentQuota",2], summary(o$res1b)$coefficients["TreatmentQuota",2]),
  nobs=c(nobs(o$res1), nobs(o$res1b)),
  equal_to_appendix=c(isTRUE(all.equal(coef(o$res1)["TreatmentQuota"], coef(a$res1)["TreatmentQuota"])),
                      isTRUE(all.equal(coef(o$res1b)["TreatmentQuota"], coef(a$res4)["TreatmentQuota"]))))
write.csv(d, file.path(OUT, "main_text_crosscheck.csv"), row.names=FALSE); print(d)
tc <- as.data.frame(table(o$all$country)); names(tc) <- c("country","n")
write.csv(rbind(tc, data.frame(country="total", n=sum(tc$n))), file.path(OUT, "descriptive_counts.csv"), row.names=FALSE); print(tc)
