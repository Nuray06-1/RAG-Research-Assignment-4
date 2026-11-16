# Assignment 4 — RAG for Scientific Literature Synthesis

## Status (16 November 2026)
Computational runs are logged (160 main, 16 ablation); results are **exploratory**. This is a reproducibility package, not proof of independent reproduction or final Moodle submission.

## Final reproducibility release
The [`final` release](https://github.com/Nuray06-1/RAG-Research-Assignment-4/releases/tag/final) identifies the archived version of the code, documentation, and saved outputs. The tag does not certify unresolved annotations, confirm hypotheses, or establish independent reproduction.

To obtain this version:
```bash
git clone --branch final --depth 1 https://github.com/Nuray06-1/RAG-Research-Assignment-4.git
cd RAG-Research-Assignment-4
git rev-parse HEAD
```

## Study
50 arXiv papers, 863 chunks; 20 TEST questions (16 answerable and 4 unanswerable) × 8 retrieval conditions. The 16 ablation runs are separate. The notebook includes outputs from the saved Colab execution.

## Publication review
**Figure correction:** `figures/fig1_metrics_by_k.png` and `figures/fig2_primary_by_condition.png` now use the supplied corrected images and match the exported condition-level metrics. Charts embedded in the archived notebook may retain the earlier discrepancy; the charts in the submitted report were checked against the exported metrics and match.

## Saved-output reanalysis
The [15 November reanalysis](docs/REANALYSIS_2026-11-15.md) reproduces the main intervals and planned tests and corrects the stale ablation CSV: completeness difference −0.050 (95% CI [−0.175, 0.0625], p=0.7197), accuracy difference −0.1187 (p=0.1688), both with 16 pairs. The [E5/E6 review queue](manual/E5_E6_review_queue.csv) contains 6 and 116 screened candidates, respectively; independent human decisions remain pending. Numerical reproduction inputs and the script are in `reproducibility/`.

## Citation repair
A [separate citation-repair version](docs/CITATION_REPAIR.md) attaches six source-backed markers to existing statements in two saved answers, using full-claim verbatim matches in the actual input passages. It is post-hoc editing, not new model behaviour or improved experimental scores. The original generations and metrics remain unchanged. A structured citation contract and generation-request preparation tool are included; a new generator run and semantic evaluation have not been executed.

## Key results
BM25-5 completeness 0.5385; dense k10 completeness 0.1500 and gold-paper recall 0.9375. Friedman completeness p=0.0647; accuracy p=0.1011. Holm-adjusted pairwise tests did not reach 0.05. Six judge-invalid scores were excluded from eligible metrics, not imputed as zeros.

## Human annotation and reconciliation
Two 144-claim label sets were compared. The first was produced by unaided manual annotation against the frozen coding scheme. The second was a model (Codex) pre-pass, later reviewed and confirmed by a team member; it is not an independent human annotation. Binary Cohen’s kappa between them is 0.3034 (n=135; 9 unclear excluded) and describes human versus model-assisted agreement, not inter-coder reliability. All 54 non-agreement items were adjudicated by a team member with a written reason for each. An earlier team report described 15 of the 54 as still disputed; candidate row-level IDs are now marked in `manual/claims_144_CORRECTED_PROVENANCE.csv`. The `final` column contains proposed labels; **do not treat it as a certified full consensus**. See [claim-level agreement status](docs/CLAIM_LEVEL_AGREEMENT_STATUS.md).

## Known limitations
- Citation compliance is very low and must not be conflated with factual hallucination.
- Judge-versus-consensus agreement is not validated.
- Seven post-freeze keypoint wording changes require protocol-deviation disclosure; instructor approval is not verified.
- Human labels record judgements about machine-generated text, not personal data, and reviewer names are pseudonymised; the package is suitable for public release.
- Independent reproduction and Moodle receipt are not verified.

## Reproduction
Open `notebooks/Assignment4_Executed_2026-11-08.ipynb` in Colab, mount Drive, inspect paths, and follow the frozen configuration. Source corpus and index reside in the separate Assignment3 directory and are **not included** in this package. The notebook contains audit-only replacements for some steps, so use it as a record of the executed analysis rather than claiming a clean end-to-end reproduction from this ZIP.

### Recompute statistics from the included saved scores
The saved-score audit is self-contained and was checked with Python 3.12.14. From the repository root:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r reproducibility/requirements-audit.txt
python reproducibility/recheck_statistics.py
python -m unittest discover -s citation_tools -p 'test_*.py'
```
The audit writes to `reproducibility/recomputed/`; check `published_vs_recomputed.csv` for numeric comparisons against the preserved historical tables. **Ten mismatches in the historical ablation snapshot are expected**: that snapshot predates the documented correction to 16 pairs. The corrected table is `results/ablation_tests.csv`; see the [reanalysis explanation](docs/REANALYSIS_2026-11-15.md#corrected-ablation-table). This reproduces calculations from saved scores, not the generator, retriever, or judge runs. The root `requirements.txt` records the earlier Colab package versions; use the separate audit requirements for these commands.

The unfinished full-corpus semantic review of 749 statements is not included in this release and supplies no new validation labels or metrics.

## Files
- `results/`: exploratory metrics, tests, validation status
- `figures/`: four charts
- `manual/`: submitted proposed post-discussion labels (not certified consensus)
- `docs/`: audits, human validation, protocol deviations
- `final_config.json`, `protocol_freeze.json`, `requirements.txt`
