# Assignment 4 — RAG for Scientific Literature Synthesis

## Status (8 November 2026)
Computational runs are logged (160 main, 16 ablation); results are **exploratory**. This is a reproducibility package, not proof of independent reproduction or final Moodle submission.

## Study
50 arXiv papers, 863 chunks; 20 TEST questions (16 answerable and 4 unanswerable) × 8 retrieval conditions. The 16 ablation runs are separate. The notebook includes outputs from the saved Colab execution.

## Publication review
**Figure correction:** `figures/fig1_metrics_by_k.png` and `figures/fig2_primary_by_condition.png` now use the supplied corrected images and match the exported condition-level metrics. Embedded charts in the archived report/notebook may retain the earlier discrepancy. See [publication review](docs/PUBLICATION_REVIEW.md). Numerical metrics are preserved.

## Key results
BM25-5 completeness 0.5385; dense k10 completeness 0.1500 and gold-paper recall 0.9375. Friedman completeness p=0.0647; accuracy p=0.1011. Holm-adjusted pairwise tests did not reach 0.05. Six judge-invalid scores were excluded from eligible metrics, not imputed as zeros.

## Human annotation and reconciliation
Two submitted 144-claim label sets yield initial binary Cohen's kappa 0.3034 (n=135; 9 unclear excluded). The team reports that 39 of 54 initially disputed/unclear items were resolved after discussion and 15 remain disputed. The exact IDs of the 15 are **not marked** in the supplied file. The `final` column contains proposed labels; **do not treat it as a certified full consensus**. Earlier Codex assistance was documented for Reviewer B's first submission; the team subsequently attested to manual review. See [claim-level agreement status](docs/CLAIM_LEVEL_AGREEMENT_STATUS.md).

## Known limitations
- Citation compliance is very low and must not be conflated with factual hallucination.
- Judge-versus-consensus agreement is not validated.
- Seven post-freeze keypoint wording changes require protocol-deviation disclosure; instructor approval is not verified.
- Human labels may be sensitive research artifacts; check sharing permissions before making the repository public.
- GitHub tag, independent reproduction and Moodle receipt are not verified.

## Reproduction
Open `notebooks/Assignment4_Executed_2026-11-08.ipynb` in Colab, mount Drive, inspect paths, and follow the frozen configuration. Source corpus and index reside in the separate Assignment3 directory and are **not included** in this package. The notebook contains audit-only replacements for some steps, so use it as a record of the executed analysis rather than claiming a clean end-to-end reproduction from this ZIP.

## Files
- `results/`: exploratory metrics, tests, validation status
- `figures/`: four charts
- `manual/`: submitted proposed post-discussion labels (not certified consensus)
- `docs/`: audits, human validation, protocol deviations
- `final_config.json`, `protocol_freeze.json`, `requirements.txt`
