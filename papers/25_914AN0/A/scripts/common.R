# Shared helpers for agent A staged run (25_914AN0). Working directory must be RUNDIR/Replication_IO.
RUNDIR <- "/workspace/audit_runs/25_914AN0/A"
PDIR <- "/workspace/projects/ff43b4ce-7fd5-48cf-8ce4-17d55fd19b5d/repo/papers/25_914AN0/A"
mem_avail_mb <- function(){ l <- readLines("/proc/meminfo"); as.numeric(gsub("\\D","",grep("^MemAvailable",l,value=TRUE)))/1024 }
peak_mb <- function(){ l <- readLines("/proc/self/status"); as.numeric(gsub("\\D","",grep("^VmHWM",l,value=TRUE)))/1024 }
logmem <- function(tag){ msg <- sprintf("[%s] %s MemAvailable=%.0f MB, this R VmHWM=%.0f MB", format(Sys.time(), tz="Asia/Kolkata", usetz=TRUE), tag, mem_avail_mb(), peak_mb()); message(msg); cat(msg, "\n", file=file.path(PDIR,"outputs","memory_log.txt"), append=TRUE) }
guard <- function(tag, need_mb=3072){ a <- mem_avail_mb(); logmem(paste0(tag," (guard)")); if(a < need_mb) stop(sprintf("Only %.0f MB available (< %d MB); not starting heavy step %s", a, need_mb, tag)) }
main_lines <- readLines("code/run2_main.R")
run_lines <- function(a, b=a){ message(sprintf("-- running run2_main.R lines %d-%d verbatim", a, b)); eval(parse(text=main_lines[a:b]), envir=globalenv()) }
