# Fresh Colab computational run — 16 November 2026

The full pipeline completed in a fresh Colab T4 runtime, writing only to a separate `RAG_Assignment4_REPRO_20261116T175303Z` folder. The computational criterion can be recorded as completed; fresh human validation and independent human reproduction remain unverified.

## Execution and preservation

- Started: 17:53:03 UTC; completed: 18:27:41 UTC (22:53–23:27, Asia/Almaty).
- New main generations: 160/160 successful; new ablations: 16/16 successful.
- Six repeated answers in the determinism check were byte-identical within this run.
- New judge scoring, confidence intervals, paired tests, subgroup/efficiency tables and all four figures were exported.
- Main score statuses: 154 `ok`, six `judge_invalid`. Invalid assessments remain explicit and are not imputed as negative labels or zeros.
- All 165 protected source files matched their pre-run SHA-256 hashes. The scope includes corpus JSON, benchmark, indexes, historical configuration, logs and results; original PDF directories are excluded from this hashing scope.
- Historical repository results, figures, manual labels and the archived executed notebook were not replaced. The existing `final` tag continues to identify the archived release.

The runnable code was copied from commit [`762d3a6`](https://github.com/Nuray06-1/RAG-Research-Assignment-4/commit/762d3a6). Subsequent commit `949d136` adds frozen-generation parameter assertions, stronger path-guard tests and corrected explanatory text; it does not change the generation or scoring algorithms used in the completed run. The saved executed copy also corrects the inherited Step 22 paragraph so that it does not claim completed human annotation of fresh answers.

Python 3.13.16, PyTorch 2.14.1+cu130, Transformers 4.57.6, Tesla T4. Generator: `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`. Judge: `microsoft/Phi-3.5-mini-instruct`, revision `2fe192450127e6a83f7441aef6e3ca586c338b77`, loaded through native Transformers. Fresh scorer: `A4_reproduction_leading_label_v2`.

## Verification and limits

The downloaded archive contains 48 files. All 47 payload files match `RESULTS_MANIFEST.json`. A separate local execution of `reproducibility/recheck_statistics.py` against the fresh score CSVs agrees with all **264 numeric fields** checked in the fresh main intervals, Friedman tests, pairwise tests and ablation tests (zero mismatches). This verifies arithmetic agreement, not correctness of the judge's semantic decisions.

Across all 160 main records, prompt hashes, configuration hashes, selected chunk IDs and paper IDs match the historical run. Answer text is byte-identical in 120/160 records; 40 differ. This is a completed computational rerun, not a claim of byte-identical reproduction across environments. Fresh numerical results remain separate and exploratory. Neither hypotheses nor disputed human labels are certified by this run.

Frozen configuration SHA-256:
`dd8f5173eafa452833c559b96a8261a39cfeddd62502c1a74fe1d75e05be9583`

Archive: `RAG_Assignment4_REPRO_20261116T175303Z_COMPUTATIONAL_REPRODUCTION.zip`

Archive SHA-256:
`5dffee6c2b37b049e087b2efae34cc6d2a117d1b80f4e24e25ae42073f7830cf`

The full archive and executed notebook were saved to the owner's Drive and downloaded locally. They are not bundled publicly because the new logs include source-passage text. Machine-readable status, environment and verification counts are in [`verification.json`](../reproducibility/runs/2026-11-16/verification.json).

Colab briefly reported an autosave conflict after computation. The current executed copy was saved successfully and downloaded; the independently written run archive was unaffected.
