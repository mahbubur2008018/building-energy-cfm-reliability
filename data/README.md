# Dataset sources and access

This repository contains **no original raw meter readings or row-level TEST labels**. Obtain source data through the provider's current access and licence conditions. The MIT licence for the author's code does not license third-party datasets.

| Cohort | Source / access | Evaluation description |
|---|---|---|
| Cairo height-shift simulation | Consult the source reference and archival citation in the manuscript and associated source notes | 2,405 high-height designs evaluated separately from EDCS |
| EDCS U-shaped geometry simulation | Consult the EDCS dataset authors' original distribution and licence | 1,536 U-shaped records; published descriptor and prose use inconsistent energy-unit conventions; no numerical rescaling imposed |
| Five-climate / Miami simulation | Consult the original five-climate research source and supplied source-author documentation | 5,759 held-out Miami designs; report outcome units as in the original source |
| Building Data Genome 2 (BDG2) | https://github.com/buds-lab/building-data-genome-project-2 | Three unseen measured test sites, 92,356 hourly observations; check current source licence |
| Drammen COFACTOR | Published dataset DOI used in the manuscript: https://doi.org/10.1038/s41597-025-04708-3 ; associated source archive: https://zenodo.org/records/14752397 | 27 FIT / 6 VAL / 5 CAL / 7 TEST buildings |
| Oslo COFACTOR-SBHUB | https://doi.org/10.60609/czgf-5e46 | 12 CAL / 36 TEST **schools**; no retraining of Drammen models |

The historical dataset splits and calibration/test-access records are recorded under `configs/`. Not every historical source used the same partitioning or measurement units.

**Use restrictions:** Do not claim distribution-free 90% coverage for unseen building clusters based only on row-level calibrated intervals. Do not retune, recalibrate, reselect a model or perform a new nominally independent evaluation using previously opened TEST labels. Consult original providers before redistributing any data.
