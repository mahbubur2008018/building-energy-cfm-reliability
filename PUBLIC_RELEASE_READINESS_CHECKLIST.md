# Current publication checklist (updated after GitHub repository creation)

**GitHub repository:** https://github.com/mahbubur2008018/building-energy-cfm-reliability  
**Status:** Public repository reported by author; verify current remote commit and contents via `git status` / `git remote -v` / `gh repo view` before making changes.  
**Licence:** MIT selected and `LICENSE` present.

## Before a versioned GitHub/Zenodo release

- [ ] Commit corrected `README.md`, `CITATION.cff`, and `data/README.md` provided in P74 patch.
- [ ] Remove superseded `LICENSING_TO_CONFIRM.md` (the real MIT `LICENSE` is already present).
- [ ] Keep old audit reports as **historical snapshots**; do not portray their 'private candidate' statuses as current.
- [ ] Verify author ORCID account ownership and GitHub repository URL in `CITATION.cff`.
- [ ] Check licence/data permissions, source-code provenance, current Git staging, and hidden files before release.
- [ ] Do not upload `.git` directories in supplementary ZIP handovers; do not publish master state, raw meter files, test-label arrays or model binaries.
- [ ] Integrate G1/G2/G3 truthfully into the manuscript; retain equal-building CI zero crossing and undercoverage.
- [ ] Replace outdated manuscript statements saying code *will* be made public with the verified GitHub URL.
- [ ] **Zenodo must be connected and this GitHub repository enabled BEFORE publishing the first GitHub release.**
- [ ] Author explicitly approves the first release and Zenodo archiving.
- [ ] Publish GitHub release `v1.0.0` after checks; verify Zenodo record/DOI; update `CITATION.cff` and manuscript with the minted DOI in a subsequent commit.

This checklist supersedes the obsolete prerelease/private-first instructions in earlier audit snapshots. A public GitHub repository is not the same as a versioned GitHub **Release**.
