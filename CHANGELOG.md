# Changelog

All notable changes to the Building Energy CFM Reliability research software repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.1.3] - 2026-11-27

### Fixed
- **Unrelated Terminology Correction in P49 Documentation:** Corrected an unrelated terminology error in `results/verified_aggregates/P49_README.md`, replacing "row-level patient data" with "row-level building energy observations" to accurately reflect building energy research data provenance.
- **External Dataset DOI and URL Reconciliation:**
  - Corrected the Cairo dataset citation in `README.md` and `data/README.md` from a misattributed BSERT DOI to the authentic publisher DOI: *Buildings* 16(5), 976 (DOI: [`10.3390/buildings16050976`](https://doi.org/10.3390/buildings16050976)).
  - Corrected the Building Data Genome Project 2 (BDG2) publication DOI in `README.md` and `data/README.md` to [`10.1038/s41597-020-00712-x`](https://doi.org/10.1038/s41597-020-00712-x) and updated the repository link to the canonical organization repository ([`https://github.com/buds-lab/building-data-genome-project-2`](https://github.com/buds-lab/building-data-genome-project-2)).
  - Updated the Five-Climate dataset citation to reflect the complete peer-reviewed reference (*Scientific Reports* 15, 4181, 2025; DOI: [`10.1038/s41598-025-32297-z`](https://doi.org/10.1038/s41598-025-32297-z)).

### Changed
- **Metadata and Software Citation:** Updated `CITATION.cff`, `.zenodo.json`, and `README.md` to release version `v1.1.3`. Clarified documentation distinguishing the concept DOI (`10.5281/zenodo.23641280`) from the version-specific DOI cited in the submitted manuscript (`10.5281/zenodo.24528248`, v1.1.2).

### Preserved
- **Scientific Integrity and Numerical Consistency:** Confirmed through cryptographic SHA-256 hashes that all model configurations (`configs/`), Python source workers (`src/`), verification scripts (`scripts/`), figure assets (`figures/`), notebook outputs (`notebooks/`), protocol records (`reproducibility/`), and evaluation aggregate CSVs (`results/`) remain strictly unchanged.

---

## [v1.1.2] - 2026-11-25

### Changed
- Removed conversational development artifacts from notebook cells and outputs in `notebooks/Training Code + Output.ipynb`, preserving all execution logs and visual outputs.
- Documented EDCS target-unit ambiguity ($\text{kWh}/\text{m}^2$ in source table vs $\text{MWh}/\text{m}^2$ in descriptor narrative) and retained exploratory qualification for Direct CFM.
- Corrected five-climate geographical description to five international cities (Cairo, Gizan, Riyadh, Sevilla, Miami).
- Detailed cohort-specific CatBoost anchor protocols (GroupKFold OOF vs fixed-split fits).
- Clarified physical-scale prediction diagnostics under out-of-distribution feature combinations.
- Added comprehensive mapping of historical figure keys (J27–J138) to final manuscript figures 1–10 in `P49_README.md`.
- Updated release and citation metadata with Zenodo release DOI `10.5281/zenodo.24528248`.

---

## [v1.1.1] - 2026-11-25

### Changed
- Reconciled Cairo cohort sample-size description to distinguish 480 simulated geometries from 2,405 held-out records.
- Refined CatBoost anchor training descriptions across cohorts.
- Removed speculative causal phrasing regarding residual bounding and trajectory collapse.

---

## [v1.1.0] - 2026-11-25

### Added
- Standardized directory structure (`configs/`, `data/`, `figures/`, `notebooks/`, `reproducibility/`, `results/`, `scripts/`, `src/`).
- Added formal computational environment and protocol disclosures.
- Included checkpoint hash verification tools.

---

## [v1.0.1] - 2026-10-25

### Added
- Initial standalone training notebook preserving complete cell execution outputs.

---

## [v1.0.0] - 2026-10-25

### Added
- Initial research software release accompanying six-cohort conditional flow matching evaluation.
- Archived under Zenodo DOI: `10.5281/zenodo.23641281`.
