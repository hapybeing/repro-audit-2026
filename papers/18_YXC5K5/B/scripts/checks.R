# Supplementary checks (code review evidence and secondary context; not targets).
# 1) Row pairing: docid order of benchmark vs model rows in the main session; FP/FN cell counts by position (main) and after docid
#    sort (R_c session) for GPT 4o Few Shot 8 labels and undergraduates 8 labels, to compare with printed Tables A5/A6 counts.
# 2) undergrads8/undergrads4 AUC/Recall/F1 vs GPT 4 Turbo Zero Shot rows of metrics_matrix.
# 3) Secondary F1 with positive class "1" (main session), GPT 4o Few Shot 8 labels.
suppressMessages({library(dplyr); library(caret)})
out <- list(); add <- function(n, v) out[[length(out) + 1]] <<- data.frame(check = n, value = format(v, digits = 17))
cnt <- function(B, M, tag) { add(paste0(tag, "|FP(model1,bench0)"), sum(M == 1 & B == 0)); add(paste0(tag, "|FN(model0,bench1)"), sum(M == 0 & B == 1));
  add(paste0(tag, "|cells"), length(B)); add(paste0(tag, "|model_1s"), sum(M == 1)); add(paste0(tag, "|bench_1s"), sum(B == 1)) }
e <- new.env(); load("outputs/session.RData", envir = e)
add("main|first10_pi_docid", paste(head(e$pi$docid, 10), collapse = " "))
add("main|first10_gpt4o10few_docid", paste(head(e$gpt_data$gpt4o_10lab_fewshot$docid, 10), collapse = " "))
add("main|rows_with_same_docid_in_same_position", sum(e$pi$docid == e$gpt_data$gpt4o_10lab_fewshot$docid))
add("main|pi_docid_sorted", !is.unsorted(e$pi$docid)); add("main|gpt4o10few_docid_sorted", !is.unsorted(e$gpt_data$gpt4o_10lab_fewshot$docid))
add("main|human10_docid_sorted", !is.unsorted(e$human_data$human_10lab$docid))
cnt(e$pi10mat, e$gpt4o10mat_fewx, "main_by_position|GPT4o8Few"); cnt(e$pi10mat, e$hum10matx, "main_by_position|Undergrad8")
mm <- e$metrics_matrix
for (s in c("AUC", "Recall", "F1")) {
  add(paste0("undergrads8_", s, "_equals_GPT4Turbo8Zero"), isTRUE(all.equal(e$undergrads8[[s]], mm["GPT 4 Turbo 8 Zero Shot", s])))
  add(paste0("undergrads4_", s, "_equals_GPT4Turbo4Zero"), isTRUE(all.equal(e$undergrads4[[s]], mm["GPT 4 Turbo 4 Zero Shot", s])))
}
f1pos1 <- sapply(1:8, function(j) { a <- factor(e$pi10mat[, j], levels = c("0","1")); p <- factor(e$gpt4o10mat_fewx[, j], levels = c("0","1"))
  confusionMatrix(p, a, positive = "1")$byClass["F1"] })
add("secondary|F1_positive1_GPT4o8Few_mean_na_rm", mean(f1pos1, na.rm = TRUE))
add("secondary|undergrads8_pct1s_as_returned_by_script", e$undergrads8[["% 1s"]])
r <- new.env(); load("outputs/session_Rc.RData", envir = r)
cnt(r$pi10mat, r$gpt4o10mat_fewx, "Rc_by_docid|GPT4o8Few"); cnt(r$pi10mat, r$hum10matx, "Rc_by_docid|Undergrad8")
# docid join check independent of sort: join author codings to model rows by docid
j <- inner_join(e$pi %>% select(docid, Theme1:Theme8), e$gpt_data$gpt4o_10lab_fewshot %>% select(docid, Theme1:Theme8), by = "docid", suffix = c(".a", ".m"))
A <- as.matrix(j[, paste0("Theme", 1:8, ".a")]); M <- as.matrix(j[, paste0("Theme", 1:8, ".m")])
add("join_by_docid|GPT4o8Few|rows", nrow(j)); add("join_by_docid|GPT4o8Few|hamming", mean(colMeans(A != M)))
write.csv(do.call(rbind, out), "outputs/checks.csv", row.names = FALSE)
print(do.call(rbind, out))
