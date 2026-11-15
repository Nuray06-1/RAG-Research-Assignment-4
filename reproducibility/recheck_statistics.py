from pathlib import Path
import csv,json,re,hashlib,platform,warnings
import numpy as np,pandas as pd,scipy,statsmodels
from scipy.stats import friedmanchisquare,wilcoxon,rankdata,binomtest
from statsmodels.stats.multitest import multipletests
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent/'inputs');parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'recomputed');args=parser.parse_args()
ROOT=args.inputs/'raw'; PUBLISHED=args.inputs/'published'; OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
SEED=42;B=10000;ORDER=['no_retrieval','random5','bm25_5','k1','k3','k5','k10','control']
def parse(s,labels):
 m=re.match(r'^\s*('+'|'.join(labels)+r')\b',str(s),re.I)
 return m[1].upper() if m else 'JUDGE_INVALID'
def reconstruct(prefix):
 a=pd.read_csv(ROOT/'results'/f'{prefix}_answer_scores.csv');c=pd.read_csv(ROOT/'results'/f'{prefix}_claim_scores.csv').fillna('');k=pd.read_csv(ROOT/'results'/f'{prefix}_keypoint_scores.csv').fillna('')
 c['reparse']=c.raw_correctness.map(lambda x:parse(x,['CORRECT','INCORRECT','UNVERIFIABLE']));k['reparse']=k.judge_raw.map(lambda x:parse(x,['COVERED','MISSING']))
 for i,r in a.iterrows():
  if not r.answerable or r.generation_status!='ok':continue
  if r.abstained:
   a.loc[i,'completeness']=0.;continue
  cc=c[(c.question_id==r.question_id)&(c.condition==r.condition)];kk=k[(k.question_id==r.question_id)&(k.condition==r.condition)]
  invalid=('JUDGE_INVALID' in set(cc.reparse)) or ('JUDGE_INVALID' in set(kk.reparse))
  a.loc[i,'completeness']=float((kk.reparse=='COVERED').sum()/len(kk)) if len(kk) and 'JUDGE_INVALID' not in set(kk.reparse) else np.nan
  a.loc[i,'accuracy']=float((cc.reparse=='CORRECT').sum()/len(cc)) if len(cc) and 'JUDGE_INVALID' not in set(cc.reparse) else np.nan
  # Grounding unchanged: UNCITED is counted ungrounded in the historical metric.
  a.loc[i,'score_status']='judge_invalid' if invalid else 'ok'
 a.to_csv(OUT/f'{prefix}_answer_scores_reparsed.csv',index=False)
 return a
main=reconstruct('test');abl=reconstruct('ablation');a=main[main.answerable].copy()
def ci(v,seed):
 v=np.asarray(pd.to_numeric(pd.Series(v),errors='coerce'),dtype=float);v=v[np.isfinite(v)]
 if not len(v):return np.nan,np.nan,np.nan,0
 rng=np.random.default_rng(seed);means=rng.choice(v,size=(B,len(v)),replace=True).mean(axis=1)
 return float(v.mean()),float(np.percentile(means,2.5)),float(np.percentile(means,97.5)),len(v)
def rb(v):
 v=np.asarray(v);v=v[np.isfinite(v)&(v!=0)]
 if not len(v):return 0.
 ranks=rankdata(abs(v),method='average');return float((ranks[v>0].sum()-ranks[v<0].sum())/ranks.sum())
def wp(d,x,y):
 if len(d)==0:return np.nan
 if np.allclose(d,0):return 1.
 return float(wilcoxon(x,y,zero_method='wilcox').pvalue)
meanrows=[]
for cond in ORDER:
 good=a[(a.condition==cond)&(a.score_status=='ok')];respond=good[~good.abstained]
 for metric,frame,seed in [('completeness',good,43),('accuracy',respond,44),('hallucination_rate',respond,45)]:
  mean,lo,hi,n=ci(frame[metric],seed);meanrows.append(dict(condition=cond,metric=metric,n=n,mean=mean,ci_low=lo,ci_high=hi,seed=seed,bootstrap_resamples=B))
pd.DataFrame(meanrows).to_csv(OUT/'main_CI_recomputed.csv',index=False)
BREADTH=['k1','k3','k5','k10','control'];PLANNED=[('k1','k3'),('k3','k5'),('k5','k10'),('k5','control')];BASE=[('k5','no_retrieval'),('k5','random5'),('k5','bm25_5')]
def wide(metric,cols):return a.pivot_table(index='question_id',columns='condition',values=metric,aggfunc='first').reindex(columns=cols)
pairs=[];omni=[]
for metric in ['completeness','accuracy','hallucination_rate']:
 w=wide(metric,BREADTH).dropna();n=len(w)
 with warnings.catch_warnings():
  warnings.simplefilter('ignore');stat,p=friedmanchisquare(*[w[c].values for c in BREADTH]) if n>=2 else (np.nan,np.nan)
 omni.append(dict(metric=metric,n_complete_pairs=n,friedman_chi_square=stat,p_value=p,kendalls_w=stat/(n*4) if n else np.nan,exploratory=True))
 for family,comparisons in [('pre_registered',PLANNED),('baselines',BASE if metric!='hallucination_rate' else BASE[1:])]:
  es=[]
  for x,y in comparisons:
   w=wide(metric,[x,y]).dropna();d=w[x].values-w[y].values;mu,lo,hi,_=ci(d,61)
   es.append(dict(metric=metric,family=family,a=x,b=y,n_pairs=len(w),n_nonzero=int(np.count_nonzero(d)),difference_a_minus_b=mu,ci_low=lo,ci_high=hi,effect_rank_biserial=rb(d),p_raw=wp(d,w[x],w[y])))
  adjusted=multipletests([e['p_raw'] if np.isfinite(e['p_raw']) else 1 for e in es],alpha=.05,method='holm')[1]
  for e,p in zip(es,adjusted):e.update(p_holm=float(p) if np.isfinite(e['p_raw']) else np.nan,p_holm_below_005=bool(np.isfinite(e['p_raw']) and p<.05),exploratory=True)
  pairs+=es
