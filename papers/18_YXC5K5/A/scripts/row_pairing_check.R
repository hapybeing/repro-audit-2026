# Code-review evidence: confusion counts (pooled over 8 labels) for GPT 4o Few Shot 8 labels and undergraduates vs the
# author codings, under the deposited row-position pairing (main session) and the docid pairing (R_c session).
# Compared later with the printed Tables A5/A6 counts quoted in PREREG.md (FP 369, FN 150; undergrads FP 254, FN 180; of 4712 cells).
suppressMessages(library(tidyverse))
cnt <- function(b, m) c(cells = length(b), TP = sum(b == 1 & m == 1), FP = sum(b == 0 & m == 1), FN = sum(b == 1 & m == 0), TN = sum(b == 0 & m == 0), mismatch_share = mean(b != m))
out <- list()
for (s in c("main", "Rc")) { e <- new.env(); load(sprintf("/workspace/audit_runs/18_YXC5K5/A/session_%s.RData", s), envir = e)
  out[[length(out)+1]] <- data.frame(session = s, model = "GPT 4o Few Shot 8", t(cnt(e$pi10mat, e$gpt4o10mat_fewx)))
  out[[length(out)+1]] <- data.frame(session = s, model = "Undergraduate Coders 8", t(cnt(e$pi10mat, e$hum10matx))) }
# also: position pairing vs docid pairing of the model files themselves (are all model files in identical docid order?)
e <- new.env(); load("/workspace/audit_runs/18_YXC5K5/A/session_main.RData", envir = e)
ref <- e$gpt_data$gpt4o_10lab_fewshot$docid
same <- c(sapply(e$gpt_data, function(d) identical(d$docid, ref)), sapply(e$claude_data, function(d) identical(d$docid, ref)), sapply(e$human_data, function(d) identical(d$docid, ref)))
res <- do.call(rbind, out); print(res); print(same)
write.csv(res, "outputs/row_pairing_confusion_counts.csv", row.names = FALSE)
write.csv(data.frame(object = names(same), identical_docid_order_to_gpt4o10few = same), "outputs/model_files_docid_order.csv", row.names = FALSE)
