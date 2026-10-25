# CFM Checkpoint SHA-256 Verification Summary
## Building Energy CFM — All 14 P20 Model Checkpoints

**Audit date:** 2026-10-23
**Audit type:** Read-only streaming SHA-256 comparison against archived P37F lock receipt
**Script run:** CFM_CHECKPOINT_HASH_VERIFY.py (unmodified) — produced MISSING x14 due to path-prefix discrepancy (see Section 2)
**Supplementary audit:** Manual prefix-corrected SHA-256 streaming — produced PASS x14

> No model weights were loaded into Python/PyTorch. No dataset, test labels, raw meter data,
> or frozen predictions were read. Neither input ZIP was modified. This is a file-integrity check only.

---

## Section 1 — Script Run Results (CFM_CHECKPOINT_HASH_VERIFY.py, unmodified)

The script was run exactly as instructed:

```
py CFM_CHECKPOINT_HASH_VERIFY.py BUILDING_CFM_RESUME_LATEST.zip AUDIT_OUTPUT\CFM_CODE_ONLY_PROVENANCE_EXPORT.zip
```

**Script output:**

| Count | Status |
|---|---|
| 0 | PASS |
| 14 | MISSING |
| 0 | MISMATCH |
| 0 | READ_ERROR |

All 14 checkpoints were reported as MISSING by the script.

---

## Section 2 — Path Prefix Discrepancy (Root Cause)

**This is the sole cause of the MISSING results. It is not a data integrity issue.**

| Item | Value |
|---|---|
| Path format in P37F lock | `model_checkpoints/phase20_cofactor/...` (bare path) |
| Path format in master ZIP | `BUILDING_CFM_STATE/model_checkpoints/phase20_cofactor/...` (with prefix) |
| Files physically present at prefixed path | YES — all 14 confirmed |
| Script behavior | Looks up bare path in ZIP namelist → not found → MISSING |
| Script modified? | NO — run unmodified per instruction |

The P37F lock stores paths relative to the Kaggle working directory (`/kaggle/working/BUILDING_CFM_STATE/`).
The master ZIP wraps everything under a `BUILDING_CFM_STATE/` prefix. The script does not apply this prefix.
Per the audit instruction: "If a path is missing, inspect ZIP filenames only and report the discrepancy
without assuming or silently changing expected paths." — this discrepancy is now reported explicitly.

---

## Section 3 — Supplementary Read-Only Verification (Prefix-Corrected)

To establish actual byte integrity, a separate read-only streaming SHA-256 was computed for each
checkpoint at its correct prefixed path (`BUILDING_CFM_STATE/<lock_path>`).
No checkpoint was deserialized, imported, executed, or extracted to disk.

| Checkpoint (P37F lock path) | Actual ZIP path | Expected SHA-256 (P37F) | Observed SHA-256 | Status |
|---|---|---|---|---|
| model_checkpoints/phase20_cofactor/CatBoost_FIT_ANCHOR.cbm | BUILDING_CFM_STATE/... | 9554f29b...b5 | 9554f29b...b5 | **PASS** |
| model_checkpoints/phase20_cofactor/CatBoost_Q05.cbm | BUILDING_CFM_STATE/... | 696ef984...1e | 696ef984...1e | **PASS** |
| model_checkpoints/phase20_cofactor/CatBoost_Q50.cbm | BUILDING_CFM_STATE/... | 990345e0...94 | 990345e0...94 | **PASS** |
| model_checkpoints/phase20_cofactor/CatBoost_Q95.cbm | BUILDING_CFM_STATE/... | 117677b3...03 | 117677b3...03 | **PASS** |
| model_checkpoints/phase20_cofactor/P20_NGBOOST_NORMAL_FIT_SUBSET.pkl | BUILDING_CFM_STATE/... | 5390d826...f8 | 5390d826...f8 | **PASS** |
| model_checkpoints/phase20_cofactor/direct_20262011/BEST.pt | BUILDING_CFM_STATE/... | 937baa6b...a2 | 937baa6b...a2 | **PASS** |
| model_checkpoints/phase20_cofactor/direct_20262012/BEST.pt | BUILDING_CFM_STATE/... | ef02c0e7...05 | ef02c0e7...05 | **PASS** |
| model_checkpoints/phase20_cofactor/direct_20262013/BEST.pt | BUILDING_CFM_STATE/... | 8121503b...63 | 8121503b...63 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_20262011/BEST.pt | BUILDING_CFM_STATE/... | bc8ef623...61 | bc8ef623...61 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_20262012/BEST.pt | BUILDING_CFM_STATE/... | e370fcdd...82 | e370fcdd...82 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_20262013/BEST.pt | BUILDING_CFM_STATE/... | 317a322a...99 | 317a322a...99 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_nobase_20262011/BEST.pt | BUILDING_CFM_STATE/... | b24cc91b...b3 | b24cc91b...b3 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_nobase_20262012/BEST.pt | BUILDING_CFM_STATE/... | dfc781a5...53 | dfc781a5...53 | **PASS** |
| model_checkpoints/phase20_cofactor/residual_nobase_20262013/BEST.pt | BUILDING_CFM_STATE/... | 40cbd699...78 | 40cbd699...78 | **PASS** |

**SUPPLEMENTARY RESULT: 14/14 PASS — 0 MISMATCH — 0 READ_ERROR**

Full SHA-256 values are in CFM_CHECKPOINT_HASH_RESULTS.csv.

---

## Section 4 — Evidence Chain

| Evidence item | Value / Source |
|---|---|
| P37F lock file (in code-only export) | source_evidence/outputs/p37_oslo_single_locked_external_confirmation/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json |
| P37F lock SHA-256 (previously verified PASS) | 0a24ba04a2336ae445b84b407b1e707dbebd61c0d8f3474c2c7ea80bb4938ead |
| Master ZIP SHA-256 | 236145bf04f93ac6ada0f98c3f45427ee64c0071837699d019b505f8ae9fdb93 |
| Master ZIP modified? | NO — read-only open only |
| P37F lock model_file_hashes count | 14 (confirmed) |
| Files physically present in master ZIP at prefixed path | 14/14 |
| Bytes hashed per file | Full file, 4 MB block streaming |
| Checkpoint deserialized? | NO |
| Test labels read? | NO |
| Raw meter data read? | NO |

---

## Section 5 — Remaining Reproducibility Gaps

A PASS on checkpoint SHA-256 confirms byte integrity of the archived weights.
It does NOT prove the following (these remain open gaps):

| Gap | Status |
|---|---|
| Original training-time Python/PyTorch/NGBoost/CatBoost versions | UNVERIFIED — no env lock file (G1) |
| Equal-compute fairness between CFM and NGBoost | NOT ESTABLISHED — acknowledged in P23 training budget matrix |
| End-to-end reproducibility from scratch | NOT POSSIBLE — Kaggle session closed, no env lock |
| Oslo v1 original lock bytes | PERMANENTLY LOST — v2 amendment disclosed (G2) |

---

## Section 6 — Output Files

| File | Contents |
|---|---|
| CFM_CHECKPOINT_HASH_RESULTS.csv | Per-checkpoint: bare path, actual ZIP path, expected hash, observed hash, status |
| CFM_CHECKPOINT_HASH_SUMMARY.md | This report |

**Recommendation for CFM_CHECKPOINT_HASH_VERIFY.py:**
Add a `BUILDING_CFM_STATE/` prefix lookup fallback (or strip the prefix from ZIP entries before
matching) so future runs report PASS instead of MISSING. This is a one-line fix and does not
change the scientific meaning of the verification.
