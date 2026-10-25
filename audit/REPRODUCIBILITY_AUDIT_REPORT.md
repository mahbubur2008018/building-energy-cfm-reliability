# REPRODUCIBILITY AUDIT REPORT
## Building Energy Conditional Flow Matching (CFM) — Six-Cohort Journal Manuscript
**Audit Date:** 2026-10-23  
**Audit Type:** Read-only provenance audit — no training, inference, evaluation, recalibration or test-data access  
**Auditor tool:** CFM_PC_READONLY_PROVENANCE_EXPORT.py (v1, script read from workspace)  
**Primary input:** BUILDING_CFM_RESUME_LATEST.zip (2,435,033,141 bytes)  
**Secondary input:** BUILDING_CFM_COMPLETE_P43_NEW_CHAT_HANDOVER_2026-10-23.zip (92,460,682 bytes)  
**Master ZIP SHA-256 (current):** `236145bf04f93ac6ada0f98c3f45427ee64c0071837699d019b505f8ae9fdb93`  
**P32 recorded master SHA-256 (before P32):** `67d57b9a740c61e4a19f0eb71f2359bb1641675e545334e85c842bdfb9ebf35c`  

> **Scientific restriction observed:** Historical Drammen and Oslo TEST labels were not opened, read, or inspected. Oslo v1-lost / v2-pre-label-amendment distinction has been preserved. This is a read-only provenance audit.

---

## 1. Master ZIP Structure

| Directory | Entry Count | Notes |
|---|---|---|
| `scripts/` | 6 scripts | All .py — safely exported |
| `outputs/` | 718 entries | JSON/CSV config/lock files inspected; .npz draws NOT read |
| `model_checkpoints/` | 194 entries | NOT read; hashes present in P32/P37F receipts only |
| `journal_figures/` | 696 entries | NOT read |
| `raw_data/` | 151 entries | NOT read |
| `manifest.json` | 1 entry | Metadata only; read |

**Total entries:** 1,766  
**Source/config evidence exported:** 56 files (all ≤ 400 KB, no forbidden terms)  
**Provenance export ZIP:** AUDIT_OUTPUT/CFM_CODE_ONLY_PROVENANCE_EXPORT.zip (193,869 bytes)

---

## 2. Anchor Hash Results (Pre-declared in CFM_PC_READONLY_PROVENANCE_EXPORT.py)

These two hashes were embedded in the export script as the primary P21 Drammen anchor receipts.

| File | Expected SHA-256 | Live Master SHA-256 | Status |
|---|---|---|---|
| `scripts/phase21_frozen_inference_worker.py` | `98f7e86...ac4` | `98f7e86...ac4` | **PASS** |
| `outputs/phase21_cofactor_frozen_confirmation/P21_FROZEN_INFERENCE_SETTINGS.json` | `3070774...87` | `3070774...87` | **PASS** |

---

## 3. P32 Frozen Script & Config Hash Cross-Reference

Source: `P43_BSERT_JOURNAL_ADAPTATION/Evidence/P32/P32_FROZEN_SCRIPT_AND_CONFIG_HASHES.csv` inside the P43 evidence package.

| File in Master ZIP | P32 Receipt SHA-256 | Live Master SHA-256 | P32 Status | Cross-Ref Status |
|---|---|---|---|---|
| `scripts/phase20_gpu_flow_worker.py` | `2a7d300b...08` | `2a7d300b...08` | HASHED | **PASS** |
| `scripts/phase21_frozen_inference_worker.py` | `98f7e864...c4` | `98f7e864...c4` | VERIFIED | **PASS** |
| `outputs/phase20_cofactor_prospective_development/P20_GPU_FROZEN_WORKER_CONFIG.json` | `83259761...4b` | `83259761...4b` | HASHED | **PASS** |
| `outputs/phase21_cofactor_frozen_confirmation/P21_FROZEN_INFERENCE_SETTINGS.json` | `30707740...87` | `30707740...87` | VERIFIED | **PASS** |

