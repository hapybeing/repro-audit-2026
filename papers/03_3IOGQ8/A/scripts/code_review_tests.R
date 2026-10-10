# Code-review tests on the authors' own functions/expressions (no data needed).
# Each test evaluates the authors' code verbatim, taken from the Rmd by line number,
# on a synthetic input, and writes the result to outputs/code_review_tests.json.
# Usage: Rscript code_review_tests.R <Rmd> <out.json>
suppressMessages({library(jsonlite); library(dplyr)})
args <- commandArgs(trailingOnly = TRUE); rmd <- args[1]; out <- args[2]
lines <- readLines(rmd)
starts <- grep("^```\\{r\\}", lines); ends <- grep("^```\\s*$", lines)
ends <- sapply(starts, function(s) min(ends[ends > s]))
chunk_exprs <- function(k) {
  first <- starts[k] + 1
  ex <- parse(text = lines[first:(ends[k] - 1)], keep.source = TRUE)
  list(ex = ex, first = first, src = attr(ex, "srcref"))
}
# chunk 1: constants and functions (library(mzR) fails and is skipped; it is not used here)
c1 <- chunk_exprs(1)
for (i in seq_along(c1$ex)) try(suppressMessages(eval(c1$ex[[i]], globalenv())), silent = TRUE)
res <- list()

## Test 1: neutral-loss ions in generate_ions_for_sequence (Rmd lines 134-345)
seq31 <- "ARTKQTARKSTGGKAPRKQLATKAARKSAPATGGGH"
mods <- data.frame(position = 9L, variable = 42.046950)   # K9 trimethyl, mass as used in the Rmd
ions <- generate_ions_for_sequence(seq31, mods)
b1 <- ions[["b_ions_charge 1"]]; bK <- ions[["b_nl_Kme3_ions_charge 1"]]
c1i <- ions[["c_ions_charge 1"]]; cK <- ions[["c_nl_Kme3_ions_charge 1"]]
loss <- 59.073499
tab <- data.frame(i = 8:12,
  b_ion_mz = b1[8:12], b_nl_Kme3_code = bK[8:12],
  b_nl_Kme3_if_from_same_fragment = b1[8:12] - loss,
  b_nl_Kme3_if_from_previous_fragment = c(NA, b1[8:11]) - loss)
res$test1_neutral_loss <- list(
  description = "b/c/a/y/z neutral-loss (Kme3, pST, Ksu) m/z at fragment i are computed from a_mass..z_mass BEFORE those are recalculated for fragment i (Rmd lines 195-284 use the masses assigned at lines 287-291 of the previous loop iteration), so they equal the loss from fragment i-1.",
  table_charge1 = tab,
  code_equals_previous_fragment_minus_loss = isTRUE(all.equal(bK[9:12], b1[8:11] - loss, tolerance = 1e-9)),
  code_equals_same_fragment_minus_loss = isTRUE(all.equal(bK[9:12], b1[9:12] - loss, tolerance = 1e-9)),
  c_code_equals_previous_fragment_minus_loss = isTRUE(all.equal(cK[9:12], c1i[8:11] - loss, tolerance = 1e-9)),
  b_charge2_code_equals_previous_fragment_minus_loss = isTRUE(all.equal(ions[["b_nl_Kme3_ions_charge 2"]][9:12], ions[["b_ions_charge 2"]][8:11] - loss / 2, tolerance = 1e-9)))

## Test 2: TMT isotope impurity correction (Rmd lines 2658-2687)
# Synthetic scan: only reagent 126 present, true signal 1000. By the Rmd's own vector
# convention (comment line 21: c(-2, -1, monoisotopic, +1, +2) per reagent), reagent 126
# spills TMT126[4] = 0.076 of its signal into channel 127. A correct correction returns 0 in 127.
tst <- tibble(scan_number = 1L, `126_intensity` = 1000, `127_intensity` = 1000 * TMT126[4],
              `128_intensity` = 0, `129_intensity` = 0, `130_intensity` = 0, `131_intensity` = 0)
# locate the authors' correction expression (the top-level expression containing line 2662)
k <- max(which(starts < 2662)); ck <- chunk_exprs(k)
idx <- which(sapply(ck$src, function(s) (ck$first + s[1] - 1) <= 2662 && (ck$first + s[3] - 1) >= 2662))
expr_lines <- c(ck$first + ck$src[[idx]][1] - 1, ck$first + ck$src[[idx]][3] - 1)
assigned_fractional_intensity_hits <- tst
eval(ck$ex[[idx]], globalenv())
o <- assigned_fractional_intensity_hits
res$test2_tmt_correction <- list(
  description = "Synthetic scan with only reagent 126 (true 1000) plus its documented +1 impurity in 127 (76). The authors' correction expression is evaluated verbatim.",
  expression_rmd_lines = expr_lines,
  input = as.list(tst[1, -1]),
  corrected = as.list(o[1, c("126_corrected","127_corrected","128_corrected","129_corrected","130_corrected","131_corrected")]),
  expected_if_impurities_removed = list(`126` = 1000, `127` = 0))
writeLines(toJSON(res, auto_unbox = TRUE, pretty = TRUE, digits = NA), out)
cat(readLines(out), sep = "\n")
