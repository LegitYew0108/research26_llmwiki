---
title: "検索による模倣学習データ選択"
type: concept
tags: [imitation-learning, behavior-cloning, retrieval, data-selection, state-action-embedding]
sources:
  - ../../../raw/papers/2304.08742v2.pdf
  - ../../../raw/temp/nasiriany_2023_sailor.pdf
updated: 2026-10-31
---

# 検索による模倣学習データ選択

## 何のために検索するのか

少数の対象タスクのデモだけでは学習が不安定になる一方、複数タスクの既存データをすべて混ぜると、無関係な行動や失敗まで模倣してしまうことがある。Behavior Retrievalでは、対象デモとの類似性で既存データから有用な部分を選び、対象デモと一緒にBCする。[出典：§I・III](../../../raw/papers/2304.08742v2.pdf)

## 検索単位とタイミング

検索の単位は状態・行動 $(s,a)$ の組。軌道のタスク名が違っても、対象タスクと共通の把持動作などは使える。画像・状態だけでなく行動も埋め込みへ反映し、似た状態で逆方向へ動くデータを区別する。[出典：§III-C・D、Fig. 8](../../../raw/papers/2304.08742v2.pdf)

流れは `既存データでVAE学習 → 対象デモに近い組を選択 → 対象デモと検索結果でBC → 学習した方策で実行`。検索した行動をその場で直接実行する仕組みとは手順が異なる。検索の段階では対象デモに記録された行動が利用できるため、クエリに行動が含まれても、実行時の正解行動を必要としない。[出典：§III、Algorithm 1](../../../raw/papers/2304.08742v2.pdf)

## 閾値と学習時の重み

各既存データの組について、対象デモ内で最も近い組との類似度を計算し、そのスコアをmin-max正規化して閾値判定する。式(3)からは、閾値が取得割合そのものを指定するとは解釈できない。取得件数はスコア分布にも依存する（式からの解釈）。また学習時には対象デモと検索データから同じbatch sizeを採るので、検索データを増やすことと、その損失の重みを増やすことを区別する。[出典：§III-D・E、式(3)–(4)、Algorithm 1](../../../raw/papers/2304.08742v2.pdf)

## 適用範囲

この論文の「unlabeled」はタスクラベルが不要という意味で、状態と対応する行動は必要。学習目的はBCであり、報酬や価値関数で選択する方法ではない。近さが有用性を保証するわけではなく、大きな見た目の差やタスクに重要な違いを埋め込みが捉えない場合が限界となる。[出典：§III-A・C・E、§V](../../../raw/papers/2304.08742v2.pdf)

## SAILOR：部分軌跡を選んでskill方策を学ぶ

[SAILOR](../../sources/retrieval/nasiriany_2023_sailor.md)は固定長の部分軌跡をskillに埋め込み、各既存候補から対象デモ集合への最小L2距離で順位付けして、候補全体の上位割合を選ぶ。検索結果は観測履歴からskillを予測する方策の教師データとなる。状態・行動の組を選ぶBehavior Retrievalとは検索単位と最終方策が異なるため、取得割合や成功率を同じ条件の比較として扱わない。[出典：SAILOR §3–4、Algorithm 2](../../../raw/temp/nasiriany_2023_sailor.pdf)、[Behavior Retrieval §III](../../../raw/papers/2304.08742v2.pdf)

SAILORのCALVIN ablationでは、Cleaning Upで関連データ検索がランダム選択を上回る一方、Setting Upでは両者が同程度である。関連性による選別の効果はタスク・データセットに依存する。[出典：Appendix A.4、Table 6](../../../raw/temp/nasiriany_2023_sailor.pdf)

## 関連ページ

- [Behavior Retrieval：詳細・実験結果・原文の注意点](../../sources/retrieval/du_2023_behavior_retrieval.md)
- [Behavior Cloning](../imitation_learning/behavior_cloning.md)
- [VAE](../generative_models/variational_autoencoder.md)