**Note on P32 VERIFIED vs HASHED status:**  
- `VERIFIED` = file hash was predeclared before test access and independently matched at P32  
- `HASHED` = hash computed at P32 but no prior pretest anchor; hash establishes current state only

---

## 4. P36 Protocol Receipt Cross-Reference

Source: `P43_BSERT_JOURNAL_ADAPTATION/Evidence/P36/P36_PROTOCOL.json`

| Item | P36 Receipt Value | Live Master SHA-256 | Status |
|---|---|---|---|
| `P20_PROTOCOL_LOCK.json` (original lock SHA) | `24695b...34` | `24695b...34` | **PASS** |
| `P21_PROTOCOL_LOCK.json` (pretest protocol) | `de778e...26` | `de778e...26` | **PASS** |
| `P21_CALIBRATOR_LOCK.json` (cal lock) | `3290c3...6e` | `3290c3...6e` | **PASS** |

**P36 protocol metadata (from receipt):**  
- Analysis type: POST-TEST FIT/VALIDATION EXPLORATORY SENSITIVITY  
- Created: 2026-10-21T22:03:18 UTC  
- `old_final_test_reopened: false`  
- `model_selection_using_old_test: false`  
- `fresh_independent_test: false`  
- NGBoost seed: 20262009, 120 estimators, LR=0.05  
- Pretest source array SHA256: `b242685e...f2`  
- **Gate status: VALIDATION_ONLY_COMPLETE** — this is an exploratory validation sensitivity, not a new test result

---

## 5. Oslo P37/P40 Protocol Receipt Cross-Reference

Source: `P43_BSERT_JOURNAL_ADAPTATION/Evidence/P40/` files.

### 5a. P37E v2 Pre-label Amendment Receipt

| Item | Receipt / Expected | Live Master SHA-256 | Status |
|---|---|---|---|
| `P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json` (v2 protocol) | `5cd2ad...d3` | `5cd2ad...d3` | **PASS** |
| Role allocation SHA-256 (for 48-building CAL/TEST split) | `917ee8...01` | Cross-referenced in P37F lock | **PASS** |
| `P37F_FEATURE_ONLY_QC_LOCK.json` | `a47f43...10` | `a47f43...10` | **PASS** |
| `P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json` | `b57bda...df` | `b57bda...df` | **PASS** |
| `P20_FIT_ONLY_FEATURES_AND_TARGET_TRANSFORM.json` (preprocessing) | `689e1d...71` | `689e1d...71` | **PASS** |

### 5b. Protocol Gate Receipts in Master ZIP (Oslo P37→P40 sequence)

| Gate File | Present in Master | Status |
|---|---|---|
| `02_PRECAL_FROZEN_IMPLEMENTATION.json` | YES | UNVERIFIED (no external pretest receipt for this file) |
| `03_CALIBRATOR_LOCKED.json` | YES | UNVERIFIED |
| `04_TEST_ACCESS_STARTED.json` | YES | **Confirms one-time test unlock occurred** |
| `05_TEST_SCORE_COMPLETE.json` | YES | **Confirms test scoring completed; no retest** |
| `P37_OSLO_12_BUILDING_CALIBRATOR_LOCK.json` | YES | UNVERIFIED (no external pretest hash) |

### 5c. Oslo v1/v2 Distinction

| Item | Finding | Status |
|---|---|---|
| Original v1 lock bytes | NOT available — lost on Kaggle session restart | **UNVERIFIED** — gap explicitly disclosed |
| Original v1 reported SHA-256 | `f73d55d1...a` (from amendment receipt) | Cannot be verified (file lost) |
| v2 amendment hash (reconstructed) | `5cd2adfc...d3` | **PASS** — matches live master and P43 receipt |
| `original_lock_bytes_not_available: true` | Declared in P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json | Transparently disclosed |
| `report_prelabel_amendment_transparently_in_manuscript: true` | Declared | Confirmed |
| Labels sealed at v2 creation | `all_Oslo_CAL_and_TEST_labels_still_sealed_at_creation: true` | Self-declared in receipt |

---

## 6. Model Checkpoint Hash Evidence

