---
title: "FAISS公式資料：検索の基本とHNSW"
type: research
tags: [FAISS, ANNS, HNSW, vector-search]
sources:
  - faiss_indexes_20261017.html
  - faiss_metrics_20261017.html
  - faiss_getting_started_20261017.html
updated: 2026-10-17
---

# FAISS公式資料：検索の基本とHNSW

公式WikiのHTMLを2026-10-17に保存。未ingest。教員の意図の推測、研究方針・実験計画は保存していない。

## 公式資料

- [Faiss indexes（保存版）](faiss_indexes_20261017.html)／[公式ページ](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
- [MetricType and distances（保存版）](faiss_metrics_20261017.html)／[公式ページ](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances)
- [Getting started（保存版）](faiss_getting_started_20261017.html)／[公式ページ](https://github.com/facebookresearch/faiss/wiki/Getting-started)

## 確認した事実

- FAISSは複数の検索indexを提供する。`IndexFlatL2`はL2の全探索、`IndexHNSWFlat`はグラフ探索、`IndexIVFFlat`は空間を分割して一部のリストを探索する方式である。FAISSとHNSWは同義ではない。[出典：Summary of methods](faiss_indexes_20261017.html)
- HNSWでは`M`がグラフの近傍数、`efConstruction`が構築時、`efSearch`が検索時の探索の広さに関係する。[出典：IndexHNSW variants](faiss_indexes_20261017.html)
- 登録は`add`、近傍検索は`search`を使う。検索結果にはデータのIDと距離が含まれる。[出典：Building an index and adding the vectors to it、Searching](faiss_getting_started_20261017.html)
- L2の返り値は二乗距離。cosine similarityの検索は、登録ベクトルとクエリの両方をL2正規化して内積検索で実現できる。[出典：METRIC_L2、How can I index vectors for cosine similarity?](faiss_metrics_20261017.html)

## 既存の一次資料との区別

- Behavior Retrievalは状態・行動の埋め込みを使い、既存データからBC用のデータを選ぶ。FAISSの利用やグラフ型ANNの優位性を示した論文としては扱わない。[出典：§III、Appendix A-G](../papers/2304.08742v2.pdf)
- KS₂はHNSWの探索中に候補を選別し、正確な距離計算を減らす仕組みとして評価されている。FAISSのPython APIを使えばKS₂が自動的に適用されるという意味ではない。[出典：§6.2、Algorithm 7](../papers/kernel_function_for_angle_testing.pdf)
