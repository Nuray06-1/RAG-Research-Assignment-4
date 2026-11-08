# Assignment 4: Claim-Level Annotation Provenance and Agreement

**Date:** 8 November 2026

**Status:** One unaided human annotation set; one model pre-pass; human adjudication of all 54 non-agreements with written reasons. Independent human-to-human agreement **NOT ESTABLISHED**. Judge validation **EXPLORATORY**.

## 1. Column names in the circulated files do not match what the columns contain

Two files were circulated before this repository was built: `claims_FINAL_144.csv` and `final_claims_with_reasons.csv`. They carry identical data for all 144 rows under different column names.

| Contains | Named in `claims_FINAL_144.csv` | Named in `final_claims_with_reasons.csv` | Named here |
|---|---|---|---|
| Unaided manual annotation by team member A | `altynay` | `system_review` | `reviewer_a` |
| Model (Codex) pre-pass | `codex` | `human_review` | `codex` |

Verified row by row: `altynay` equals `system_review` in **144/144** rows, and `codex` equals `human_review` in **144/144** rows. This is a renaming, not two separate annotation passes.

The naming in `final_claims_with_reasons.csv` is inverted. The set produced by a person is labelled `system_review`, and the set produced by a model is labelled `human_review`. The 54 written adjudication reasons in that file repeat the inversion in their prose: sentences such as *"The human 'no' rests on lack of support"* refer to the **model** column, and *"System may have accepted a plausible product description"* refers to the **human annotator's** column.

This explains any earlier description of the second set as a manual review. Such statements were made in good faith by reading a column named `human_review`. The column name was wrong. This document records the accurate attribution, which is consistent with `PROTOCOL_DEVIATIONS_FINAL.md` (PD-06) and `FINAL_RESULTS_AUDIT_VERIFIED.md` (section 4).

## 2. Provenance chain

1. **Team member A** annotated all 144 claims manually against the frozen coding scheme, without model assistance and without access to judge output.
2. **A model pre-pass (Codex)** produced a parallel set of 144 labels. This is not a second annotator.
3. **A human adjudicator (team member D)** reviewed all 54 non-agreement rows and recorded a written reason for each, arguing from the reference answer. The adjudication sided with annotator A in 38 rows, with the model pre-pass in 15, and with neither in 1.

`claims_144_CORRECTED_PROVENANCE.csv` holds the same 144 rows under accurate column names, with the adjudication outcome made explicit per row.

## 3. The 39 / 15 split is recoverable

The release notes record that 15 items remained unresolved and that their claim IDs were not identified. The adjudication outcome recovers a candidate split matching the reported counts exactly:

- **39** = 38 rows where adjudication confirmed annotator A, plus 1 row where it matched neither label
- **15** = rows where adjudication overrode annotator A in favour of the model pre-pass

These 15 are identified individually in `claims_144_CORRECTED_PROVENANCE.csv` (`adjudication_status = disputed`). All 15 run in the same direction: annotator A marked `yes`, the adjudicated value is `no`. The team should confirm that this is what the 39/15 figure referred to before the mapping is relied on. The counts agreeing exactly is suggestive, not proof.

## 4. Agreement, and why kappa is the wrong headline

Annotator A against the model pre-pass, agreement variable `human_correct`:

| A (down) / model (across) | yes | no | Total |
|---|---:|---:|---:|
| yes | 21 | 42 | 63 |
| no | 3 | 69 | 72 |
| **Total** | **24** | **111** | **135** |

- Binary, 9 `unclear` excluded: observed 90/135 = **66.67%**, expected 52.15%, **Cohen's kappa = 0.3034**
- Three categories, all 144: observed **62.50%**, **Cohen's kappa = 0.2770**

Both reproduce exactly from the CSV. What they measure is **human versus model-assisted** agreement, which is descriptive only. It is not an inter-coder reliability estimate for the coding scheme, and it does not validate the automated judge.

The disagreements are almost entirely one-directional: **42 of 45** discordant pairs are A=`yes` / model=`no`, against 3 in the other direction. Exact McNemar two-sided **p = 8.7 x 10^-10**. Yes-rate 0.467 for annotator A against 0.178 for the model pre-pass.

