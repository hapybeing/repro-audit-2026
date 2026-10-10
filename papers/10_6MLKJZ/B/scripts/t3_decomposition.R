# Agent B: decompose the civic respondents in pooled_df2 by their survey_data.csv sector value (context for T3).
args <- commandArgs(TRUE); RUN <- args[1]; OUT <- args[2]; SURV <- args[3]
d <- readRDS(file.path(RUN, "pooled_df2.rds"))
civ <- unique(as.character(d$respondentIndex[grepl("civic", d$Sample)]))
s <- data.table::fread(SURV, data.table = FALSE, select = c("v9","sector","v184_ger"))
sec <- s$sector[match(civ, s$v9)]; v184 <- s$v184_ger[match(civ, s$v9)]
cat_ <- ifelse(is.na(sec), "not_in_survey_data", ifelse(sec == "", "sector_empty_string", sec))
tab <- as.data.frame(table(category = cat_)); write.csv(tab, file.path(OUT, "t3_civic_decomposition.csv"), row.names = FALSE)
alt <- sum(cat_ %in% c("Private Sector","Public Sector","sector_empty_string"))
x <- as.data.frame(table(sector = ifelse(is.na(sec), "<not in survey>", ifelse(sec == "", "<empty>", sec)), v184_ger = ifelse(is.na(v184), "<not in survey>", ifelse(v184 == "", "<empty>", v184))))
write.csv(x[x$Freq > 0, ], file.path(OUT, "t3_sector_by_v184_ger.csv"), row.names = FALSE)
writeLines(c(paste0("civic_respondents_in_pooled_df2,", length(civ)), paste0("civic_private_public_or_empty_sector,", alt)), file.path(OUT, "t3_alt_count.csv"))
print(tab); print(x[x$Freq > 0, ]); cat("alt:", alt, "\n")
