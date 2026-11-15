"""Attach source markers only to full existing claims found verbatim in shown evidence.
No inference, no relabelled human decisions, no changes to the historical run.
"""
import argparse,csv,json,re,hashlib,collections
from pathlib import Path
from tokenizers import Tokenizer

def normalise(text):
    return re.sub(r'\s+',' ',re.sub(r'[*_`]+','',str(text))).strip()

def matching_source(claim,passages):
    needle=normalise(claim)
    if len(needle.split())<8:return None
    for index,p in enumerate(passages,1):
        if needle in normalise(p['text']):return index
    return None

def insert_marker(answer,claim,source_index):
    # Exact full-span occurrence required; never attach to a guessed boundary.
    if answer.count(claim)!=1:raise ValueError('Claim span is absent or ambiguous')
    return answer.replace(claim,claim+f' [Source {source_index}]',1)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw',type=Path,required=True)
    parser.add_argument('--tokenizer',type=Path,required=True)
    parser.add_argument('--freeze',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    freeze=json.loads(args.freeze.read_text())
    for name,key in [('final_chunks.json','chunks_sha256'),('benchmark_questions_v2.json','benchmark_sha256')]:
        assert hashlib.sha256((args.raw/'data'/name).read_bytes()).hexdigest()==freeze[key],name
    tokenizer=Tokenizer.from_file(str(args.tokenizer));chunks={x['chunk_id']:x for x in json.loads((args.raw/'data/final_chunks.json').read_text())}
    generations=[json.loads(l) for l in (args.raw/'logs/generations_test.jsonl').read_text().splitlines()]
    claims=list(csv.DictReader((args.raw/'results/test_claim_scores.csv').open()))
    assert len({(x['question_id'],x['condition']) for x in generations})==len(generations)==160
    grouped=collections.defaultdict(list)
    for c in claims:grouped[c['question_id'],c['condition']].append(c)
    repairs=[];records=[];queue=[]
    for g in generations:
        entries=[] if g['condition']=='no_retrieval' else g['virtual_control_passages'] if g['condition']=='control' else [chunks[c] for c in g['chunk_ids']]
        shown=[{**e,'text':tokenizer.decode(tokenizer.encode(str(e['text']),add_special_tokens=False).ids[:550],skip_special_tokens=True)} for e in entries]
        answer=g['answer'];patches=[]
        for c in grouped[g['question_id'],g['condition']]:
            if c['cited_sources']:continue # Original markers are preserved, not automatically certified.
            source=matching_source(c['claim'],shown)
            if source is None:
                queue.append(dict(question_id=g['question_id'],condition=g['condition'],claim_id=c['claim_id'],status='no_verbatim_witness_not_a_verdict_of_falsehood',claim=c['claim']));continue
            if answer.count(c['claim'])!=1:
                queue.append(dict(question_id=g['question_id'],condition=g['condition'],claim_id=c['claim_id'],status='ambiguous_answer_span',claim=c['claim']));continue
            answer=insert_marker(answer,c['claim'],source)
            e=shown[source-1];r=dict(question_id=g['question_id'],condition=g['condition'],claim_id=c['claim_id'],claim=c['claim'],source_index=source,source_chunk_id=e['chunk_id'],source_paper_id=e['paper_id'],source_url='https://arxiv.org/abs/'+e['paper_id'],verification='full_existing_claim_verbatim_in_shown_passage',support_scope='source-text attribution, not independent verification of the paper itself',passage_sha256=hashlib.sha256(e['text'].encode()).hexdigest())
            repairs.append(r);patches.append(r['claim_id'])
        records.append(dict(question_id=g['question_id'],condition=g['condition'],original_answer_sha256=hashlib.sha256(g['answer'].encode()).hexdigest(),posthoc_answer=answer,posthoc_answer_sha256=hashlib.sha256(answer.encode()).hexdigest(),attached_claim_ids=patches,version='posthoc-verbatim-citation-v1',original_model_output_changed=bool(patches),historical_model_behaviour=False))
    (args.output/'answers_with_verified_source_markers.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    for name,rows in [('verified_citation_attachments.csv',repairs),('claims_without_verbatim_witness.csv',queue)]:
        with (args.output/name).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    stats=dict(original_generations=len(generations),original_claims=len(claims),original_strict_cited_claims=sum(bool(c['cited_sources']) for c in claims),new_verbatim_supported_citation_attachments=len(repairs),changed_answers=sum(bool(r['attached_claim_ids']) for r in records),claims_without_verbatim_witness=len(queue),original_generation_status_counts=dict(collections.Counter(g['status'] for g in generations)),stop_reasons=dict(collections.Counter(g['stop_reason'] for g in generations)),outputs_reaching_512_tokens=sum(g['output_tokens']>=512 for g in generations),human_validation_claimed=False,completeness_or_accuracy_improvement_claimed=False,new_hallucination_rate_computed=False,original_judge_scores_reused_for_repaired_answers=False)
    (args.output/'citation_repair_status.json').write_text(json.dumps(stats,indent=2))
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
