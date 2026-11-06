"""Write final Japanese report from completed experimental artifacts."""
import csv
import json
from pathlib import Path
import statistics as st
from datetime import datetime, timedelta, timezone

root = Path(__file__).resolve().parent
rows = list(csv.DictReader((root/'results/metrics.csv').open()))
assert len(rows) == 70, f'Expected 70 measured conditions, found {len(rows)}'
env = json.loads((root/'results/environment.json').read_text())
assert 'finished' in env
summ = json.loads((root/'results/summary.json').read_text())
def val(r,k): return float(r[k])
def get(kind,n,method,ef=None):
    return [r for r in rows if r['distribution']==kind and int(r['n'])==n and r['method']==method and (ef is None or r['ef_search']==str(ef))]
def bounds(data,k,factor=1):
    a=[val(r,k)*factor for r in data]
    return f'{min(a):.3f}–{max(a):.3f}'

text='''---
title: "kubera GPU2：FAISS HNSW ベクトル検索実証"
type: experiment
tags: [experiment, FAISS, HNSW, vector-search, Docker, kubera]
sources:
  - ../../artifacts/faiss_hnsw_demo/metrics.csv
  - ../../artifacts/faiss_hnsw_demo/environment.json
  - ../../artifacts/faiss_hnsw_demo/run.log
  - ../../raw/papers/malkov_2018_hnsw.pdf
updated: 2026-11-06
---

# kubera GPU2：FAISS HNSW ベクトル検索実証

ユーザーの依頼に基づき、人工128次元ベクトルで実験を実施した。HNSWによる検索の動作、高速化、精度とのトレードオフを確認した。ロボットや模倣学習への有効性を測定した実験ではない。

結果の一次記録は[全測定値](../../artifacts/faiss_hnsw_demo/metrics.csv)、[実行ログ](../../artifacts/faiss_hnsw_demo/run.log)、[環境情報](../../artifacts/faiss_hnsw_demo/environment.json)。下記の数値・結論はこれらに基づく。

## 実行環境と測定条件

- サーバー：kubera、Xeon Silver 4210R。専用Dockerコンテナ、CPU上限8コア、RAM上限12GiB。
- GPU：物理GPU2、Quadro RTX 6000 23,040MiB、UUID `GPU-afb08f75-2bc5-9c02-469e-c29b6940c8f2`。このGPUだけを公開し、コンテナ内番号は0。
- HNSWとCPU全探索はCPU実行。GPU2では `GpuIndexFlatL2` による全探索を測定した。HNSW自体をGPUで実行したという意味ではない。
- 開始時にGPU2は19,479MiB使用中、空き3,212MiB。他ジョブを停止・変更していない。GPU測定は共有負荷の影響を含み、専有状態での性能上限を示さない。
- Python 3.11.9、NumPy 1.26.4、FAISS 1.9.0。PyPI配布の `faiss-gpu-cu12==1.9.0.post1` を使用。
- FAISSのコンパイル設定は `OPTIMIZE GENERIC GPU`。CPUのAVX2/AVX512向け最適化ビルドとの比較はしていない。今回の倍率を最適化済みCPU実装への一般的な優位性として扱わない。
- 登録：1万・10万・100万件、128次元float32。L2距離、top-10。
- クラスタ：100中心（各成分は標準偏差3の正規分布）＋標準偏差1の正規ノイズ。比較用：各成分が標準正規分布に従う独立ベクトル。
- クエリ：登録データと独立に生成した1,000件。自己検索は動作確認にのみ使用。
- 10万件はseed 0/1/2、1万・100万件はseed 0。大規模条件のseed間の再現性は未検証。
- HNSW：`M=32`、`efConstruction=200`、`efSearch=16/32/64/128/256`。構築8スレッド、検索1スレッド。並列構築は非決定性を含む。
- 単発時間：ウォームアップ後、1,000クエリを3巡。各巡の順序をshuffleし、計3,000回の中央値とp95を算出。
- バッチQPS：1,000クエリをまとめた検索を5回、時間の中央値で算出。単発時間の逆数ではない。
- GPU：float32、NumPyホスト入出力、転送込み、明示的に同期。テンポラリメモリは128MiBに制限。
- Recall@10：CPU全探索の上位10 ID集合との共通ID数/10をクエリで平均。GPUの浮動小数点演算差による順位差も反映する。
- 検索時間にデータ生成・インデックス構築・ディスクI/Oは含めない。

'''
jst = timezone(timedelta(hours=9))
started_jst = datetime.fromisoformat(env['started']).astimezone(jst).isoformat()
finished_jst = datetime.fromisoformat(env['finished']).astimezone(jst).isoformat()
text += f"実行開始：`{started_jst}`、終了：`{finished_jst}`（JST）。環境JSONの元記録はUTC。70条件の測定を完了。\n\n"
text += '''## クラスタデータ：95%以上のRecallで高速化できたか

各規模のseed 0について、測定したHNSW設定のうちRecall@10が95%以上で単発中央値が最も短いものを掲載する。設定は測定後に選んだもので、別の検証データで最適化したものではない。

| 登録件数 | efSearch | Recall@10 | CPU全探索 ms | HNSW中央値 ms | HNSW p95 ms | CPU全探索/HNSW |
| --- | --- | --- | --- | --- | --- | --- |
'''
for r in summ:
    if r['distribution'] != 'clustered' or r['seed'] != 0: continue
    h=r['hnsw_95']
    if h:
        text+=f"| {r['n']:,} | {h['ef_search']} | {100*h['recall_at_10']:.2f}% | {r['cpu_flat_ms']:.3f} | {h['single_median_ms']:.3f} | {h['single_p95_ms']:.3f} | {r['speedup']:.1f}倍 |\n"
    else:
        text+=f"| {r['n']:,} | — | 95%到達なし | {r['cpu_flat_ms']:.3f} | — | — | — |\n"
