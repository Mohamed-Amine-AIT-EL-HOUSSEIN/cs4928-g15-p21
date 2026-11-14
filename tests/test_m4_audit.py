import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from scripts.m4_audit import directed_edge, audit, change_visibility

class M4AuditTests(unittest.TestCase):
    def test_direction_matters(self):
        self.assertNotEqual(directed_edge('a -> b'), directed_edge('b -> a'))
        self.assertEqual(directed_edge('Service-A -> B'), directed_edge('service_a -> b'))

    def test_reversed_match_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            labels = Path(tmp) / 'labels.csv'
            metrics = Path(tmp) / 'metrics.csv'
            with labels.open('w', newline='') as f:
                w = csv.writer(f); w.writerow(['id','characteristic','item','label','match_id'])
                w.writerow(['G001','connection','a -> b','TP','T001'])
                w.writerow(['T001','connection','b -> a','MATCH','G001'])
            with metrics.open('w', newline='') as f:
                w = csv.writer(f); w.writerow(['scope','TP','FP','FN','precision','recall','F1'])
                w.writerow(['endpoint',0,0,17,'',0,0]); w.writerow(['all',32,2,20,.941,.615,.7441860465116279])
            result = audit(labels, metrics)
            self.assertEqual(result['endpoint_coverage']['status'], 'no_tool_endpoints_reported')
            self.assertIsNone(result['endpoint_coverage']['precision'])
            self.assertTrue(result['directed_edge_validation']['reverse_edge_errors'])

    def test_real_event_a_frozen_scores(self):
        root = Path(__file__).resolve().parents[1]
        result = audit(root/'eventA/results/final_labels.csv', root/'eventA/results/metrics.csv')
        self.assertEqual(result['endpoint_coverage']['reference_count'], 17)
        self.assertEqual(result['endpoint_coverage']['reported_count'], 0)
        self.assertAlmostEqual(result['frozen_overall_F1'], 0.7441860465116279)
        self.assertFalse(result['directed_edge_validation']['reverse_edge_errors'])

    def _run(self, tmp, name, flows):
        path = Path(tmp) / name
        path.write_text(json.dumps({'microservices': {'0': {'servicename': 'a'}, '1': {'servicename': 'b'}},
                                    'external_components': {},
                                    'information_flows': {str(i): {'sender': s, 'receiver': r}
                                                          for i, (s, r) in enumerate(flows)}}))
        return path

    def test_new_link_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = self._run(tmp, 'before.json', [('a', 'b')])
            after = self._run(tmp, 'after.json', [('b', 'a'), ('a', 'b')])  # new link, IDs shuffled
            labels = [{'id': 'G001', 'characteristic': 'connection', 'item': 'a -> b'}]
            result = change_visibility(before, after, labels)
            self.assertEqual(result['connections_added'],
                             [{'connection': 'b -> a', 'in_reference_labels': False}])
            self.assertEqual(result['connections_removed'], [])

    def test_no_change_gives_empty_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = self._run(tmp, 'before.json', [('a', 'b')])
            result = change_visibility(before, before, [])
            self.assertEqual(result['connections_added'], [])
            self.assertEqual(result['components_added'], [])

    def test_real_event_b_runs(self):
        root = Path(__file__).resolve().parents[1]
        runs = root / 'eventB' / 'runs'
        name = 'fernandoabcampos--spring-netflix-oss-microservices.json'
        if not (runs / 'before' / name).exists():
            self.skipTest('Event B runs not present')
        with open(root / 'eventA/results/final_labels.csv', newline='', encoding='utf-8') as f:
            labels = list(csv.DictReader(f))
        result = change_visibility(runs / 'before' / 'dict_fernandoabcampos_spring-netflix-oss-microservices.txt',
                                   runs / 'after' / 'dict_fernandoabcampos_spring-netflix-oss-microservices.txt', labels)
        self.assertEqual(result['connections_added'],
                         [{'connection': 'statement_service -> card_service', 'in_reference_labels': False}])
        self.assertEqual(result['connections_removed'], [])

if __name__ == '__main__':
    unittest.main()
