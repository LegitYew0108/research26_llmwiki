"""CPU HNSW vs CPU/GPU exhaustive L2; run only in server Docker."""
import csv
import gc
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

import faiss
import numpy as np

OUT = Path('results')
OUT.mkdir(exist_ok=True)
D, K, NQ = 128, 10, 1000


def elapsed(fn):
    start = time.perf_counter()
    value = fn()
    return value, time.perf_counter() - start


def recall(ids, truth):
    return float(np.mean([len(set(a) & set(b)) / K for a, b in zip(ids, truth)]))


def measure(index, queries, truth, sync=lambda: None):
    index.search(queries[:32], K)
    sync()
    latencies = []
    # Three passes in independently shuffled order; transfer/allocation included.
    for repeat in range(3):
        for i in np.random.default_rng(900 + repeat).permutation(len(queries)):
            sync()
            start = time.perf_counter()
            index.search(queries[i:i+1], K)
            sync()
            latencies.append((time.perf_counter() - start) * 1000)
    batch_times = []
    for _ in range(5):
        sync()
        start = time.perf_counter()
        _, ids = index.search(queries, K)
        sync()
        batch_times.append(time.perf_counter() - start)
    return dict(recall_at_10=recall(ids, truth),
                single_median_ms=float(np.median(latencies)),
                single_p95_ms=float(np.percentile(latencies, 95)),
                batch_qps=float(len(queries) / np.median(batch_times)))


def dataset(n, kind, seed):
    rng = np.random.default_rng(seed)
    centers = rng.normal(0, 3, (100, D)).astype('float32')
    def generate(count):
        x = rng.normal(0, 1, (count, D)).astype('float32')
        if kind == 'clustered':
            x += centers[rng.integers(0, len(centers), count)]
        return np.ascontiguousarray(x)
    return generate(n), generate(NQ)


def main():
    assert faiss.get_num_gpus() == 1, 'Expose only physical GPU2 to container'
    gpu = faiss.StandardGpuResources()
    gpu.setTempMemory(128 * 1024 * 1024)
    sync = gpu.syncDefaultStreamCurrentDevice
    metadata = dict(faiss=faiss.__version__, numpy=np.__version__,
                    python=platform.python_version(), compile_options=faiss.get_compile_options(),
                    gpu=subprocess.check_output(['nvidia-smi', '--query-gpu=index,uuid,name,memory.used,memory.free,utilization.gpu', '--format=csv'], text=True),
                    cpu=subprocess.check_output(['lscpu'], text=True),
                    dimensions=D, k=K, queries=NQ, build_threads=8, search_threads=1,
                    started=time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                    gpu_timing='NumPy host inputs/outputs; transfers included; synchronized',
                    seeds='10000 and 1000000: seed0; 100000: seeds0,1,2')
    (OUT / 'environment.json').write_text(json.dumps(metadata, indent=2))
    fields = ['distribution', 'n', 'seed', 'method', 'ef_search', 'build_s',
              'index_bytes', 'peak_process_rss_mib', 'recall_at_10',
              'single_median_ms', 'single_p95_ms', 'batch_qps']
    with (OUT / 'metrics.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        for n in [10000, 100000, 1000000]:
            for seed in ([0, 1, 2] if n == 100000 else [0]):
                for kind in ['clustered', 'gaussian']:
                    print(f'START n={n} seed={seed} distribution={kind}', flush=True)
                    x, q = dataset(n, kind, seed)
                    faiss.omp_set_num_threads(1)
                    flat = faiss.IndexFlatL2(D)
                    _, flat_build = elapsed(lambda: flat.add(x))
                    _, truth = flat.search(q, K)
                    def record(method, index, build, size, ef='', sync_fn=lambda: None):
                        result = dict(distribution=kind, n=n, seed=seed, method=method,
                                      ef_search=ef, build_s=build, index_bytes=size,
                                      **measure(index, q, truth, sync_fn))
                        result['peak_process_rss_mib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
                        writer.writerow(result)
                        file.flush()
                        print(json.dumps(result), flush=True)
                    record('cpu_flat', flat, flat_build, n * D * 4)
                    config = faiss.GpuIndexFlatConfig()
                    config.device = 0
                    config.useFloat16 = False
                    gpu_flat = faiss.GpuIndexFlatL2(gpu, D, config)
                    sync()
                    start = time.perf_counter()
                    gpu_flat.add(x)
                    sync()
                    gpu_build = time.perf_counter() - start
                    record('gpu_flat', gpu_flat, gpu_build, n * D * 4, sync_fn=sync)
                    del gpu_flat
                    gc.collect()
                    hnsw = faiss.IndexHNSWFlat(D, 32)
                    hnsw.hnsw.efConstruction = 200
                    faiss.omp_set_num_threads(8)
                    _, build_s = elapsed(lambda: hnsw.add(x))
                    faiss.omp_set_num_threads(1)
                    size = len(faiss.serialize_index(hnsw))
                    for ef in [16, 32, 64, 128, 256]:
                        hnsw.hnsw.efSearch = ef
                        record('cpu_hnsw', hnsw, build_s, size, ef)
                    if n == 10000:
                        path = OUT / f'smoke_{kind}.faiss'
                        faiss.write_index(hnsw, str(path))
                        restored = faiss.read_index(str(path))
                        a, ia = hnsw.search(q[:10], K)
                        b, ib = restored.search(q[:10], K)
                        assert np.array_equal(ia, ib) and np.array_equal(a, b)
                        distances, ids = hnsw.search(x[:10], 1)
                        assert np.array_equal(ids[:, 0], np.arange(10))
                        assert np.allclose(distances, 0, atol=1e-4)
                        print('SMOKE self-search and serialization PASS', flush=True)
                        del restored
                    del hnsw, flat, x, q, truth
                    gc.collect()
    metadata['finished'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    metadata['gpu_after'] = subprocess.check_output(['nvidia-smi'], text=True)
    (OUT / 'environment.json').write_text(json.dumps(metadata, indent=2))
    print('COMPLETE', flush=True)


if __name__ == '__main__':
    main()
