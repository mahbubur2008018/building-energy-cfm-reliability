# G3: COMPUTE BUDGET AND WALL-TIME — BEST EFFORT RECONSTRUCTION
## Building Energy CFM — GPU Training Time Evidence

**Status:** PARTIAL — log files establish a session time window and epoch-level
per-model timing (from P8 earlier-phase logs). P20 logs do not contain timestamps.
An exact GPU-hour claim cannot be made.
**Severity:** HIGH — unequal compute budgets must be disclosed.

---

## Session Timeline (from manifest.json timestamps)

| Event | UTC Timestamp | Derived From |
|---|---|---|
| Earliest manifest stage | 2026-10-19T16:48:37 UTC | manifest.json phase1_hot_climate_source |
| Latest pre-P20 stage | 2026-10-20T13:12:14 UTC | phase19_fitonly_development_distributional_comparators |
| P20 patch applied | 2026-10-20T14:35:53 UTC | P20_WORKER_SOURCE_PATCH_AUDIT.json |
| P21 test access started | 2026-10-20T15:23:40 UTC | P21_TEST_ACCESS_STARTED.json |
| P21 test completed | 2026-10-20T15:25:39 UTC | P21_ONE_TIME_FINAL_EVALUATION_COMPLETE.json |
| Kaggle session total span | ~22.6 hours | manifest earliest to P21 completion |
| P20 training window | ~13:12 to ~14:35 UTC on 2026-10-20 | manifest + patch timestamp |

Note: P20 GPU training ran within an ~83-minute window (13:12 to 14:35 UTC on 2026-10-20),
plus earlier residual_nobase seeds before the patch. The patch itself records completion
at 14:35; P21 (inference only) completed at 15:25. P20 training therefore took
approximately 1.0-1.5 hours total wall-clock time on two CUDA GPUs.

---

## Per-Epoch Timing Evidence (from P8 training logs — earlier phase, same code family)

P8 used the same CFM architecture on BDG2 in-domain data (smaller dataset).
P8 logs show: 80 epochs in ~15.8 seconds wall-clock (per-seed, per-variant).
This suggests very rapid per-epoch iteration for smaller datasets.

For P20 (Drammen 45 buildings, 88584 FIT rows sampled every 11th):
- Flow epochs: up to 60, min 18, patience 12
- Effective training rows: 88584 / 11 = ~8053 sampled rows for CFM
- 9 CFM models total (3 variants x 3 seeds) on 2 GPUs in parallel
- NGBoost: 40,000 rows x 120 estimators on CPU

---

## Training Budget Fairness Matrix (from P23_TRAINING_BUDGET_AND_FAIRNESS_MATRIX.csv)

| Model | FIT Rows Available | Rows Used | Iterations/Epochs | Seeds | Compute Matched? |
|---|---|---|---|---|---|
| CatBoost point anchor | 88,584 | Full FIT | 400 tree iterations | 20262000 | Deterministic baseline |
| CatBoost quantiles Q05/Q50/Q95 | 88,584 | Full FIT | 300 tree iterations | 20262000 | Quantile only |
| NGBoost Normal | 88,584 | 40,000 (cap) | 120 estimators | 20262009 | NOT compute matched |
| CFM direct | 88,584 | FIT-internal stopping holdout | max 60 epochs | 20262011/12/13 | NOT equal-budget |
| CFM residual | 88,584 | FIT-internal stopping holdout | max 60 epochs | 20262011/12/13 | NOT equal-budget |
| CFM residual_nobase | 88,584 | FIT-internal stopping holdout | max 60 epochs | 20262011/12/13 | NOT equal-budget |

Explicit disclosure in P22_SCIENTIFIC_AUDIT.json:
  "NGBoost fitted on 40k FIT rows; flow models used different training budgets;
   no compute-matched superiority claim"

---

## What Cannot Be Established

1. Exact GPU-hours for CFM training (logs contain only epoch-level results, no wall-time in P20 logs)
2. Whether early stopping caused materially different total compute per seed
3. Whether NGBoost CPU time exceeded CFM GPU time or vice versa
4. Carbon or energy cost of training run

---

## Required Manuscript Disclosure (template)

"CatBoost baselines were trained on all 88,584 FIT rows. NGBoost was capped at 40,000 FIT rows
due to computational constraints. CFM models were trained with internal early stopping (patience=12,
max 60 epochs) on two CUDA GPUs, with a 15% inner-site validation holdout. These represent
different computational budgets and architectures; no equal-compute superiority claim is made.
Approximate total P20 training wall-time was 1.0-1.5 hours on two CUDA GPUs (2026-10-20 UTC),
reconstructed from protocol timestamps; exact GPU-hours were not logged."

---

## Resolution Status
G3 is DOCUMENTED — a narrow training window (1.0-1.5 hrs, 2026-10-20 UTC) is established
from timestamp evidence. Exact GPU-hours cannot be recovered. Unequal-budget limitation is
already explicitly recorded in multiple protocol files. Manuscript disclosure template provided.
