# README Preview — For Author Review
## What GitHub visitors will see when they open the repository

> This is a preview of the repository landing page for author verification.
> The actual README.md is in the root of PUBLIC_GITHUB_RELEASE/.

---

The README.md (created 2026-10-24) covers:

1. **Repository status banner** — clearly states "safe release candidate under author review"
2. **Research objectives** — four clearly stated objectives; no overclaiming
3. **Six cohorts table** — with official DOIs for Drammen and Oslo datasets
4. **Critical note on shared models** — explicitly states cohorts did NOT share a single model
5. **Four source-specific evaluations vs. one transfer study** — correctly distinguished
6. **Three model variant table** — Direct CFM, Full Residual CFM, No-base Residual CFM
   with correct descriptions of CatBoost anchor usage in each
7. **Baseline methods** — CatBoost, CatBoost Quantiles, Random Forest, NGBoost Normal;
   NGBoost compute imbalance explicitly flagged
8. **Drammen-Oslo transfer study** — correctly described as transfer not replication;
   Oslo v1 gap disclosed
9. **Key reproducibility parameters** — seeds, epochs, ODE steps, MC draws
10. **Source code section** — 6 scripts with P32 hash status; Kaggle path caveat
11. **Code patch record** — P20.0.2 patch documented
12. **Six reproducibility limitations** — clearly numbered; all two CIs noted as spanning zero
13. **Data access table** — DOIs only; no data redistribution
14. **Verified hash records** — summarises 13/13 + 14/14 checkpoint PASS results
15. **Repository structure tree** — accurate directory listing
16. **Citation section** — explicitly states DOI not yet assigned; no fabricated citation
17. **Licence** — deferred to LICENSING_TO_CONFIRM.md

---

## Key Reviewable Language

The following phrases in README.md require author verification before public release:

| Location | Phrase | Action |
|----------|--------|--------|
| Top banner | "single-author study" | Confirm this is accurate |
| Cohort 1 | "33 FIT + 5 CAL" | Verify building counts |
| Model variants table | No-base description: "anchor not passed to flow" | Confirm technical accuracy |
| Baselines | "Random Forest — source-specific use" | Confirm scope |
| Oslo result | "+1.871 kWh, CI [-2.27, +6.37]" | Verify against P40 JSON |
| Drammen result | "CI spans zero [-2.15, +4.08] kWh" | Verify against P21 audit |
| Limitation 1 | P32 package versions listed | Confirm "NOT verified" label is correct |
| Citation | "DOI not yet assigned" | Ensure no DOI is added before Zenodo submission |

---

## Internal Link Validation

The README references the following files that should exist in the release:

| Link | File Present? |
|------|--------------|
| CITATION.cff | YES |
| LICENSING_TO_CONFIRM.md | YES |
| data/README.md | YES |
| audit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md | YES |
| audit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md | YES |
| audit/G3_COMPUTE_BUDGET_BEST_EFFORT.md | YES |
| audit/REPRODUCIBILITY_AUDIT_RESULTS.csv | YES |
| audit/CFM_CHECKPOINT_HASH_RESULTS.csv | YES |
| configs/drammen/P20_PROTOCOL_LOCK.json | YES |
| configs/oslo/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json | YES |
| configs/oslo/P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json | YES |
| configs/oslo/P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json | YES |
| src/ (6 scripts) | YES |
| results/verified_aggregates/ | YES |

All internal links validated at time of release preparation.

---

*Preview generated 2026-10-24. Author must approve the full README.md content before release.*
