# Model Checkpoint SHA-256 Manifest

**Source lock:** configs/oslo/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json
**Supplementary verification:** audit/CFM_CHECKPOINT_HASH_RESULTS.csv
**Supplementary audit result:** 14/14 PASS (streaming SHA-256 against P37F lock)

> Checkpoint weight binaries are NOT distributed in this repository.
> These are records-of-record only. PASS confirms byte integrity against the
> archived lock; it does NOT prove end-to-end reproducibility or authenticate
> the original training environment.
>
> Path prefix note: P37F lock stores paths relative to Kaggle working dir
> (model_checkpoints/...). The master ZIP wraps them under BUILDING_CFM_STATE/.
> See audit/CFM_CHECKPOINT_HASH_SUMMARY.md for full explanation.

---

## CatBoost Models (Trained on Drammen FIT — all 88,584 rows)

| Lock path | SHA-256 | Verification |
|-----------|---------|-------------|
| model_checkpoints/phase20_cofactor/CatBoost_FIT_ANCHOR.cbm | 9554f29b8cebc51a863540c3b98dbcd73fab8f531ab98828d26453ece1714db5 | PASS |
| model_checkpoints/phase20_cofactor/CatBoost_Q05.cbm | 696ef984728aa6b5efd3448c5e203c6351e2fb9f0c34922f23d6f6c27314031e | PASS |
| model_checkpoints/phase20_cofactor/CatBoost_Q50.cbm | 990345e086f0bacbe424a4128ea2ec1bd963ad89a2706a2e0a23b23e6ddd9e94 | PASS |
| model_checkpoints/phase20_cofactor/CatBoost_Q95.cbm | 117677b3b88889d9db9c64a2d60806778e53b0bf97b270699b80f1a34d98d803 | PASS |

## NGBoost Normal Model (40,000 FIT row cap — unequal compute, see G3)

| Lock path | SHA-256 | Verification |
|-----------|---------|-------------|
| model_checkpoints/phase20_cofactor/P20_NGBOOST_NORMAL_FIT_SUBSET.pkl | 5390d826a47960333d74033457142b83c4ef6b92bd440f62fd079cd3fad1d6f8 | PASS |

## Direct CFM — No CatBoost anchor in flow conditioning (3 seeds)

| Lock path | SHA-256 | Verification |
|-----------|---------|-------------|
| model_checkpoints/phase20_cofactor/direct_20262011/BEST.pt | 937baa6b08cbb085cffd2b6206cdf51bb1ce8cc73ac42d3df1138dcde25d49a2 | PASS |
| model_checkpoints/phase20_cofactor/direct_20262012/BEST.pt | ef02c0e7ef59433c607c2b25e41434e51f04cee51cac85d2bceb49ebdd8bfd05 | PASS |
| model_checkpoints/phase20_cofactor/direct_20262013/BEST.pt | 8121503bcf960f7cd450b256e882a8932ef67b15131d31df472e3fe8b433a963 | PASS |

## Full Residual CFM — CatBoost anchor in conditioning AND reconstruction (3 seeds)

| Lock path | SHA-256 | Verification |
|-----------|---------|-------------|
| model_checkpoints/phase20_cofactor/residual_20262011/BEST.pt | bc8ef623d921430185f472e6e526ce8a398fbeaa279f78cdb3977c6478394e61 | PASS |
| model_checkpoints/phase20_cofactor/residual_20262012/BEST.pt | e370fcdd2aede0dcd80b7e36700d06b84429b5f3138ea8a9fd19817340314b82 | PASS |
| model_checkpoints/phase20_cofactor/residual_20262013/BEST.pt | 317a322ab5aaf49795ad6d64f05d6f1c0738ceefdc98ca9a80ed903b33a9b599 | PASS |

## No-base Residual CFM — CatBoost in reconstruction ONLY, NOT in flow conditioning (3 seeds)

| Lock path | SHA-256 | Verification |
|-----------|---------|-------------|
| model_checkpoints/phase20_cofactor/residual_nobase_20262011/BEST.pt | b24cc91b40e724b166e760e758743aef68275d1729b3f3be52536d5fd3516ab3 | PASS |
| model_checkpoints/phase20_cofactor/residual_nobase_20262012/BEST.pt | dfc781a5734369b06b33e0f288fbff9f4527b6f18bf852897a8d15ebdff7d053 | PASS |
| model_checkpoints/phase20_cofactor/residual_nobase_20262013/BEST.pt | 40cbd69902a1f304d43d54312a6fd4ede2e989748fffc86b2d8a6e51c1406178 | PASS |
