# Building Energy Conditional Flow Matching - Six-Cohort Reliability Study

> **Repository status:** Public release — MIT License (Copyright 2026 Md. Mahbubur Rahman)
> **Target journal:** Building Services Engineering Research and Technology (BSER&T)
> **Prepared:** 2026-10-24 | **Published:** 2026-10-25
> **Author:** Md. Mahbubur Rahman | ORCID: https://orcid.org/0009-0004-0252-9140

---

## Overview

This repository contains the source code, historical protocol locks, and verified aggregate results for a
six-cohort probabilistic building energy estimation study using **Conditional Flow Matching (CFM)**.
The study evaluates CFM against established distributional baselines across diverse building datasets
and geographical contexts, targeting a journal submission to BSER&T.

**This is a single-author study.** Author identity and ORCID are to be completed before public release
(see CITATION.cff).

---

## Research Objectives

1. Evaluate whether CFM provides competitive probabilistic energy forecasts compared to strong gradient
   boosting and distributional regression baselines across geographically and architecturally diverse
   building datasets.
2. Assess calibration reliability of conformal prediction intervals across source-specific holdout sets.
3. Conduct an external transfer experiment: apply frozen Drammen-trained models unchanged to an
   independent Oslo school building dataset.
4. Characterise the descriptive magnitude and statistical uncertainty of any observed performance
   differences, without overclaiming statistical significance.

---

## Six Cohorts

| # | Cohort | Dataset | Buildings | Study role |
|---|--------|---------|-----------|------------|
| 1 | **Drammen COFACTOR FIT/VAL** | Drammen COFACTOR v3 (Zenodo: 10.5281/zenodo.14752397) | 33 FIT + 5 CAL (prospective) | Training cohort for all Drammen-trained models |
| 2 | **Drammen COFACTOR TEST** | Drammen COFACTOR v3 | 7 TEST buildings | Frozen one-time evaluation (P21); primary Drammen result |
| 3 | **EDCS U-geometry (Cairo)** | EDCS (Cairo, public) | Grouped by building height | Source-specific OOD evaluation; height-shift sensitivity |
| 4 | **Miami five-climate holdout** | EDCS five-climate | Miami climate held out | Held-out climate; frozen calibration-to-Miami transfer |
| 5 | **BDG2 three-site** | Building Data Genome 2 | Three sites | Point-error and extremes evaluation |
| 6 | **Oslo COFACTOR-SBHUB** | Oslo COFACTOR-SBHUB (DOI: 10.60609/czgf-5e46) | 12 CAL + 36 TEST (48 total) | External transfer; frozen Drammen models applied unchanged |

> **Critical note:** Each cohort used models appropriate to its role. Only the frozen Drammen-trained
> models (P20/P21 checkpoints) were transferred unchanged to Oslo. The six cohorts did not share a
> single trained model. No cross-cohort superiority claim is made.

---

## Three Source-Specific Evaluations vs. Transfer Study

This study includes **four historical source-specific evaluations** and **one transfer study**:

### Source-specific evaluations (model trained on each source)
1. Cairo / EDCS: height-group OOD shift analysis
2. EDCS U-geometry: calibration-to-holdout coverage assessment
3. Miami: five-climate held-out climate evaluation
4. BDG2: three-site extreme-event and point-error evaluation

### Transfer study (frozen Drammen models applied unchanged)
5. **Drammen-to-Oslo transfer (Cohort 6):** Seven-building Drammen TEST result (Cohorts 1-2) followed
   by 36-school Oslo TEST using the identical frozen checkpoints. These represent distinct experimental
   arms; the Oslo result is a transfer evaluation, not an in-domain replication.

---

## Model Variants

Three CFM architectures were evaluated:

| Variant | CatBoost anchor in flow conditioning? | CatBoost in reconstruction? | Target construction |
|---------|--------------------------------------|----------------------------|---------------------|
| **Direct CFM** | No | No | Raw energy target directly |
| **Full Residual CFM** | Yes - anchor included in flow conditioning | Yes | CatBoost residual; anchor added at reconstruction |
| **No-base Residual CFM** | **No** - anchor excluded from flow conditioning | Yes | CatBoost residual for target/reconstruction; anchor **not** passed to flow |

Each CFM variant was trained with three random seeds: {20262011, 20262012, 20262013}.

---

## Baseline Methods

| Baseline | Description | Notes |
|----------|-------------|-------|
| **CatBoost point anchor** | Point prediction; tree depth 6, 400 iterations | Full FIT rows |
| **CatBoost Quantiles (Q05/Q50/Q95)** | Quantile regression; 300 iterations | Full FIT rows |
| **Random Forest** | Scikit-learn ensemble | Source-specific use |
| **NGBoost Normal** | NGBoost with Normal distribution; 120 estimators, LR=0.05 | Capped at 40,000 FIT rows - **unequal compute** |

