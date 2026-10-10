#!/bin/bash
# Runs the three target scripts unmodified, each in a fresh R session, from the R project folder (copy at $RUN/work).
RUN=/workspace/audit_runs/15_1BBC4E/B
OUT=/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/15_1BBC4E/B/outputs
export R_LIBS_USER=$RUN/rlib
cd $RUN/work
Rscript -e "pdf('$OUT/figures_comparison.pdf'); source('Scripts/Comparing Indices/Comparison.R', echo=TRUE, max.deparse.length=Inf); dev.off(); saveRDS(corr.ea, '$OUT/corr_ea.rds'); write.csv(as.data.frame(corr.ea), '$OUT/corr_ea_fullprec.csv', row.names=FALSE)" > $OUT/console_comparison.log 2>&1; echo "comparison exit $?"
Rscript -e "pdf('$OUT/figures_share.pdf'); source('Scripts/Comparing Indices/Share_Common_Sample.R', echo=TRUE, max.deparse.length=Inf); dev.off(); writeLines(as.character(nrow(ead)), '$OUT/share_nrow_ead.txt')" > $OUT/console_share.log 2>&1; echo "share exit $?"
Rscript -e "pdf('$OUT/figures_agreement.pdf'); source('Scripts/Comparing Indices/Agreement across all.R', echo=TRUE, max.deparse.length=Inf); dev.off(); write.csv(ead2, '$OUT/agreement_ead2_tally.csv', row.names=FALSE)" > $OUT/console_agreement.log 2>&1; echo "agreement exit $?"