text+='''
## 10万件：seedを変えた3回の結果

以下は3つのseedの最小–最大。固定した設定で集計し、独立な再構築・データ生成で傾向を確認した。

| 分布 | efSearch | Recall@10 % | 単発中央値 ms | 構築秒（8スレッド） |
| --- | --- | --- | --- | --- |
'''
for kind,ef in [('clustered',32),('clustered',64),('gaussian',128),('gaussian',256)]:
    a=get(kind,100000,'cpu_hnsw',ef)
    text+=f"| {kind} | {ef} | {bounds(a,'recall_at_10',100)} | {bounds(a,'single_median_ms')} | {bounds(a,'build_s')} |\n"
text+='''
10万件のクラスタでは95%以上を維持してCPU全探索より速い設定が得られた。一方、独立正規乱数データは今回の探索範囲では95%未達。データ分布に依存し、任意のベクトルで同じ精度・倍率になるとは言えない。

## GPU2による全探索との比較

seed 0の値。GPUは共有状態、転送込み。CPU HNSWは固定efSearch=64であり、規模・分布によってRecallが異なる。速度だけの比較で同じ品質とみなさない。

| 分布 | 件数 | GPU全探索中央値 ms | GPU Recall@10 | GPUバッチQPS | HNSWバッチQPS | HNSW Recall@10 |
| --- | --- | --- | --- | --- | --- | --- |
'''
for kind in ['clustered','gaussian']:
    for n in [10000,100000,1000000]:
        g=next(r for r in get(kind,n,'gpu_flat') if r['seed']=='0')
        h=next(r for r in get(kind,n,'cpu_hnsw',64) if r['seed']=='0')
        text+=f"| {kind} | {n:,} | {val(g,'single_median_ms'):.3f} | {100*val(g,'recall_at_10'):.2f}% | {val(g,'batch_qps'):,.0f} | {val(h,'batch_qps'):,.0f} | {100*val(h,'recall_at_10'):.2f}% |\n"
