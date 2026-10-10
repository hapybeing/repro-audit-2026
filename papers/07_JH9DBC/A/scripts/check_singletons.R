# Data fact behind nobs 586 vs 600 under fixest >= 0.13: districts observed once in the 2015/2018 data
suppressMessages({library(haven); library(dplyr)})
d <- read_dta("/workspace/audit_runs/07_JH9DBC/A/run/data.dta") |> filter(year_2012 == 0)
tab <- table(d$unique_id)
cat("rows", nrow(d), "districts", length(tab), "districts_with_1_row", sum(tab == 1), "rows_in_singletons", sum(tab[tab == 1]), "\n")
s <- d[d$unique_id %in% names(tab)[tab == 1], ]
cat("singleton rows by elec_year:\n"); print(table(s$elec_year))
cat("singleton rows juicio==1:", sum(s$juicio == 1), "\n")