The two sets are therefore not noisily disagreeing about one standard. They are applying **different thresholds**. Annotator A scored a claim `yes` when it was topically true of the literature; the model pre-pass scored `yes` only when the claim was substantively stated in the reference answer. The adjudication reasons confirm this, with 22 of 54 falling under *"detail or mechanism not stated in the reference."*

Cohen's kappa penalises exactly this kind of systematic marginal difference, so 0.3034 reflects a definitional gap in the coding scheme more than it reflects careless annotation. The honest reporting is the asymmetry and its cause, with kappa quoted alongside. The coding scheme did not pin down whether "correct" means *true* or *supported by the reference*, and that is the finding.

## 5. What is and is not established

Established: one unaided human annotation set; a model pre-pass; human adjudication of every non-agreement with a written, reference-grounded reason; a documented, statistically unambiguous threshold disagreement between the two label sets.

Not established:

- **Independent human-to-human kappa.** Only one unaided human set exists. The adjudicator saw both labels and only the 54 disagreement rows, so those judgements are conditioned on the disagreement and cannot yield an independent inter-coder coefficient. The frozen protocol's requirement that the sample be *"scored independently by two team members"* is **unmet**.
- **A certified consensus set**, pending team confirmation of section 3.
- **Judge-versus-consensus agreement**, which keeps every judge-derived metric and hypothesis test **exploratory**.
- **Human validation of the primary metric.** The protocol names **completeness** as primary. The 124 key-point judgements built for it have not been annotated by anyone. All human annotation to date covers claim-level correctness, a secondary measure. This is the largest remaining gap, and it limits every claim made about completeness.

## 6. Two defensible ways to close this

**Option 1: obtain the missing set.** A second team member annotates the same 144 claims unaided (`claims_denis_TODO.csv`, `human_correct` only, no model output visible). This yields a genuine inter-human kappa and satisfies the protocol. The adjudicator cannot be that person for rows already adjudicated.

**Option 2: declare the design as executed.** Report the study as *single unaided annotator, model pre-pass, human adjudication of disagreements*, state that independent inter-coder reliability was not obtained, report kappa = 0.3034 as human versus model-assisted with the asymmetry in section 4, and carry the unmet protocol requirement in the deviations table. This is fully defensible if declared, and matches the treatment Assignment 3 gave `step97_ai_review.csv`, described there as a *"model-assisted second opinion, not human gold-standard verification."*

Either way the gaps in section 5 remain outstanding, and no option permits describing the model pre-pass as a human reviewer.

## 7. Report-ready paragraph

> Claim-level correctness was annotated for a stratified 20% sample of 144 claims. One team member annotated all 144 items unaided against the frozen coding scheme. A parallel label set was generated by a language model as a pre-pass, and a second team member adjudicated all 54 non-agreement items, recording a written justification for each against the reference answer; the adjudication confirmed the human annotator in 38 cases and the model pre-pass in 15. Comparing the human annotation against the model pre-pass gives 66.67% observed agreement and Cohen's kappa = 0.3034 on 135 binary items (kappa = 0.2770 across all 144 with `unclear` retained). This coefficient describes human versus model agreement and is not an inter-coder reliability estimate: 42 of 45 discordant items ran in a single direction (human `yes` / model `no`; exact McNemar p = 8.7 x 10^-10), indicating that the two passes applied different thresholds for "correct", topical truth as against support by the reference answer, rather than disagreeing at random. The coding scheme did not resolve that distinction in advance, which we record as a limitation of the instrument. Independent human-to-human agreement was not obtained within the assignment period, no consensus set is certified, and the primary outcome measure, completeness, received no human annotation. All judge-derived metrics and hypothesis tests are therefore reported as exploratory.

**Final status:** one unaided human set; model pre-pass declared as such; human adjudication documented; kappa = 0.3034 reported as human versus model-assisted with the asymmetry; independent human-to-human agreement **NOT ESTABLISHED**; consensus **NOT CERTIFIED** pending section 3 confirmation; primary-metric human validation **ABSENT**; judge validation **EXPLORATORY**.
