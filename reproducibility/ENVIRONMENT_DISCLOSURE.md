# Environment Disclosure — Best-Effort Reconstruction
## Building Energy CFM Training-Time Package Evidence

**Status:** PARTIAL — No pip freeze, conda env, or lock file was saved during training.
**Severity:** HIGH — Mandatory manuscript disclosure required.

---

## Execution Context

| Evidence | Value | Source |
|----------|-------|--------|
| Platform | Kaggle cloud notebook | P20 worker.log tracebacks |
| Kaggle working dir | /kaggle/working/BUILDING_CFM_STATE/ | P20 worker.log |
| GPU requirement | 2x CUDA GPUs | P20_PROTOCOL_LOCK.json |
| Session start | 2026-10-19T16:48:37 UTC | manifest.json earliest timestamp |
| P20 patch applied | 2026-10-20T14:35:53 UTC | P20_WORKER_SOURCE_PATCH_AUDIT.json |
| P21 test access | 2026-10-20T15:23:40 UTC | P21_TEST_ACCESS_STARTED.json |
| P21 test completed | 2026-10-20T15:25:39 UTC | P21_ONE_TIME_FINAL_EVALUATION_COMPLETE.json |
| Total session span | ~22.6 hours | manifest timestamps |
| Estimated P20 training time | ~1.0-1.5 hours on two CUDA GPUs | Timestamp evidence |

---

## Post-Hoc Audit Session Packages (P32 — NOT historical training versions)

These were recorded during the read-only P32 audit in a SEPARATE Kaggle session
on 2026-10-21. They MUST NOT be presented as original training-time versions.

| Package | P32 Session Version | Historically Verified? |
|---------|--------------------|-----------------------|
| Python | 3.13.15 | NO |
| numpy | 2.1.3 | NO |
| pandas | 2.3.3 | NO |
| torch | 2.11.0+cu128 | NO |
| catboost | 1.2.10 | NO |
| ngboost | not installed in P32 session | NO |
| scikit-learn | 1.6.1 | NO |
| scipy | 1.16.3 | NO |
| matplotlib | 3.10.0 | NO |
| xgboost | 3.4.1 | NO |

Source: P32_REPRODUCIBILITY_STATUS.json:
  "training_environment": "NOT established by current-session package versions"

---

## What Cannot Be Recovered

1. Exact pip freeze — no requirements.txt, environment.yml or lock file in master archive
2. Kaggle Docker image tag or hash — not recorded
3. Exact CUDA driver and cuDNN versions — not in any log
4. NGBoost exact version — not installed in P32 session; training version unknown
5. Whether packages differed across Kaggle restarts within the training session

---

## Inferred Lower Bounds From Script Analysis

- PyTorch >= 1.10 (DDP + CUDA required by training scripts)
- Best estimate for Kaggle Q4 2026: PyTorch ~2.x + CUDA 12.x
- CatBoost >= 1.0 (GPU .cbm format required)
- NGBoost >= 0.3.12 (Normal distribution API required)

---

## Required Manuscript Disclosure

"Model training was performed on Kaggle using two CUDA GPUs (session opened
2026-10-19, closed 2026-10-20 UTC). No pip freeze or conda environment file was
saved during the training session. Package versions are therefore not certifiable
from the archived research state. A post-hoc audit session (P32, 2026-10-21)
recorded Python 3.13.15, PyTorch 2.11.0+cu128, CatBoost 1.2.10, and
scikit-learn 1.6.1, but these are NOT verified training-time versions.
The original Kaggle session is closed and cannot be restarted for environment
verification."

Full evidence: audit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md
