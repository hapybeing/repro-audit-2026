## Agent B: pre-registered robustness checks R_b, R_c and the MLE candidate (mode "fast"),
## and R_a nonparametric bootstrap (mode "ra", resumable via saved RNG state).
## Working directory = RUNDIR (replication/). Uses the agent's own output/Prepped_survey_data.csv.
args <- commandArgs(trailingOnly = TRUE)
mode <- args[1]; out_dir <- args[2]; state_dir <- args[3]
suppressMessages({library(nnet); library(MASS)})
data <- read.csv(file="output/Prepped_survey_data.csv")
## authors' formula, copied from 03_Estimate main models.R lines 17-19 and 39
form_raw <- "factor(Y) ~ 1 + I(T_health_cap == \"Great\") + log(T_cases) + 
  + Authoritarianism + I(Age/100) +
  + Gender_male + Edu_university + I(I(LR != -99) * LR) + I(LR == -99)"
this_form <- as.formula(paste0(form_raw, "+ I(T_who == \"WHO\") + I(T_who == \"WHO.Ratified\")"))
terms_who <- c('I(T_who == "WHO")TRUE', 'I(T_who == "WHO.Ratified")TRUE')
tid <- function(country, term) paste0(c(UK="T", US="T")[country], if (country=="UK") c(1,2)[match(term, terms_who)] else c(3,4)[match(term, terms_who)])

## note: weights passed as the data column w (identical values to tmp$w; multinom evaluates weights inside data)
sim_fit <- function(tmp, df_n, weighted=TRUE) {
  set.seed(1230)
  mod <- if (weighted) multinom(formula=this_form, data=tmp, weights=w, Hess=TRUE, maxit=500, trace=FALSE) else
                       multinom(formula=this_form, data=tmp, Hess=TRUE, maxit=500, trace=FALSE)
  theta <- mvrnorm(n=5000, mu=c(t(coef(mod))), vcov(mod))
  cn <- paste0(rep(rownames(coef(mod)), each=ncol(coef(mod))), ":", rep(colnames(coef(mod)), nrow(coef(mod))))
  colnames(theta) <- cn
  out <- list()
  for (term in terms_who) {
    x <- theta[, paste0("2:", term)]
    out[[term]] <- data.frame(term=term, Mean=mean(x), SD=sd(x), pvalue=2*pt(q=-abs(mean(x)/sd(x)), df=df_n),
                              MLE=coef(mod)["2", term], SE_analytic=sqrt(diag(vcov(mod)))[paste0("2:", term)],
                              p_wald=2*pnorm(-abs(coef(mod)["2", term]/sqrt(diag(vcov(mod)))[paste0("2:", term)])),
                              convergence=mod$convergence, N=nrow(tmp))
  }
  do.call(rbind, out)
}

if (mode == "fast") {
  ## Main model, refit: MLE candidate for T1-T4 (and check of Mean/SD/p against authors' saved run)
  main <- do.call(rbind, lapply(c("UK","US"), function(cn) cbind(country=cn, sim_fit(subset(data, Country==cn), nrow(data)))))
  main$id <- mapply(tid, main$country, main$term)
  write.csv(main, file.path(out_dir, "main_refit_mle.csv"), row.names=FALSE)
  ## R_b extreme-weight exclusion
  keep <- rep(TRUE, nrow(data)); info <- list()
  for (cn in c("UK","US")) {
    idx <- which(data$Country == cn); w <- data$w[idx]; z <- (w - mean(w))/sd(w)
    drop <- abs(z) > 3; rule <- "|z(w)| > 3 within country"
    if (sum(drop) == 0) { drop <- w > quantile(w, 0.99, type=7); rule <- "top 1% of w within country (no |z|>3 rows)" }
    keep[idx[drop]] <- FALSE
    zc <- (log(data$T_cases[idx]) - mean(log(data$T_cases[idx])))/sd(log(data$T_cases[idx]))
    za <- (data$Age[idx] - mean(data$Age[idx]))/sd(data$Age[idx])
    info[[cn]] <- data.frame(country=cn, rule=rule, rows_dropped=sum(drop), n_before=length(idx), n_after=length(idx)-sum(drop),
                             max_w=max(w), w_cutoff_value=if (grepl("top", rule)) unname(quantile(w,0.99,type=7)) else mean(w)+3*sd(w),
                             info_n_absz3_logcases=sum(abs(zc) > 3), info_n_absz3_age=sum(abs(za) > 3))
  }
  d_b <- data[keep, ]
  rb <- do.call(rbind, lapply(c("UK","US"), function(cn) cbind(country=cn, sim_fit(subset(d_b, Country==cn), nrow(d_b)))))
  rb$id <- mapply(tid, rb$country, rb$term)
  write.csv(rb, file.path(out_dir, "R_b_extreme_weights.csv"), row.names=FALSE)
  write.csv(do.call(rbind, info), file.path(out_dir, "R_b_exclusion_info.csv"), row.names=FALSE)
  ## R_c unweighted
  rc <- do.call(rbind, lapply(c("UK","US"), function(cn) cbind(country=cn, sim_fit(subset(data, Country==cn), nrow(data), weighted=FALSE))))
  rc$id <- mapply(tid, rc$country, rc$term)
  write.csv(rc, file.path(out_dir, "R_c_unweighted.csv"), row.names=FALSE)
  print(main); print(rb); print(do.call(rbind, info)); print(rc)
}

