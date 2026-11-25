# Building Energy Conditional Flow Matching: Six-Cohort Reliability Study

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23641280.svg)](https://doi.org/10.5281/zenodo.23641280)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Historical research code, frozen protocol configurations, and verified aggregate evaluation data accompanying the manuscript:

> **Reliability of conditional flow matching for building-energy estimation under distribution shift: A six-cohort evaluation**  
> *Target Journal:* Energy and Buildings (Elsevier)  
> *Author:* Md. Mahbubur Rahman  
> *Affiliation:* Department of Mechatronics Engineering, Rajshahi University of Engineering & Technology (RUET), Rajshahi, Bangladesh  
> *ORCID:* [0009-0004-0252-9140](https://orcid.org/0009-0004-0252-9140)  
> *Permanent Repository:* [https://github.com/mahbubur2008018/building-energy-cfm-reliability](https://github.com/mahbubur2008018/building-energy-cfm-reliability)  
> *Archived Software Release (Zenodo):* Concept DOI [10.5281/zenodo.23641280](https://doi.org/10.5281/zenodo.23641280) | Version DOI [10.5281/zenodo.23641281](https://doi.org/10.5281/zenodo.23641281)

---

## 1. Research Overview

Continuous normalizing flows using **Conditional Flow Matching (CFM)** learn time-dependent vector fields that transport simple prior densities to complex target distributions. This repository provides the historical experimental code, frozen configuration records, baseline models (CatBoost, Random Forest, NGBoost), and source-level aggregate evaluation data for a six-cohort empirical investigation of building energy prediction under distribution shifts.

### Evaluation Scope
1. **Model Formulations:** Empirical comparison of *Direct CFM*, *Full Residual CFM*, and *No-Base Residual CFM*.
2. **Distribution-Shift Metrics:** Point accuracy (RMSE, MAE), probabilistic calibration, continuous ranked probability score (CRPS), and nominal 90% prediction interval coverage under geometry, climate, meter site, and building transfers.
3. **Physical-Scale Diagnostics:** Diagnostic checks of unconstrained generative flow predictions under out-of-distribution feature combinations.

---

## 2. Six Evaluation Cohorts

The study evaluates six distinct cohorts, preserving source-specific outcome definitions, native units, and evaluation protocols:

| Cohort | Context & Building Type | Shift / Test Partition | Target Outcome & Units | Evaluation Protocol |
|:---|:---|:---|:---|:---|
| **1. Cairo** | Residential apartments | Building height shift ($> 12.76\,\text{m}$ holdout) | Annual site electricity ($\text{kWh}/\text{year}$) | 12,000 total simulated records across 480 building geometry configurations; 2,405 high-height records form the test holdout; remaining records allocated to fitting (6,716), validation (1,439), and calibration (1,440). |
| **2. EDCS** | Office / Institutional | Unseen courtyard geometry (U-shape holdout) | Total annual load ($\text{kWh}/\text{m}^2$; cooling + heating) | 8,535 verified records in Zenodo spreadsheets (1,536 L + 5,463 O + 1,536 U). 6,999 L/O records for fitting/calibration; 1,536 U-shaped records form test holdout. Direct CFM evaluated as exploratory comparison. |
| **3. Miami** | Five US climate zones | Extreme climate shift (Miami zone 1A holdout) | Energy consumption per floor area ($\text{kWh}/\text{m}^2$) | 28,787 total designs; 5,759 Miami designs form frozen climate holdout; remaining four cities provide fitting (16,118), validation (3,454), and calibration (3,456). |
| **4. BDG2** | Commercial & university buildings | Multi-site cross-building holdout (3 sites) | Hourly whole-building electrical consumption ($\text{kWh}$) | Three commercial sites; out-of-site building holdout with extreme prediction diagnostics. |
| **5. Drammen** | Norwegian municipal buildings | In-city unseen building holdout | Hourly space heating consumption ($\text{kWh}$) | 88,584 retained fitting rows; pre-locked building cluster partitions; CRPS evaluation. |
| **6. Oslo** | Primary & secondary schools | Cross-city transfer from Drammen models | Hourly space heating consumption ($\text{kWh}$) | Zero-shot model transfer across 36 school buildings without parameter retraining. |

---

## 3. Model Formulations and Anchor Protocols

Three CFM formulations are investigated:

```
Direct CFM:
Conditioner:    c = x
Target:         y
Reconstruction: y_hat = sample(c)

Full Residual CFM:
Conditioner:    c = [x, y_hat_base]
Target:         r = y - y_hat_base
Reconstruction: y_hat = sample(c) + y_hat_base

No-Base Residual CFM:
Conditioner:    c = x
Target:         r = y - y_hat_base
Reconstruction: y_hat = sample(c) + y_hat_base
```

### CatBoost Anchor Generation Protocol
- **Direct CFM:** The CatBoost prediction is completely bypassed during both conditioning and reconstruction.
- **Residual Formulations:** CatBoost serves as the point prediction anchor ($\hat{y}_{\text{base}}$). During training, anchor predictions are generated using cohort-appropriate validation splits:
  - In cross-validation cohorts (e.g., Cairo, BDG2), out-of-fold (OOF) predictions are generated via GroupKFold on building/geometry clusters to avoid training-label leakage.
  - In fixed split cohorts (e.g., EDCS, Miami, Drammen), base models are trained strictly on the designated training/fit partition and evaluated on holdout partitions.
- Full Residual CFM includes $\hat{y}_{\text{base}}$ in the velocity network conditioning vector $c = [x, \hat{y}_{\text{base}}]$.
- No-Base Residual CFM conditions strictly on the input features $c = x$, adding $\hat{y}_{\text{base}}$ only during final target reconstruction.

---

## 4. Repository Structure

```text
building-energy-cfm-reliability/
├── README.md               <- Academic research overview and reproduction guide
├── LICENSE                 <- MIT License
├── CITATION.cff            <- Machine-readable software citation metadata
├── .zenodo.json            <- Zenodo archival deposit metadata
├── .gitignore              <- Git ignore rules (includes __pycache__ and *.pyc)
├── requirements.txt        <- Python dependency requirements
├── configs/                <- Protocol lock files and frozen model configurations
│   ├── bdg2/
│   ├── drammen/
│   ├── edcs/
│   ├── miami/
│   └── oslo/
├── data/
│   └── README.md           <- Official dataset acquisition links, citations, and access
├── figures/                <- Author-approved manuscript figures and graphical abstract
├── notebooks/
│   └── Training Code + Output.ipynb <- Historical notebook preserving all execution outputs
├── reproducibility/        <- Computational environment disclosures and protocol overviews
│   ├── CHECKPOINT_HASH_MANIFEST.md
│   ├── ENVIRONMENT_DISCLOSURE.md
│   └── PROTOCOL_OVERVIEW.md
├── results/
│   └── verified_aggregates/ <- Verified aggregate evaluation CSVs and figure summaries
│       ├── figures_1_8/
│       └── P49_AGGREGATE_EXPORT_HASH_MANIFEST.csv
├── scripts/                <- Verification utilities and provenance export tools
│   ├── CFM_CHECKPOINT_HASH_VERIFY.py
│   └── CFM_PC_READONLY_PROVENANCE_EXPORT.py
└── src/                    <- PyTorch CFM and baseline worker implementations
    ├── cfm_ddp_worker.py
    ├── p18_bdg2_gpu_catboost_fit_worker.py
    ├── p19_dualgpu_distributional_worker.py
    ├── phase20_gpu_flow_worker.py
    ├── phase21_frozen_inference_worker.py
    └── phase4_standard_cfm_worker.py
```

---

## 5. Installation and Environment

### Prerequisites
- Python $\ge 3.10$ and $\le 3.13$
- CUDA-compatible GPU recommended for neural flow training and ODE integration

```bash
# Clone the repository
git clone https://github.com/mahbubur2008018/building-energy-cfm-reliability.git
cd building-energy-cfm-reliability

# Set up virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

---

## 6. Dataset Acquisition

In compliance with provider licensing, third-party raw datasets are not bundled in this repository. Refer to [`data/README.md`](data/README.md) for official download links, repository DOIs, and access instructions for:
- Cairo height-shift EnergyPlus simulations (Wefki et al., 2026; DOI: `10.1177/01436244251405976`)
- EDCS building geometry simulations (Zenodo DOI: `10.5281/zenodo.15073304`)
- Five-climate US commercial simulation benchmark (Aloshan & Aldali)
- Building Data Genome Project 2 (BDG2; Miller et al., 2020; DOI: `10.1038/s41597-020-00710-x`)
- COFACTOR municipal buildings dataset (Drammen; DOI: `10.1038/s41597-025-04708-3`)
- COFACTOR-SBHUB school buildings dataset (Oslo; DOI: `10.60609/czgf-5e46`)

---

## 7. Available Code, Historical Artifacts, and Reproduction

This repository provides historical implementation code, protocol locks, and verified evaluation summaries:
- **Executed Workflow:** Complete model fitting, calibration, and metric evaluation are preserved with all 77 cell outputs in [`notebooks/Training Code + Output.ipynb`](notebooks/Training%20Code%20+%20Output.ipynb).
- **Core Model Workers:** Standalone PyTorch implementations are provided in `src/` for standard CFM (`src/phase4_standard_cfm_worker.py`), multi-building flow training (`src/phase20_gpu_flow_worker.py`), and frozen inference (`src/phase21_frozen_inference_worker.py`).
- **Checkpoint Verification:** Integrity of model weight files can be verified against locked SHA-256 digests using `python scripts/CFM_CHECKPOINT_HASH_VERIFY.py`.

---

## 8. Principal Verified Findings

1. **Cairo (Height Shift):** Out-of-fold Full residual CFM achieved a **19.6% RMSE reduction** relative to CatBoost (4,992 vs 6,205 kWh/year). Direct CFM achieved 84.6% empirical coverage with an interval score of 18,738.
2. **EDCS (Unseen Geometry Holdout):** The analytical cohort contains **8,535 verified records**. Exploratory Direct CFM achieved an RMSE of **0.201** and MAE of 0.173 ($\text{kWh}/\text{m}^2$). The preselected No-base residual variant achieved an RMSE of 0.351 (an 8.4% improvement relative to CatBoost, 0.384).
3. **Drammen (Holdout Municipal Buildings):** Direct CFM achieved a row-weighted CRPS of **15.58 kWh** versus 16.57 kWh for NGBoost (a 6.0% row-weighted reduction). Equal-building comparisons showed heterogeneous effects across individual facilities.
4. **Oslo (Zero-Shot Cross-City Transfer):** Direct CFM achieved a row-weighted CRPS of **38.59 kWh** versus 40.61 kWh for NGBoost (a 5.0% row-weighted reduction). At the individual school level, NGBoost yielded lower CRPS on 21 of 36 schools, reflecting heterogeneous performance across building sizes.
5. **BDG2 (Multi-Site Commercial Holdout):** Full residual CFM post-calibration coverage reached **92.5%** with an interval score of **635.7 kWh**. Direct CFM generated 163 hourly predictions above $10^6\,\text{kWh}$ in extreme feature regions, illustrating the practical value of residual anchoring for physical-scale plausibility.
6. **Miami (Extreme Climate Transfer):** Four-city calibration coverage of 92.6% collapsed to **0.0% coverage** under zero-shot transfer to Miami climate zone 1A, highlighting the sensitivity of conformal prediction intervals to severe climate shift.

---

## 9. Reproducibility Disclosures

- **Environment Provenance (G1):** Original model training was executed in a cloud notebook environment without a saved `pip freeze`. Lower-bound versions and audit environment records are disclosed in [`reproducibility/ENVIRONMENT_DISCLOSURE.md`](reproducibility/ENVIRONMENT_DISCLOSURE.md).
- **Oslo Protocol (G2):** Feature selection and pre-label role definitions were locked prior to accessing test evaluation labels, as certified in [`configs/oslo/`](configs/oslo/).
- **Baseline Budgets (G3):** NGBoost comparisons on large hourly cohorts (Drammen and Oslo) were fitted on a 40,000-row computational sub-budget due to tree-complexity constraints; comparisons reflect practical computational trade-offs rather than unbounded theoretical performance.

---

## 10. Citation

If you use this software, protocol records, or empirical evaluation data, please cite the archived release:

```bibtex
@software{rahman_2026_building_cfm,
  author       = {Rahman, Md. Mahbubur},
  title        = {Building Energy Conditional Flow Matching: Six-Cohort Reliability Study},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.1.1},
  doi          = {10.5281/zenodo.23641281},
  url          = {https://github.com/mahbubur2008018/building-energy-cfm-reliability}
}
```

---

## 11. License

This repository is licensed under the [MIT License](LICENSE). Third-party datasets are subject to their respective original provider licenses and terms.
