# PREREG: 17_T1NXVQ

Written 2026-10-10, 23:05 IST, before any analysis code was run. No script of the authors (replication.R, scripts/**, or the pspm package functions) was executed to write this file. The main text of the article was read in full (published version, see below); Table 1 numbers were readable and are copied from it. The Supporting Information (SI) was not opened; nothing below depends on it.

What was done before writing: the deposit's file list was read through the Dataverse API; README, codebook, logs, all R scripts and the pspm package source were downloaded and read; `maindata.Rdata`, `graph_hexagonal.rds`, `pool_model.ls.rds` and `pool_se.ls.rds` were downloaded and opened with `load()` / `readRDS()` only, to list object names, graph attribute names and the stored estimates. No model was fitted, no sampler was run.

- Paper: Müller-Crepon, C., Schvitz, G. and Cederman, L.-E. "Shaping states into nations: The effects of ethnic geography on state borders". American Journal of Political Science, published online 2024 (META.md), issue version 69(1), 132-147 (2025, per the LSE repository cover page). DOI https://doi.org/10.1111/ajps.12838 . Licence CC BY-NC-ND 4.0.
- Text read: published version from LSE Research Online, http://eprints.lse.ac.uk/120409/1/American_J_Political_Sci_2024_M_ller_Crepon_Shaping_states_into_nations_The_effects_of_ethnic_geography_on_state.pdf (HTTP 200, 4,391,122 bytes, 17 pages incl. 1 cover page, sha256 67e1f23d126112145766273bd7645a2bdfb7f94d0712f570ffad59b152dc3516). The Wiley pdfdirect URL returned HTTP 403 to a scripted request. Page numbers below are the journal's printed page numbers inside the article (1 to 16).
- Dataset: "Replication Data for: Shaping States into Nations: The Effects of Ethnic Geography on State Borders", Harvard Dataverse, https://doi.org/10.7910/DVN/T1NXVQ , version 1.0, 167 files, 1,988,578,335 bytes, none restricted. Terms: custom ("made available with limited information on how it can be used"); public download, no sign-in.
  - File list API: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/T1NXVQ (saved: `data_statement_raw/dataverse_T1NXVQ.json`).
  - Per-file download: `https://dataverse.harvard.edu/api/access/datafile/<id>` with User-Agent "repro-audit-2026"; `.tab` files with `?format=original` (CSV originals). Every downloaded file's md5 matched the Dataverse checksum.
  - Not downloaded (not needed for Table 1): the 80+ other `data/models/*.rds` files, `data/analysis_data/graph_*.rds` and `sdm_*.rds` (except graph_hexagonal.rds), `uch_cam_12_georef.tif`, the geography folder's geojson/shapefiles, `data/monte_carlo_res/*.rds`. Largest single file: `data/models/shiftcheck_sdmcox.rds`, 1,000,366,457 bytes.

Files downloaded at pre-registration (sha256 also in `prereg_download_checksums.sha256`; scratch copies in /workspace/audit_runs/17_T1NXVQ/prereg/):

| path in deposit | datafile id | bytes | sha256 |
|---|---|---|---|
| `README.txt` | 7436032 | 32163 | 22277b49890f029eb0bbfa3e41816c3cda458d08a91768660d279fce895e9932 |
| `codebook.pdf` | 7436031 | 179225 | 105bff54e71aafd9a46f1039d8930dbff3542476bbd7a65c142b5e18121304df |
| `data/analysis_data/graph_hexagonal.rds` | 6980026 | 976020 | 2e0a630d81c9cf40fbc21f08960c5f0b052bf6176f855f5f616db07886940c3d |
| `data/analysis_data/maindata.Rdata` | 6980033 | 3583904 | 36a02de1a92420f91ffba84b4e4fb5b5d4cf656f2c970d1d9229626eb3f15857 |
| `data/geography/HEG/heg_author_nationalities.tab` | 6980051 | 2366 | 6c3180fac939fe489348d889f5d8d096b6731b257a130680fb1a8c19d94a4984 |
| `data/geography/HEG/heg_langmatch.tab` | 6980056 | 114571 | 61702bb306d4313dfa69c557f6764141cfda892823f771c2124e9376f324b208 |
| `data/geography/HEG/heg_meta.tab` | 6980053 | 15554 | c3b88586ec436be4813e68b803c3b4dca2d9bdff31ced277b28cd2b943781ca5 |
| `data/models/pool_model.ls.rds` | 6980089 | 61309927 | f3b09b98f0ba07ceb5d6216d6df06a149b5713e90369f276721b0cd305601375 |
| `data/models/pool_se.ls.rds` | 6980083 | 27051 | 074e506ebced7aca5a86d1da9484698cd3f64af40f26d05ebfb3b6d6dbc8fd87 |
| `data/monte_carlo_res/mc_bootse/cluster_progress.txt` | 6980142 | 38637 | 0e5039fd0cc9fb9de2192fb26772eca4ae3a9a4b518bfa780755473e26ab02d7 |
| `data/monte_carlo_res/mc_bootse/logfile.txt` | 6980140 | 867 | 0c259c9dd44f388e6e8e67db52aab632e2add8f66ef8228ba2f2ac28e290ec95 |
| `data/monte_carlo_res/mc_burnin/cluster_progress.txt` | 6980146 | 38637 | 46df4e024f9fddf27f012825d67244e21195c4ba39598804ed1088755b566525 |
| `data/monte_carlo_res/mc_burnin/logfile.txt` | 6980144 | 894 | 9c22d4702695c86b64470ef624bf192bd840828a62c9eecb4904c17e0a97670e |
| `data/monte_carlo_res/mc_instances/cluster_progress.txt` | 6980147 | 38637 | bb157ede05e7d175b7eec5a11663cbbb85979ea88b7e114f298ffeb43d656861 |
| `data/monte_carlo_res/mc_instances/logfile.txt` | 6980149 | 882 | fbd1f5f8e4706cdf26703d359bac71f55143f76923935a40e270cc779fe6dc8d |
| `data/monte_carlo_res/mc_size/cluster_progress.txt` | 6980172 | 70938 | 96616ca23d678f6b958472f227976f040c1e1e504e1cbdd4c22f4b5f564d837c |
| `data/monte_carlo_res/mc_size/logfile.txt` | 6980175 | 983 | 7da6bea664e84ed92a6760184ec64675b6bd976c696da746861073755ae52f23 |
| `logs/cluster_log.txt` | 6980014 | 13052 | ec7ea69212f50efce4963390c9be8a94839b49832c61c0b5e279f61e96c646ea |
| `logs/replication_20230311.log` | 6980013 | 55131 | e8c27e820fcc502c05a1eeabd3b5455a3f1b569b1a85ebfc3c50fd31db9900f8 |
| `pspm/pspm_1.0.tar.gz` | 6980176 | 127931 | fa4364fc2c410b1a99cc246fa87ca4c90e49ef0db10472841de633125c039959 |
| `replication.R` | 6980012 | 1320 | 2b2945bcc135377953489560b2aa0a3b1c1adf38f33882a3cc726941415b40a7 |
| `scripts/analysis/analysis_all.R` | 6980310 | 5756 | b26d35f3d8ce3b9ae575528ca87422ddfa3bbee71a92ad99020406a3455b5f40 |
| `scripts/analysis/analysis_globals.R` | 7351688 | 4001 | c4b1680a7b2fe4215ee2acefd5da80d426f591b65e86d54349b12acd8750e980 |
| `scripts/analysis/data/analysis_descriptives.R` | 6980276 | 16454 | 3e6849380848b8576c09e96214994a643f3c4fca9414567a7b0fff5298ab8e35 |
| `scripts/analysis/data/heg_comparison_plot.R` | 6980274 | 3553 | e6145039ec069e07b623d3855a99f7d932d29e7fce60298ea8c381cb1af5d78c |
| `scripts/analysis/data/meta_data_table.R` | 6980275 | 3909 | a2cc97270d5add63744fda7d008a3f8c973b6445c83ed24bdd450ad15ffe8968 |
| `scripts/analysis/mc_plots/examples.R` | 6980279 | 2187 | e6dd858dd25052400736464463c3deef30c425dbfd85a2bea9ad2c07df4d871c |
| `scripts/analysis/mc_plots/mc_inference.R` | 6980277 | 7954 | 0d261aaa74b3285a0f4338aca1d5b7370840fb743af6c492c9b3558cdddc53b6 |
| `scripts/analysis/mc_plots/mc_init.R` | 6980278 | 2119 | a737977e64878be49ddcc691b3649aca884539a42c5e1b33b1a1d689ab7dd39c |
| `scripts/analysis/mc_plots/mc_uncertainty.R` | 6980280 | 5704 | 5eb7b10798e5f5937a0c18f29195b35e120a1d88a550f15c97333471637a8725 |
| `scripts/analysis/mc_plots/pspm_example.R` | 6980281 | 4313 | 5afda2fea96de5ac9290fe9c0d6f5f5d7c96dda89d2c3255f4c7ff6e7f57bcc2 |
| `scripts/analysis/pspm/analysis_1886adm.R` | 6980290 | 3713 | a3b8bb5c602ccac05a8a13094a5e27252259c3912ef8d59fd936a0435c195b36 |
| `scripts/analysis/pspm/analysis_austhung.R` | 6980286 | 4306 | bb48db4cab07b6bc481e8bd3ec86d417f276730f7d00f3ae87253ccaa12fdaca |
| `scripts/analysis/pspm/analysis_burninbootse.R` | 6980293 | 8912 | 11a507eb67823a4250a878201fb04b8027466b48952cc97584d6f5b0332f1d63 |
| `scripts/analysis/pspm/analysis_bymap.R` | 6980287 | 3864 | b92e6726d52c3c7dc95e10fd1c79edb912a71a6d09aa96f4555d00690ea5b5b9 |
| `scripts/analysis/pspm/analysis_continents.R` | 6980284 | 3510 | a8efe73b3f2915ab418b27909f774eed9316bc9140483300fe0b56379004b17a |
| `scripts/analysis/pspm/analysis_controls.R` | 6980288 | 4503 | a38f06ec3435fad9a9bb2bcfa109db338fa3290e77ca67d23cfa835a21dc3ca2 |
| `scripts/analysis/pspm/analysis_cuts.R` | 6980285 | 2775 | 7a0979ebd0b576d8915c3db1500b936a2ca06e751c53f4adf82b0c5f9195b884 |
| `scripts/analysis/pspm/analysis_cutxsec.R` | 6980283 | 2637 | 685d1a3c78968eda6d6e2a21c008cad45a1c5afcf402a00b87dfe05ad5e88e7e |
| `scripts/analysis/pspm/analysis_edgelevel.R` | 6980291 | 4466 | f0afb26fb4e47eba11dea11e2640414f6dd3c84d90744c3d2a0891e23ea319d8 |
| `scripts/analysis/pspm/analysis_fullint.R` | 6980289 | 6439 | dc18ab898f73e8ea4b02c50deadaca86501aea58056a739fd883ff0489523fa4 |
| `scripts/analysis/pspm/analysis_lingdist.R` | 6980292 | 6204 | 2416a59be45c3c385d8f268ad925a2b0705fca06fb30a66c973d06e47c7c1e69 |
| `scripts/analysis/pspm/analysis_long.R` | 6980282 | 2940 | a2a0c9b7a6a85afc14848f4be5c8880cafae932e29443f604abe3aecb42a6751 |
| `scripts/analysis/pspm/analysis_longxsec.R` | 6980301 | 2685 | 361b0b3b9482c455558b4ff26d2aa515d022ca15a5527fa27d297df384cc2bd4 |
| `scripts/analysis/pspm/analysis_periodicity.R` | 6980294 | 4090 | e21fb962a27d16ad267f5151f8dabe22e55101e0fa92825194a01b645350ec15 |
| `scripts/analysis/pspm/analysis_pool.R` | 6980302 | 3638 | fc5122374f2f6183d4c621dd0202be558e616662c2fb11eaca2c97ba7488211e |
| `scripts/analysis/pspm/analysis_popint.R` | 6980300 | 5504 | d7e9c8b893b85452eaade34b9d2012cc777bf70d1027d41413684148178f13e9 |
| `scripts/analysis/pspm/analysis_resolution.R` | 6980295 | 3853 | 8c3b50258d6f07ff375f18cf3c695fb37767d03f13d4c141dc514133eef45442 |
| `scripts/analysis/pspm/analysis_shift_notrun.R` | 6980298 | 4625 | ebbb5e324a6362764398c08986940ff26b718167b3b384941b38ae3224bddf21 |
| `scripts/analysis/pspm/analysis_structure.R` | 6980296 | 3903 | 060fe5af27674d4014ffe2dc6411234f73de97a61f0f7cf3695af41c781833b3 |
| `scripts/analysis/pspm/controlsonly.R` | 6980303 | 3748 | f1ab93ce0e5e5e1f15ddb25ddbbe2dd06540926b3dbdcca8398f6d20faa1ac33 |
| `scripts/analysis/pspm/main_margprob.R` | 6980297 | 10516 | 2a176aeead8410d9343082c5f6074f79216bb95ed97a03399e8c072500e9a467 |
| `scripts/analysis/pspm/main_plots_tables.R` | 6980299 | 50671 | b364e9c18f792559951578e6d7b8dfd6214d16d6f911bf2a09e696a067ecb6ac |
| `scripts/analysis/sdm/analysis_resolcheck.R` | 6980304 | 3377 | 1ba1294929ff7c7ddc0842dd61cd16058ea9e409b1adf4f96cdc0d128c7464df |
| `scripts/analysis/sdm/analysis_sdm.R` | 6980308 | 13578 | 134523807d7c289c407347367230c8d09c2aaca011e6e80e4851b84a54a12b9d |
| `scripts/analysis/sdm/analysis_shiftcheck.R` | 6980307 | 3004 | 2e022d6f28c7648ae4c41ce132270ab1824cb9af8b7a21c4f28280ca6e8460da |
| `scripts/analysis/sdm/analysis_shiftcheck_notrun.R` | 6980306 | 3320 | b83e18083f86cf2755ed81c6c8a5e69d43f25b22fd9634780eb7b7bce2db2422 |
| `scripts/analysis/sdm/analysis_structcheck.R` | 6980305 | 3698 | 678b51c17392f4494a9cb41a546be549cf3bf1fef8bcd1eccceb385a50a1c55e |
| `scripts/data_prep/expand_LEDA.R` | 6980333 | 7399 | fa4f0605bc81f7518b9d25ba98bd39886c282d58779ba1d94b00e0d9fc939541 |
| `scripts/data_prep/heg_polygons_compare.R` | 6980338 | 8999 | e4ffa5c24e431d083f3cca79ff26eca57593f12451373d52abd42687dcf884d9 |
| `scripts/data_prep/make_realnw_functions.R` | 6980332 | 26072 | dc93de563d7c333b288f590a8a2afa7e03db7a07c12accb2f31493c0e6d5c66e |
| `scripts/data_prep/optimize_nwresolution.R` | 6980334 | 2729 | ab9b7898c0898738c06a64438cc0e6d3116a591105156507450b60fa86c3529f |
| `scripts/data_prep/prep_final_data.R` | 6980336 | 9228 | f7f2cfe8ab6434630f930e01714c294f5e5c6f23ba45167169ca4d44a5c4f0d1 |
| `scripts/data_prep/prepare_all.R` | 6980337 | 1346 | 4c419e0cda8a79862d0c4f90f22bf77e28d58592c07087822446a3144510872c |
| `scripts/data_prep/prepare_networks.R` | 6980335 | 7831 | f2d06f412726d79b423e84f925b735022a937e12de7b5cb3a0120b08e9f7aa3e |
| `scripts/functions/analysis/stargazer.R` | 6980321 | 5211 | a49638865a558c916fa061e04eb23dcdd75a7df21b063927982db93409674fb5 |
| `scripts/functions/data_mgt/albers_hexgrid.R` | 6980316 | 17126 | f754c085cf66d24603853468552829a21a0d75431bb9d636b5f39013fa1ab86e |
| `scripts/functions/data_mgt/crop_graph.R` | 6980314 | 1168 | 93333258426f0a4f7abe84dbd3a8b50a9f7501071057d38a24054c9dcacc7a0d |
| `scripts/functions/data_mgt/dist_km_fast.R` | 6980317 | 2501 | 412efd13de4eac4c2a21dabf89b82546b5374b9b72caef8c813d01dc02635ced |
| `scripts/functions/data_mgt/expand_LEDA.R` | 6980318 | 6704 | 89a720e91c8d91692796d15a4a01ff229519b5bfc7c32ca7bf1b821ea6d93deb |
| `scripts/functions/data_mgt/load_fao.R` | 6980315 | 2840 | b779dbd70b00ee33133110676307f59c0aaac2576814febe1ec20f8419cd9bb1 |
| `scripts/functions/data_mgt/load_hydrobasins.R` | 6980313 | 1928 | 0f08d5ffe7f2b5e0eedba706404a9e3e528824eb6ca6ed1bb8d223b2c2757ec8 |
| `scripts/functions/data_mgt/postgresql2R_spatial.R` | 6980320 | 5015 | f119b1e48d45c8fc86a0466261817586bf701816140594f662db18f6c51e2afa |
| `scripts/functions/data_mgt/prepare_graph.R` | 6980319 | 14020 | 576f0ff0377b00058b80c259dfc58fcf7ef388eac2547e44108574729f8738ec |
| `scripts/functions/data_mgt/prepare_sdm_analysis.R` | 6980312 | 19782 | 905c0c6daa95c0f49193a61f06f969aece9d7198d35d4dc90ee20b000ebe35e8 |
| `scripts/functions/monte_carlos/estimate_montecarlo.R` | 6980311 | 16413 | 8b2bfd25e7959d1e9e60676b6b79cd5990248e05edd23f928fb82a28f3da9ada |
| `scripts/functions/plot_graph/plot_spatial_graph.R` | 6980322 | 1969 | e4793cf633377d905df150eed4406a44bd2b5dcdaaadb999973f16c1ed28bdb1 |
| `scripts/libraries.R` | 7351687 | 2761 | 2a001e23eb00f6fcfede4be6ade321825717efd76bc9235deda56ecd8fc3e568 |
| `scripts/monte_carlos/mc_all.R` | 6980329 | 897 | 6f7ef07d61d9535606ac28cbac75e00c6de558f6a0da8bb573fb6690205fd209 |
| `scripts/monte_carlos/mc_bootse.R` | 6980330 | 1303 | a4c587505b6af853bad1bcbf767881e268b61993b96b308495c4bd159b87420a |
| `scripts/monte_carlos/mc_burnin.R` | 6980328 | 1332 | 369c6a4e4fd9ffb797a8bc988ef722ec157da913ae3c34cbb2fcb81e07de27e1 |
| `scripts/monte_carlos/mc_size.R` | 6980327 | 2199 | c9f2b5cf16185b8bade2c42392d22bf3735b5c7d164179e431a2c746ad0dd746 |

Files needed for the Table 1 reproduction: `replication.R` is NOT run (see section 2). Needed: `scripts/analysis/analysis_globals.R`, `scripts/analysis/pspm/analysis_pool.R`, `scripts/analysis/pspm/main_plots_tables.R` (lines 14 to 80 only), `scripts/data_prep/make_realnw_functions.R` and every file under `scripts/functions/` (both are sourced by analysis_globals.R; they only define functions), `data/analysis_data/maindata.Rdata`, `pspm/pspm_1.0.tar.gz`. Downloaded only for comparison, never as an input to the run: `data/models/pool_model.ls.rds`, `data/models/pool_se.ls.rds`.

## 1. Headline result and targets

Main claim (abstract, p. 1): "Using new data on Europe's ethnic geography since 1855, we find that ethnic boundaries increase the conditional probability that two locations they separate are, or will become, divided by a state border." The table that reports it is Table 1 (p. 9), "Determinants of state borders in Europe, 1886-2011": column "Baseline" (the "are" part) and column "Lagged dependent variable" (the "will become" part). The model is a Probabilistic Spatial Partition Model (PSPM) fitted by maximum (penalized) composite likelihood; brackets are 95% percentile intervals from a parametric bootstrap; "*" = "Statistically significant at the 95% level".

Table 1 as printed (all values copied from p. 9):

| row | Baseline | Lagged dependent variable |
|---|---|---|
| Constant | -2.50* [-3.04, -1.91] | -3.01* [-3.98, -2.47] |
| Ethnic boundary_t | 1.22* [1.06, 1.40] | |
| Ethnic boundary_t-1 | | 1.02* [0.79, 1.24] |
| State border_t-1 | | 1.65* [1.46, 1.96] |
| Deep lag | | 0.74* [0.36, 1.15] |
| Number of periods | 6 | 5 |
| Number of vertices | 6769 | 5412 |
| Number of edges | 17923 | 14243 |
| Number of states | 189 | 177 |
| Controls | Yes | Yes |

Targets (paper values copied exactly; each mapped to the statistic and code object that produces it):

| id | quantity | paper value | decimals | location | statistic and code object |
|---|---|---|---|---|---|
| T1 | Ethnic boundary_t coefficient, baseline model | 1.22 | 2 | Table 1, p. 9, column "Baseline", row "Ethnic boundary_t" | point estimate (maxLik BFGS, penalized composite likelihood): `pool_model.ls[["pool_xsec"]]$estimate["cuteth"]` (model 2 of `form.ls`, analysis_pool.R lines 35-37) |
| T2 | Ethnic boundary_t-1 coefficient, LDV model | 1.02 | 2 | Table 1, p. 9, column "Lagged dependent variable", row "Ethnic boundary_t-1" | `pool_model.ls[["pool_ldv"]]$estimate["cuteth_lag"]` (model 1 of `form.ls`, lines 32-34) |
| T3 | State border_t-1 coefficient, LDV model | 1.65 | 2 | Table 1, p. 9, LDV column, row "State border_t-1" | `pool_model.ls[["pool_ldv"]]$estimate["cshp_lag"]` |
| T4 | Deep lag coefficient, LDV model | 0.74 | 2 | Table 1, p. 9, LDV column, row "Deep lag" | `pool_model.ls[["pool_ldv"]]$estimate["abram_sum"]` |
| T5 | Number of vertices, baseline model | 6769 | 0 | Table 1, p. 9, "Number of vertices", Baseline | `sum(pool_model.ls[["pool_xsec"]]$N)` (pspm2table sums the per-period vector; pspm R/pspm2texreg.R) |
| T6 | Number of vertices, LDV model | 5412 | 0 | Table 1, p. 9, "Number of vertices", LDV | `sum(pool_model.ls[["pool_ldv"]]$N)` |

Label-to-variable mapping: main_plots_tables.R lines 45-48 (`var.labs`) and 60-79 (`pspm2table(list(pool.model.ls[[2]], pool.model.ls[[1]]), ...)`): column 1 "Baseline" = `pool.model.ls[[2]]` = `pool_xsec`; column 2 = `pool.model.ls[[1]]` = `pool_ldv`; "Ethnic boundary_t" = `cuteth`, "Deep lag" = `abram_sum`, "State border_t-1" = `cshp_lag`, "Ethnic boundary_t-1" = `cuteth_lag`.

Ambiguities, with candidates (first listed is pre-registered):
- "Number of vertices" is the SUM over periods of the vertices in each period's graph after the authors' cleaning (`sum(m$N)`), not the number of distinct locations (the lattice has 1150 vertices). Candidates: (1) `sum(m$N)`; (2) none other found in the code.
- Bracketed intervals: (1) percentile interval, rows 3:4 (`LB_Perc`, `UB_Perc`) of `se$ci_mat` (pspm2table default `boottype = "percentile"`); (2) basic interval, rows 1:2. The deposited `pool_se.ls.rds` percentile rows round to the printed brackets for every Table 1 coefficient (read at pre-registration with `readRDS`); the basic rows do not for most of them (for example baseline `cuteth` basic interval 1.041 to 1.378 against the printed [1.06, 1.40]).
- Significance "*": the paper's star is "95% CI excludes 0" from the bootstrap; pspm2table is also given `stars = c(.01, .05, .1)` with maxLik Wald p-values, but when `override.ci.*` is supplied texreg marks a coefficient whose CI excludes its `ci.test` value (default 0) instead (texreg documentation; not verified by running). Pre-registered reading: CI excludes 0.

Secondary numbers (reported for context, not targets): edges 17923 / 14243 (`sum(m$N_edges)`), states 189 / 177 (`sum(m$N_groups)`), periods 6 / 5 (`m$N_instances`), constants -2.50 / -3.01, and the printed percentile brackets. Text p. 10 also gives odds ratios for bridge edges, 3.4 [2.9, 4.0] (baseline) and 2.8 [2.2, 3.4] (LDV), which equal exp() of T1 and T2 to the printed rounding; and predicted probabilities 11.2% to 29.9% and 6.1% to 15.3%, and the 34 and 17 percentage-point joint effects (p. 11, from 120 sampled partitionings, main_margprob.R). These are not targets: they need the bootstrap draws or the sampler, which are out of compute scope (section 4).

Conclusion criterion for `same_conclusion`:
- T1 to T4: true if the reproduced coefficient is positive (as printed) AND the reproduced bootstrap interval excludes 0, where the interval is estimate +/- 1.96 x SD of the K reproduced parametric-bootstrap draws for that coefficient (authors' seeds i = 1..K; section 2 step 6). If no bootstrap draw could be produced, `same_conclusion` = null with the reason; it is not inferred from maxLik's analytic SE.
- T5, T6: true if the reproduced count is within 1% of the printed count (any difference is still reported exactly; see CHANGELOG #6 for how an N-only mismatch is classed).
- `match_to_rounding` follows AGENT_RUNBOOK.md (round to 2 decimals for T1 to T4, exact for T5, T6).

Inconsistencies noticed (described, not judged):
- README says ncore is set "around line 34" with "default 60" and that the analysis used 60 CPUs; `analysis_globals.R` sets `ncore <- 40` at line 46. README hardware note: "total of 56 cores and 112 threads".
- README tells users to log to `logs/replication_20230309.log`; the deposited log is `logs/replication_20230311.log` (run 2023-03-11 20:27 to 2023-03-13 06:35, timestamps in CET).
- README gives `scripts/monte_carlos/analysis_all.R` and `scripts/monte_carlos/prepare_all.R`; the files are at `scripts/analysis/analysis_all.R` and `scripts/data_prep/prepare_all.R`.
- README's package list gives two versions for several packages: igraph 1.4.1 and 1.3.5, Rcpp 1.0.10 and 1.0.9, reticulate 1.28 and 1.26, rgeos 0.6-1 and 0.5-9, sp 1.6-0 and 1.5-1, cli 3.5.0 and 3.4.1, digest 0.6.31 and 0.6.30, jsonlite 1.8.4 and 1.8.3, png 0.1-8 and 0.1-7. The cluster log shows rgdal 1.6-2 and rgeos 0.6-1 linked to sp 1.5-1.
- The deposited `pspm_1.0.tar.gz` DESCRIPTION says `Date: 2023-12-26` and `Packaged: 2023-03-09 16:36:15 UTC`; the replication log is from 2023-03-11 and the Dataverse version was released 2023-10-03.
- README names `heg_meta.csv`, `heg_langmatch.csv`, `heg_author_nationalities.csv`; the deposit holds them as ingested `.tab` files whose originals are CSV (not on the Table 1 path).
- README calls `graph_hexagonal.rds` the "Main graph for most analyses", but the Table 1 code loads `graph` from `maindata.Rdata` (`load_data()`, analysis_globals.R line 154). The two graphs have the same 1150 vertices and 3047 edges and identical `cuteth2011` and `length.norm`; `graph_hexagonal.rds` lacks the 5-year cshapes and ethnic attributes and the `_ld` variables.
- Deposited `pool_model.ls.rds` (read, not re-run) gives cuteth 1.2182 (baseline), cuteth_lag 1.0151, cshp_lag 1.6542, abram_sum 0.7377, N 6769 / 5412, edges 17923 / 14243, states 189 / 177, periods 6 / 5: all equal to Table 1 at its rounding. This is a statement about the deposited outputs only, not a reproduction.

## 2. Reproduction plan

Working directory: a fresh copy of the deposit tree at `RUNDIR/replication/` (the code uses relative paths from the deposit root). Before running, move the deposited `data/models/pool_model.ls.rds` and `pool_se.ls.rds` to `RUNDIR/deposited_models/` so the run cannot read them and so `analysis_pool.R` lines 88, 110-111 do not overwrite them; compare against them afterwards.

Environment (clean per-run library `R_LIBS_USER=RUNDIR/rlib`, system R 4.5.x; authors used R 4.2.2 on Ubuntu 22.04, x86_64):
1. Python: `python3 -m venv RUNDIR/venv`, `pip install numpy scipy networkx` (pspm DESCRIPTION Config/reticulate lists scipy, numpy, networkx plus stdlib modules; no versions pinned; record `pip freeze`).
2. Pinned R versions (README "Packages with version used"): try these first with `remotes::install_version` for the packages on the estimation path: igraph 1.4.1 (first listed; 1.3.5 is the second), maxLik 1.5-2, miscTools 0.6-26, reticulate 1.28, texreg 1.38.6, infotheo 1.2.0.1. If a pinned version fails to build on R 4.5 / aarch64, or takes more than 20 minutes, install the current CRAN version instead and record which. R6, sp, doParallel, foreach: current CRAN (R6 is not in the README list).
3. `R CMD INSTALL pspm/pspm_1.0.tar.gz` into the run library (the deposited replication version, as libraries.R line 63 instructs; do NOT install from GitHub).
4. Other packages loaded by `library()` in analysis_globals.R lines 59-89 and the cluster init lines 119-137: install current CRAN versions (raster, plyr, dplyr, tidyr, ggplot2, scico, abind, gridExtra, cshapes (must be 2.x), ggridges, survival, MASS, fasterize, sf, viridis, tidyverse, xtable, smoothr, stargazer, lfe). rgeos and rgdal were archived on CRAN on 2023-10-16: try the last archived versions (rgeos 0.6-4, rgdal 1.6-7) with system GEOS/GDAL/PROJ headers first. Not needed: CEoptim, imager, MapColoring, glmmML, pracma, devtools (libraries.R only; not loaded on the Table 1 path). Do not run `scripts/libraries.R` itself (it installs into the default library).

Allowed environment fixes (each saved as a unified diff with a reason in `diffs/README.md`):
- E1 `analysis_globals.R` line 58 and line 120: `Sys.setenv(RETICULATE_PYTHON = '/usr/bin/python3')` to the venv python (path fix; system python has no numpy).
- E2 `analysis_globals.R` line 46: `ncore <- 40` to `ncore <- 1` (README explicitly allows adapting ncore).
- E3 only if rgeos or rgdal cannot be installed: delete `library(rgeos)`, `library(rgdal)` at lines 69-70 and 125-126. Justification checked at pre-registration: no rgeos or rgdal function (`readOGR`, `gBuffer`, etc.) is called by analysis_pool.R, by main_plots_tables.R lines 14-80, or by the pspm package; they are used only inside data-prep functions that the Table 1 path defines but never calls.
- E4 igraph 2.x deprecation warnings (`clusters`, `delete.edges`, `get.edgelist`) are not errors and need no fix. If a deprecated igraph function is missing (error), the fix is installing an igraph version that has it (pinned 1.4.1 first), not editing code.
- Path-only mapping (no rename needed on the Table 1 path): none. For completeness, if any other script is run, `data/geography/HEG/heg_meta.tab` etc. must be saved as `.csv` from their `?format=original` downloads.

Memory and compute (machine: 7 GB shared by two agents; brief threshold about 3 GB):
- Estimate: the deposited 4-model `pool_model.ls.rds` occupies about 3.2 GB in R once loaded (R reported Vcells 3155 Mb after `readRDS`, pre-registration check). Each PSPM instance holds dense N x N adjacency and predictor matrices (N about 1100 per period) in R, plus copies and an all-pairs edge dictionary in Python (`sl3.py` SpatialLattice constructor loops over all i < j). Running `analysis_pool.R` as written (4 models fitted in parallel workers, returned to the master, then exported again to every bootstrap worker) is expected to exceed 3 GB and could exceed 7 GB. One Table 1 model in one process is estimated at 1.5 to 3 GB, with transient growth during a bootstrap iteration (new instances are built).
- Therefore the pre-registered run is the fallback, chosen before running: same estimation lines, same seeds, fewer models per process. In a copy of `analysis_pool.R` saved under `scripts/` (diff kept):
  - F1 restrict `form.ls` (lines 32-43, unchanged text) to one element per R process: process 1 `form.ls["pool_xsec"]`, process 2 `form.ls["pool_ldv"]`. The two `_long` models are not part of Table 1 and are not run.
  - F2 call the authors' anonymous estimation function of lines 50-87 with `lapply` in the master instead of `parLapply(cl, ...)`; its body, including `set.seed(1)`, `fit_pspm_model(..., sigma2 = 10, force_contiguous = TRUE, na.rm = T, min_component_size = 2, vertex_coords = c("x","y"), return_pspm = T, return_g_ls = T)`, is unchanged. `clusterExport_fast` (line 26) is then not needed.
  - F3 `saveRDS` each fitted model to `outputs/pool_<name>_model.rds`; skip lines 96-111 (the 120-draw bootstrap) and replace them by step 6 below.
  - Record peak RSS of each process (e.g. poll `/proc/<pid>/status` VmHWM, or `ps`) in LOG.md. Run the two processes one after the other, never at the same time.
- Time: the authors' log shows pooled model estimation took about 3.5 minutes (4 models in parallel) and each pooled 120-draw bootstrap about 13 to 14 minutes on 40 workers, that is about 4.7 core-minutes per draw on their Xeon. A full 120-draw bootstrap for the two Table 1 models is therefore about 19 core-hours: beyond the runbook's 2-hour limit. The printed brackets are therefore not targets, and the bootstrap is run with a reduced number of draws (step 6). This is a scope decision made now, not a result.

Script order:
1. Download the files listed above to `RUNDIR/replication/`, check sha256 against this file.
2. Set up the environment (steps 1 to 4 above).
3. Process 1 (baseline): source `analysis_globals.R` (with E1, E2, E3 if needed), `load_data()`, then the F1 to F3 copy for `pool_xsec`. Save `outputs/pool_pool_xsec_model.rds` and stdout to `outputs/run_pool_xsec.log`.
4. Process 2 (LDV): same for `pool_ldv`.
5. Extraction script `scripts/extract_targets.R`: reads the two saved models, writes `outputs/targets_extracted.csv` with every coefficient (`$estimate`), maxLik `stdEr()`, `sum(N)`, `sum(N_edges)`, `sum(N_groups)`, `N_instances`. Optional: call `pspm2table(..., type = "text")` with `bootci = FALSE` to print a Table-1-like text table to `outputs/pool_table_text.txt`.
6. Reduced parametric bootstrap with the authors' seeds (used for the T1 to T4 significance criterion). For each model, in its own process after re-fitting or loading the model and calling `reset_pspmlearn` (lines 92-94): for i in 1..K: `set.seed(i); reticulate::py_set_seed(i, disable_hash_randomization = TRUE); learn_obj$bootstrap_composite_log_likelihood(n_boot_iter = 1, burnin = 100, ci_level = 0.95, return_sims = TRUE, report_every = 5, cache_samples = TRUE)`; keep `$beta_boot`. This is exactly the body of the authors' parallel worker (pspm R/pspm_R6.R, `par_bootstrap_composite_log_likelihood`, the `foreach` block) run serially, with `burnin = 100` from analysis_globals.R line 49. Choice of K, fixed now: time the first draw (baseline, i = 1) as t minutes; K = min(10, floor(25 / t)), at least 3; the same K for both models. If one set exceeds 35 minutes it stops after the current draw and reports the draws completed. If K would be below 3, step 6 is not run and T1 to T4 `same_conclusion` = null. Write draws to `outputs/boot_authorseeds_<model>.csv`.
   - Comparison (reported, not a target): the reproduced draw for seed i against row i of the deposited `pool_se.ls.rds` `beta_boot` (list element 2 = `pool_xsec`, element 1 = `pool_ldv`, same order as `form.ls`). Exact equality is not expected to be guaranteed (Python, numpy and networkx versions and platform differ) but is informative.
7. `scripts/build_results.py` builds `results.json` from `outputs/` only.

Not run: `replication.R`, `analysis_all.R` (about 34 hours on 40 cores per the log), the descriptives, Monte Carlo, data-prep and every other analysis script.

## 3. Robustness checks (pre-registered)

Primary quantity for all checks: the T1 coefficient (`cuteth`, baseline model `pool_xsec`). Secondary, reported in the same files: T2 (`cuteth_lag`, `pool_ldv`). "Same direction and significance as the paper" = coefficient > 0 AND estimate - 1.96 x SD > 0, with SD as defined per check. All other settings (formula, `sigma2 = 10`, `force_contiguous`, `na.rm`, `min_component_size = 2`, `set.seed(1)`, `burnin = 100`) stay as in the authors' code unless the check says otherwise. Run order: R_b, R_c (cheap, point estimates), then R_a (bootstrap).

R_a. Different bootstrap seeds. Same procedure as step 6, but with seeds i = 1001..(1000 + K), K the same as in step 6, for both models (baseline first; LDV only if the bootstrap time budget of about 100 minutes in total for step 6 plus R_a is not exhausted). Report: the original point estimate, the mean and SD of the K draws, the interval estimate +/- 1.96 x SD (as `se_or_ci`), the percentile 2.5% and 97.5% of the K draws (descriptive only, K is small), and the number of draws that failed. `p_value`: null (no p-value is defined for this interval). Same direction and significance: estimate > 0 and the +/- 1.96 x SD interval excludes 0. Also report whether the SD from seeds 1001+ differs from the SD from seeds 1..K by more than a factor of 1.5 (descriptive).

R_b. Outlier exclusion. The outcome is a categorical partition membership (state per vertex), so z-scores on the outcome are meaningless; the brief's binary-outcome rule says to apply the |z| > 3 rule to the main continuous predictor, but the main predictor `cuteth` is bounded in [0, 1] with about half of edges at 0, and on the 1150-vertex lattice |z| > 3 flags 0 edges for `cuteth1986` and `cuteth2011` (pre-registration data check), so that rule would exclude nothing. Pre-registered rule instead: on the static lattice `graph` (3047 edges; these covariates do not vary over time), compute z for the two genuinely continuous controls `length.norm` and `elevmean.norm` (z over all edges with non-missing values, sample SD); set to NA every edge with |z| > 3 on either variable (the pre-registration check counted 73 edges for length.norm and 56 for elevmean.norm; the union is computed in the run), then refit both Table 1 models exactly as in steps 3 and 4. The authors' `na.rm = TRUE` (pspm `model_graphframe`) deletes those edges in every period; `min_component_size = 2` then drops any isolated vertex. Report the number of edges and vertices dropped (summed over periods), the coefficient, maxLik `stdEr()` (descriptive), and judge significance with estimate - 1.96 x SD_boot, where SD_boot is the SD of the step-6 draws for the same coefficient (the bootstrap is not re-run for R_b). If step 6 did not run, significance = null.

R_c. Alternative analysis choice: penalty strength. Every PSPM fit in the deposit uses `sigma2 = 10` (the variance of the Gaussian penalty `sum(beta^2) / (2 * sigma2)` on the composite log likelihood; the value is never varied in the scripts). Check: refit both Table 1 models with `sigma2 = 1000` (a penalty 100 times weaker, close to unpenalized maximum composite likelihood), nothing else changed, same `set.seed(1)`. Report coefficient, maxLik `stdEr()` (descriptive), and significance with SD_boot from step 6 as in R_b. If step 6 did not run, significance = null.

## 4. Known risks

- Compute (could make the paper E for the bootstrap part only): full bootstrap infeasible on this machine (about 19 core-hours for the two models); handled by the reduced-K design above. If even the point estimates cannot be produced within about 2 hours, the paper is E.
- Memory: per-process peak not measured yet; estimate 1.5 to 3 GB per Table 1 model, more during a bootstrap draw. Two agents running at once could exhaust 7 GB. If a process is killed for memory, retry once alone; if it fails again, report it (E for that part) with the peak RSS seen.
- Retired packages: rgeos and rgdal (archived 2023-10-16) must build against current GDAL/GEOS/PROJ, else fix E3. igraph 1.4.1 may not build on R 4.5; igraph 2.x keeps the deprecated functions pspm uses (with warnings), but a removal would need the pinned version.
- Python stack: pspm's core is Python (`inst/python/sl3.py`, `crackpack.py`) called via reticulate; numpy, scipy and networkx versions are not pinned anywhere in the deposit. `nx.adjacency_matrix` returns a sparse array in networkx 3.x (used only in `get_adjacency_matrix`, not seen on the estimation path). Version differences could change the Gibbs sampler draws (bootstrap) even with the same seeds; the point estimates do not use the sampler and should be deterministic given the data, up to floating-point summation order.
- Platform: authors x86_64 Linux, R 4.2.2; here aarch64 Debian, R 4.5.x. BFGS optimum could differ in late decimals; targets are at 2 decimals.
- The deposited `pool_model.ls.rds` would be overwritten by `analysis_pool.R` line 88 if run in place; handled by moving it out (section 2).
- Materials: everything the Table 1 path reads is in the deposit (DATA_STATEMENT.md). Missing from the deposit: `data/analysis_data/res_optim.rds` (read only by two `*_notrun.R` scripts and by data prep) and the raw inputs of the data-preparation step, which README says are not included. These do not touch any target. The data construction (step 2 of README's workflow) cannot be reproduced from the deposit.
- No other risk of C identified for the targets: code, data and package source for Table 1 are all deposited.
