# Saved-output reanalysis — 15 November 2026

The saved generations were retained. Leading-label parsing of the original judge responses restores the documented scoring snapshot without new model inference. Main means and confidence intervals, Friedman statistics and all 20 published paired Wilcoxon comparisons reproduce. Statistical conclusions remain exploratory; no corrected-significant superiority is established.

## Corrected ablation table

The prior repository CSV used a stale exact-line parser snapshot. After the documented leading-label restoration, 16 pairs are available for both metrics:

| Outcome, without minus with citation instruction | Difference | 95% percentile bootstrap CI | Wilcoxon p |
|---|---:|---|---:|
| Completeness | -0.0500 | [-0.1750, 0.0625] | 0.7197 |
| Reference accuracy | -0.1187 | [-0.2606, 0.0176] | 0.1688 |

These values agree with the supplied Assignment 4 v6 report. The previous CSV had only six completeness pairs and zero accuracy pairs. Its contents remain available as `reproducibility/inputs/published/ablation_tests.csv`, explicitly a historical comparison snapshot. Citation compliance remains zero in both ablation conditions; this is not a validated factual-hallucination comparison.

## E5/E6 screening queue

`manual/E5_E6_review_queue.csv` contains six E5 and 116 E6 candidate answer records. E5 screening uses the saved answerability flag and historical exact-abstention detector. E6 screening uses MISSING labels in saved automatic judge responses after leading-label parsing. The queue includes original generated answers, frozen expected keypoints and retrieved chunk IDs. It is **not completed human validation**. Human decision, reviewer, date and rationale fields remain empty. Counts describe screened candidates, not verified error frequencies. Expanded refusals can be missed by the historical exact-abstention detector; the six E5 candidates do not exhaust all refusals.

Review each E5 against the actual retrieved passages, distinguishing partial evidence from sufficient evidence for a complete answer. Review E6 against the five reference points with a consistent semantic rubric; an automatic MISSING verdict can itself be wrong. The existing 30 manually recorded E1 cases remain unchanged. No new E5/E6 human labels or consensus decisions are asserted, and the previously disputed claim adjudications are not resolved by this numerical reanalysis.

## Reproduce the calculations

From `reproducibility/`:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-audit.txt
.venv/bin/python recheck_statistics.py
```

Outputs go to `recomputed/`. Input score tables and raw judge labels sufficient for numerical reproduction are included; full article texts and model weights are not. The frozen benchmark and chunks were privately checked against their protocol SHA-256 values. A complete fresh generation run still needs the frozen corpus/index and original environment.

The implementation preserves 10,000 question-level bootstrap resamples, seed 42 with recorded metric-specific offsets, percentile 95% intervals, Friedman over k1/k3/k5/k10/control, and the four planned Wilcoxon contrasts with Holm. Baseline comparisons form a separate family. The historical main table excludes globally invalid rows, while pairwise tests retain available values per metric; these denominators are deliberately reproduced and disclosed. Reanalysis does not silently replace the frozen citation-grounding construct with a factual-truth metric.

The standalone paired interval for k5 minus k10 completeness is [0.075, 0.375], but its Holm-adjusted p=0.0562 is above 0.05. The interval is not multiplicity-adjusted. Undefined Friedman output for the near-constant citation proxy is not proof of equality. The saved-generation recalculation is not independent human validation or an independent end-to-end reproduction.

The input comparison tables refer to pre-reanalysis commit `097c9d5e2f1523d03f79ad6086a3463c061b9806`. The supplied v6 report and older executed notebook are historical documents; they are not silently rewritten as new executions.
