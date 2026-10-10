# Code-review evidence: undergrads8/undergrads4 AUC, Recall, F1 (Rmd lines 2050-2064) vs the GPT 4 Turbo Zero Shot rows of metrics_matrix.
e <- new.env(); load("/workspace/audit_runs/18_YXC5K5/A/session_main.RData", envir = e)
mm <- e$metrics_matrix
r <- data.frame(stat = rep(c("AUC","Recall","F1"), 2), labels = rep(c(8,4), each = 3),
  undergrads = c(e$undergrads8$AUC, e$undergrads8$Recall, e$undergrads8$F1, e$undergrads4$AUC, e$undergrads4$Recall, e$undergrads4$F1),
  gpt4turbo_zero = c(mm["GPT 4 Turbo 8 Zero Shot", c("AUC","Recall","F1")], mm["GPT 4 Turbo 4 Zero Shot", c("AUC","Recall","F1")]))
r$identical <- r$undergrads == r$gpt4turbo_zero
print(r); write.csv(r, "outputs/undergrad_row_check.csv", row.names = FALSE)