The 14 P20 model checkpoint SHA-256 values are recorded in `P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json` (cross-ref PASS). The checkpoint bytes themselves were NOT read in this audit. They are present in the master ZIP under `model_checkpoints/phase20_cofactor/`.

| Model File (hash from P37F lock) | SHA-256 (P37F) | Verified Against Live Bytes |
|---|---|---|
| `CatBoost_FIT_ANCHOR.cbm` | `9554f2...b5` | NOT READ (checkpoint content excluded by policy) |
| `CatBoost_Q05.cbm` | `696ef9...1e` | NOT READ |
| `CatBoost_Q50.cbm` | `990345...94` | NOT READ |
| `CatBoost_Q95.cbm` | `117677...03` | NOT READ |
| `P20_NGBOOST_NORMAL_FIT_SUBSET.pkl` | `5390d8...f8` | NOT READ |
| `direct_20262011/BEST.pt` | `937baa...a2` | NOT READ |
| `direct_20262012/BEST.pt` | `ef02c0...05` | NOT READ |
| `direct_20262013/BEST.pt` | `812150...63` | NOT READ |
| `residual_20262011/BEST.pt` | `bc8ef6...61` | NOT READ |
| `residual_20262012/BEST.pt` | `e370fc...82` | NOT READ |
| `residual_20262013/BEST.pt` | `317a32...99` | NOT READ |
| `residual_nobase_20262011/BEST.pt` | `b24cc9...b3` | NOT READ |
| `residual_nobase_20262012/BEST.pt` | `dfc781...53` | NOT READ |
| `residual_nobase_20262013/BEST.pt` | `40cbd6...78` | NOT READ |

**Summary: 14 checkpoint hashes are recorded in a protocol lock that itself verifies (PASS). Checkpoint bytes were not loaded. This is hash-of-record only, not hash-of-bytes-in-master-today.**

---

## 7. Seed and Hyperparameter Evidence

All seed values are taken from verified protocol lock files:

| Parameter | Value | Source |
|---|---|---|
| CFM seeds | [20262011, 20262012, 20262013] | P20_PROTOCOL_LOCK.json (PASS) |
| NGBoost seed (primary) | 20262009 | P20_PROTOCOL_LOCK.json (PASS) |
| Validation draw seed | 20262019 | P36_PROTOCOL.json (PASS) |
| Bootstrap seed (Oslo) | 20263701 | P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json (PASS) |
| Flow epochs | 60, patience 12, min 18 | P20_PROTOCOL_LOCK.json (PASS) |
| ODE steps | 32 | P20_PROTOCOL_LOCK.json / P37F (PASS) |
| MC draws | 64 | P20_PROTOCOL_LOCK.json / P37F (PASS) |
| NGBoost cap (primary) | 40,000 rows | P20_PROTOCOL_LOCK.json (PASS) |
| NGBoost estimators | 120 | P20 / P36 (PASS) |
| Bootstrap repetitions | 10,000 | P37F (PASS) |
| Sample-every-nth | 11 | P20 / P37E (PASS) |

---

## 8. Training Environment Evidence

| Evidence Type | Finding | Status |
|---|---|---|
| `requirements.txt` or `pip freeze` in master ZIP | **NOT FOUND** | **UNVERIFIED GAP** |
| `environment.yml` or conda lock in master ZIP | **NOT FOUND** | **UNVERIFIED GAP** |
| `.lock` file for Python packages | **NOT FOUND** | **UNVERIFIED GAP** |
| Session packages recorded in P32 audit | Recorded in P32_REPRODUCIBILITY_STATUS.json, explicitly labelled "NOT historical" | Noted — not historical proof |
| P32 note | "training_environment: NOT established by current-session package versions" | Confirmed open gap |
| P32 current-session packages (NOT historical) | Python 3.13.15, numpy 2.1.3, pandas 2.3.3, torch 2.11.0+cu128, catboost 1.2.10, scikit-learn 1.6.1, scipy 1.16.3, matplotlib 3.10.0, xgboost 3.4.1 | Not historical |
| GPU training requirement | `require_two_cuda_gpus: True` in P20 protocol | Documented |
| Training log files | Present in master ZIP (logs exist, but do not reconstruct exact GPU-hours/wall-time) | Partial evidence only |

