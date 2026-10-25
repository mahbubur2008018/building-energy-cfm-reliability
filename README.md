# Building Energy Conditional Flow Matching: Six-Cohort Reliability Study

**Author:** Md. Mahbubur Rahman  
**Affiliation:** Department of Mechatronics Engineering, Rajshahi University of Engineering & Technology (RUET), Rajshahi, Bangladesh  
**ORCID:** https://orcid.org/0009-0004-0252-9140  
**Repository:** https://github.com/mahbubur2008018/building-energy-cfm-reliability  
**Licence (original code):** MIT  
**Status:** Public source-code and research-evidence repository; Zenodo software DOI pending.

## Purpose and contribution

This repository supports a six-cohort evaluation of **conditional flow matching (CFM)** for building-energy estimation under geometry, climate, meter-site, building and city shifts. The investigation tests (i) source-specific performance of direct and residual CFM variants, (ii) predictive accuracy and calibration with building-level comparisons, and (iii) numerical plausibility of extreme predictions. The study is an **empirical reliability evaluation**, not a new CFM architecture or a universal model-superiority claim.

The six cohorts have different physical outcomes, units and evaluation arrangements. Their errors should not be pooled. The Drammen models alone were transferred unchanged to Oslo; the other historical cohorts have their own source-specific modelling records.

## Six evaluation cohorts

| Cohort | Shift / test set | Outcome and role |
|---|---|---|
| **1. Cairo** (simulated) | Height-out-of-distribution; **2,405** held-out designs | Annual building energy, kWh/year; historical source-specific comparison |
| **2. EDCS** (simulated) | Unseen U-shaped courtyards; **1,536** held-out records | Simulated heating-plus-cooling load; reported kWh/m² convention, with source-unit ambiguity documented in the manuscript |
| **3. Five-climate / Miami** (simulated) | Unseen Miami climate; **5,759** designs | Source-authored energy-per-floor-area target, reported separately |
| **4. BDG2** (measured) | Three unseen sites; **92,356** hourly records | Hourly electricity use, kWh; predictive-tail diagnostics retained |
| **5. Drammen COFACTOR** (measured) | **7** test buildings; **23,136** hourly records | Hourly imported electricity (kWh); preselected model-pair and building-level comparison |
| **6. Oslo COFACTOR-SBHUB** (measured) | **36** test schools; **224,709** hourly records | Hourly imported electricity (kWh); unchanged frozen Drammen models transferred to another city |

**Drammen frozen split:** 27 FIT buildings (88,584 rows), 6 VAL (19,467), 5 CAL (14,864) and 7 TEST (23,136).  
**Oslo frozen split:** 12 CAL schools (51,794 rows) and 36 TEST schools (224,709); 48 metadata-eligible schools overall. The Oslo models were not retrained.

## CFM variants and baselines

| Variant | Modelling arrangement | Role of CatBoost |
|---|---|---|
| **Direct CFM** | Conditional flow predicts the transformed energy target directly | No anchor |
| **Full Residual CFM** | Conditional flow predicts residuals relative to a CatBoost point prediction | Anchor included in flow conditioning and final reconstruction |
| **No-base Residual CFM** | Conditional flow predicts CatBoost-relative residuals without anchor as a conditioning input | Anchor used for residual-target construction and final reconstruction, **not** flow conditioning |

**Historical baselines (according to cohort):** CatBoost point regression, CatBoost quantiles, Random Forest and NGBoost Normal. They were not all trained or compared with identical resources in every cohort.

## Principal frozen findings

| Evaluation | Archived descriptive finding |
|---|---|
| Drammen | Direct CFM row-weighted CRPS **15.582 kWh** versus NGBoost **16.568 kWh**; equal-building mean (NGBoost minus Direct) **+0.976 kWh**, descriptive 95% building-bootstrap interval **[−2.152, +4.076]** |
| Oslo | Direct CFM row-weighted CRPS **38.593 kWh** versus NGBoost **40.609 kWh**; equal-building mean **+1.871 kWh**, descriptive 95% interval **[−2.266, +6.366]**; NGBoost performed better on **21 of 36** schools |
| Oslo calibration | Nominal-90% interval coverage: Direct CFM **84.86%**, NGBoost **79.64%** |
| BDG2 | Direct CFM generated **163** predictions above **1,000,000 kWh** for an hourly record; the original extreme tail was retained |

Both primary building-bootstrap intervals cross zero. These descriptive comparisons do **not** establish universal or statistically conclusive superiority of CFM. The BDG2 numerical extremes were not post-hoc clipped or excluded.

## Repository contents

- [`src/`](src/) — six archived Python worker scripts; historical research artefacts, not a stand-alone rerun pipeline.
- [`configs/`](configs/) — source-specific protocol and model configuration records, including frozen building-role receipts.
- [`scripts/`](scripts/) — read-only provenance and checkpoint hash verification utilities.
- [`results/verified_aggregates/`](results/verified_aggregates/) — selected original figure-source aggregate CSVs and figure metadata.
- [`reproducibility/`](reproducibility/) — protocol overview, environment disclosure and checkpoint-hash references.
- [`audit/`](audit/) — historical provenance audit receipts and G1/G2/G3 evidence notes.
- [`data/README.md`](data/README.md) — original dataset citations, access guidance and data-rights cautions.

The public repository does **not** redistribute the complete Kaggle resume state, raw meter observations, original test-label arrays or model checkpoint binaries. Checkpoint hash receipts are available for provenance review. The historical scripts contain Kaggle-specific file paths and require the original permitted datasets and full preprocessing context to execute.

## Reproducibility and scientific scope

**G1 — Environment provenance.** No authenticated `pip freeze`, container image digest or complete environment lock from the original Kaggle training period was preserved. Versions recorded during the separate P32 audit session must not be represented as training-time versions. See [`audit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md`](audit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md).

**G2 — Oslo protocol amendment.** The original P37E v1 lock bytes were lost following a Kaggle session restart. The controlling available record is the v2 metadata-only amendment created while Oslo energy labels were still sealed. The v2 hash is not the recovered v1 hash. See [`audit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md`](audit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md).

**G3 — Unequal computational budgets.** Drammen NGBoost used **40,000** FIT rows; the CFM models followed their separately archived sampling, early-stopping and GPU configurations. These models were not compute matched. See [`audit/G3_COMPUTE_BUDGET_BEST_EFFORT.md`](audit/G3_COMPUTE_BUDGET_BEST_EFFORT.md).

The scripts and archived aggregates enable inspection of the reported evidence. They do not, without the controlled dataset inputs, full original execution state and training environment, guarantee complete byte-for-byte end-to-end reproduction. **No new model training or previously opened TEST evaluation was performed to prepare this repository.**

## Data access

The original datasets remain with their respective providers. Follow [`data/README.md`](data/README.md) for original links, role protocols and licence/redistribution requirements. Dataset-provider permissions are separate from this repository's MIT licence for the author's original code.

## Citation and DOI

Use the GitHub **Cite this repository** feature based on [`CITATION.cff`](CITATION.cff) for the current software citation. A version-specific Zenodo DOI will be added **only after** a GitHub release is archived successfully on Zenodo. No DOI has been assigned in this repository metadata yet.

## Licence

The author's original research code is licensed under the [MIT License](LICENSE). Third-party datasets, software dependencies and other externally owned content remain governed by their original licences.
