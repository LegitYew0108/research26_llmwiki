---
title: "HNSW：階層グラフによる近似近傍検索"
type: concept
tags: [HNSW, ANNS, vector-search, graph-search]
sources:
  - ../../../raw/papers/1603.09320v4.pdf
  - ../../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-11-02
---

# HNSW：階層グラフによる近似近傍検索

HNSW（Hierarchical Navigable Small World）は、データ間の接続を探索してクエリに近いデータを探す近似近傍検索手法である。データをランダムな高さで複数の層に配置し、疎な上位層から最下層へ降りる。上位層で大まかに移動し、全ノードを含む最下層で候補を詳しく探す。[出典：§3–4、Fig.1](../../../raw/papers/1603.09320v4.pdf#page=3)

## 検索と構築を分ける

**検索**ではグラフをたどり、上位層では `ef=1`、最下層では複数の候補を保持する `ef` を用いる。候補集合から最後に近いk件を返す。`ef` は返す件数kと異なり、探索途中に保持する有望な候補数を調整する。訪問数そのものの上限ではない。[出典：Algorithms 2・5](../../../raw/papers/1603.09320v4.pdf#page=5)

**構築**ではデータを1件ずつ挿入し、探索で得た候補から接続先を選ぶ。`M` は挿入時の接続数、`efConstruction` は構築時の探索候補数に関係する。既存ノードの接続上限は別途 `Mmax`、最下層では `Mmax0` で制御する。[出典：§4、Algorithm 1](../../../raw/papers/1603.09320v4.pdf#page=4)

## 近い点だけにつながない理由

近い点だけを選ぶと接続が同じクラスタに偏ることがある。近傍選択heuristicは、選択済みノードとの距離も調べて重複した方向への接続を抑え、別方向への経路を残す。階層と近傍選択はそれぞれ異なる工夫である。[出典：§3–4、Fig.2、Algorithm 4](../../../raw/papers/1603.09320v4.pdf#page=4)

## 理解するときの注意

- 近似検索なので、返ったk件が真のk近傍と一致する保証はない。速度とRecallを合わせて評価する。[出典：§1・5](../../../raw/papers/1603.09320v4.pdf#page=1)
- 対数的な検索スケーリングの説明には条件があり、任意の高次元データに対する最悪計算量の保証として扱わない。[出典：§4.2.1](../../../raw/papers/1603.09320v4.pdf#page=7)
- 検索のために接続を保存するメモリと、グラフの構築時間が必要になる。[出典：§4.2.2–4.2.3](../../../raw/papers/1603.09320v4.pdf#page=8)

詳しいパラメータ・実験条件は[原論文の要約](../../sources/vector_search/malkov_2018_hnsw.md)を参照。候補ごとの正確な距離計算を減らす拡張については[確率的ルーティングとKS₂](probabilistic_routing_ks2.md)を参照。[出典：KS論文§6.2](../../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)