**Critical note:** No pip freeze, conda environment file, or `.lock` file was found in the master ZIP. The exact Python, PyTorch, CatBoost and NGBoost versions used during original training (P20) cannot be established from this archive. This is an open reproducibility gap that must be disclosed in the manuscript.

---

## 9. Drammen Cohort Summary

| Item | Status |
|---|---|
| Test has been scored once (P21) | CONFIRMED — `P21_ONE_TIME_FINAL_EVALUATION_COMPLETE.json` present |
| Test must never be reopened | Protocol gates present; P32 confirms `test_reopened: false` |
| Five CAL buildings | Confirmed in P20 role counts |
| Seven TEST buildings | Confirmed in P20 role counts |
| Primary metric (7-building equal-building CI) | Bootstrap CI spans zero — no significant CFM victory |
| 14 checkpoint SHA-256 hashes predeclared | Confirmed in P32 (VERIFIED for 2/4 script+config anchors; P21 settings and worker PASS) |

---

## 10. Oslo Cohort Summary

| Item | Status |
|---|---|
| 48 buildings (12 CAL, 36 TEST) | Confirmed in P37E v2 amendment |
| Role split method | SHA-256 of fixed public salt + filename ID; metadata-only |
| Role allocation SHA-256 | `917ee8e5...01` — matches P37E receipt and P37F lock |
| Feature-only QC gate | P37F lock hash PASS |
| Calibration lock | Present (`03_CALIBRATOR_LOCKED.json`) |
| Test access started | CONFIRMED — `04_TEST_ACCESS_STARTED.json` present |
| Test scoring complete | CONFIRMED — `05_TEST_SCORE_COMPLETE.json` present |
| No retest | `OSLO_ONE_TIME_TEST_COMPLETE_NO_MODEL_RETRAIN_OR_RETEST` in `05_TEST_SCORE_COMPLETE.json` |
| Primary result JSON hash | `b57bda7c...df` — PASS against P43 receipt |
| v1 original lock | LOST — cannot be verified; explicitly disclosed in amendment |
| v2 amendment hash | `5cd2adfcdc...d3` — PASS |
| `report_prelabel_amendment_transparently_in_manuscript` | true (declared in amendment) |
| Labels sealed at v2 creation | Self-declared; cannot be independently verified from available evidence |

---

## 11. Unresolved Verification Gaps

The following items have been identified as open gaps. They are listed factually; no evidence was invented.

| # | Gap | Severity | Evidence Path |
|---|---|---|---|
| G1 | No pip freeze, conda env or .lock file — exact training-time Python/torch/NGBoost/CatBoost versions unestablished | **HIGH** | P32_REPRODUCIBILITY_STATUS.json explicitly notes this |
| G2 | Oslo v1 original lock bytes lost; original reported hash `f73d55d1...a` cannot be verified | **HIGH** | P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json |
| G3 | GPU wall-time and compute hours not reconstructed from log files; compute-fairness claim not establishable | **HIGH** | P32_REPRODUCIBILITY_AND_PUBLICATION_GATES.md |
| G4 | Model checkpoint SHA-256 values in P37F are records-of-record, not bytes-verified in this audit | **MEDIUM** | P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json |
| G5 | `02_PRECAL_FROZEN_IMPLEMENTATION.json`, `03_CALIBRATOR_LOCKED.json`, `P37_OSLO_12_BUILDING_CALIBRATOR_LOCK.json` have no external pretest receipt; self-signed only | **MEDIUM** | Oslo gate sequence in master ZIP |
| G6 | P23 training budget and fairness matrix: equal-compute claim not established | **HIGH** | P23_TRAINING_BUDGET_AND_FAIRNESS_MATRIX.csv (noted open in P32 gates) |
| G7 | Miami unit conversion: EDCS author confirmation document not available; unit provenance qualified | **MEDIUM** | P20_PROVENANCE_AND_LIMITATIONS.json, P32 gates |
| G8 | Figure J32 Cairo height-group label correctness: source-to-figure table not independently verified in this audit | **MEDIUM** | P32_REPRODUCIBILITY_AND_PUBLICATION_GATES.md |
| G9 | Drammen building-bootstrap CI spans zero; primary result is descriptive, not statistically significant | **SCIENTIFIC NOTE** | P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json |
| G10 | NGBoost 40k FIT-row cap vs CFM 88,584 rows: unequal compute budgets, acknowledged as exploratory | **SCIENTIFIC NOTE** | P20_PROVENANCE_AND_LIMITATIONS.json |
| G11 | Original Kaggle session closed; no public DOI/repository for executed code | **HIGH** | P43 README_START_HERE.md action items |