---

## Oslo Cohort: Building Roles

| Role | Count | Method |
|------|-------|--------|
| Calibration (CAL) | 12 buildings | SHA-256 of fixed public salt + filename |
| Test (TEST) | 36 buildings (7 schools) | Same deterministic allocation |
| Total | 48 buildings | Oslo COFACTOR-SBHUB dataset |

> **Oslo v1 provenance disclosure:** The original P37E v1 lock file was lost during a Kaggle session
> restart. A v2 amendment was created immediately after, with all labels still sealed. This is
> transparently disclosed in udit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md.

> **Oslo primary result:** Mean equal-building CRPS delta (NGBoost40k minus DirectCFM seed 20262013)
> = **+1.871 kWh** (favours Direct CFM). Bootstrap 95% CI: **[-2.27, +6.37] kWh** - CI spans zero.
> Result is descriptive only; no claim of statistical significance is made.

---

## Drammen Cohort: Building Roles and Primary Result

| Role | Count | Description |
|------|-------|-------------|
| FIT | 33 buildings | Model training |
| CAL | 5 buildings | Conformal calibration |
| TEST | 7 buildings | One-time frozen evaluation (P21, 2026-10-20 UTC) |

> **Drammen primary result:** 7-building equal-building bootstrap CI for best CFM vs best baseline
> **spans zero** ([-2.15, +4.08] kWh). Result is descriptive only.

---

## Key Reproducibility Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| CFM seeds | 20262011, 20262012, 20262013 | configs/drammen/P20_PROTOCOL_LOCK.json |
| NGBoost seed | 20262009 | configs/drammen/P20_PROTOCOL_LOCK.json |
| Validation draw seed | 20262019 | P36 protocol |
| Oslo bootstrap seed | 20263701 | configs/oslo/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json |
| Flow epochs (max / min / patience) | 60 / 18 / 12 | configs/drammen/P20_PROTOCOL_LOCK.json |
| ODE solver steps | 32 | configs/drammen/P20_PROTOCOL_LOCK.json |
| MC draws | 64 | configs/drammen/P20_PROTOCOL_LOCK.json |
| NGBoost FIT-row cap | 40,000 | configs/drammen/P20_PROTOCOL_LOCK.json |
| Sample-every-nth (FIT subsampling) | 11 | configs/drammen/P20_PROTOCOL_LOCK.json |
| Bootstrap repetitions (Oslo) | 10,000 | configs/oslo/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json |
| GPU requirement | 2x CUDA GPUs | configs/drammen/P20_PROTOCOL_LOCK.json |

---

## Source Code

Six historical scripts are provided in src/, extracted from the verified provenance export
(SHA-256 anchors in udit/REPRODUCIBILITY_AUDIT_RESULTS.csv):

| Script | P32 Hash Status | Role |
|--------|----------------|------|
| phase20_gpu_flow_worker.py | HASHED (PASS) | CFM training worker (DDP, multi-GPU) |
| phase21_frozen_inference_worker.py | VERIFIED (PASS, pre-test anchor) | Frozen inference + calibration |
| cfm_ddp_worker.py | Not in P32 anchor set | DDP multi-GPU wrapper |
| p18_bdg2_gpu_catboost_fit_worker.py | Not in P32 anchor set | BDG2 CatBoost baseline training |
| p19_dualgpu_distributional_worker.py | Not in P32 anchor set | Distributional baselines |
| phase4_standard_cfm_worker.py | Not in P32 anchor set | Earlier-phase CFM worker |

> All scripts are presented exactly as extracted from the archived master ZIP. No code was
> modified or reconstructed. Scripts contain Kaggle-specific absolute paths (/kaggle/working/)
> which must be adapted for any reproduction attempt. These are historical records, not
> ready-to-run scripts.

**Code patch record:**
- Patch P20.0.2-seed-checkpoint-variable-shadowing: applied 2026-10-20T14:35:53 UTC.
- Previous SHA-256: 5a16cb19...ce -> Fixed: 2a7d300b...08. No checkpoint files changed.
- See configs/drammen/P20_WORKER_SOURCE_PATCH_AUDIT.json.

---

## Reproducibility Limitations

> **IMPORTANT: Full end-to-end reproduction from this repository alone is not possible.**

### 1. Training environment not authenticated (HIGH severity)
No requirements.txt, conda environment.yml, or pip freeze was saved during the original
Kaggle training session (2026-10-19 to 2026-10-20 UTC). Package versions cannot be certified.
Post-hoc audit (P32, 2026-10-21) recorded: Python 3.13.15, PyTorch 2.11.0+cu128,
CatBoost 1.2.10, scikit-learn 1.6.1 - these are NOT verified training-time versions.
See udit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md.

