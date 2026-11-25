# Building Energy Conditional Flow Matching: Six-Cohort Reliability Study

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23641280.svg)](https://doi.org/10.5281/zenodo.23641280)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Accompanying research code, frozen protocol configurations, and verified evaluation data for the manuscript:

> **Reliability of conditional flow matching for building-energy estimation under distribution shift: A six-cohort evaluation**  
> *Target Journal:* Energy and Buildings (Elsevier)  
> *Author:* Md. Mahbubur Rahman  
> *Affiliation:* Department of Mechatronics Engineering, Rajshahi University of Engineering & Technology (RUET), Rajshahi, Bangladesh  
> *ORCID:* [0009-0004-0252-9140](https://orcid.org/0009-0004-0252-9140)  
> *Permanent Repository:* [https://github.com/mahbubur2008018/building-energy-cfm-reliability](https://github.com/mahbubur2008018/building-energy-cfm-reliability)  
> *Archived Software Release (Zenodo):* Concept DOI [10.5281/zenodo.23641280](https://doi.org/10.5281/zenodo.23641280) | Version DOI [10.5281/zenodo.23641281](https://doi.org/10.5281/zenodo.23641281)

---

## 1. Research Overview

Continuous normalizing flows using **Conditional Flow Matching (CFM)** offer scalable generative modelling of complex probability paths. While CFM has demonstrated strong performance in generative tasks, its empirical reliability for building energy prediction under severe distribution shifts (geometry, climate, meter-level operational regimes, and cross-city transfers) requires rigorous evaluation.

This repository provides the complete implementation, frozen evaluation protocols, baseline comparisons (CatBoost, Random Forest, NGBoost), and prediction data across six distinct building energy cohorts.

### Key Evaluation Focus
1. **Model Formulations:** Empirical contrast between *Direct CFM*, *Full Residual CFM*, and *No-Base Residual CFM*.
2. **Distribution Shift Reliability:** Point accuracy (RMSE, MAE), probabilistic calibration, continuous ranked probability score (CRPS), and prediction interval coverage under distribution shift.
3. **Physical Plausibility:** Diagnostic auditing of unconstrained flow sampling in extreme feature regimes.

---

## 2. Six Evaluation Cohorts

The evaluation spans six independent cohorts representing diverse operational contexts, climates, and data distributions:

| Cohort | Context & Building Type | Shift / Test Partition | Target Outcome & Units | Evaluation Protocol |
|:---|:---|:---|:---|:---|
| **1. Cairo** | Residential apartments | Building height shift (15--24 m holdout) | Annual electricity consumption (kWh/year) | 80/20 train/test split across 480 simulated geometries |
| **2. EDCS** | Office / Institutional | Unseen geometry holdout (U-shape test set) | Total annual load: cooling + heating ($\text{kWh}/\text{m}^2$) | 8,535 verified cases (1,536 L + 5,463 O fit/cal; 1,536 U test) |
| **3. Miami** | Five US climate zones | Extreme climate shift (Miami zone 1A holdout) | Total site energy consumption (kWh) | 4-climate training/calibration; zero-shot transfer to Miami |
| **4. BDG2** | Commercial & university buildings | Multi-site cross-building holdout (3 sites) | Hourly whole-building electrical consumption (kWh) | Out-of-site building holdout; extreme prediction diagnostics |
| **5. Drammen** | Norwegian municipal buildings | In-city unseen building holdout | Hourly space heating consumption (kWh) | Pre-locked building cluster partitions; CRPS evaluation |
| **6. Oslo** | Primary & secondary schools | Cross-city transfer from Drammen models | Hourly space heating consumption (kWh) | Zero-shot model transfer without retraining; school-level CRPS |

---

## 3. Model Formulations

Three CFM formulations are implemented and evaluated against gradient-boosted decision tree baselines:

```
Direct CFM:
Conditioner: c = x
Target:      y
Reconstruction: y_hat = sample(c)

Full Residual CFM:
Conditioner: c = [x, y_hat_base]
Target:      r = y - y_hat_base
Reconstruction: y_hat = sample(c) + y_hat_base

No-Base Residual CFM:
Conditioner: c = x
Target:      r = y - y_hat_base
Reconstruction: y_hat = sample(c) + y_hat_base
```

- **Base Anchor:** CatBoost regressor predictions ($\hat{y}_{\text{base}}$). During training, base anchors are generated via 4-fold GroupKFold out-of-fold (OOF) cross-validation to strictly prevent target leakage.
- **Velocity Network:** Time-conditioned multi-layer perceptron parameterizing vector field $v_\theta(x_t, t, c)$.
- **Probability Path:** Optimal transport affine interpolation $x_t = (1 - t) x_0 + t x_1$ between standard Gaussian noise $x_0 \sim \mathcal{N}(0, I)$ and target distribution $x_1$.
- **Inference:** Numerical ODE integration from $t = 0$ to $t = 1$ via fixed-step Runge-Kutta / midpoint solvers.

---

## 4. Repository Structure

```text
building-energy-cfm-reliability/
├── README.md               <- Research overview and reproduction documentation
├── LICENSE                 <- MIT License
├── CITATION.cff            <- Machine-readable software citation metadata
├── .zenodo.json            <- Zenodo archival deposit metadata
├── requirements.txt        <- Python dependency requirements
├── configs/                <- Protocol lock files and frozen model configurations
│   ├── bdg2/
│   ├── drammen/
│   ├── edcs/
│   ├── miami/
│   └── oslo/
├── data/
│   └── README.md           <- Source dataset access and preprocessing guide
├── figures/                <- High-resolution publication artwork and diagrams
├── notebooks/
│   └── Training Code + Output.ipynb <- Complete executed training and evaluation workflow
├── reproducibility/        <- Computational environment and checkpoint hash receipts
│   ├── CHECKPOINT_HASH_MANIFEST.md
│   ├── ENVIRONMENT_DISCLOSURE.md
│   └── PROTOCOL_OVERVIEW.md
├── results/
│   └── verified_aggregates/ <- Source-level evaluation data and figure summary CSVs
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

## 5. Installation and Setup

### Prerequisites
- Python $\ge 3.10$ and $\le 3.13$
- CUDA-compatible GPU recommended for neural flow training and ODE sampling

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/mahbubur2008018/building-energy-cfm-reliability.git
cd building-energy-cfm-reliability

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 6. Dataset Acquisition

In accordance with original provider licensing, raw third-party datasets are not directly redistributed in this repository. Instructions for acquiring each primary source are detailed in [`data/README.md`](data/README.md):

1. **Cairo Dataset:** EnergyPlus simulated apartment buildings across building height variations.
2. **EDCS Dataset:** EnergyPlus Building Energy Performance Simulation dataset across geometric footprints (Zenodo record `10.5281/zenodo.15073304`).
3. **Miami / Five-Climate Dataset:** Multi-climate US commercial building energy simulation benchmarks.
4. **Building Data Genome Project 2 (BDG2):** Hourly electrical meter recordings from real-world non-residential buildings (Miller et al., *Scientific Data*, 2020).
5. **COFACTOR Drammen:** Hourly heating consumption in Norwegian municipal buildings (*Scientific Data*, 2025; DOI: `10.1038/s41597-025-04708-3`).
6. **COFACTOR-SBHUB Oslo:** Hourly heating consumption in 36 Oslo educational buildings (DOI: `10.60609/czgf-5e46`).

---

## 7. Execution and Reproduction

### Executed Training and Evaluation Workflow
The complete, end-to-end training, calibration, inference, and visualization pipeline is preserved with all 77 cell outputs in:
```bash
notebooks/Training Code + Output.ipynb
```

### Standalone Model Training Workers
- **Standard CFM:** Run [`src/phase4_standard_cfm_worker.py`](src/phase4_standard_cfm_worker.py) for baseline flow training.
- **GPU Distributed Flow Worker:** Run [`src/phase20_gpu_flow_worker.py`](src/phase20_gpu_flow_worker.py) for locked multi-building training.
- **Frozen Inference Worker:** Run [`src/phase21_frozen_inference_worker.py`](src/phase21_frozen_inference_worker.py) for sealed one-time evaluation on test holdout buildings.

### Verification of Checkpoint Integrity
Verify the cryptographic SHA-256 integrity of all model checkpoint files against the locked manifest:
```bash
python scripts/CFM_CHECKPOINT_HASH_VERIFY.py
```

---

## 8. Principal Verified Findings

1. **Cairo (Height Shift):** Out-of-fold residual CFM achieved a **19.6% RMSE reduction** relative to CatBoost (4,991.73 vs 6,204.90 kWh/year); direct CFM achieved a 15.1% reduction.
2. **EDCS (Unseen Geometry Holdout):** The analytical cohort contains exactly **8,535 records** across L, O, and U geometries. Exploratory Direct CFM achieved an RMSE of **0.201** (a **47.7% reduction** relative to CatBoost, 0.384). The preselected No-base residual variant improved on CatBoost by 8.4% (0.351 vs 0.384).
3. **Drammen (Holdout Municipal Buildings):** Direct CFM improved row-weighted CRPS by **6.0%** over NGBoost (15.58 vs 16.57 kWh). However, building-cluster bootstrap 95% confidence intervals cross zero ($[-2.152, +4.076]$ kWh), indicating that pooled improvements are heterogeneous across buildings.
4. **Oslo (Zero-Shot Cross-City Transfer):** Direct CFM improved row-weighted CRPS by **5.0%** over NGBoost (38.59 vs 40.61 kWh). At the individual building level, NGBoost outperformed Direct CFM on **21 of 36 schools** (58.3%), illustrating Simpson's aggregation paradox where pooled metrics are dominated by high-consumption facilities.
5. **BDG2 (Multi-Site Commercial Holdout):** Full residual CFM post-calibration coverage reached **92.5%** with an interval score of **635.7 kWh**. In unconstrained Direct CFM, extreme out-of-distribution feature combinations caused trajectory explosion on 163 hourly predictions ($> 10^6$ kWh), demonstrating the essential role of residual bounding.
6. **Miami (Extreme Climate Transfer):** 90% prediction intervals calibrated on temperate/cold zones collapsed to **0.0% coverage** under zero-shot transfer to tropical climate zone 1A, establishing the necessity of climate-aware re-calibration.

---

## 9. Reproducibility Disclosures

In accordance with transparent reporting guidelines:
- **Environment Provenance (G1):** Original model training was performed in a cloud execution environment without a locked `pip freeze`. Standard library versions have been verified through post-hoc audit sessions and documented in [`reproducibility/ENVIRONMENT_DISCLOSURE.md`](reproducibility/ENVIRONMENT_DISCLOSURE.md).
- **Oslo Protocol (G2):** Pre-label role definitions and feature selections were established prior to accessing test evaluation labels, as certified in [`configs/oslo/`](configs/oslo/).
- **Baseline Budgets (G3):** NGBoost comparisons on large hourly cohorts (Drammen and Oslo) were evaluated under a 40,000-row computational sub-budget due to tree-complexity constraints; these comparisons reflect practical computational trade-offs rather than unbounded theoretical superiority.

---

## 10. Citation

If you use this software, protocol records, or empirical evaluation data, please cite the archived release:

```bibtex
@software{rahman_2026_building_cfm,
  author       = {Rahman, Md. Mahbubur},
  title        = {Building Energy Conditional Flow Matching: Six-Cohort Reliability Study},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.1.0},
  doi          = {10.5281/zenodo.23641281},
  url          = {https://github.com/mahbubur2008018/building-energy-cfm-reliability}
}
```

---

## 11. License

This repository is licensed under the [MIT License](LICENSE). Third-party datasets referenced in this research are governed by their respective original licenses and source providers.
