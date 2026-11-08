# Assignment 4 — Final Results Audit (evidence-based; validation pending)

**Audit date:** 2026-11-08. **Scope:** exported artifacts in `RAG_Assignment4_BENCHMARK_V2`. This is a finalized *audit document*, NOT a claim that the experiment is fully validated or submitted.

## 1. Run accounting and score eligibility

The frozen protocol specifies 20 TEST questions (16 answerable, 4 unanswerable) × 8 conditions = **160 planned main generations**. The `main_results_DRAFT_not_for_submission.csv` table reports **16 planned answerable observations per condition** (128 total) because its completeness/accuracy table excludes the four unanswerable questions per condition; the unanswerable outcomes appear separately in `unanswerable_abstention.csv` (4 per condition, 32 outcomes). **Do not interpret 128 as 32 missing generations.** **Raw-log verification completed:** `logs/generations_test.jsonl` contains exactly 160 records, 160 distinct question–condition keys, 20 records per condition, and all 160 have generation status `ok`. The 16 ablation runs are a separate design and should not be added to main-condition denominators.

For the answerable subset, reported valid score counts by condition are: no_retrieval 16/16, random5 15/16, bm25_5 13/16, k1 16/16, k3 15/16, k5 16/16, k10 16/16, control 15/16. These counts sum to **122 valid / 128 planned answerable observations**, with **6 excluded from the main summary**. `incomplete_or_invalid_scores.csv` lists six `judge_invalid` score records (Q02/bm25_5, Q11/bm25_5, Q12/control, Q14/bm25_5, Q17/random5, Q17/k3). These are **scoring failures**, not automatically generation failures. The table's `n_failure` is a summary exclusion count; report the detailed `score_status` and generation status separately. Retain all invalid rows and raw judge outputs.

## 2. Main answerable-question results

Numbers below are exploratory exports, **not human-validated final estimates**. The intervals are the reported bootstrap confidence intervals; do not infer significance from unpaired interval overlap alone.

| Condition | Valid / 16 | Completeness | Reported 95% CI | Accuracy (answered, scoreable only) | Gold-paper recall |
|---|---:|---:|---|---:|---:|
| no_retrieval | 16 | 0.3625 | [0.2500, 0.4875] | 0.3974 | 0.0000 |
| random5 | 15 | 0.4933 | [0.3600, 0.6133] | 0.3496 | 0.0889 |
| bm25_5 | 13 | 0.5385 | [0.3692, 0.6923] | 0.4135 | 0.8974 |
| k1 | 16 | 0.3875 | [0.2625, 0.5250] | 0.4449 | 0.3021 |
| k3 | 15 | 0.3067 | [0.1733, 0.4667] | 0.3127 | 0.6889 |
| k5 | 16 | 0.3750 | [0.2250, 0.5250] | 0.3052 | 0.7917 |
| k10 | 16 | 0.1500 | [0.0375, 0.3000] | 0.1595 | 0.9375 |
| control | 15 | 0.4000 | [0.2400, 0.5733] | 0.4583 | 0.3000 |

**Interpretation:** BM25-5 has the highest descriptive completeness (0.5385) among these exports; dense k10 has the highest gold-paper recall (0.9375) but lowest completeness (0.1500). This does not establish causal superiority or a monotonic benefit of more passages. Different `n_valid` values and the six judge-invalid cases limit direct comparison.

**Critical metric caveat:** Almost every answered claim is marked uncited; the resulting `hallucination_rate` near 1.0 measures **lack of support by supplied passages under the scoring rule**, not a proven rate of false scientific statements. Closed-book answers have no supplied passages by design; their 1.0 unsupported rate is definitional. Citation grounding (whether a recognized citation maps to an available passage) and semantic evidence support (whether a passage substantiates a claim) must be reported separately. `citation_rate=0` does not prove a statement is false. For accuracy and unsupported-claim rates, show `n_answered`, `n_accuracy`, and `n_hallucination` and never impute missing scores as zeros.

## 3. Hypothesis testing and confidence intervals

