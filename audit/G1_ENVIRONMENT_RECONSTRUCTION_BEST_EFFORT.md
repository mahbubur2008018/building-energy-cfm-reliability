# G1: ENVIRONMENT RECONSTRUCTION — BEST EFFORT
## Building Energy CFM — Training-Time Package Version Evidence

**Status:** PARTIAL — no pip freeze or conda env lock file was found in the master ZIP.
All version evidence is derived from safe configuration/log files only.
It is NOT a historical training receipt.
**Severity:** HIGH — mandatory manuscript disclosure required.

---

## What Is Known From Protocol Files

### Execution context
| Evidence | Value | Source |
|---|---|---|
| Kaggle working dir | /kaggle/working/BUILDING_CFM_STATE/ | P20 worker.log tracebacks |
| require_two_cuda_gpus | true | P20_PROTOCOL_LOCK.json |
| Kaggle session start | 2026-10-19T16:48:37 UTC | manifest.json earliest stage timestamp |
| P20 patch applied | 2026-10-20T14:35:53 UTC | P20_WORKER_SOURCE_PATCH_AUDIT.json |
| P21 test access | 2026-10-20T15:23:40 UTC | P21_TEST_ACCESS_STARTED.json |
| P21 test completed | 2026-10-20T15:25:39 UTC | P21_ONE_TIME_FINAL_EVALUATION_COMPLETE.json |
| Total session wall-clock span | ~22.6 hours | manifest earliest vs latest timestamp |

### P32 audit-session packages (2026-10-21 — NOT historical training versions)
These were recorded during the read-only P32 audit, a separate Kaggle session.
They MUST NOT be presented as original training-time versions.

| Package | P32 Session Version | Historically Verified? |
|---|---|---|
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

## Inferred Constraints From Code/Log Evidence

### PyTorch
- P20 worker uses torch.from_numpy(), .to(device), DDP multi-GPU
- require_two_cuda_gpus: true in P20 protocol
- Batch size 1024, ODE steps 32, LR=0.0005
- Lower bound: PyTorch >= 1.10 (DDP + CUDA required)
- Best estimate (Kaggle 2026-Q4): PyTorch ~2.x + CUDA 12.x

### CatBoost
- GPU training confirmed in P18 logs
- Tree depth 6, 400/300/250 iterations, LR 0.05
- Version not recorded; CatBoost >= 1.0 required for GPU .cbm format

### NGBoost
- n_estimators=120, lr=0.05, max_depth=3, min_samples_leaf=30
- Distribution: Normal on standardized log1p target
- Not installed in P32 audit session; training version unknown
- NGBoost >= 0.3.12 required for Normal distribution API

### Script patch record (P20 phase only)
| Patch ID | Time (UTC) | Previous SHA-256 | Fixed SHA-256 |
|---|---|---|---|
| P20.0.2-seed-checkpoint-variable-shadowing | 2026-10-20T14:35:53 | 5a16cb19...ce | 2a7d300b...08 |
Note: No checkpoint files changed by patch; locked training config unchanged.

---

## What Cannot Be Recovered

1. Exact pip freeze list — no requirements.txt, environment.yml or .lock file in master ZIP
2. Kaggle Docker image tag or hash — not recorded
3. Exact CUDA driver and cuDNN versions — not in any log
4. NGBoost exact version — unknown
5. Whether packages differed across any Kaggle restarts within the training session

---

## Required Manuscript Disclosure (template)

"Model training was performed on Kaggle (2026-10-19 to 2026-10-20 UTC) using two CUDA GPUs.
No pip freeze or conda environment file was saved during the training session.
Package versions are therefore not certifiable from the archived research state.
A post-hoc audit session (P32, 2026-10-21) recorded Python 3.13.15, PyTorch 2.11.0+cu128,
CatBoost 1.2.10, and scikit-learn 1.6.1, but these are NOT verified training-time versions.
The original Kaggle session is closed and cannot be restarted for environment verification."

---

## Resolution Status
G1 is DOCUMENTED — the gap cannot be closed without a new reproducible run.
All available evidence has been extracted and recorded above.
Manuscript disclosure template is provided above.
