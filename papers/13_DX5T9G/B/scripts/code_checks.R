## Agent B code-review checks (run from RUNDIR). Writes outputs/code_checks.txt via sink.
args <- commandArgs(trailingOnly = TRUE); out <- args[1]
sink(file.path(out, "code_checks.txt"), split=TRUE)
suppressMessages({library(plyr); library(foreign); library(arm); library(mvtnorm)})
cat("Locale LC_COLLATE:", Sys.getlocale("LC_COLLATE"), "\n\n")

## Check 1: BES LR type after 01 lines 137-141 (file 01_Prepare data.R)
BES <- read.dta("data/BES/bes_f2f_2017_v1.5.dta")
BES <- BES[, c("wt_demog", "Age", "y09", "e01")]
BES$LR <- mapvalues(x=BES$e01, from=c("Not stated", "Refused", "Don`t know", "0 Left", 1:9, "10 Right"),
                    to=c(rep(-99, 3), (0:10 - 0) / (10-0)))
cat("Check 1: class of BES$LR after mapvalues:", class(BES$LR), "\n")
dummy <- data.frame(w=1, LR=0.5, Age=30, Gender_male=1)
BES2 <- na.omit(data.frame(w=BES$wt_demog, Age=BES$Age, Gender_male=ifelse(BES$y09=="Male",1,0), LR=BES$LR))
comb <- rbind(dummy, BES2)[-1, ]
cat("class of LR after rbind with numeric CCES-like frame:", class(comb$LR), "\n")
num <- as.numeric(as.character(comb$LR))
for (lc in c(Sys.getlocale("LC_COLLATE"), "C")) {
  old <- Sys.getlocale("LC_COLLATE"); invisible(Sys.setlocale("LC_COLLATE", lc))
  a <- comb$LR >= 0.0 & comb$LR <= 0.3; b <- comb$LR >= 0.7
  cat(sprintf("collate=%s: rows where string comparison differs from numeric: left-dummy %d, right-dummy %d (n=%d)\n",
      lc, sum(a != (num >= 0 & num <= 0.3)), sum(b != (num >= 0.7)), nrow(comb)))
  invisible(Sys.setlocale("LC_COLLATE", old))
}
cat("value counts of LR string:\n"); print(table(comb$LR))

## Check 2: 06_Estimate Open.R lines 197-203, weight column w1
data <- read.csv("output/Prepped_survey_data.csv")
cat("\nCheck 2: columns of Prepped_survey_data.csv:", paste(colnames(data), collapse=", "), "\n")
cat("is.null(subset(data, Country=='UK' & T_cases >= 10000 & T_health_cap=='Poor')$w1):",
    is.null(subset(data, Country == "UK" & T_cases >= 10000 & T_health_cap == "Poor")$w1), "\n")

## Check 3: 06_Estimate Open.R line 72, simulation data for country i is the combined data
data$Y_open <- ifelse(data$Y == 1, 1, 0)
form <- as.formula("I(Y_open == 1)~ 1 + I(T_health_cap == \"Great\") + log(T_cases) + 
+ I(T_who == \"WHO\") + I(T_who == \"WHO.Ratified\") + Authoritarianism + I(Age/100) +
+ Gender_male + Edu_university + I(I(LR != -99) * LR) + I(LR == -99)")
set.seed(4242)
for (cn in c("US","UK")) {
  tmp <- subset(data, Country == cn)
  mod <- bayesglm(formula=form, data=tmp, family=binomial("probit"), weights=w)
  beta <- rmvnorm(n=1000, coef(mod), vcov(mod))
  for (v in list(c("T_who","None","WHO"), c("Gender_male","0","1"))) {
    f <- function(D) { d0 <- d1 <- D
      d0[, v[1]] <- if (v[1]=="T_who") v[2] else as.numeric(v[2]); d1[, v[1]] <- if (v[1]=="T_who") v[3] else as.numeric(v[3])
      mean(apply(pnorm(model.matrix(form, d1) %*% t(beta)) - pnorm(model.matrix(form, d0) %*% t(beta)), 2, mean)) }
    cat(sprintf("Check 3 %s %s %s->%s: mean change using combined data (as coded, n=%d) %.4f; using own-country rows (n=%d) %.4f\n",
                cn, v[1], v[2], v[3], nrow(data), f(data), nrow(tmp), f(tmp)))
  }
}
sink()
