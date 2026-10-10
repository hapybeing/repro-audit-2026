# Checks that get_model_data(...)[7, ] used at replication.R lines 438 and 455 is the interaction term
.libPaths(c("/workspace/audit_runs/07_JH9DBC/A/rlib", .libPaths()))
suppressMessages({library(lme4); library(sjPlot)})
load("/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A/outputs/session.RData")
g <- get_model_data(model2, type = "est", ci.lvl = 0.95)
print(as.data.frame(g)[, c("term", "estimate", "conf.low", "conf.high")])
cat("row7 term:", as.character(g$term[7]), " row7 estimate:", g$estimate[7], " fixef interaction:", fixef(model2)["juicio:year_2018"], "\n")
