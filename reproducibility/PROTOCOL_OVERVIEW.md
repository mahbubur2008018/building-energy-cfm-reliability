# Protocol Overview — Six-Cohort CFM Study

## Study Design Philosophy

This study followed a pre-registration-style protocol:
- All metrics and comparisons were pre-declared before TEST label access.
- TEST labels were accessed exactly once per cohort (one-time frozen evaluation).
- Protocol lock files (JSON) were created and hashed before any test data was opened.
- All audit records use SHA-256 for cryptographic chain-of-custody.

---

## Phase Sequence (Drammen Cohorts 1 and 2)

| Phase | Description | Protocol Gate |
|-------|-------------|---------------|
| P18 | BDG2 CatBoost baseline fitting | PHASE13_2_FIT_VAL_PROTOCOL_FROZEN.json |
| P19 | Distributional baselines (NGBoost, RF) | P19_FITONLY_POLICY_LOCK.json |
| P20 | CFM training (3 variants x 3 seeds) | P20_PROTOCOL_LOCK.json |
| P20.0.2 | Bug fix: seed/checkpoint variable shadowing | P20_WORKER_SOURCE_PATCH_AUDIT.json |
| P21 | ONE-TIME FROZEN INFERENCE + Drammen TEST | P21_PROTOCOL_LOCK.json |
| P22 | Post-test scientific audit | P22_AUDIT_INPUT_LOCK.json |
| P23 | Training budget and fairness matrix | P23_INPUT_FINGERPRINT_LOCK.json |
| P32 | Reproducibility audit (separate Kaggle session) | P32_FROZEN_SCRIPT_AND_CONFIG_HASHES.csv |
| P36 | Fair-row validation sensitivity (FIT-only) | P36_PROTOCOL.json |

## Phase Sequence (Oslo Transfer — Cohort 6)

| Phase | Description | Protocol Gate |
|-------|-------------|---------------|
| P37C | Oslo schema preflight (metadata only) | BUILDING_CFM_OSLO_PRECHECK_INVENTORY.json |
| P37D | Oslo schema exception handling | — |
| P37E | Pre-label Oslo role allocation (v2 after v1 loss) | P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json |
| P37F | Feature-only QC + 14-checkpoint model lock | P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json |
| P38/P39 | Oslo calibration (12 CAL buildings) | P37_OSLO_12_BUILDING_CALIBRATOR_LOCK.json |
| P40 | ONE-TIME OSLO TEST ACCESS AND SCORING | P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json |

---

## Key Protocol Commitments

1. **Test reopening prevention:** All TEST labels accessed once only. Confirmed by
   P21_ONE_TIME_FINAL_EVALUATION_COMPLETE.json (Drammen) and 05_TEST_SCORE_COMPLETE.json (Oslo).

2. **Pre-test model selection:** Oslo primary model (Direct CFM seed 20262013) was selected
   before Oslo label access. Declared: model_selection_frozen_before_oslo_outcomes: true (P37F).

3. **Conformal calibration protocol:** CAL labels used only for calibration, never for
   model selection. Calibration performed after TEST gate was locked.

4. **Transparency obligation:** Oslo v1 lock loss disclosed. Manuscript reporting mandatory
   (report_prelabel_amendment_transparently_in_manuscript: true in P37E v2).

---

## Hash Verification Summary

| Category | PASS | FAIL | UNVERIFIED |
|----------|------|------|------------|
| Script/config anchor hashes (predeclared) | 2 | 0 | 0 |
| P32 frozen script/config receipts | 4 | 0 | 0 |
| P36 protocol cross-references | 3 | 0 | 0 |
| P37F/P40 Oslo protocol hashes | 4 | 0 | 0 |
| Model checkpoints (supplementary audit) | 14 | 0 | 0 |
| **Total verifiable hashes** | **27** | **0** | — |

Full details: audit/REPRODUCIBILITY_AUDIT_REPORT.md

---

## What This Protocol Does NOT Establish

- Exact training-time package versions (no environment lock file — G1 gap)
- Equal compute between CFM and NGBoost (NGBoost capped at 40k rows — G3 gap)
- Statistical superiority of CFM (both primary CIs span zero — G9 scientific note)
- Generalisability beyond within-city or single-source evaluations (G10 scientific note)