pd.DataFrame(omni).to_csv(OUT/'friedman_recomputed.csv',index=False);pd.DataFrame(pairs).to_csv(OUT/'pairwise_recomputed.csv',index=False)
ab=[];base=a[a.condition=='k5'].set_index('question_id');v=abl.set_index('question_id')
for metric in ['completeness','accuracy','hallucination_rate','citation_rate']:
 w=base[[metric]].join(v[[metric]],lsuffix='_with',rsuffix='_without').dropna();d=w[f'{metric}_without']-w[f'{metric}_with'];mu,lo,hi,_=ci(d,42)
 ab.append(dict(metric=metric,n_pairs=len(w),without_minus_with=mu,ci_low=lo,ci_high=hi,wilcoxon_p=wp(d,w[f'{metric}_without'],w[f'{metric}_with']),exploratory=True))
pd.DataFrame(ab).to_csv(OUT/'ablation_recomputed.csv',index=False)
mc=[];w=a[a.score_status=='ok'].pivot_table(index='question_id',columns='condition',values='abstained',aggfunc='first')
for x,y in [('k3','k5'),('k5','control'),('k5','no_retrieval')]:
 z=w.reindex(columns=[x,y]).dropna();b=int(((z[x]==False)&(z[y]==True)).sum());c=int(((z[x]==True)&(z[y]==False)).sum());p=binomtest(min(b,c),b+c,.5).pvalue if b+c else 1.
 mc.append(dict(a=x,b=y,n_pairs=len(z),discordant_b=b,discordant_c=c,exact_mcnemar_p=p))
pd.DataFrame(mc).to_csv(OUT/'mcnemar_recomputed.csv',index=False)
# Compare all numeric columns actually present in the current published tables.
comparisons=[]
def compare(name,new,keys,cols):
 old=pd.read_csv(PUBLISHED/name)
 for _,r in old.iterrows():
  matches=[z for z in new if all(str(z[k])==str(r[k]) for k in keys)];assert len(matches)==1,(name,dict(r),len(matches))
  z=matches[0]
  for col in cols:
   ov=float(r[col]);nv=float(z[col]);both_nan=np.isnan(ov) and np.isnan(nv);ok=both_nan or np.isclose(ov,nv,rtol=1e-9,atol=1e-12,equal_nan=True)
   comparisons.append(dict(table=name,key='|'.join(str(r[k]) for k in keys),field=col,published=ov,recomputed=nv,match=bool(ok)))
compare('friedman_tests.csv',omni,['metric'],['n_complete_pairs','friedman_chi_square','p_value','kendalls_w'])
compare('pairwise_tests.csv',pairs,['metric','family','a','b'],['n_pairs','n_nonzero','difference_a_minus_b','ci_low','ci_high','effect_rank_biserial','p_raw','p_holm'])
compare('ablation_tests.csv',ab,['metric'],['n_pairs','without_minus_with','ci_low','ci_high','wilcoxon_p'])
old=pd.read_csv(PUBLISHED/'main_results_DRAFT_not_for_submission.csv')
for _,r in old.iterrows():
 for metric in ['completeness','accuracy','hallucination_rate']:
  z=next(e for e in meanrows if e['condition']==r.condition and e['metric']==metric)
  for col,newcol in [(metric,'mean'),(('hallucination' if metric=='hallucination_rate' else metric)+'_ci_low','ci_low'),(('hallucination' if metric=='hallucination_rate' else metric)+'_ci_high','ci_high')]:
   comparisons.append(dict(table='main_results_DRAFT_not_for_submission.csv',key=r.condition+'|'+metric,field=col,published=float(r[col]),recomputed=z[newcol],match=bool(np.isclose(float(r[col]),z[newcol],rtol=1e-9,atol=1e-12,equal_nan=True))))
pd.DataFrame(comparisons).to_csv(OUT/'published_vs_recomputed.csv',index=False)
env=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,statsmodels=statsmodels.__version__,bootstrap_resamples=B,seed=SEED,ci_method='percentile bootstrap of question-level values; paired differences resampled within contrast',filters='historical main table: whole-row score_status == ok; historical pairwise tests: metric-specific nonmissing pairs',unchanged_machine_labels='leading-label reparse only; AI semantic review not used to recalculate these tests')
(OUT/'statistics_environment.json').write_text(json.dumps(env,indent=2));print('Comparison fields:',len(comparisons),'mismatches:',sum(not e['match'] for e in comparisons));print(pd.DataFrame(comparisons).query('match==False').to_string(index=False));print('OMNIBUS',omni);print('ABLATION',ab)
