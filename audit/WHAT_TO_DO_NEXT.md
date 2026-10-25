# WHAT TO DO NEXT — AUTHOR ACTION PLAN
## Building Energy CFM Six-Cohort Journal Manuscript
**Prepared by:** Local read-only reproducibility audit (2026-10-23)
**Based on:** P43 handover package + master ZIP provenance audit (13 PASS, 0 FAIL hashes)

This document lists every action the author must take before submitting to BSERT.
Items are grouped by priority. Nothing in this list requires re-running any experiment
or reopening any sealed test labels.

---

## PRIORITY 1 — MUST DO BEFORE SUBMISSION (Blocking)

### 1A. Declare exact environment versions or admit they are unavailable
- [ ] Try to recover the original Kaggle training environment (open a new Kaggle notebook
      and run `pip freeze` in the nearest available Python/PyTorch environment)
- [ ] Label the output clearly: "best-effort approximation — not the original training session"
- [ ] Add this as a supplementary file and add the disclosure paragraph from
      G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md to the manuscript Methods section
- **Evidence file:** AUDIT_OUTPUT/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md
- **Manuscript section:** Methods > Implementation Details

### 1B. Disclose the Oslo v1 lock loss transparently in the manuscript
- [ ] Copy the disclosure paragraph from G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md
      into the manuscript (Methods > Data Splitting / Protocol section)
- [ ] Confirm the exact wording with co-authors
- [ ] Do NOT rephrase it to hide or minimise the provenance gap
- **Evidence file:** AUDIT_OUTPUT/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md

### 1C. Disclose unequal compute budgets in the manuscript
- [ ] Add the compute-budget disclaimer from G3_COMPUTE_BUDGET_BEST_EFFORT.md
      to the manuscript (Methods > Model Training section)
- [ ] State explicitly: "no equal-compute superiority claim is made"
- [ ] The approximate training window (1.0–1.5 hours, 2026-10-20 UTC) can be quoted
- **Evidence file:** AUDIT_OUTPUT/G3_COMPUTE_BUDGET_BEST_EFFORT.md

### 1D. Create a public code repository or state unavailability accurately
- [ ] Follow G11_REPOSITORY_RELEASE_TEMPLATE.md step by step
- [ ] Option A: Create a GitHub repo + Zenodo DOI containing the 6 scripts and protocol JSON files
      (starting from AUDIT_OUTPUT/CFM_CODE_ONLY_PROVENANCE_EXPORT.zip)
- [ ] Option B: If you cannot release code, add to the manuscript:
      "Source code is available from the corresponding author upon reasonable request.
       The original Kaggle training session is no longer accessible."
- [ ] Add the DOI or unavailability statement to the manuscript Data Availability section
- **Evidence file:** AUDIT_OUTPUT/G11_REPOSITORY_RELEASE_TEMPLATE.md

### 1E. Complete all author declarations (required by SAGE/BSERT)
- [ ] Fill in real author names, affiliations and ORCID IDs (BSERT_TITLE_PAGE_AUTHOR_TO_COMPLETE.docx)
- [ ] Write CRediT author contribution statement
- [ ] Write Competing Interests statement
- [ ] Write AI-use declaration (if any AI tools were used in writing)
- [ ] Write Funding statement
- [ ] Write Ethics statement (data use permissions for Drammen/Oslo/EDCS/BDG2/Miami datasets)
- **Source:** P43 Editorial/FINAL_AUTHOR_ACTIONS.txt in handover package

### 1F. Complete and verify all 21 references in exact SAGE Vancouver style
- [ ] Three high-priority references [9], [11], [21] have metadata corrections noted in P43
- [ ] Verify every cited DOI resolves correctly
- [ ] Confirm all data source licences permit the use described
- **Source:** P43 README_START_HERE.md action item 3

---

## PRIORITY 2 — STRONGLY RECOMMENDED BEFORE SUBMISSION

### 2A. Verify every plotted figure value against the original archived source CSV
- [ ] Compare all numbers in the 8 journal figures against P34 plot data CSVs
- [ ] Pay special attention to J32 (Cairo) height-group label mapping — potential non-monotonic labelling
- [ ] Visual/render checks and hash checks alone are NOT sufficient for this step
- [ ] Record each comparison in a figure-verification ledger
- **Source:** P43 README_START_HERE.md action item 2; P32_REPRODUCIBILITY_AND_PUBLICATION_GATES.md

### 2B. Review figure axis labels and units
- [ ] J127: axis label should say kWh, not kWh/hour
- [ ] J131–J136: confirm cohort labels are correct
- [ ] Old J001–J138 must be preserved; only journal editorial copies may be relabelled
- **Source:** P32_REPRODUCIBILITY_AND_PUBLICATION_GATES.md section "Figure corrections"

