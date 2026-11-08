# Assignment 4 — Protocol Deviations and Measurement Clarifications

**Prepared:** 2026-11-08. **Status:** Final documentation of known deviations and limitations; not a statement of instructor approval or completed validation.

| ID | Item | Recorded condition / change | Consequence and required action |
|---|---|---|---|
| PD-01 | Post-freeze benchmark revision | README reports seven key-point wording revisions after the original freeze of `benchmark_questions_v2.json`. Frozen protocol lists benchmark SHA256 `2e62cd61ece5d17cb0e3213bfe4194a514881681880c12a6bc4dd2f6e70a733d`. | Preserve before/after versions, seven-item change log, hashes and timestamps; obtain/document instructor approval. Do not imply the signed protocol authorized changes without evidence. |
| PD-02 | Control passage construction | Five non-overlapping windows of up to 550 tokens from the top-ranked paper, rather than five distinct papers. | Report control as single-paper five-passage control; include source spans and prompt-token matching audit; request review if interpretation differs from signed protocol. |
| PD-03 | Citation parsing / grounding | Generated outputs often lack recognizable source citations; `citation_rate` near zero. | Separate syntactic citation compliance, citation-to-source grounding, and semantic support by any supplied evidence. An uncited but true statement is not necessarily a factual hallucination. Preserve raw responses and parser version. |
| PD-04 | Judge invalid / missingness | Six answerable TEST scores flagged `judge_invalid`; some completeness or accuracy values missing. | Exclude invalid scores only from metrics they cannot support, show denominators, preserve original judge responses and parser revision. Avoid zero-imputation and avoid labeling scoring errors as failed generations. |
| PD-05 | Closed-book evidence support | No retrieval passages by design; claims unsupported by supplied passages score 1.0 by definition. | Do not interpret unsupported rate as a factual hallucination rate or evidence of retrieval causality. Analyze reference correctness independently. |
| PD-06 | Manual validation provenance | Reviewer A described as human-reviewed; Reviewer B labels described as Codex-assisted and Reviewer B-confirmed. Comparison κ=0.3034, n=135 is descriptive only. | Human–human independent κ remains unavailable. Do not call it verified; obtain two unaided independent label sets and adjudication, or report the limitation. Judge-derived results remain exploratory. |
| PD-07 | Experiment denominators | 20 TEST questions × 8 conditions = 160 planned generations, of which 16 answerable × 8 = 128 rows for main answerable metrics and 4 unanswerable × 8 = 32 for abstention analysis. | State denominators explicitly; verify raw generation log completeness, statuses and duplicates. Never infer 32 missing runs from the main answerable-only table. |
| PD-08 | Ablation and hypothesis interpretation | 16 ablation runs are separate from the main 160. Holm-adjusted k5 vs k10 completeness p=0.05621 despite positive descriptive CI. | Apply pre-registered multiple-comparison correction. No adjusted-significant superiority claim; do not conflate descriptive intervals with multiplicity-adjusted inference. |
| PD-09 | Reproduction and submission | Current output status says independent reproduction, GitHub release and Moodle receipt not verified. | Keep these marked unverified until logs, commit/tag and receipt evidence exist. |

## Measurement definitions for the report

**Citation compliance:** fraction of claims containing a recognized citation marker. **Citation grounding:** fraction of citation markers correctly mapping to supplied source passages. **Evidence support:** fraction of factual claims substantively supported by the passages, with or without explicit citation, using a clearly documented evidence rubric. **Factual correctness:** whether the claim is scientifically accurate according to reference sources; cannot be inferred from citation presence alone. **False abstention:** refusal despite sufficient evidence, assessed on answerable items. **Retrieval miss:** missing gold reference papers in retrieved set, not necessarily an incorrect generated answer.

## Approval log (not yet verified)

- Signed protocol and actual upload timestamp: **UNVERIFIED**.
- Benchmark post-freeze change approval: **UNVERIFIED**.
- Independent human–human agreement: **NOT ESTABLISHED**.
- Independent clean reproduction: **UNVERIFIED**.
- GitHub release and Moodle submission receipt: **UNVERIFIED**.

This document is ready to attach as an honest deviation record. It does not authorize converting incomplete validation to a completed state.
