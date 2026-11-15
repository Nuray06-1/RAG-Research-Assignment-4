import unittest,json
from citation_contract import validate_output,render_checked
from repair_existing_citations import matching_source,insert_marker

class CitationTests(unittest.TestCase):
    def setUp(self):
        self.passages=[{'text':'The framework uses document-specific agents to extract evidence from each report.'}]
    def obj(self,text=None,index=1,quote=None):
        return json.dumps({'abstained':False,'missing_information':'','claims':[{'text':text or self.passages[0]['text'],'citations':[{'source_index':index,'evidence_quote':quote or self.passages[0]['text']}]}]})
    def test_exact_source_statement_passes(self):
        result=validate_output(self.obj(),self.passages)
        self.assertTrue(render_checked(result).endswith('[Source 1]'))
    def test_reference_to_absent_source_rejected(self):
        with self.assertRaises(ValueError):validate_output(self.obj(index=2),self.passages)
    def test_fabricated_quote_rejected(self):
        with self.assertRaises(ValueError):validate_output(self.obj(quote='The model achieved ninety nine percent accuracy.'),self.passages)
    def test_real_quote_does_not_validate_unrelated_claim(self):
        with self.assertRaises(ValueError):validate_output(self.obj(text='The method was tested on one million documents.'),self.passages)
    def test_paraphrase_requires_separate_support_decision(self):
        result=validate_output(self.obj(text='An agent is assigned to each document.'),self.passages,lambda *args:'SUPPORTED')
        self.assertEqual(result['claims'][0]['citations'][0]['support_method'],'separate_semantic_verifier')
    def test_invalid_judge_response_not_converted_to_support(self):
        with self.assertRaises(ValueError):validate_output(self.obj(text='The model is guaranteed to be accurate.'),self.passages,lambda *args:'probably supported')
    def test_no_source_cannot_get_a_citation(self):
        with self.assertRaises(ValueError):validate_output(self.obj(),[])
    def test_matching_text_in_different_source_uses_actual_index(self):
        claim=self.passages[0]['text'];self.assertEqual(matching_source(claim,[{'text':'Irrelevant document.'}]+self.passages),2)
    def test_ambiguous_span_not_silently_patched(self):
        with self.assertRaises(ValueError):insert_marker('Same sentence. Same sentence.','Same sentence.',1)
    def test_original_text_preserved_by_attachment(self):
        s=self.passages[0]['text'];self.assertEqual(insert_marker(s,s,1).replace(' [Source 1]',''),s)
if __name__=='__main__':unittest.main()
