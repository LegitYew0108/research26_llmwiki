"""Validate completeness and numerical integrity of the experimental record."""
import csv
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent / 'results'
rows = list(csv.DictReader((root / 'metrics.csv').open()))
expected = set()
for n in [10000, 100000, 1000000]:
    for seed in ([0, 1, 2] if n == 100000 else [0]):
        for kind in ['clustered', 'gaussian']:
            for method, ef in [('cpu_flat', ''), ('gpu_flat', '')] + [('cpu_hnsw', str(e)) for e in [16,32,64,128,256]]:
                expected.add((kind, n, seed, method, ef))
actual = [(r['distribution'], int(r['n']), int(r['seed']), r['method'], r['ef_search']) for r in rows]
assert len(actual) == len(set(actual)) == 70
assert set(actual) == expected
for r in rows:
    for key in ['build_s', 'index_bytes', 'peak_process_rss_mib', 'recall_at_10', 'single_median_ms', 'single_p95_ms', 'batch_qps']:
        assert math.isfinite(float(r[key])) and float(r[key]) >= 0, (key, r)
    assert 0 <= float(r['recall_at_10']) <= 1
    assert float(r['single_p95_ms']) >= float(r['single_median_ms']) > 0
    assert float(r['batch_qps']) > 0
    if r['method'] == 'cpu_flat':
        assert float(r['recall_at_10']) == 1
log = (root/'run.log').read_text()
assert log.count('SMOKE self-search and serialization PASS') == 2
assert log.rstrip().endswith('COMPLETE') and 'Traceback' not in log
metadata = json.loads((root/'environment.json').read_text())
assert metadata.get('finished') and 'GPU-afb08f75-2bc5-9c02-469e-c29b6940c8f2' in metadata['gpu']
assert 'exit_code=0' in (root/'audit.txt').read_text()
assert 'status=exited' in (root/'audit.txt').read_text()
print('PASS: 70 unique expected conditions, finite metrics, 2 smoke checks, COMPLETE, GPU2 UUID, Docker exit 0')
