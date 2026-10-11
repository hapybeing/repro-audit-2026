## [ENV FIX] per-run library, working directory, model save folder (agent A)
.libPaths(c("/workspace/audit_runs/24_U9CKK6/A/rlib", .libPaths()))
setwd("/workspace/audit_runs/24_U9CKK6/A/run")
cat("START", format(Sys.time()), "\n")
####################ISSUE SALIENCE EFFECTS ############
library(lme4)
library(texreg)
library(sjPlot)
library(sjstats)
library(fixest)
library(ggplot2)
library(ggeffects)
library(zoo)
library(skimr)
library(tidyverse)
load("Data/EP_debates_07062023.Rdata")
## [ENV FIX F1] blank unused speech-text columns 4 and 6 (positions kept)
EP_debates$text <- NA_character_; EP_debates$ori_text <- NA_character_

##### LOAD DATA FROM RAUH AND DE WILDE

load("Data/RdW_salience.Rdata")

### PREP RdW Data for Merging
padpanel$eu.w[is.na(padpanel$eu.w)] <- 0
months_sal <- padpanel %>% group_by(country, month) %>% summarise(EU_sal= mean(eu.w))

months_sal$year_mon <- as.yearmon(months_sal$month)
months_sal <- mutate(months_sal,
                      country = case_when(country == "DE" ~ "Germany",
                                          country == "ES" ~ "Spain",
                                          country == "NL" ~ "Netherlands",
                                          country == "UK" ~ "United Kingdom"))
months_sal$month <- NULL

EP_debates$year_mon <- as.yearmon(EP_debates$date)

EP_debates_sal <- left_join(EP_debates, months_sal, by = c("country", "year_mon"))



EP_debates_sal$radical <- abs(EP_debates_sal$lrgen - 5)
range(EP_debates_sal$radical, na.rm = TRUE)

centFUN <- function(x) {
  x - mean(x, na.rm = TRUE)
}

result <- apply(EP_debates_sal[,c(22:24, 27:71, 73:75, 77:107,117:118)], MARGIN = 2, FUN = centFUN)
result <- as.data.frame(result)


EP_eurobar_cent <- cbind(EP_debates_sal[,-c(22:24, 27:71, 73:75, 77:107,117:118)], result)

rm(list=setdiff(ls(), "EP_eurobar_cent"))

EP_eurobar_cent$embed_dict_scale <- scale(EP_eurobar_cent$embed_dict)
EP_eurobar_cent$aut_dict_scale <- scale(EP_eurobar_cent$aut_dict)
EP_eurobar_cent$immi_dict_scale <- scale(EP_eurobar_cent$immi_dict)
EP_eurobar_cent$int_dict_scale <- scale(EP_eurobar_cent$int_dict)
EP_eurobar_cent$lrgen_scale <- scale(EP_eurobar_cent$lrgen)
EP_eurobar_cent$radical_scale <- scale(EP_eurobar_cent$radical)

EP_eurobar_cent$aut_sal <- scale(EP_eurobar_cent$mip_n_govdebt_ipol)
EP_eurobar_cent$immi_sal <- scale(EP_eurobar_cent$mip_n_immigration_ipol)
EP_eurobar_cent$image_ipol <- scale(EP_eurobar_cent$image_ipol)
EP_eurobar_cent$EU_sal <- scale(EP_eurobar_cent$EU_sal)

##### AUSTERITY SALIENCE (EUROBAROMETER)

## ---- agent A robustness prep: save estimation samples ----
w <- warnings(); cat("N_WARNINGS", length(w), "\n"); print(head(w, 5)); print(table(sub("\x27.*", "", names(w))))
suppressMessages(library(lme4))
m <- readRDS("/workspace/audit_runs/24_U9CKK6/A/models/AUT_sal_model.rds")
mf <- model.frame(m); idx <- match(rownames(mf), rownames(EP_eurobar_cent))
stopifnot(!anyNA(idx), nrow(mf) == nobs(m))
vars <- intersect(all.vars(formula(m)), names(EP_eurobar_cent))
smp <- EP_eurobar_cent[idx, vars]
saveRDS(list(data = smp, formula = formula(m), rows = idx), "/workspace/audit_runs/24_U9CKK6/A/models/sample_AUT_sal_model.rds")
cat("SAMPLE AUT_sal_model", nrow(smp), ncol(smp), "\n")
rm(m, mf, smp); invisible(gc())
m <- readRDS("/workspace/audit_runs/24_U9CKK6/A/models/EU_sal_model.rds")
mf <- model.frame(m); idx <- match(rownames(mf), rownames(EP_eurobar_cent))
stopifnot(!anyNA(idx), nrow(mf) == nobs(m))
vars <- intersect(all.vars(formula(m)), names(EP_eurobar_cent))
smp <- EP_eurobar_cent[idx, vars]
saveRDS(list(data = smp, formula = formula(m), rows = idx), "/workspace/audit_runs/24_U9CKK6/A/models/sample_EU_sal_model.rds")
cat("SAMPLE EU_sal_model", nrow(smp), ncol(smp), "\n")
rm(m, mf, smp); invisible(gc())
