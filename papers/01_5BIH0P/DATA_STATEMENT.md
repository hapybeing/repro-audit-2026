# DATA_STATEMENT: 01_5BIH0P (ThermoPCD, Database 2024, doi 10.1093/database/baae015)

Written 2026-10-10 (IST). Checks run 2026-10-10 between 06:20 and 06:45 UTC (11:50 to 12:15 IST). No sign-in, no author contact, no large file downloaded (HEAD requests and API listings only). No classification or result file was changed.

## Source read
- Europe PMC full text XML, PMC10950042: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10950042/fullTextXML (saved: `data_statement_raw/europepmc_fulltext_PMC10950042.xml`).
- The article has no section titled "Data availability". The relevant statements are in the Abstract, the Introduction, "Database and web interface", and "Code availability".

## Verbatim statements
- Abstract: "MD trajectories are freely available. Processed data include Protein Data Bank outputs for all files obtained every 50 ns, and free binding energy calculations for some of the immune complexes. Protocols for using the data are also available. Individual datasets contain unique DOIs. We created a web interface, ThermoPCD, as a platform to explore the data. [...] ThermoPCD is a free to use database of immune complexes' trajectories at different temperatures that does not require registration and allows for all the data to be available for download. Database URL: https://sites.google.com/view/thermopcd/home"
- Introduction: "To each trajectory of a particular protein or protein complex at any particular temperature, we have assigned a unique and permanent DOI in the free-to-use Harvard Dataverse (https://dataverse.harvard.edu)."
- Database and web interface: "All data are stored in the free and open Harvard Dataverse Repository (HDR, https://dataverse.harvard.edu) with full and free public access for downloading the datasets. Permanent DOIs are available for each individual file [...]" and "We have created the website ThermoPCD to HDR by using Google Sites. It provides a user-friendly interface where users can browse the whole database, avail of the hyperlinks to HDR data, and where an overview of all entries is managed."
- Code availability: "No custom code was used for the creation of this database and of the interface website. All software deployed is open source, including Modeller (25), Gromacs (29), AmberTools23 (30), PyMol (31) and ChimeraX (32)."

Correction to the premise of the review: the paper does not say the trajectories are hosted on its own website. It says the data are stored in Harvard Dataverse (one DOI per trajectory) and that the Google Sites page is an index that hyperlinks to those Dataverse records.

## Locations the statement points to
1. Harvard Dataverse, collection ThermoPCD: https://dataverse.harvard.edu/dataverse/ThermoPCD (the paper names https://dataverse.harvard.edu; the site links the collection).
2. ThermoPCD website (index only): https://sites.google.com/view/thermopcd/home ; the 2XWT entry is on https://sites.google.com/view/thermopcd/autoimmune-diseases/tshr-2x .
3. No GitHub, no "on request", no other repository.

## Reachability check (2026-10-10)
- Website home and TSHR page: HTTP 200, no sign-in (`data_statement_raw/site_home.html`, `site_tshr-2x.html`, `reachability_checks.json`). The pages contain only DOI links to Harvard Dataverse; no direct file hosting, no Google Drive links.
- On the TSHR page, the row "TSH receptor in complex with autoantibody K1-70 (310K, 37°C, 400 ns): seed #3" links to https://doi.org/10.7910/DVN/5BIH0P (this audit's dataset) and its "RMSD, SASA, RMSF, Rg, H-bonds" link goes to https://doi.org/10.7910/DVN/TZAPSH .
- DVN/5BIH0P (`dataverse_5BIH0P.json`): version 6, 146 files, 938,233,575 bytes, none restricted. Trajectory files present: only em.trr, nvt.trr (323,010,120 bytes), npt.trr (323,010,120 bytes), i.e. minimisation and 100 ps equilibration. No production .xtc.
- DVN/TZAPSH (`dataverse_TZAPSH.json`): version 2, 28 files, 21,194,573 bytes: .xvg, .tab and 15 PDB snapshots (every 50 ns). No trajectory file.
- Whole ThermoPCD collection, Dataverse Search API for files named *.xtc (`search_xtc_in_ThermoPCD_all.json`, 333 hits; titles of the 257 datasets with xtc files over 10 MB in `large_xtc_dataset_titles.json`): 26 xtc files belong to 2XWT datasets (other seeds and temperatures, 78 MB to 1.55 GB each), but none belongs to 2XWT 310K seed #3. A Dataverse-wide dataset search for title 2XWT (`search_2xwt_datasets_all_dataverse.json`, 46 datasets) returns only 5BIH0P and TZAPSH for 310K seed #3.
- Files that the deposited analysis was run on and that are absent everywhere checked: dynamic-nopbc.xtc and dynamic-nopbc-2.xtc (read by the .xvg analyses) and system_reduced.xtc (read by gmx_MMPBSA), per PREREG.md.
- Sign-in: sibling 2XWT trajectories in the same collection are downloadable without sign-in (HEAD on /api/access/datafile/7474501, 7468395, 7528268 returns HTTP 303 to a public S3 URL). So access is open in general; the specific seed 3, 310 K trajectory is simply not deposited.
- Rough size of what is missing (inferred from siblings, not measured): comparable 2XWT production trajectories are 0.39 GB (PIM6IY, 312 K, 400 ns, seed 2, dynamic-nopbc.xtc), 0.16 GB (8YWAEK, 310 K, 400 ns, seed 1, system_reduced.xtc), 0.78 GB (200 ns, seeds 4 and 5, dynamic-nopbc.xtc) and 1.55 GB (5Q0TL3, 312 K, 400 ns, seed 3, system_reduced.xtc.1). The missing seed 3, 310 K trajectory is therefore likely in the 0.4 to 1.6 GB range.
- Note: during the run Harvard Dataverse returned HTTP 403 for roughly 10 minutes after a burst of metadata requests, then recovered; all saved JSON is from successful responses.

## Does the paper report any computed quantitative result?
Yes, but none for 2XWT. The computed numbers are (a) pembrolizumab, PDB 5DK3: RMSD against the crystal structure after 100 ns of 0.36 nm (310 K) and 1.52 nm (313 K); (b) PD-1/PD-L2, PDB 6UMT: mean binding free energies of -114.2 +/- 6.4, -132 +/- 2.9, -148 +/- 9.2 and -126.3 +/- 8.1 kJ/mol at 310 to 313 K (Figure 5) and "about 30%" increase from 37 to 39 °C. 2XWT appears only as a Table 1 metadata row (5 seeds, 200 ns, footnote "Free binding energy calculations are available"). The paper is otherwise a database description.

## Finding
External location unavailable: the paper points to Harvard Dataverse (via the website index), the website and Dataverse are reachable without sign-in, but the 2XWT 310 K seed 3 production trajectory is not deposited at any pointed-to location (estimated 0.4 to 1.6 GB if it existed), and the paper reports no computed number for 2XWT in any case.
