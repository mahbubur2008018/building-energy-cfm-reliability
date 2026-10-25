# Public Release Safety Report
## Building Energy CFM — building-energy-cfm-reliability

**Prepared:** 2026-10-24
**Scope:** Explicit allowlist-based safety check of all files staged for release.

---

## Safety Check Results

### PASS — Files confirmed safe for release

| Check | Status | Evidence |
|-------|--------|---------|
| No master ZIP included (2.3 GiB) | PASS | BUILDING_CFM_RESUME_LATEST.zip excluded |
| No handover ZIP included (92 MB) | PASS | P43 ZIP excluded |
| No raw meter data | PASS | raw_data/ excluded; data/README.md provides DOIs only |
| No row-level TEST labels | PASS | P21 and P40 TEST CSV records not extracted or included |
| No row-level predictions (actual vs predicted) | PASS | Forbidden terms blocked by allowlist in CFM_PC_READONLY_PROVENANCE_EXPORT.py |
| No model checkpoint binaries | PASS | .pt, .cbm, .pkl files excluded; SHA-256 hashes only |
| No credentials, tokens, passwords | PASS | Scripts scanned; no hard-coded credentials found |
| No private file paths exposing personal identity | PASS | Kaggle working dir paths (/kaggle/working/) are generic |
| No fabricated DOI in CITATION.cff | PASS | Placeholder text "TO_BE_ASSIGNED" used; no fake DOI |
| No fabricated validation results | PASS | All hash values sourced from verified audit records |
| All files below 100 MB GitHub limit | PASS | Largest file: figure_index.json (142 KB) |
| No nested large archives | PASS | No ZIP within ZIP that could hide forbidden content |
| No unreviewed notebook outputs | PASS | building-cfm-3.ipynb not included |
| No uncertain-provenance files | PASS | All included files traced to verified audit records |

### UNVERIFIED — Items requiring author action before public release

| Item | Gap | Action Required |
|------|-----|----------------|
| Licensing | No licence file in effect | Author must confirm ownership and choose licence |
| Author identity | CITATION.cff has placeholder | Author must complete before public release |
| ORCID | Missing | Author must add |
| GitHub repository URL | Not yet created | Insert after repo creation |
| Zenodo DOI | Not yet assigned | Do not fabricate; insert after submission |
| EDCS Miami unit confirmation | Not independently obtained | Manuscript must qualify claim |
| BDG2 building overlap | Cannot be disproved | Manuscript must include caveat |
| Figure J32 height-group correctness | Not independently verified in this audit | Author must verify |

### FAIL — Known reproducibility gaps (must be disclosed in manuscript)

| Gap ID | Description | Severity |
|--------|-------------|---------|
| G1 | No pip freeze or env lock file; training versions unestablished | HIGH |
| G2 | Oslo v1 lock permanently lost; v2 amendment disclosed | HIGH |
| G3 | Unequal compute budgets (NGBoost 40k vs CFM full FIT) | HIGH |
| G9 | Drammen primary CI spans zero [-2.15, +4.08] kWh | SCIENTIFIC NOTE |
| G10 | Oslo primary CI spans zero [-2.27, +6.37] kWh | SCIENTIFIC NOTE |

---

## Forbidden Content Allowlist

The following patterns were used to screen all files before inclusion.
Any file matching a forbidden pattern was EXCLUDED:

| Pattern | Reason |
|---------|--------|
| prediction, prediction_array | Row-level predictions |
| test_cache, test_label, test_target | TEST label content |
| raw_data, raw_meter, meter_data | Raw electricity readings |
| target_array, cal_label, cal_target | Calibration label content |
| weights, checkpoint, state_dict | Model binary weights |
| feature_array | Raw feature matrices |
| credentials, secret, token, password | Authentication data |

---

## Scanning Notes

- Scripts in src/: Checked for Kaggle absolute paths. Present (/kaggle/working/) but generic,
  not personally identifying. No credentials found.
- JSON configs: No raw measurement values detected. Protocol metadata only.
- Aggregate CSVs (J-series): Extracted via P49 allowlist (EXPORTED_AGGREGATE_ONLY label).
  No row-level observed/predicted values.
- Audit records: Documentation files only; contain hash values and descriptive text.

---

## File Size Check

| Threshold | Status |
|-----------|--------|
| GitHub per-file limit: 100 MB | All files PASS (largest: 142 KB) |
| GitHub recommended limit: 50 MB | All files PASS |
| Zenodo upload: check current limits | Not applicable yet |

---

*Safety report generated 2026-10-24 by automated release curation.*
*Author must perform independent review before any public visibility change.*