### 2. Oslo v1 lock permanently lost (HIGH severity)
The original P37E v1 role-allocation lock was lost on Kaggle session restart. A v2 amendment
was created with all labels still sealed; its SHA-256 is verified (PASS). The v1 bytes
cannot be recovered. See udit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md.

### 3. Unequal compute budgets (HIGH severity)
NGBoost trained on 40,000 FIT rows; CFM used all available FIT rows with internal early stopping
on two CUDA GPUs. No equal-compute superiority claim is made.
See udit/G3_COMPUTE_BUDGET_BEST_EFFORT.md.

### 4. Model checkpoint weights not redistributed
Checkpoint SHA-256 hashes (14/14 PASS verified against P37F lock) are in
udit/CFM_CHECKPOINT_HASH_RESULTS.csv. Weight binaries are excluded due to size (~2.3 GiB master archive).

### 5. Kaggle training session closed
The original training session (Kaggle, 2026-10-19 to 2026-10-20 UTC) is closed and cannot
be restarted for environment verification. Approximate training wall-time: 1.0-1.5 hours on two
CUDA GPUs, reconstructed from timestamp evidence.

### 6. Both primary CIs span zero
- Drammen 7-building bootstrap CI: [-2.15, +4.08] kWh - spans zero.
- Oslo 36-building bootstrap CI: [-2.27, +6.37] kWh - spans zero.
Both results are descriptive only. No claim of statistically significant CFM superiority is made.

---

## Data Access

Raw electricity meter data **cannot be distributed from this repository**. Obtain from official sources:

| Dataset | Source | DOI / Link |
|---------|--------|-----------|
| Drammen COFACTOR v3 | Zenodo | https://zenodo.org/records/14752397 |
| Oslo COFACTOR-SBHUB | Norwegian data archive | https://doi.org/10.60609/czgf-5e46 |
| EDCS (Cairo, five-climate) | EDCS consortium | See data/README.md |
| BDG2 | Building Data Genome Project | See data/README.md |

See data/README.md for full dataset descriptions, licences, split protocols, and access instructions.

---

## Verified Hash Records

| Verification | Result | Source |
|-------------|--------|--------|
| Phase 21 frozen inference worker (pre-test anchor) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| Phase 21 inference settings (pre-test anchor) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| Phase 20 training worker (P32 receipt) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| Phase 20 training config (P32 receipt) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| Oslo v2 amendment (P37F + P43 receipts) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| Oslo primary result JSON (P43 receipt) | PASS | audit/REPRODUCIBILITY_AUDIT_RESULTS.csv |
| All 14 P20 model checkpoints (P37F lock) | 14/14 PASS | audit/CFM_CHECKPOINT_HASH_RESULTS.csv |
| Total verifiable hashes | 13/13 PASS | audit/REPRODUCIBILITY_AUDIT_REPORT.md |

---

## Repository Structure

`
building-energy-cfm-reliability/
|-- README.md
|-- CITATION.cff
|-- LICENSING_TO_CONFIRM.md
|-- .gitignore
|-- src/                              # 6 vetted historical scripts
|-- configs/                          # Protocol locks by cohort
|   |-- drammen/                      # 14 Drammen P20/P21 lock files
|   |-- oslo/                         # 10 Oslo P37/P40 lock files
|   |-- edcs/                         # 3 EDCS lock files
|   |-- miami/                        # 3 Miami lock files
|   +-- bdg2/                         # 2 BDG2 lock files
|-- scripts/                          # Provenance verification utilities
|-- results/
|   +-- verified_aggregates/
|       +-- figures_1_8/              # 23 verified aggregate CSVs (J-series)
|-- reproducibility/                  # Environment and protocol disclosures
|-- data/
|   +-- README.md                     # Dataset access and licence instructions
|-- audit/                            # Full provenance audit (13/13 PASS)
|-- PUBLIC_RELEASE_FILE_MANIFEST.csv
|-- PUBLIC_RELEASE_PROVENANCE_AUDIT.csv
|-- PUBLIC_RELEASE_SAFETY_REPORT.md
|-- PUBLIC_RELEASE_READINESS_CHECKLIST.md
+-- PUBLIC_RELEASE_README_PREVIEW.md
`

---

## Citation

> **Citation DOI not yet assigned.** This repository has not been submitted to Zenodo.
> Do not cite until a DOI is assigned and author review is complete.

Once a Zenodo DOI is assigned, cite as:
[Author name(s)], [Year]. Building Energy Conditional Flow Matching - Six-Cohort Reliability Study.
Zenodo. DOI: [TO BE ASSIGNED AFTER ZENODO SUBMISSION]

See CITATION.cff for machine-readable citation metadata.

---

## Licence

This repository is released under the **MIT License**.
See [LICENSE](LICENSE) for the full licence text.
Copyright (c) 2026 Md. Mahbubur Rahman.

---

*This repository was prepared by automated curation tools on 2026-10-24 and is pending author review.*
