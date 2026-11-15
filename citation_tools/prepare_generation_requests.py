"""Prepare a separate citation-format experiment using the original retrievals.
Does not run a model or access reference answers/keypoints during generation.
"""
import argparse,json,hashlib
from pathlib import Path
from tokenizers import Tokenizer
from citation_contract import CITED_OUTPUT_INSTRUCTION

def main():
    p=argparse.ArgumentParser();p.add_argument('--raw',type=Path,required=True);p.add_argument('--tokenizer',type=Path,required=True);p.add_argument('--freeze',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    freeze=json.loads(args.freeze.read_text())
    for name,key in [('final_chunks.json','chunks_sha256'),('benchmark_questions_v2.json','benchmark_sha256')]:
        assert hashlib.sha256((args.raw/'data'/name).read_bytes()).hexdigest()==freeze[key],name
    tok=Tokenizer.from_file(str(args.tokenizer));chunks={x['chunk_id']:x for x in json.loads((args.raw/'data/final_chunks.json').read_text())};bench={x['question_id']:x for x in json.loads((args.raw/'data/benchmark_questions_v2.json').read_text())};generations=[json.loads(l) for l in (args.raw/'logs/generations_test.jsonl').read_text().splitlines()]
    requests=[]
    for g in generations:
        if g['condition']=='no_retrieval':continue # No source exists for a closed-book answer.
        es=g['virtual_control_passages'] if g['condition']=='control' else [chunks[x] for x in g['chunk_ids']]
        sources=[{'source_index':i,'paper_id':e['paper_id'],'chunk_id':e['chunk_id'],'text':tok.decode(tok.encode(e['text'],add_special_tokens=False).ids[:550],skip_special_tokens=True)} for i,e in enumerate(es,1)]
        payload={'question':bench[g['question_id']]['question'],'sources':sources}
        # Deliberately exclude reference_answer, key_points and any human/judge labels.
        user=json.dumps(payload,ensure_ascii=False);messages=[{'role':'system','content':CITED_OUTPUT_INSTRUCTION},{'role':'user','content':user}]
        requests.append({'question_id':g['question_id'],'condition':g['condition'],'variant':'structured-citations-v2-exploratory','messages':messages,'generator':'Qwen/Qwen2.5-1.5B-Instruct','seed':42,'do_sample':False,'max_new_tokens':512,'original_prompt_sha256':g['prompt_sha256'],'request_sha256':hashlib.sha256(json.dumps(messages,ensure_ascii=False).encode()).hexdigest(),'validation_required':'citation_contract.validate_output with an actual separate semantic verifier for paraphrases','generation_executed':False})
    assert len(requests)==140
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in requests));print('Prepared',len(requests),'requests; no generation executed; private source snippets must not be published without licence review')
if __name__=='__main__':main()
