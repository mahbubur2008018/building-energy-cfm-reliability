# G11: REPOSITORY RELEASE TEMPLATE
## Building Energy CFM — Code + Data Release Checklist for GitHub/Zenodo

**Status:** Template only — no files have been uploaded.
No internet access, GitHub operations or Zenodo submissions have been performed.
This document provides a ready-to-execute release checklist and README template.
**Severity:** HIGH — a public DOI or accurate unavailability disclosure is required before journal submission.

---

## DECISION REQUIRED FROM AUTHOR

Choose ONE of the following release paths:

### Path A — Full public release (recommended for Q1 reproducibility)
Create a tagged GitHub repository and Zenodo DOI containing:
- All safe source scripts (6 .py files from master ZIP — already exported to CFM_CODE_ONLY_PROVENANCE_EXPORT.zip)
- All protocol lock JSON files and audit receipts
- A new pip freeze from the closest reproducible Kaggle environment
- Data access instructions (DOIs only; no redistribution of raw meter files)
- Model checkpoint SHA-256 manifest (hashes only, not weights)

### Path B — Limited release with accurate unavailability statement
If model weights or data cannot be released:
  "Trained model weights and raw electricity meter data cannot be redistributed.
   Source code and protocol receipts are available at [URL].
   The original Kaggle training environment is no longer accessible.
   Reproducibility is therefore limited to code inspection."

---

## README Template for GitHub Release

```markdown
# Building Energy CFM — Six-Cohort Probabilistic Estimation

## Overview
This repository contains source code and protocol receipts for the six-cohort
Conditional Flow Matching (CFM) building energy estimation study submitted to
Building Services Engineering Research and Technology (BSERT).

## Cohorts
1. Drammen COFACTOR (45 buildings, Zenodo DOI: 10.5281/zenodo.14752397)
2. EDCS Miami (external replication)
3. Five-climate parallel replication
4. BDG2 (three-site frozen evaluation)
5. Drammen CAL+TEST (P21 frozen evaluation, 5 CAL + 7 TEST buildings)
6. Oslo COFACTOR-SBHUB (48 buildings, DOI: 10.60609/czgf-5e46; 12 CAL + 36 TEST)

## Scripts
- scripts/phase20_gpu_flow_worker.py  — CFM training worker (SHA-256: 2a7d300b...)
- scripts/phase21_frozen_inference_worker.py  — frozen inference (SHA-256: 98f7e864...)
- scripts/cfm_ddp_worker.py  — DDP multi-GPU wrapper
- scripts/p18_bdg2_gpu_catboost_fit_worker.py  — BDG2 CatBoost baseline
- scripts/p19_dualgpu_distributional_worker.py  — distributional baselines
- scripts/phase4_standard_cfm_worker.py  — earlier CFM phase

## Reproducibility Limitations
The original Kaggle training session (2026-10-19 to 2026-10-20 UTC) is closed.
No pip freeze or conda environment lock was saved during training. The Kaggle
environment at the time of training cannot be exactly reconstructed. Post-hoc
audit (2026-10-21) recorded: Python 3.13.15, PyTorch 2.11.0+cu128,
CatBoost 1.2.10, scikit-learn 1.6.1 — these are NOT verified training-time versions.

## Data
Raw electricity meter data must be obtained directly from the source providers.
Do NOT download data from this repository; only DOIs are provided.

- Drammen COFACTOR v3: https://zenodo.org/records/14752397
- Oslo COFACTOR-SBHUB: https://doi.org/10.60609/czgf-5e46

## Model Weights
Model checkpoint SHA-256 hashes are provided in protocol/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json.
Checkpoint bytes are not redistributed here due to size.

## Key Hashes (for verification)
- phase21_frozen_inference_worker.py: 98f7e86449ed85aa90ee7f43311b5eceb9dd235a1f16e24a594f402b3ec15ac4
- P21_FROZEN_INFERENCE_SETTINGS.json: 3070774cdac28679e91deadd07c7d88884fc4f6e1f811dcd1d503a06cf7b0a87
- Oslo v2 pre-label amendment: 5cd2adfcdc4f87a29cda40b2093a1060ec20d726fb311456961fcf7d5464bad3

## Citation
[To be completed by author after DOI is assigned]
```

---

## Release Checklist

Before uploading to GitHub/Zenodo, verify each item:

### Code
- [ ] Include all 6 scripts from CFM_CODE_ONLY_PROVENANCE_EXPORT.zip source_evidence/scripts/
- [ ] Remove any hardcoded Kaggle paths (replace with relative paths)
- [ ] Confirm no credentials, API keys or private file paths remain in scripts
- [ ] Add MIT or Apache 2.0 license file (confirm with supervisor/institution)

### Protocol receipts (all safe to release — no label data)
- [ ] outputs/phase20_cofactor_prospective_development/P20_PROTOCOL_LOCK.json
- [ ] outputs/phase20_cofactor_prospective_development/P20_FIT_ONLY_FEATURES_AND_TARGET_TRANSFORM.json
- [ ] outputs/phase21_cofactor_frozen_confirmation/P21_FROZEN_INFERENCE_SETTINGS.json
- [ ] outputs/phase21_cofactor_frozen_confirmation/P21_PROTOCOL_LOCK.json
- [ ] outputs/phase21_cofactor_frozen_confirmation/P21_CALIBRATOR_LOCK.json
- [ ] outputs/p37_oslo_single_locked_external_confirmation/P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json
- [ ] outputs/p37_oslo_single_locked_external_confirmation/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json
- [ ] outputs/p37_oslo_single_locked_external_confirmation/P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json
- [ ] All four AUDIT_OUTPUT files from this audit

### DO NOT include
- [ ] EXCLUDE: outputs/p37_oslo_single_locked_external_confirmation/PRIVATE_*
- [ ] EXCLUDE: outputs/p37_oslo_single_locked_external_confirmation/PRIVATE_TEST_*
- [ ] EXCLUDE: outputs/phase21_cofactor_frozen_confirmation/P21_ONE_TIME_FROZEN_TEST_*.csv
- [ ] EXCLUDE: raw_data/ (any raw meter readings)
- [ ] EXCLUDE: model_checkpoints/ (weights too large; SHA-256 manifest only)
- [ ] EXCLUDE: BUILDING_CFM_RESUME_LATEST.zip itself

### Environment
- [ ] Obtain a fresh pip freeze from the nearest available Kaggle Python/PyTorch environment
- [ ] Clearly label it as "best-effort approximation, not the original training environment"
- [ ] Record CUDA version and GPU type used in reproduction attempt

### Zenodo
- [ ] Create DOI with "Restricted" access if weights/data cannot be public
- [ ] Tag GitHub release matching Zenodo DOI version
- [ ] Add to manuscript as [Author, Year. Title. Zenodo. DOI: xxx]

---

## Resolution Status
G11 is TEMPLATE-READY. No actual upload has been performed.
Author must execute the checklist above after scientific and ethical review.
The CFM_CODE_ONLY_PROVENANCE_EXPORT.zip (193,869 bytes) in AUDIT_OUTPUT is
the correct starting point for the source-code component of the release.
