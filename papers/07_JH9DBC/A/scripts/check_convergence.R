.libPaths(c("/workspace/audit_runs/07_JH9DBC/A/rlib", .libPaths()))
suppressMessages(library(lme4))
P <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/07_JH9DBC/A"
load(file.path(P, "outputs/session.RData"))
objs <- ls(); for (o in objs) { x <- get(o); if (inherits(x, "merMod")) {
  msg <- paste(c(x@optinfo$conv$lme4$messages, x@optinfo$warnings), collapse=" | ")
  cat(o, "singular=", isSingular(x), " conv:", ifelse(nchar(msg)==0, "none", msg), "\n") } }
