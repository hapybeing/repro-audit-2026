# Agent B: applies E1, E2, E3 to analysis_globals.R and F1-F3 (copy analysis_pool_B.R) as pre-registered. Idempotent from originals in /workspace/audit_runs/17_T1NXVQ/B/orig.
S='/workspace/audit_runs/17_T1NXVQ/B'
s=open(S+'/orig/analysis_globals.R').read()
s=s.replace("Sys.setenv(RETICULATE_PYTHON = '/usr/bin/python3')","Sys.setenv(RETICULATE_PYTHON = '"+S+"/venv/bin/python3')  # [AUDIT B, E1]")
s=s.replace("ncore <- 40","ncore <- 1  # [AUDIT B, E2] was 40")
s=s.replace("  library(rgeos)\n  library(rgdal)\n","  # [AUDIT B, E3] library(rgeos), library(rgdal) removed: archived packages fail to build (sp.h not shipped by sp 2.x)\n")
s=s.replace("      library(rgdal)\n      library(rgeos)\n","      # [AUDIT B, E3] library(rgdal), library(rgeos) removed\n")
open(S+'/replication/scripts/analysis/analysis_globals.R','w').write(s)
s=open(S+'/orig/analysis_pool.R').read()
old='''## Make cluster
if(!exists("cl")){
  cl <- make_cluster(ncore)
  stop.cl <- T
} else {
  stop.cl <- F
}

## Export stuff to cluster
clusterExport_fast(cl, c("graph", "cut_yrs"), envir = globalenv())
'''
assert old in s
s=s.replace(old,'''## [AUDIT B, F2] no cluster: models fitted serially with lapply in the master
## clusterExport_fast(cl, c("graph", "cut_yrs"), envir = globalenv())
''')
old='''                                 paste0("cuteth", cut_yrs[1]))))
'''
assert old in s
s=s.replace(old, old+'''## [AUDIT B, F1] one Table 1 model per R process, chosen by env var AUDIT_MODEL
form.ls <- form.ls[Sys.getenv("AUDIT_MODEL")]
''')
old="model.ls <- parLapply(cl, form.ls, function(f){"
assert old in s
s=s.replace(old,"model.ls <- lapply(form.ls, function(f){  ## [AUDIT B, F2] was parLapply(cl, form.ls, ...)")
i=s.index('saveRDS(model.ls, file = file.path(tem_res.path, "pool_model.ls.rds"))')
s=s[:i]+'''## [AUDIT B, F3] save to the audit models folder; original lines 88-118 (save over deposit, 120-draw bootstrap, cluster stop) not run
saveRDS(model.ls[[1]], file = file.path(Sys.getenv("AUDIT_OUT"), paste0("pool_", names(form.ls), "_model.rds")))
'''
open(S+'/replication/scripts/analysis/pspm/analysis_pool_B.R','w').write(s)
