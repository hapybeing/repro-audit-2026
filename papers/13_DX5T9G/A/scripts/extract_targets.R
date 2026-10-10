## Extract pre-registered targets T1-T6 for 13_DX5T9G from the authors' saved output.
## Usage: Rscript extract_targets.R <path to Estimates-Main.Rdata> <path to Prepped_survey_data.csv> <out csv>
## Candidate (1) per PREREG: Mean / SD / pvalue / N of store_estimates[[k]]$Coefficients, Subset == 1.
## Candidate (2): MLE coef and analytic SE from a refit of the identical multinom call (labelled refit).
suppressMessages({library(nnet); library(MASS)})
args <- commandArgs(trailingOnly = TRUE)
load(args[1])
out <- c()
rows <- c('2:I(T_who == "WHO")TRUE', '2:I(T_who == "WHO.Ratified")TRUE')
ids <- list(UK = c("T1", "T2"), US = c("T3", "T4"))
data <- read.csv(file = args[2])
form_raw <- "factor(Y) ~ 1 + I(T_health_cap == \"Great\") + log(T_cases) + 
  + Authoritarianism + I(Age/100) +
  + Gender_male + Edu_university + I(I(LR != -99) * LR) + I(LR == -99)"
this_form <- as.formula(paste0(form_raw, "+ I(T_who == \"WHO\") + I(T_who == \"WHO.Ratified\")"))
for (cc in c("UK", "US")) {
  k <- ifelse(cc == "US", 1, 2)
  co <- store_estimates[[k]]$Coefficients
  tmp <- subset(data, Country == cc)
  set.seed(1230)
  mod <- multinom(formula = this_form, data = tmp, weights = tmp$w, Hess = TRUE, maxit = 500, trace = FALSE)
  V <- vcov(mod); cf <- coef(mod)
  for (r in 1:2) {
    x <- co[co$X1 == rows[r] & co$Subset == 1, ]
    stopifnot(nrow(x) == 1)
    vn <- sub("^2:", "", rows[r])
    mle <- cf["2", vn]; se <- sqrt(V[rows[r], rows[r]])
    out <- rbind(out, data.frame(id = ids[[cc]][r], country = cc, X1 = rows[r], Mean = x$Mean, SD = x$SD,
                                 pvalue = x$pvalue, N = x$N, MLE_refit = mle, SE_analytic_refit = se,
                                 p_wald_refit = 2 * pnorm(-abs(mle / se)), convergence_refit = mod$convergence))
  }
}
nn <- out[!duplicated(out$country), c("country", "N")]
out <- rbind(out, data.frame(id = ifelse(nn$country == "UK", "T5", "T6"), country = nn$country, X1 = "N", Mean = NA, SD = NA,
                             pvalue = NA, N = nn$N, MLE_refit = NA, SE_analytic_refit = NA, p_wald_refit = NA, convergence_refit = NA))
write.csv(out, args[3], row.names = FALSE)
print(out, digits = 8)
