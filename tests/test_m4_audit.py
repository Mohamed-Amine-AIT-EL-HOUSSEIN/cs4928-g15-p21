import csv
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from m4_audit import directed_edge, audit

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

if __name__ == '__main__':
    unittest.main()
