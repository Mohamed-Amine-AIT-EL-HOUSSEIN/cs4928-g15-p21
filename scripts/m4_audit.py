"""This script checks our Event A results without changing the original scores."""
import argparse
import csv
import json
from pathlib import Path


def directed_edge(text):
    parts = text.split('->')
    if len(parts) != 2 or not all(p.strip() for p in parts):
        raise ValueError(f'Not a directed connection: {text!r}')
    return tuple(p.strip().casefold().replace('-', '_').replace(' ', '_') for p in parts)


def audit(labels_path, metrics_path):
    with open(labels_path, newline='', encoding='utf-8') as f:
        labels = list(csv.DictReader(f))
    with open(metrics_path, newline='', encoding='utf-8') as f:
        metrics = {r['scope']: r for r in csv.DictReader(f)}
    if not labels or 'endpoint' not in metrics or 'all' not in metrics:
        raise ValueError('Missing required Event A labels/metrics')
    endpoint = metrics['endpoint']
    tp, fp, fn = (int(endpoint[k]) for k in ('TP', 'FP', 'FN'))
    endpoint_status = ('no_tool_endpoints_reported' if tp + fp == 0 and tp + fn > 0
                       else 'no_reference_or_tool_endpoints' if tp + fp + fn == 0
                       else 'tool_endpoints_reported')
    errors = []
    matches = {r['id']: r for r in labels}
    for r in labels:
        if r['characteristic'] != 'connection' or r['label'] not in ('TP', 'MATCH'):
            continue
        match_id = (r.get('match_id') or '').strip()
        if not match_id or match_id not in matches:
            errors.append(f"{r['id']}: missing matched item {match_id!r}")
            continue
        other = matches[match_id]
        if other['characteristic'] != 'connection':
            errors.append(f"{r['id']}: matched item is not a connection")
            continue
        # Some services might have different names in the results.      
        # We only flag connections that are clearly going in the wrong direction.
        try:
            a, b = directed_edge(r['item']), directed_edge(other['item'])
            if a == tuple(reversed(b)) and a != b:
                errors.append(f"{r['id']}: reverse direction against {match_id}")
        except ValueError as e:
            errors.append(str(e))
    return {
        'source_labels': str(labels_path), 'source_metrics': str(metrics_path),
        'endpoint_coverage': {'status': endpoint_status, 'reference_count': tp + fn,
                              'reported_count': tp + fp, 'TP': tp, 'FP': fp, 'FN': fn,
                              'precision': None if tp + fp == 0 else tp / (tp + fp)},
        'directed_edge_validation': {'checked_matched_rows': sum(
            r['characteristic'] == 'connection' and r['label'] in ('TP', 'MATCH') for r in labels),
            'reverse_edge_errors': errors,
            'limitation': 'This only checks connections that are exactly reversed. Different service names still need to be checked manually.'},
        'frozen_overall_F1': float(metrics['all']['F1']),
        'note': 'This is an extra check. It does not change our original labels or precision, recall and F1 scores.'
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--labels', default='eventA/results/final_labels.csv')
    p.add_argument('--metrics', default='eventA/results/metrics.csv')
    p.add_argument('--out', default='m4/results/audit.json')
    a = p.parse_args()
    result = audit(Path(a.labels), Path(a.metrics))
    dest = Path(a.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    if result['directed_edge_validation']['reverse_edge_errors']:
        raise SystemExit('Direction validation flagged possible errors; inspect audit.json')


if __name__ == '__main__':
    main()