if (mode == "ra") {
  B <- 1000; chunk <- as.integer(args[4]); if (is.na(chunk)) chunk <- 50
  st_file <- file.path(state_dir, "ra_state.rds")
  if (file.exists(st_file)) { st <- readRDS(st_file); .Random.seed <- st$seed } else {
    set.seed(20261010)
    st <- list(country_i=1, b=0, draws=data.frame(), seed=NULL)
  }
  countries <- c("UK","US"); done_this_call <- 0
  while (st$country_i <= 2 && done_this_call < chunk) {
    cn <- countries[st$country_i]; tmp <- subset(data, Country == cn); n <- nrow(tmp)
    ii <- sample(n, n, replace=TRUE); tb <- tmp[ii, ]
    mod <- multinom(formula=this_form, data=tb, weights=w, Hess=TRUE, maxit=500, trace=FALSE)
    cf <- coef(mod)
    st$draws <- rbind(st$draws, data.frame(country=cn, b=st$b+1, convergence=mod$convergence,
                      who=if ("2" %in% rownames(cf)) cf["2", terms_who[1]] else NA,
                      who_rat=if ("2" %in% rownames(cf)) cf["2", terms_who[2]] else NA,
                      n_levels=length(unique(tb$Y))))
    st$b <- st$b + 1; done_this_call <- done_this_call + 1
    if (st$b >= B) { st$country_i <- st$country_i + 1; st$b <- 0 }
  }
  st$seed <- .Random.seed; saveRDS(st, st_file)
  cat("progress: country_i", st$country_i, "b", st$b, "rows", nrow(st$draws), "\n")
  if (st$country_i > 2) {
    write.csv(st$draws, file.path(out_dir, "R_a_bootstrap_draws.csv"), row.names=FALSE)
    main <- read.csv(file.path(out_dir, "main_refit_mle.csv"))
    summ <- list()
    for (cn in countries) for (k in 1:2) {
      d <- st$draws[st$draws$country == cn, ]; ok <- d$convergence == 0 & !is.na(d[[c("who","who_rat")[k]]])
      b <- d[[c("who","who_rat")[k]]][ok]; term <- terms_who[k]
      est <- main$MLE[main$country == cn & main$term == term]
      summ[[paste(cn,k)]] <- data.frame(id=tid(cn, term), country=cn, term=term, estimate_MLE=est, boot_SE=sd(b),
        ci95_lo=quantile(b,.025), ci95_hi=quantile(b,.975), ci99_lo=quantile(b,.005), ci99_hi=quantile(b,.995),
        p_boot=if (est < 0) min(2*mean(b >= 0), 1) else min(2*mean(b <= 0), 1),
        n_nonconverged=sum(d$convergence != 0), n_missing_level=sum(is.na(d[[c("who","who_rat")[k]]])), n_used=length(b))
    }
    write.csv(do.call(rbind, summ), file.path(out_dir, "R_a_bootstrap_summary.csv"), row.names=FALSE)
    print(do.call(rbind, summ))
  }
}
