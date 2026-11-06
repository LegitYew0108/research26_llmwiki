# FAISS HNSW 実証（2026-11-06）

kubera の Docker 内で実施。物理 GPU 2 (UUID `GPU-afb08f75-2bc5-9c02-469e-c29b6940c8f2`) のみを公開する。コンテナ内番号は0。

HNSWはCPU、全探索はCPUとGPUの2条件。GPU使用中の他ジョブを停止・変更しない。GPU全探索の性能は共有負荷の影響を受ける。

```sh
docker build --network=host -t research26-faiss:hnsw-20261106 .
docker run --name research26-faiss-hnsw-20261106 \
  --gpus device=GPU-afb08f75-2bc5-9c02-469e-c29b6940c8f2 \
  --cpus=8 --memory=12g --network=none -e TZ=Asia/Tokyo \
  -v "$PWD:/work" research26-faiss:hnsw-20261106
```

- 128次元float32、L2、k=10、登録とは独立な1000クエリ。
- クラスタ：100中心（正規分布、標準偏差3）に標準偏差1のノイズ。比較用は標準正規分布の独立ベクトル。
- 1万件・100万件はseed0。10万件はseed0/1/2。大規模条件は単一seedの参考値。
- HNSW: M=32、efConstruction=200、efSearch=16/32/64/128/256。
- 構築8スレッド、検索1スレッド。並列構築のためseed固定でも完全再現を保証しない。
- CPU Flatの上位10 ID集合を正解とするRecall@10。
- 単発検索は1000クエリ×3巡（巡回順序をshuffle）。中央値とp95を記録。
- バッチ検索は1000クエリ×5回の時間中央値からQPSを算出。
- GPUはfloat32、CPU側NumPy入力・出力で転送込み、明示的に同期。テンポラリメモリ128MiB。
- CPUとGPUの演算差による僅差の順位差はRecallに反映される。
- `index_bytes`: HNSWは直列化バイト数、Flatはベクトル本体のみ。GPU一時領域は含まない。
- `peak_process_rss_mib`: プロセス開始以来の累積最大RSS。各index単独のメモリ使用量ではなく、GPUメモリも含まない。
- 1万件では自己検索・保存再読込の一致をassertで検証。

`results/metrics.csv` は逐次flush、`results/environment.json` に環境を記録。Dockerログの `COMPLETE` が全条件の完了を示す。ローカルでは実験を行わない。

公式仕様: [Faiss indexes](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)、[GPU](https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU)。GPU用Python wheelは `faiss-gpu-cu12==1.9.0.post1`（PyPI配布）を使用。

実行結果：2026-11-06 17:13:35–17:51:31 JST、70条件完了、Docker終了コード0。`environment.json` とGPU監視の元時刻はUTC。1万件と100万件はseed0、10万件は3seedで実施。各件数でデータを生成するため、異なるNのDB・クエリは完全な包含関係にはない。

解析は回収したCSVに対してローカルで行う（ベンチマーク実行はサーバーDockerのみ）。Matplotlibを使用し、`python3 summarize.py` で図・集計JSON、`python3 validate_results.py` で完全性を検証する。Wiki内のアーカイブではCSV等を直下に配置しているが、実行用の元ディレクトリは `results/` 以下に保持する。