The Friedman omnibus test for completeness reports χ²=8.8584, **p=0.06474**, 15 complete pairs, Kendall's W=0.1476: **not significant at α=0.05**. Accuracy reports χ²=7.7526, p=0.10107, 11 complete pairs: also not significant. The hallucination-rate Friedman statistic is missing and must not be described as a successful test.

In Holm-adjusted pre-registered completeness comparisons, k1 vs k3 (p_adj=1.0), k3 vs k5 (p_adj=1.0), k5 vs k10 (p_adj=0.05621), and k5 vs control (p_adj=1.0) are **not significant**. The k5−k10 descriptive paired difference is +0.225 with reported bootstrap CI [0.075, 0.375], but the Holm-adjusted p-value is 0.05621; do not label it statistically significant. Baseline comparisons for completeness and the accuracy comparisons likewise show no adjusted significance in the exported table. For the ablation, completeness `without_minus_with = -0.05`, CI [-0.175, 0.0625], Wilcoxon p=0.7197: no detectable effect. The other ablation results are also not significant. McNemar abstention comparisons report p=1.0, 0.5, and 1.0, respectively; none significant.

**Hypothesis decision:** On the current exploratory data, **none of the tested superiority/difference hypotheses is statistically confirmed at corrected α=0.05**. More retrieved gold papers do not reliably translate to better answer completeness in these observations. A claim about hallucination reduction cannot be made using the uncited-claim proxy. Keep formal H1–Hn wording aligned with the signed protocol rather than inventing hypothesis labels.

## 4. Validation status and reviewer attribution

`validation_status.json` explicitly states `complete=false`, `independent_human_human_kappa_available=false`, `judge_grounding_kappa=null`, and `judge_exploratory=true`.

- **Reviewer A:** team-reported human-reviewed assessment. Independent completion and review protocol should be documented from original sheets and timestamps.
- **Reviewer B:** AI-assisted (Codex), reviewed/confirmed by Reviewer B according to the status file. This must **not** be labeled a second unaided independent human review.
- **Reviewer A vs Reviewer B (AI-assisted):** n=135, raw agreement 0.6667, descriptive κ=0.3034; the `independent_human_kappa` field is empty. **Do not report independent human–human kappa as confirmed.**
- **Judge validation:** no verified judge-versus-independent-human grounding kappa. Therefore judge-derived outcomes remain **EXPLORATORY**. Independent review and documented consensus are required for a validated result.

The error taxonomy export contains **30 E1 retrieval misses (100% of the 30 classified cases)**. This is a purposive, non-representative selection and cannot be presented as the population-wide E1–E7 distribution. No E2–E7 frequency is established by that table.

## 5. Finalization gate / what remains

1. **TEST generation log verified (160/160 unique, all `ok`).** Still audit the ablation raw log and check CI implementation against paired resampling code.
2. Resolve or transparently retain six `judge_invalid` scores; rerun scoring only with a documented deterministic method and preserve original logs.
3. Obtain independent human labels from a second unaided reviewer (or explicitly report this requirement unmet), adjudicate consensus, calculate genuine human–human κ and judge–human κ on aligned items.
4. Document protocol deviations, benchmark hashes, post-freeze wording edits and instructor approval; verify independent reproduction and Moodle receipt separately.
5. Only after the gates pass regenerate the main table and replace the `DRAFT_not_for_submission` name with a validated `FINAL` output. **Do not rename an exploratory file as a validated final result.**

## Source artifacts

`protocol_freeze.json`; `final_config.json`; `results/main_results_DRAFT_not_for_submission.csv`; `results/incomplete_or_invalid_scores.csv`; `results/friedman_tests.csv`; `results/pairwise_tests.csv`; `results/ablation_tests.csv`; `results/mcnemar_abstention.csv`; `results/validation_status.json`; `results/judge_validation_transparent.csv`; `results/reviewer_a_reviewer_b_label_comparison.csv`; `results/appendix_B_error_analysis.csv`; `results/unanswerable_abstention.csv`; `README.md`.
