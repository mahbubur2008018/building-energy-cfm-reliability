# G2: OSLO V1 ORIGINAL LOCK — FORMAL DISCLOSURE DOCUMENT
## Building Energy CFM — Pre-Label Role Allocation Provenance

**Status:** PERMANENTLY UNRECOVERABLE — the original P37C review ZIP and P37E v1 role-lock
bytes were lost on Kaggle session restart. This document provides full transparent disclosure.
**Severity:** HIGH — must be explicitly disclosed in the manuscript.

---

## Chain of Evidence

### What was recorded before any label access
| Item | Value | Source |
|---|---|---|
| Original v1 reported SHA-256 | f73d55d11f7e370bfa083c054a66f2401f9ef7523edf3dc12b7a0c86ebf7dd2a | P37E_V2_PRELABEL_AMENDMENT_HASH_RECEIPT.json |
| Original lock file status | LOST on Kaggle session restart | P37E_V2_PRELABEL_ROLE_AND_PROVENANCE_AMENDMENT.json |
| Original P37C compact bytes | NOT available | amendment_context.original_P37C_compact_bytes_not_available: true |
| All Oslo CAL/TEST labels at v2 creation | STILL SEALED | amendment_context.all_Oslo_CAL_and_TEST_labels_still_sealed_at_creation: true |
| Old Drammen final test not opened | TRUE | amendment_context.old_seven_building_Drammen_final_test_not_opened: true |

### What the v2 amendment preserved
| Item | Value | Source |
|---|---|---|
| v2 amendment SHA-256 | 5cd2adfcdc4f87a29cda40b2093a1060ec20d726fb311456961fcf7d5464bad3 | hash receipt + live master (PASS) |
| Role allocation SHA-256 | 917ee8e5148661475bf93c8e276be33a482d620af884433cdb1232954d29df01 | P37F lock (PASS) |
| Role split method | SHA-256 of fixed public salt + filename ID; metadata-only; never outcome-based | amendment JSON |
| 12 calibration buildings | Fixed (listed in amendment) | P37E_V2 role_allocation.calibration |
| 36 test buildings | Fixed (listed in amendment) | P37E_V2 role_allocation.test |
| Model selection | Frozen before Oslo outcomes | model_selection_frozen_before_oslo_outcomes: true |
| Reconstructed from original script | TRUE | amendment_context.reproduced_using_original_P37C_and_P37E_script: true |
| All model and metric policies unchanged | TRUE | amendment_context.original_filename_salt_role_algorithm...unchanged: true |
| Resulting SHA not misrepresented as v1 | TRUE | amendment_context.resulting_SHA256_not_equal_to_original_and_not_misrepresented_as_such: true |
| report_prelabel_amendment_transparently | TRUE | amendment JSON |

### Reconstruction metadata
| Item | Value |
|---|---|
| Reconstructed header/metadata SHA-256 | cd5b935bba5056f8f67e897d018b29a40cfe24b81023692bf44b1289820eaed3 |
| Source rows read at v2 creation | ONLY METADATA AND HEADER; ZERO ELECTRICITY LABEL VALUES |
| Protocol ID | OSLO_P37E_EXTERNAL_FROZEN_DRAMMEN_MODELS_TRANSFER_v2_PRELABEL_RECOVERY |

---

## What Cannot Be Verified

1. That v2 role allocation is byte-for-byte identical to v1 — this is explicitly disclosed as not equal
2. Whether any building's role changed between v1 and v2 — the amendment states algorithm and policies
   are identical but the resulting hash differs; the role list in the v2 amendment is the authoritative record
3. The original v1 file itself — permanently lost, cannot be reconstructed

---

## Required Manuscript Disclosure (template)

"Oslo building role allocation (12 calibration, 36 test) was determined by SHA-256 of a fixed public
salt concatenated with the building filename, applied before any energy label access. The original
pre-label protocol file (P37E v1) was lost during a Kaggle session restart. A v2 amendment was
created immediately after, using the identical role-allocation algorithm and public salt, with all
Oslo calibration and test labels still sealed. The v2 amendment (SHA-256:
5cd2adfcdc4f87a29cda40b2093a1060ec20d726fb311456961fcf7d5464bad3) cannot be verified as
byte-for-byte identical to the lost v1 file, but the resulting calibration and test building lists
are considered identical to those intended under v1. This provenance gap is disclosed transparently."

---

## Resolution Status
G2 is DOCUMENTED with full transparency. The file is permanently lost and cannot be recovered.
The v2 amendment itself is fully verified (hash PASS against all protocol receipts).
The gap requires explicit manuscript disclosure — template provided above.
