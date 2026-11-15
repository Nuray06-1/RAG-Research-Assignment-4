# Citation repair: historical run and separate revisions

## Why the citations were missing

The historical generator was instructed to cite [Source N], but the instruction was not enforced by a validation gate. All 160 outputs ended with EOS and none reached 512 generated tokens: output-budget truncation does not explain the missing markers in these saved runs. Only four of the 759 extracted claims had recognised in-range source markers. Literal Source N mentions occur in only six answers. Accepting alternative syntax cannot recover citations that were never produced.

Several answers also confuse method identities, including FAIR-RAG evidence refinement versus a different study of fairness in RAG. Numbering an unrelated passage would not fix such a claim. A missing citation, an unsupported attribution and an incorrect scientific statement are distinct failures.

## Changes actually executed

All 160 historical input prompts were reconstructed from frozen benchmark questions, original retrievals, Qwen tokenization and the 550-token passage cap. Every reconstructed SHA-256 matched the logged prompt hash. The frozen chunks and benchmark also match their archived hashes.

`results/citation_repair_v1/` contains a **post-hoc revised copy**, not fresh model generations. The tool checked every previously uncited extracted claim and found six full existing statements reproduced verbatim in the exact displayed source text. It attached the corresponding source marker to those six statements, changing two answers: Q06/k3 and Q08/control. Each attachment records the original claim ID, source position, chunk, paper, URL and passage hash. No wording or factual content was rewritten. The original logs and historical metrics remain unchanged.

The six attachments establish textual attribution to a supplied passage, not independent verification of the paper's assertions. The four pre-existing citation markers were preserved and are not newly certified. Another 749 uncited claims have no full-claim verbatim witness under this conservative rule; that does not mean they are false. Paraphrases require a separate semantic support check. No blanket citation list is counted as claim-level grounding.

The revised answers must not inherit the old judge scores, claim IDs computed from modified text, or a claim of improved completeness/accuracy/hallucination. New evaluation has not been executed. Merely attaching a marker adds no missing key point and corrects no false factual claim. BM25's stronger descriptive completeness is not explained away by the missing citations.

## Gate for a new generation version

`citation_tools/citation_contract.py` supplies a structured-output instruction and fail-closed validation:

- Each atomic statement must name an existing source and supply a short exact supporting excerpt.
- Nonexistent source indices, invented excerpts and uncited claims are rejected.
- Excerpt existence alone never validates a paraphrased claim. A separate actual semantic verifier must return SUPPORTED. Without one, only a statement equal to the source quotation can pass.
- A rejected/invalid response is recorded as a failure, not converted into a supported claim. A complete refusal still requires a relevance check.
- Only checked statements can be rendered as [Source N] answers. This is not a statement of independent human validation.

`prepare_generation_requests.py` prepares 140 separate retrieval-condition requests using the original retrieved passages. The 20 closed-book cases cannot receive citations to nonexistent input evidence. Generation inputs omit reference answers, keypoints and annotation labels. Preparation is not execution. The model remains Qwen/Qwen2.5-1.5B-Instruct, greedy decoding, seed42 and max_new_tokens512; JSON/evidence overhead must be recorded when comparing output budgets.

These already-inspected TEST questions cannot serve as an untouched confirmatory set for prompt tuning. Develop the new format on DEV; a rerun on the old TEST set must be labelled exploratory. Any confirmatory improvement requires independent evaluation data and separately reported original/new results. Do not retry or select variants until significance appears.

## Commands

From the repository root, using a local environment with the listed dependency:

```sh
python -m pip install -r citation_tools/requirements.txt
python citation_tools/repair_existing_citations.py --raw /path/to/private/raw --tokenizer /path/to/qwen_tokenizer.json --freeze protocol_freeze.json --output /path/to/posthoc-citation-copy
python citation_tools/prepare_generation_requests.py --raw /path/to/private/raw --tokenizer /path/to/qwen_tokenizer.json --freeze protocol_freeze.json --output /path/to/private/requests.jsonl
python citation_tools/run_generation_requests.py --requests /path/to/private/requests.jsonl --output /path/to/new-run-only/generations.jsonl
python -m unittest discover -s citation_tools -p 'test_*.py'
```

The private raw folder needs logs/generations_test.jsonl, results/test_claim_scores.csv, data/final_chunks.json and data/benchmark_questions_v2.json. Full source articles and private request payloads are not distributed here.

The generation runner requires a separate CUDA runtime with the original project torch/transformers environment. It refuses to overwrite an output file, logs one attempt for every request, retains raw invalid responses, and never treats quotation existence as semantic validation of paraphrases. It has not been executed as part of this repair; no new model answers or improved scores are reported.
