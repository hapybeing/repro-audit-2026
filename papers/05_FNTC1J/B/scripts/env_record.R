# Agent B: record versions of every package the script attaches, from the same library paths used for the run.
p <- c("pacman","tidyverse","dplyr","magrittr","haven","descr","tidycomm","htmlTable","sjmisc","sjlabelled","psych","stats","report","naniar","correlation","xtable","Hmisc","MVN","lavaan","writexl","GPArotation","stargazer","MissMech","finalfit","careless","labelled","skimr","broom","blorr","splines","arm","sjPlot","ggplot2","ggridges","RColorBrewer","DescTools","viridis","patchwork","multcomp","car","gridExtra","lmtest","olsrr","sandwich","MASS","boot","kableExtra","cowplot","mice","DT","htmltools","officer","flextable","parameters","tibble","tidyr","tinytable","insight","datawizard","bayestestR","effectsize","performance")
for (x in p) suppressPackageStartupMessages(library(x, character.only = TRUE))
v <- data.frame(package = p, version = sapply(p, function(x) as.character(packageVersion(x))),
                lib = sapply(p, function(x) dirname(dirname(system.file(package = x)))) , row.names = NULL)
v$lib <- sapply(p, function(x) sub("/[^/]+$", "", system.file(package = x)))
print(v, row.names = FALSE)
cat("\nRNGkind:", RNGkind(), "\n\n"); print(sessionInfo())
