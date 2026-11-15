"""Fail-closed citation contract for a separately registered generation experiment."""
import json,re,hashlib

def normalise(text):
    return re.sub(r'\s+',' ',str(text)).strip()

CITED_OUTPUT_INSTRUCTION = '''Answer only from the supplied sources. Give a useful partial answer when only part of the question is supported; do not invent the missing part. Do not confuse similarly named methods. Return one JSON object with keys abstained, missing_information and claims. Each claim must be one atomic statement. Each claim must have a citations list; each item must contain source_index (the integer number of a supplied source) and evidence_quote (an exact short excerpt from that source). A quotation must support this particular claim, not merely share its topic. Never insert a source number without checking its content. If no source supports any relevant answer, set abstained to true and claims to an empty list. Do not use outside knowledge, reference answers or unsupported numerical assertions.'''

def validate_output(raw,passages,semantic_verifier=None):
    """A real semantic verifier must return exactly SUPPORTED before paraphrases pass.
    Without it, only verbatim statements can pass. Quote existence alone is insufficient.
    """
    data=json.loads(raw)
    if not isinstance(data,dict) or type(data.get('abstained')) is not bool or not isinstance(data.get('claims'),list):
        raise ValueError('Invalid response schema')
    if not isinstance(data.get('missing_information'),str):raise ValueError('Missing limitations field')
    if data['abstained']:
        if data['claims']:raise ValueError('Abstention cannot contain factual claims')
        return dict(status='abstained_relevance_still_requires_review',claims=[],missing_information=data['missing_information'])
    if not data['claims']:raise ValueError('Non-abstaining answer must contain claims')
    validated=[]
    for claim in data['claims']:
        text=claim.get('text');cites=claim.get('citations')
        if not isinstance(text,str) or not text.strip() or not isinstance(cites,list) or not cites:raise ValueError('Uncited or empty claim')
        checked=[]
        for cite in cites:
            index=cite.get('source_index');quote=cite.get('evidence_quote')
            if type(index) is not int or not 1<=index<=len(passages):raise ValueError('Source index not supplied')
            passage=passages[index-1]['text']
            if not isinstance(quote,str) or len(quote.split())<5 or len(quote.split())>40 or normalise(quote) not in normalise(passage):raise ValueError('Quote missing, too long/short, or not present in cited source')
            # Full existing statement must be in the displayed source for the deterministic path.
            exact = normalise(text)==normalise(quote)
            verdict='SUPPORTED' if exact else semantic_verifier(text,quote,passage) if semantic_verifier else 'PENDING'
            if verdict!='SUPPORTED':raise ValueError('Semantic support not established; do not render/count as grounded')
            checked.append(dict(source_index=index,evidence_quote=quote,support_method='verbatim_statement' if exact else 'separate_semantic_verifier',passage_sha256=hashlib.sha256(passage.encode()).hexdigest()))
        validated.append(dict(text=text,citations=checked))
    return dict(status='citation_contract_passed_not_human_validation',claims=validated,missing_information=data['missing_information'])

def render_checked(result):
    if result['status']!='citation_contract_passed_not_human_validation':raise ValueError('Only checked claims may be rendered')
    lines=[]
    for c in result['claims']:
        lines.append(c['text']+' '+' '.join(f"[Source {v}]" for v in sorted({x['source_index'] for x in c['citations']})))
    if result['missing_information']:lines.append('Missing information: '+result['missing_information'])
    return '\n\n'.join(lines)