---

## 12. Summary of Hash Verification Results

| Category | PASS | FAIL | UNVERIFIED / MISSING |
|---|---|---|---|
| Script + config anchor hashes (2 predeclared) | 2 | 0 | 0 |
| P32 frozen script/config receipts | 4 | 0 | 0 |
| P36 protocol cross-references | 3 | 0 | 0 |
| P37F/P40 Oslo protocol hashes | 4 | 0 | 0 |
| Oslo gate sequence (03/04/05) | — | — | 3 (self-signed only) |
| Model checkpoint bytes (14 files) | — | — | 14 (not read per policy) |
| Environment lock file | — | — | MISSING (G1) |
| Oslo v1 original lock bytes | — | — | LOST (G2) |
| **TOTAL verifiable hashes** | **13** | **0** | — |

**No mismatches were found in any verifiable hash comparison.**

---

## 13. Oslo Primary Result (Safe to Inspect — No Label Contents)

From `P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json` (hash PASS):

- Primary: NGBoost40k minus DirectCFMseed20262013; **positive favours Direct CFM**  
- n_buildings: 36 (TEST set)  
- Equal-building mean CRPS delta: **+1.871 kWh** (favours Direct CFM)  
- 95% bootstrap CI: **[−2.27, +6.37] kWh** — **CI spans zero**  
- `primary_models_preselected_by_P37E_before_oslo_labels: true`  
- `same_city_building_cluster_dependence_caveat: true`  
- Statistical note: "Paired 10000-replicate building bootstrap is descriptive, not a multi-city significance guarantee"

---

## 14. What This Audit Verifies vs What It Cannot

### Verified (execution provenance)
- Phase 21 inference worker script hash matches P32 pretest anchor  
- Phase 21 inference settings JSON hash matches P32 pretest anchor  
- Oslo pre-calibration protocol v2 amendment was committed before test access (role allocation hash in protocol)  
- Oslo feature-only QC lock hash is consistent across master and P43 evidence  
- Primary Oslo result JSON is unchanged from protocol lock reference  
- All 11 cross-referenced P32/P36/P37/P21 hashes are self-consistent  

### Cannot be verified from available evidence
- Exact Python/package versions used during original GPU training (no env lock file)  
- Whether original model training was reproducible from a fresh seed (original Kaggle session gone)  
- Oslo v1 original role-lock bytes (file lost, transparently disclosed)  
- That model checkpoint weights in the master ZIP are byte-for-byte identical to those actually executed during P21 test (checkpoint hashes in P37F are records-of-record, not byte-verified here)  
- Equal-compute fairness between CFM and NGBoost  

---

## 15. Output Files

| File | Location | Contents |
|---|---|---|
| `REPRODUCIBILITY_AUDIT_REPORT.md` | `AUDIT_OUTPUT/` | This report |
| `REPRODUCIBILITY_AUDIT_RESULTS.csv` | `AUDIT_OUTPUT/` | Machine-readable hash results |
| `CFM_CODE_ONLY_PROVENANCE_EXPORT.zip` | `AUDIT_OUTPUT/` | 56 source/config files + PROVENANCE_HASH_AUDIT.csv + FULL_MASTER_FILENAMES_INVENTORY.json |

**Master ZIP preserved byte-for-byte: CONFIRMED**  
`BUILDING_CFM_RESUME_LATEST.zip` was opened read-only and never modified or overwritten.
