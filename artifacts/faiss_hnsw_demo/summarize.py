"""Analyze recorded CSV only; does not execute benchmarks."""
import csv
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / 'results/metrics.csv').open()))
for r in rows:
    for key in ['n', 'seed']:
        r[key] = int(r[key])
    for key in ['recall_at_10', 'single_median_ms', 'single_p95_ms', 'batch_qps', 'build_s', 'index_bytes']:
        r[key] = float(r[key])

selected = []
for kind in ['clustered', 'gaussian']:
    for n in [10000, 100000, 1000000]:
        subset = [r for r in rows if r['distribution'] == kind and r['n'] == n]
        if not subset:
            continue
        for seed in sorted({r['seed'] for r in subset}):
            sample = [r for r in subset if r['seed'] == seed]
            flat = next(r for r in sample if r['method'] == 'cpu_flat')
            gpu = next((r for r in sample if r['method'] == 'gpu_flat'), None)
            candidates = [r for r in sample if r['method'] == 'cpu_hnsw' and r['recall_at_10'] >= .95]
            best = min(candidates, key=lambda r:r['single_median_ms']) if candidates else None
            selected.append(dict(distribution=kind, n=n, seed=seed,
                                 cpu_flat_ms=flat['single_median_ms'],
                                 gpu_flat=gpu, hnsw_95=best,
                                 speedup=flat['single_median_ms'] / best['single_median_ms'] if best else None))
(ROOT / 'results/summary.json').write_text(json.dumps(selected, indent=2))
for r in selected:
    h = r['hnsw_95']
    print(r['distribution'],r['n'],r['seed'],
          'ef', h['ef_search'] if h else 'NO RECALL>=.95',
          'recall',round(h['recall_at_10'],4) if h else '',
          'cpu_ms',round(r['cpu_flat_ms'],3),
          'hnsw_ms',round(h['single_median_ms'],3) if h else '',
          'speedup',round(r['speedup'],1) if h else '')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12,4.5), constrained_layout=True)
colors = {10000:'#2563eb',100000:'#ea580c',1000000:'#16a34a'}
for ax, kind in zip(axes, ['clustered','gaussian']):
    for n in [10000,100000,1000000]:
        data = sorted([r for r in rows if r['distribution']==kind and r['n']==n and r['seed']==0 and r['method']=='cpu_hnsw'], key=lambda r:int(r['ef_search']))
        if not data:
            continue
        ax.plot([r['single_median_ms'] for r in data], [r['recall_at_10'] for r in data], 'o-', color=colors[n],label=f'HNSW N={n:,}')
    ax.axhline(.95,color='gray',linestyle='--',linewidth=1)
    ax.set(xscale='log',xlabel='Single-query median latency (ms)',ylabel='Recall@10',title=kind,ylim=(0,1.04))
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
fig.suptitle('FAISS HNSW: accuracy / latency (seed 0, CPU 1 thread)\nPoints: efSearch = 16, 32, 64, 128, 256; dashed line: recall 0.95', fontsize=12)
fig.savefig(ROOT/'results/recall_latency.png',dpi=180)
plt.close(fig)

fig, axes = plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
for ax, kind in zip(axes,['clustered','gaussian']):
    for method,label,color in [('cpu_flat','CPU exhaustive','#64748b'),('gpu_flat','GPU exhaustive (shared GPU)','#7c3aed'),('cpu_hnsw','CPU HNSW ef=64','#ea580c')]:
        data=sorted([r for r in rows if r['distribution']==kind and r['seed']==0 and r['method']==method and (method!='cpu_hnsw' or r['ef_search']=='64')],key=lambda r:r['n'])
        ax.plot([r['n'] for r in data],[r['single_median_ms'] for r in data],'o-',label=label,color=color)
    ax.set(xscale='log',yscale='log',xlabel='Number of database vectors',ylabel='Single-query median latency (ms)',title=kind)
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
fig.suptitle('Scaling (seed 0); HNSW recall differs by distribution and N')
fig.savefig(ROOT/'results/scaling.png',dpi=180)
plt.close(fig)
