# Publication review — 8 November 2026

This package preserves the supplied experimental metrics. Publication does not certify scientific validation or independent reproduction.

## Figure correction and archived snapshots

The standalone `figures/fig1_metrics_by_k.png` and `figures/fig2_primary_by_condition.png` have been replaced with the supplied corrected images. Their SHA-256 hashes are `ca50745882cf0e6ad63cef04f45e78cb26e67374853d2d05e90f541a305e0ead` and `55be98a404a3d0b9d689f305ef3940f1e9d11626cb20586900738053ca6b994b`, respectively. Their plotted condition-level means and confidence intervals agree with the exported CSV at the displayed precision. Numerical tables were not changed.

The report and executed notebook remain archived execution records and may embed older charts. In those earlier fig1/fig2 snapshots, k5 completeness was near 0.48 rather than the exported 0.375; the earlier fig1 accuracy also differed. Use the corrected standalone images with the exported table. Fig3 requires observation-level records absent from this package for full verification.

## Validation and reproduction

- Fifteen post-discussion disputes remain unresolved. Their claim IDs are absent; `final` is proposed, not certified consensus. No judge-versus-consensus result is established.
- Saved notebook: 62 cells, no stored error outputs. Execution was not rerun during publication review.
- JSON and CSV files parse successfully. There are eight main conditions, 128 planned answerable observations and 122 valid judge scores.
- The package lacks the Assignment3 corpus/index, full generation logs, benchmark JSON, and several appendices referenced by the report. It is an execution record, not a standalone end-to-end reproduction.
- requirements.txt is the supplied environment snapshot; installation and compatibility are not verified.
- No complete scientific-paper PDFs are present. Textual claims and reference summaries remain research artifacts; per-source redistribution permissions are not established by this check.
- Automated pattern scans found no credential tokens, email addresses or user-home paths. Personal names are pseudonymized in the publication copy, including annotation headers and notebook text. Label values and methodological provenance are preserved. Nonessential notebook widget metadata was removed. Original archive remains local and is not uploaded.

## Remote publication

Initial publication was verified with release `v1.0.0`. These final corrections preserve the scientific results and prepare the `assignment-4` tag and requested public publication; consult GitHub for the verified commit, tag and current visibility.