text+='''
GPU全探索は1,000件をまとめた処理で高いスループットを示した。単発問い合わせとバッチ処理では最適な選択が異なるため、研究への導入時は実際の問い合わせ頻度・バッチサイズで判断する。

## 構築時間・保存容量

seed 0。HNSWは直列化サイズ、Flatはベクトル本体のサイズで、一時バッファやGPUコンテキストを含まない。

| 件数 | HNSW構築秒 clustered | HNSW構築秒 gaussian | HNSW MiB | Flatベクトル MiB |
| --- | --- | --- | --- | --- |
'''
for n in [10000,100000,1000000]:
    c=next(r for r in get('clustered',n,'cpu_hnsw',64) if r['seed']=='0')
    g=next(r for r in get('gaussian',n,'cpu_hnsw',64) if r['seed']=='0')
    text+=f"| {n:,} | {val(c,'build_s'):.3f} | {val(g,'build_s'):.3f} | {val(c,'index_bytes')/2**20:.2f} | {n*128*4/2**20:.2f} |\n"
text+=f"\nCSVの最大RSSはプロセス開始からの累積ピーク（全条件で最大{max(val(r,'peak_process_rss_mib') for r in rows):.1f}MiB）であり、各インデックス単独のメモリ使用量ではない。GPUメモリを含まない。[GPU監視ログ](../../artifacts/faiss_hnsw_demo/gpu_monitor.csv)も共有GPU全体の値であり、本実験単独の使用量ではない。\n"
text+='''
## 動作検証とグラフ

1万件の両分布で、既知ベクトル10件の自己検索（ID一致・距離0）と保存・再読込後のID・距離の完全一致をassertで検証した。実行ログに両条件のPASSと全条件終了の `COMPLETE` がある。全70条件のCSV列・件数も回収後に検証した。

![Recallと単発検索時間](../../artifacts/faiss_hnsw_demo/recall_latency.png)

![件数と単発検索時間](../../artifacts/faiss_hnsw_demo/scaling.png)

## 成果物と再実行

- ローカル実装：`/home/wada-lab/Univ/research26_workspace/faiss_hnsw_demo/`。
- サーバー：`/home/wadaharuto/research26_workspace/faiss_hnsw_demo/`。
- [コード](../../artifacts/faiss_hnsw_demo/benchmark.py)、[Dockerfile](../../artifacts/faiss_hnsw_demo/Dockerfile)、[再実行手順](../../artifacts/faiss_hnsw_demo/README.md)、[集計コード](../../artifacts/faiss_hnsw_demo/summarize.py)、[集計JSON](../../artifacts/faiss_hnsw_demo/summary.json)。
- インデックス保存検証用の `.faiss` ファイルは実装ディレクトリの `results/` とサーバーに保持し、Wikiには重複保存しない。
- ホスト名のDNS解決が不安定だったため、過去の実験記録にあるIP `10.0.16.19` に `HostKeyAlias=kubera.bigdata-lab` を指定し、既知のホスト鍵を検証して接続した。

公式仕様：[Faiss indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)、[Faiss on the GPU](https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU)。HNSWの背景：[原論文](../../raw/papers/malkov_2018_hnsw.pdf)。今後ロボットに接続する場合は、実際の埋め込みの分布と検索件数で同じ比較を行い、検索結果が方策の性能に与える影響を別途検証する必要がある。
'''
negative = get('gaussian', 1000000, 'cpu_hnsw', 256)[0]
detail = f"100万件の乱数データは、efSearch=256でもRecall@10が{100*val(negative,'recall_at_10'):.2f}%、単発中央値{val(negative,'single_median_ms'):.3f}msだった。今回の設定では95%の目標を満たさなかった。\n\n"
text = text.replace('## GPU2による全探索との比較', detail + '## GPU2による全探索との比較')
(root/'results/report.md').write_text(text)
