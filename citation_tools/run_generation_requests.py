"""Run the separate prepared variant on a CUDA runtime; retain every failed output.
Requires the original project transformers/torch environment. No retries or score selection.
"""
import argparse,json,hashlib,datetime,time
from pathlib import Path
from citation_contract import validate_output,render_checked

def main():
    p=argparse.ArgumentParser();p.add_argument('--requests',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists():raise FileExistsError('Use a new output path; original runs must never be overwritten')
    requests=[json.loads(x) for x in args.requests.read_text().splitlines() if x.strip()]
    if not requests:raise ValueError('Empty request list')
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM,set_seed
    if not torch.cuda.is_available():raise RuntimeError('Run in a separate CUDA runtime such as the original Colab environment')
    names={r['generator'] for r in requests}
    if len(names)!=1:raise ValueError('One fixed generator is required')
    name=next(iter(names));tok=AutoTokenizer.from_pretrained(name);model=AutoModelForCausalLM.from_pretrained(name,torch_dtype=torch.float16,device_map='auto').eval()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:
        for r in requests:
            result={'question_id':r['question_id'],'condition':r['condition'],'variant':r['variant'],'request_sha256':r['request_sha256'],'original_prompt_sha256':r['original_prompt_sha256'],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempt':1,'historical_model_output':False}
            start=time.perf_counter()
            try:
                assert hashlib.sha256(json.dumps(r['messages'],ensure_ascii=False).encode()).hexdigest()==r['request_sha256']
                set_seed(r['seed']);prompt=tok.apply_chat_template(r['messages'],tokenize=False,add_generation_prompt=True);inputs=tok(prompt,return_tensors='pt').to(model.device)
                result['input_tokens']=inputs['input_ids'].shape[1]
                with torch.inference_mode():generated=model.generate(**inputs,max_new_tokens=r['max_new_tokens'],do_sample=False,pad_token_id=tok.eos_token_id)
                ids=generated[0,inputs['input_ids'].shape[1]:];raw=tok.decode(ids,skip_special_tokens=True);result.update(raw_response=raw,output_tokens=len(ids),generation_status='ok')
                try:
                    checked=validate_output(raw,json.loads(r['messages'][1]['content'])['sources'])
                    result['citation_check']=checked
                    result['citation_status']=checked['status']
                    if checked['status']=='citation_contract_passed_not_human_validation':result['checked_answer']=render_checked(checked)
                except (ValueError,TypeError,KeyError) as e:
                    result.update(citation_status='invalid_or_semantic_review_required',citation_error=str(e))
            except Exception as e:
                result.update(generation_status='error',error_type=type(e).__name__,error=str(e))
            result['latency_sec']=time.perf_counter()-start;f.write(json.dumps(result,ensure_ascii=False)+'\n');f.flush()
    print('Saved all attempts; no automatic scientific improvement or human validation is claimed:',args.output)
if __name__=='__main__':main()
