# P49 Historical Figure-Source Export

This directory contains historical figure-level aggregate data and index metadata extracted during the Phase 49 research provenance audit.

## Purpose and Scientific Restrictions
- These files are **historical aggregate exports** preserved to document data provenance for published figures.
- They contain summary distributions, error metrics, and interval statistics; no individual raw/test target meter records or row-level patient data are included.
- Figure-level aggregate data must not be used for post-hoc hyperparameter tuning, model re-selection, or test set recalibration.

## Mapping of Historical Internal Figures to Final Manuscript Figures

| Historical Key in `figures_1_8/` | Historical Caption / Internal Name | Current Final Manuscript Figure Number & Name | Primary Topic / Metric |
|:---|:---|:---|:---|
| **J131–J133, J137** | Figure 1 / Figure 2 (COFACTOR Drammen) | **Figure 3:** `Figure_03_drammen_test_performance_and_coverage.pdf` | Drammen frozen test point error (RMSE) and interval coverage |
| **J134, J138** | Figure 3 (Drammen Building Delta) | **Figure 4:** `Figure_04_building_level_contrasts.pdf` | Drammen building-level paired CRPS contrasts |
| **J27–J33** | Figure 4 (Cairo Height OOD) | **Figure 5:** `Figure_05_cairo_height_shift.pdf` | Cairo building-height shift point error and coverage by height group |
| **J49–J55** | Figure 5 (EDCS U-Geometry Holdout) | **Figure 6:** `Figure_06_edcs_u_shape_holdout.pdf` | EDCS unseen U-shape courtyard point accuracy and calibration shift |
| **J68–J70** | Figure 6 (Five-Climate / Miami Holdout) | **Figure 7:** `Figure_07_miami_transfer_holdout.pdf` | Miami extreme climate transfer point accuracy and calibration shift |
| **J103–J104, J112** | Figure 7 (BDG2 Extreme Tail Diagnostics) | **Figure 8:** `Figure_08_bdg2_reliability_diagnostics.pdf` | BDG2 out-of-site commercial holdout extreme prediction diagnostics |
| **J109–J110** | Figure 8 (Cross-Source Synthesis) | **Figure 10:** `Figure_10_cross_cohort_synthesis.pdf` | Cross-cohort point accuracy and nominal-90% coverage synthesis |
| *(P40 Oslo)* | Phase 40 Oslo School Contrast | **Figure 9:** `Figure_09_oslo_school_level_crps.pdf` | Oslo 36-school zero-shot transfer CRPS evaluation |
| *(Architecture)* | Velocity Network & Formulations | **Figure 2:** `Figure_02_CFM_Architecture_selected.png` | Velocity network schematic and CFM prediction formulations |
| *(Framework)* | Conceptual Reliability Framework | **Figure 1:** `Figure_01_conceptual_framework.pdf` | Six-cohort distribution-shift evaluation framework |

## Files in this Directory
- Aggregate evaluation CSVs: `J27`, `J28`, `J31`–`J33` (Cairo); `J49`, `J50`, `J55` (EDCS); `J68`–`J70` (Miami); `J97`, `J103`, `J104`, `J112` (BDG2); `J131`–`J134`, `J137`, `J138` (Drammen); `J109`, `J110` (Cross-cohort).
- Metadata files: `figure_index.json`, `figure_inventory.csv`, `figure_captions.md`, `P49_AGGREGATE_EXPORT_HASH_MANIFEST.csv`.
