# Agent B, 14_CJISMY. Context check for the PREREG-noted prose (p. 824: min-to-max change "predicts a 0.2 point increase", Figure 2 left panel).
# Not a target and not a robustness check; it only records the model quantities the prose could refer to.
args <- commandArgs(trailingOnly = TRUE)
suppressPackageStartupMessages(library(fixest))
load(args[1])
g <- coef(full_model_h1_graph)
gname <- grep("resource_and_agriculture", names(g), value = TRUE)
out <- data.frame(
  quantity = c("Model 1 coef resource_and_agriculture (min 0 to max 1 change)",
               paste0("full_model_h1_graph coef ", gname, " (Figure 2 left panel model)"),
               "Model 3 coef resource_and_agriculture",
               "range of resource_and_agriculture in estimation sample (min|max)"),
  value = c(unname(coef(full_model_h1)["resource_and_agriculture"]),
            unname(g[gname][1]),
            unname(coef(full_model_h1_max)["resource_and_agriculture"]),
            NA))
r <- range(as.data.frame(mean_h1)$resource_and_agriculture, na.rm = TRUE)
out$value <- as.character(signif(out$value, 4)); out$value[4] <- paste(r, collapse = "|")
write.csv(out, args[2], row.names = FALSE)
print(out)
