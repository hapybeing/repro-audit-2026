## Code-review check for 06_Estimate Open.R lines 197-203 (footnote 20 probit models).
## The call passes w=subset(data, ...)$w1. Does the prepared data contain a column w1, and is the
## resulting fit identical to an unweighted fit (and different from a fit weighted by w)?
## Mirrors the data steps of 06 needed for Y_open (read prepared data; Y_open = Y == 1).
suppressMessages(library(arm))
args <- commandArgs(trailingOnly = TRUE)
data <- read.csv(file = args[1])
src <- readLines(args[2])
cat("06 lines 195-203 as deposited:\n"); cat(src[195:203], sep = "\n")
cat("\nYopen line(s) in 06:\n"); print(grep("Y_open", src, value = TRUE)[1:3])
data$Y_open <- ifelse(data$Y == 1, 1, 0)
res <- c()
for (cc in c("UK", "US")) {
  s <- subset(data, Country == cc & T_cases >= 10000 & T_health_cap == "Poor")
  f <- Y_open ~ 1 + I(T_who == "WHO") + I(T_who == "WHO.Ratified") + log(T_cases) + Authoritarianism + I(Age/100) + Gender_male + Edu_university + I(I(LR != -99) * LR) + I(LR == -99)
  m_as <- bayesglm(f, data = s, family = binomial(link = "probit"), w = s$w1)
  m_un <- bayesglm(f, data = s, family = binomial(link = "probit"))
  m_w  <- bayesglm(f, data = s, family = binomial(link = "probit"), weights = s$w)
  res <- rbind(res, data.frame(country = cc, n = nrow(s), w1_column_exists = "w1" %in% names(data),
                               coef_WHO_as_deposited = coef(m_as)[2], coef_WHO_unweighted = coef(m_un)[2], coef_WHO_weighted_w = coef(m_w)[2],
                               coef_WHORat_as_deposited = coef(m_as)[3], coef_WHORat_unweighted = coef(m_un)[3], coef_WHORat_weighted_w = coef(m_w)[3],
                               as_deposited_equals_unweighted = isTRUE(all.equal(coef(m_as), coef(m_un))),
                               as_deposited_equals_weighted_w = isTRUE(all.equal(coef(m_as), coef(m_w)))))
}
write.csv(res, args[3], row.names = FALSE)
print(res)
