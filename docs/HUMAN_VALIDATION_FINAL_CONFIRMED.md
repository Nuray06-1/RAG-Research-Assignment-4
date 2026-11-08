# Assignment 4 — FINAL Human–Human Validation Report

**Date:** 8 November 2026  
**Status:** Human annotation and inter-rater agreement calculation completed; consensus adjudication and judge-versus-human validation are separate follow-up analyses.

## 1. Reviewers and provenance

Reviewer A and Reviewer B submitted claim-level review datasets. The project team explicitly confirms that **Reviewer B completed his review manually**. Reviewer A's review was also completed manually, as reported by the team. This report records the team's confirmation as the basis for describing the submitted annotations as human reviews. The CSV files independently establish the labels and numerical agreement, but do not themselves provide an audit trail of the reviewers' procedures.

The Reviewer B submission `claims_reviewer_b_LABELLED_human_review.csv` contains the same 144 labels and notes as the earlier `claims_reviewer_b_LABELLED.csv`, plus an `index` column. This is a provenance observation, not a reason to disregard the team's explicit confirmation of manual review.

## 2. Data matching

Both reviewer datasets contain **144 claim annotations**, and all **144** records match by `claim_id`. The agreement variable is `human_correct`, with categories `yes`, `no`, and `unclear`.

## 3. Primary agreement: binary yes/no

Nine items marked `unclear` by Reviewer B are excluded from the primary binary analysis, leaving **135 paired observations**.

| Reviewer A / Reviewer B | yes | no | Total |
|---|---:|---:|---:|
| yes | 21 | 42 | 63 |
| no | 3 | 69 | 72 |
| **Total** | **24** | **111** | **135** |

- Observed agreement: **90/135 = 66.67%**.
- Chance-expected agreement: **52.15%**.
- **Cohen's kappa: 0.3034**.

This is a completed human–human inter-rater agreement calculation. The magnitude of kappa indicates limited/modest agreement and must not be described as strong reliability.

## 4. Sensitivity analysis: three categories

Including `unclear` as a distinct category yields **144 paired observations**, **62.50%** observed agreement and **Cohen's kappa = 0.2770**.

## 5. Interpretation and remaining validation work

The two human annotation sets and their agreement calculation are complete. The results reveal **45 binary disagreements** (42 Reviewer A=yes / Reviewer B=no; 3 Reviewer A=no / Reviewer B=yes) and **9 unclear cases**. These should be adjudicated transparently, preserving both original annotations. This is a separate step from calculating human–human kappa.

The human–human coefficient does **not** establish judge-versus-human agreement. Automated-judge scores and statistical hypothesis tests should continue to be identified as exploratory until the relevant judge-validation and adjudication steps are complete. The six recorded `judge_invalid` cases also require explicit handling in downstream analyses. These limitations do not negate the completion of manual annotation or the numerical kappa calculation.

## 6. Report-ready paragraph

Two reviewers, Reviewer A and Reviewer B, completed claim-level manual annotation, as confirmed by the project team. Their submitted datasets contained 144 annotations each and were matched one-to-one by claim ID. Excluding nine `unclear` labels from the primary binary comparison, 135 paired ratings yielded 66.67% observed agreement and Cohen's kappa of 0.3034. A three-category sensitivity analysis including `unclear` yielded 62.50% agreement and kappa of 0.2770 across all 144 items. Thus, human–human agreement was calculated and documented, although its magnitude indicates limited inter-rater reliability. Disagreements require consensus adjudication, and judge-versus-human validation remains a separate assessment.

**Final status for this section:** Manual reviewer submissions received; human–human agreement calculated and documented. No claim of high agreement or completed judge-versus-human validation is made.
