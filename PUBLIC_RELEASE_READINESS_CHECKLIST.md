# Public Release Readiness Checklist
## building-energy-cfm-reliability

**Prepared:** 2026-10-24
**Status:** STAGED FOR AUTHOR REVIEW — Not yet published.

---

## BLOCKING (Must complete before any public visibility)

### Author Identity and Legal

- [ ] Complete `CITATION.cff`: family-names, given-names, ORCID, affiliation
- [ ] Replace `LICENSING_TO_CONFIRM.md` with actual `LICENSE` file (MIT or Apache 2.0 recommended)
- [ ] Confirm code ownership: all 6 scripts in `src/` authored solely by you
- [ ] Confirm no institutional restrictions on public code sharing

### Repository Creation (PRIVATE FIRST)

- [ ] `git init` inside `PUBLIC_GITHUB_RELEASE/` (NOT in `Building_CFM_Audit/`)
- [ ] `git add` using explicit allowlist (see below)
- [ ] `git commit -m "Initial safe release candidate"`
- [ ] Create GitHub repository as **PRIVATE** first
- [ ] `git remote add origin https://github.com/[username]/building-energy-cfm-reliability`
- [ ] `git push -u origin main`
- [ ] Verify repository at GitHub — confirm no forbidden files present
- [ ] **STOP — do not change visibility to PUBLIC without separate explicit approval**

### Manuscript Integration

- [ ] Add G1 disclosure paragraph to manuscript Methods section (from `audit/G1_ENVIRONMENT_RECONSTRUCTION_BEST_EFFORT.md`)
- [ ] Add G2 Oslo v1 loss disclosure to manuscript (from `audit/G2_OSLO_V1_LOSS_FORMAL_DISCLOSURE.md`)
- [ ] Add G3 compute budget disclaimer to manuscript (from `audit/G3_COMPUTE_BUDGET_BEST_EFFORT.md`)
- [ ] Confirm both primary CIs span zero; no "significant superiority" language in manuscript
- [ ] Add Data Availability statement with repository URL (once created)

---

## STRONGLY RECOMMENDED (Before final submission)

- [ ] Verify each figure value against original archived source CSV
- [ ] Check figure J32 (Cairo height-group) label correctness independently
- [ ] Check figure J127 axis label (should say kWh, not kWh/hour)
- [ ] Obtain EDCS Miami source unit confirmation from EDCS authors
- [ ] Add BDG2 building-overlap caveat to manuscript
- [ ] Confirm all 21 manuscript references are correct (DOIs resolve; 3 high-priority corrections noted in P43)
- [ ] Complete all BSER&T author declarations (CRediT, competing interests, AI-use, funding, ethics)

---

## ZENODO SUBMISSION (Requires separate explicit approval)

- [ ] Author approval to change repository from PRIVATE to PUBLIC
- [ ] Create Zenodo account / link to GitHub
- [ ] Submit Zenodo record and obtain DOI
- [ ] Tag GitHub release matching Zenodo version
- [ ] Insert Zenodo DOI into `CITATION.cff`
- [ ] Add Zenodo DOI to manuscript Data Availability section
- [ ] Do NOT submit Zenodo record without author approval

---

## ALLOWLIST FOR git add (Use explicitly — do NOT `git add .` without review)

```bash
git add README.md
git add CITATION.cff
git add LICENSING_TO_CONFIRM.md   # Replace with LICENSE when ready
git add .gitignore
git add src/
git add configs/
git add scripts/
git add results/
git add reproducibility/
git add data/
git add audit/
git add PUBLIC_RELEASE_FILE_MANIFEST.csv
git add PUBLIC_RELEASE_PROVENANCE_AUDIT.csv
git add PUBLIC_RELEASE_SAFETY_REPORT.md
git add PUBLIC_RELEASE_READINESS_CHECKLIST.md
git add PUBLIC_RELEASE_README_PREVIEW.md
```

### NEVER add these:
```bash
# These must NEVER be committed:
# BUILDING_CFM_RESUME_LATEST.zip
# BUILDING_CFM_COMPLETE_P43_NEW_CHAT_HANDOVER_*.zip
# Any raw meter data files
# Any file matching: *test_label*, *_TEST_*.csv, *observed_predicted*
# Model checkpoint binaries: *.pt, *.cbm, *.pkl (only SHA-256 hashes are safe)
# Jupyter notebook with outputs: building-cfm-3.ipynb (outputs may contain data)
```

---

## Reproducibility Summary for Manuscript

| Component | Status |
|-----------|--------|
| Source scripts (6 files) | Available — hash-verified; Kaggle paths require adaptation |
| Protocol lock JSONs (32 files) | Available — hash-verified |
| Verified aggregate CSVs (23 files) | Available — hash-verified via P49 manifest |
| Model checkpoint weights | NOT distributed — SHA-256 hashes only |
| Training environment | NOT established — no env lock file (G1) |
| Raw data | NOT redistributed — DOIs provided |
| End-to-end reproduction | NOT POSSIBLE from this repository alone |

*Prepared by automated release curation on 2026-10-24.*
*Author must review and sign off before any git operations.*
