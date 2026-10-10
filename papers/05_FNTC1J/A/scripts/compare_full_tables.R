# Secondary: compare every row of the paper's Tables A1/A2 (parsed from pdftotext output of the open PDF,
# sha256 fcc1b66c...7357) with the reproduced models, using the authors' own table code logic
# (HC3, Bonferroni over 19 terms, stars, parameters::standardize_parameters(method = "sdy", robust = TRUE)).
# Usage: Rscript compare_full_tables.R <session.RData> <paper.txt> <out.csv>
args <- commandArgs(trailingOnly = TRUE)
suppressMessages({library(sandwich); library(lmtest); library(parameters)})
load(args[1])
txt <- readLines(args[2])
lab <- c("(Intercept)" = "(Intercept)", ConspMent_index = "Conspiracy Mentality", EpistBel_Truth_index = "Truth is Political",
  EpistBel_IT_index = "Intuitive Thinking", EpistBel_AOT_index = "Actively Open-Minded", SDO_index = "Social Dominance",
  polorientation = "Political Orientation", MediaUse_traditional_index = "Traditional Media Use",
  MediaUse_online_index = "Online Media Use", MediaUse_socialMedia_index = "Social Media Use", AltMed_index = "Alternative Media Use",
  TrustMedia_index = "Trust in Media", TrustAltMed_index = "Trust in Alternative Media", TrustScience = "Trust in Science",
  TrustPolitical_index = "Trust in Politics", gender_maleMale = "Male", age = "Age", "edu_highHigh Education" = "High Education",
  religiousity = "Religiosity")
a1 <- grep("Table A1\\.", txt); a2 <- grep("Table A2\\.", txt); a3 <- grep("Table A3\\.", txt)
blocks <- list(CTB = txt[a1:(a2 - 1)], misinfo = txt[a2:(a3 - 1)])
num <- "(-?[0-9]*\\.[0-9]+)"
res <- list()
for (mn in names(blocks)) {
  m <- if (mn == "CTB") model_CTB else model_misinfo
  V <- vcovHC(m, type = "HC3"); ct <- coeftest(m, vcov = V); ci <- coefci(m, vcov = V)
  padj <- p.adjust(ct[, 4], "bonferroni")
  stars <- as.character(cut(padj, c(-Inf, .001, .01, .05, Inf), labels = c("***", "**", "*", "")))
  sp <- as.data.frame(standardize_parameters(m, method = "sdy", ci = 0.95, robust = TRUE))
  ys <- setNames(sp$Std_Coefficient, sp$Parameter)
  for (tm in rownames(ct)) {
    ln <- grep(paste0("^ ", gsub("([()])", "\\\\\\1", lab[[tm]]), "\\s"), blocks[[mn]], value = TRUE)[1]
    rest <- sub(paste0("^ ", gsub("([()])", "\\\\\\1", lab[[tm]])), "", ln)
    toks <- regmatches(rest, gregexpr("-?[0-9]*\\.[0-9]+|\\*+", rest))[[1]]
    nums <- as.numeric(toks[!grepl("\\*", toks)])
    st <- toks[grepl("\\*", toks)]
    res[[length(res) + 1]] <- data.frame(model = mn, term = tm, paper_line = trimws(ln),
      paper_logodds = nums[1], repro_logodds = ct[tm, 1], paper_se = nums[2], repro_se_hc3 = ct[tm, 2],
      paper_ystd = nums[3], repro_ystd = unname(ys[tm]), paper_or = nums[4], repro_or = exp(ct[tm, 1]),
      paper_ci_low = nums[5], repro_ci_low = exp(ci[tm, 1]), paper_ci_high = nums[6], repro_ci_high = exp(ci[tm, 2]),
      paper_stars = if (length(st)) st[1] else "", repro_stars = stars[match(tm, rownames(ct))], repro_p_bonf = padj[tm])
  }
}
out <- do.call(rbind, res)
r2 <- function(x) sprintf("%.2f", x)
out$match_logodds_2dp <- r2(out$repro_logodds) == r2(out$paper_logodds)
out$match_se_2dp <- r2(out$repro_se_hc3) == r2(out$paper_se)
out$match_ystd_2dp <- r2(out$repro_ystd) == r2(out$paper_ystd)
out$match_or_2dp <- r2(out$repro_or) == r2(out$paper_or)
out$match_ci_2dp <- r2(out$repro_ci_low) == r2(out$paper_ci_low) & r2(out$repro_ci_high) == r2(out$paper_ci_high)
out$match_stars <- out$repro_stars == out$paper_stars
write.csv(out, args[3], row.names = FALSE)
mm <- out[!(out$match_logodds_2dp & out$match_se_2dp & out$match_ystd_2dp & out$match_or_2dp & out$match_ci_2dp & out$match_stars), ]
print(mm[, c("model", "term", "paper_line", "repro_logodds", "repro_se_hc3", "repro_ystd", "repro_or", "repro_ci_low", "repro_ci_high", "repro_stars", "repro_p_bonf")], digits = 5)
cat("rows:", nrow(out), " rows with any mismatch:", nrow(mm), "\n")
