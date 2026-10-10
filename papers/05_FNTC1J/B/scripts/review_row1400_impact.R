# Agent B code review: impact on T1-T4 of keeping the case removed at line 1770 (raw row name "1400").
# Refits the final model_CTB / model_misinfo formulas on model_CTB$data plus that one case (taken from the initial
# model's data, with gender_male / edu_high relabelled exactly as lines 1806-1812 do).
args <- commandArgs(trailingOnly = TRUE); e <- new.env(); load(args[1], envir = e)
d1 <- as.data.frame(e$model_CTB$data); d0 <- as.data.frame(e$model$data)
add <- d0["1400", , drop = FALSE]
add$gender_male <- factor(add$gender_male, levels = c("0","1"), labels = c("Female","Male"))
add$edu_high <- factor(add$edu_high, levels = c("0","1"), labels = c("Low Education","High Education"))
d2 <- rbind(d1, add[, names(d1)])
o <- function(f, lab) { m <- glm(f, data = d2, family = binomial)
  data.frame(model = lab, nobs = nobs(m), OR_ConspMent = exp(coef(m)["ConspMent_index"]), OR_Truth = exp(coef(m)["EpistBel_Truth_index"]), row.names = NULL) }
out <- rbind(o(formula(e$model_CTB), "model_CTB_with_row1400"), o(formula(e$model_misinfo), "model_misinfo_with_row1400"))
print(out); write.csv(out, file.path(args[2], "review_row1400_impact.csv"), row.names = FALSE)
