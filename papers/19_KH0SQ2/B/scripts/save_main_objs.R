# Evaluates lines 1-364 of the deposited main_text_figs_JEPP_FINAL.R unchanged (working dir = run_main copy of the deposit)
# so that res1 (l.325) and res1b (l.363) are captured before res1 is reassigned at l.639.
setwd("/workspace/audit_runs/19_KH0SQ2/B/run_main")
src <- readLines("main_text_figs_JEPP_FINAL.R"); invisible(capture.output(eval(parse(text=src[1:364]))))
saveRDS(list(res1=res1, res1b=res1b, all=all), "/workspace/audit_runs/19_KH0SQ2/B/main_objs.rds")
