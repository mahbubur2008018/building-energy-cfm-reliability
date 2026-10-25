# Data Access and Licensing

This repository does NOT contain raw electricity meter data or row-level measurement records.
All raw data must be obtained directly from official source providers using the DOIs below.

## Datasets

### 1. Drammen COFACTOR v3 (Cohorts 1 and 2)
- DOI: https://zenodo.org/records/14752397
- Role: FIT (33 buildings), CAL (5), TEST (7)
- Access: Public Zenodo download

### 2. Oslo COFACTOR-SBHUB (Cohort 6)
- DOI: https://doi.org/10.60609/czgf-5e46
- Role: CAL (12), TEST (36). Frozen Drammen models applied unchanged.
- Access: Follow DOI access instructions

### 3. EDCS - Cairo and Five-Climate (Cohorts 3 and 4)
- Source: EDCS consortium
- Cohort 3 (Cairo): Height-group OOD shift analysis
- Cohort 4 (Miami): Five-climate held-out climate evaluation
- Miami unit provenance: Supported by official supplied code; EDCS author-level
  simulator confirmation not independently obtained (qualified in manuscript)
- Access: Contact EDCS consortium

### 4. Building Data Genome 2 (Cohort 5)
- Source: https://github.com/buds-lab/building-data-genome-project-2
- Licence: Creative Commons CC BY 4.0 (verify current licence at source)
- Overlap caveat: Anonymous physical-building overlap with Drammen COFACTOR
  cannot be confirmed or excluded from available IDs alone

## Split Protocols

All FIT/VAL/CAL/TEST splits were performed before any label access.
Lock files are in configs/ subdirectories.

## Data Use Notices

1. Do not redistribute raw data. Only aggregate CSVs in results/verified_aggregates/ are included.
2. TEST labels are not included. Drammen TEST accessed once (P21); Oslo TEST once (P40).
3. Verify current licence at each official source before use.

*Created 2026-10-24.*
