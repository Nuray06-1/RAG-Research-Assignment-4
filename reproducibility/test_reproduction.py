"""Exercise fresh generation, safe resumption, and preservation of source logs."""
import json,hashlib,tempfile,unittest,types,datetime
from pathlib import Path
import os
import pandas as pd
NOTEBOOK=Path(__file__).resolve().parents[1]/'notebooks/Assignment4_Reproduce.ipynb'
class ReproductionTests(unittest.TestCase):
 def test_cells_compile_and_no_historical_output_resets(self):
  n=json.loads(NOTEBOOK.read_text())
  for i,c in enumerate(n['cells']):
   if c['cell_type']!='code':continue
   s=''.join(c['source']);compile('\n'.join(x for x in s.splitlines() if not x.startswith('%')),str(i),'exec')
   self.assertNotIn('run_dir = "/content/drive/MyDrive/RAG_Assignment4_BENCHMARK_V2"',s)
  self.assertTrue(all(not c.get('outputs') for c in n['cells'] if c['cell_type']=='code'))
 def test_160_new_records_resume_without_reusing_source_answers(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);source=root/'historical.jsonl';source.write_text('ARCHIVED ANSWER\n')
   digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
   before=digest(source);out=root/'reproduction';(out/'logs').mkdir(parents=True)
   conditions=['no_retrieval','random5','bm25_5','k1','k3','k5','k10','control']
   benchmark=[dict(question_id=f'Q{i:02}',question='test',answerable=True,question_type='smoke',supporting_papers=['p']) for i in range(20)]
   calls=[]
   def generate(prompt):calls.append(prompt);return dict(answer='NEW ANSWER',input_tokens=3,output_tokens=2,latency_sec=0,stop_reason='eos')
   env=dict(os=os,json=json,hashlib=hashlib,Path=Path,datetime=datetime.datetime,timezone=datetime.timezone,pd=pd,
    REPRODUCTION_MODE=True,run_dir=str(out),output_root=out.resolve(),file_sha256=digest,PROTECTED_SOURCE_HASHES={str(source):before},
    benchmark=benchmark,TEST_IDS=[q['question_id'] for q in benchmark],CONFIG={'conditions':conditions},CONFIG_SHA256='config',
    freeze={'benchmark_sha256':'benchmark'},SEED=42,MAX_NEW_TOKENS=512,CONTROL_ALGORITHM='control',
    torch=types.SimpleNamespace(cuda=types.SimpleNamespace(empty_cache=lambda:None,OutOfMemoryError=MemoryError)),
    get_evidence=lambda q,c:[] if c=='no_retrieval' else [dict(chunk_id='chunk',paper_id='p',text='evidence')],
    prompt_for_condition=lambda *a:'prompt',generate=generate)
   code=''.join(json.loads(NOTEBOOK.read_text())['cells'][33]['source'])
   import contextlib,io
   with contextlib.redirect_stdout(io.StringIO()):exec(code,env)
   path=out/'logs/generations_test.jsonl';initial=path.read_bytes()
   self.assertEqual(len(calls),160);self.assertEqual(len(initial.splitlines()),160)
   self.assertEqual(digest(source),before);self.assertNotIn(b'ARCHIVED ANSWER',initial)
   with contextlib.redirect_stdout(io.StringIO()):exec(code,env)
   self.assertEqual(len(calls),160);self.assertEqual(path.read_bytes(),initial)
   # Refuse a changed configuration rather than mixing different runs on resume.
   env['CONFIG_SHA256']='different'
   with self.assertRaises(AssertionError),contextlib.redirect_stdout(io.StringIO()):exec(code,env)
   self.assertEqual(path.read_bytes(),initial)
if __name__=='__main__':unittest.main()