### 2C. Obtain EDCS Miami source unit confirmation
- [ ] Obtain the official EDCS author confirmation document for unit/time horizon
- [ ] Miami mapping is supported by official supplied code but no simulator-level conversion proof exists
- [ ] Unit/time horizon must remain qualified in the manuscript until confirmed
- **Source:** P20_PROVENANCE_AND_LIMITATIONS.json; P32 gates

### 2D. Clarify Drammen primary result language in manuscript
- [ ] The 7-building bootstrap CI spans zero ([-2.15, +4.08] kWh) — this means
      CFM superiority is NOT statistically established
- [ ] Oslo CI also spans zero ([-2.27, +6.37] kWh) — same caveat
- [ ] Both results are descriptive only; ensure no claim of "significant superiority" appears
- **Evidence:** P21_JOURNAL_READINESS_AUDIT.json; P40_OSLO_PREDECLARED_BUILDING_CRPS_CONTRAST.json

---

## PRIORITY 3 — BEFORE FINAL SUBMISSION SIGN-OFF

### 3A. Resolve BDG2 building-overlap caveat
- [ ] Anonymous physical-building overlap between Drammen COFACTOR and BDG2
      cannot be proved or disproved from available IDs alone
- [ ] Add appropriate caveat to the manuscript
- **Source:** P20_PROVENANCE_AND_LIMITATIONS.json field "overlap_caveat"

### 3B. Calibration coverage caveat
- [ ] Drammen: only 5 CAL buildings — rowwise conformal expansion cannot guarantee 90% cluster-level coverage
- [ ] Oslo: 12 CAL buildings — same caveat applies
- [ ] Ensure both are stated as "descriptive only" in the manuscript
- **Source:** P21_JOURNAL_READINESS_AUDIT.json; P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json

### 3C. Generalisation scope statement
- [ ] All cohorts are within-city or single-source evaluations
- [ ] No multi-city or future-hour forecasting validation has been established
- [ ] Ensure the abstract and conclusion do not overclaim
- **Source:** P22_SCIENTIFIC_AUDIT.json limitations list

### 3D. Submit cover letter and title page (author approval required)
- [ ] Review BSERT_COVER_LETTER_AUTHOR_APPROVAL_REQUIRED.txt in P43 Editorial/
- [ ] Fill in actual author names and institutional affiliations
- [ ] Do NOT submit the placeholder cover letter

---

## WHAT YOU DO NOT NEED TO DO (Already Complete)

| Item | Status |
|---|---|
| Run any new model training or inference | NOT REQUIRED — all results are frozen |
| Reopen Drammen or Oslo TEST labels | FORBIDDEN — already opened and scored once |
| Re-run P21 or P40 evaluations | NOT REQUIRED — results verified as correct |
| Verify script and config hashes | DONE — 13/13 PASS, 0 FAIL |
| Create the code provenance export ZIP | DONE — CFM_CODE_ONLY_PROVENANCE_EXPORT.zip |
| Write the reproducibility audit report | DONE — REPRODUCIBILITY_AUDIT_REPORT.md |

---

## FILE MAP — AUDIT_OUTPUT DIRECTORY

| File | Purpose |
|---|---|
| REPRODUCIBILITY_AUDIT_REPORT.md | Full 15-section provenance audit with all hash evidence |
| REPRODUCIBILITY_AUDIT_RESULTS.csv | Machine-readable 22-row hash result table (PASS/FAIL/UNVERIFIED) |
| CFM_CODE_ONLY_PROVENANCE_EXPORT.zip | 56 safe source/config files exported from master ZIP |
| G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md | All known package version evidence + disclosure template |
| G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md | Oslo v1 lock loss chain-of-evidence + disclosure template |
| G3_COMPUTE_BUDGET_BEST_EFFORT.md | Training window timestamps + fairness matrix + disclosure template |
| G11_REPOSITORY_RELEASE_TEMPLATE.md | GitHub README template + release checklist |
| WHAT_TO_DO_NEXT.md | THIS FILE — prioritised author action plan |

---

## SUMMARY

| Priority | Items | Blocking submission? |
|---|---|---|
| P1 — Must do | 6 items (1A–1F) | YES |
| P2 — Strongly recommended | 4 items (2A–2D) | Should be done |
| P3 — Before sign-off | 4 items (3A–3D) | Advisable |
| Already done | All hash verification, audit, code export | N/A |

**The research science is sound and all verifiable hashes pass.
The remaining work is documentation, declarations and disclosure — not new experiments.**
