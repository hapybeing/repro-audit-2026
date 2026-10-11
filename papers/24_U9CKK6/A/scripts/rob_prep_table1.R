## [ENV FIX] per-run library, working directory, model save folder (agent A)
.libPaths(c("/workspace/audit_runs/24_U9CKK6/A/rlib", .libPaths()))
setwd("/workspace/audit_runs/24_U9CKK6/A/run")
cat("START", format(Sys.time()), "\n")
################################################################################
################################################################################
################################################################################
############### Analysis Script 1 ##############################################
############### Null Models, Anti-Establishment Rhetoric########################
############### Electoral Cycle Models##########################################
################################################################################
load("Data/EP_debates_07062023.Rdata")
## [ENV FIX F1] blank unused speech-text columns 4 and 6 (positions kept)
EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_
library(lme4)
library(texreg)
library(sjPlot)
library(sjstats)
library(fixest)
library(ggplot2)

#####

levels(EP_debates$EU_party)
levels(EP_debates$EU_party) <- c("NGL", "EFD/EFDD", "ECR",
                                 "EDD", "ALDE",  "EPP",
                                 "Greens","S&D", "ID",
                                 "No Group", "UEN", "EFD/EFDD", 
                                 "NGL", "Greens", "No Group")
levels(EP_debates$EU_party)

### BEGIN BY CENTERING AND SCALING EVERYTHING

EP_debates$radical <- abs(EP_debates$lrgen - 5)
range(EP_debates$radical, na.rm = TRUE)

centFUN <- function(x) {
  x - mean(x, na.rm = TRUE)
}

result <- apply(EP_debates[,c(22:24, 27:71, 73:75, 77:107,117:118)], MARGIN = 2, FUN = centFUN)
result <- as.data.frame(result)


EP_eurobar_cent <- cbind(EP_debates[,-c(22:24, 27:71, 73:75, 77:107,117:118)], result)

rm(list=setdiff(ls(), "EP_eurobar_cent"))

EP_eurobar_cent$embed_dict_scale <- scale(EP_eurobar_cent$embed_dict)
EP_eurobar_cent$aut_dict_scale <- scale(EP_eurobar_cent$aut_dict)
EP_eurobar_cent$immi_dict_scale <- scale(EP_eurobar_cent$immi_dict)
EP_eurobar_cent$int_dict_scale <- scale(EP_eurobar_cent$int_dict)
EP_eurobar_cent$lrgen_scale <- scale(EP_eurobar_cent$lrgen)
EP_eurobar_cent$radical_scale <- scale(EP_eurobar_cent$radical)

EP_eurobar_cent$aut_sal <- scale(EP_eurobar_cent$mip_n_govdebt_ipol)
EP_eurobar_cent$immi_sal <- scale(EP_eurobar_cent$mip_n_immigration_ipol)
EP_eurobar_cent$eum_ipol <- scale(EP_eurobar_cent$eum_ipol)

############### ANTI-ESTABLISHMENT CYCLE MODEL #################################

### For Plotting Only
EP_eurobar_cent$chall_fact <- as.factor(ifelse(EP_eurobar_cent$challenge == 1, "Challenger", "Mainstream"))
str(EP_eurobar_cent$chall_fact)
range(EP_eurobar_cent$days_from_EP)

EP_eurobar_cent$days_to_EP <- scale(EP_eurobar_cent$days_from_EP)# Make them more intuitive as of reviewer request
EP_eurobar_cent$days_to_nat <- scale(EP_eurobar_cent$days_from_nat)

## ---- agent A robustness prep: save estimation samples ----
w <- warnings(); cat("N_WARNINGS", length(w), "\n"); print(head(w, 5)); print(table(sub("\x27.*", "", names(w))))
suppressMessages(library(lme4))
m <- readRDS("/workspace/audit_runs/24_U9CKK6/A/models/cycle_AE_fit2.rds")
mf <- model.frame(m); idx <- match(rownames(mf), rownames(EP_eurobar_cent))
stopifnot(!anyNA(idx), nrow(mf) == nobs(m))
vars <- intersect(all.vars(formula(m)), names(EP_eurobar_cent))
smp <- EP_eurobar_cent[idx, vars]
saveRDS(list(data = smp, formula = formula(m), rows = idx), "/workspace/audit_runs/24_U9CKK6/A/models/sample_cycle_AE_fit2.rds")
cat("SAMPLE cycle_AE_fit2", nrow(smp), ncol(smp), "\n")
rm(m, mf, smp); invisible(gc())
