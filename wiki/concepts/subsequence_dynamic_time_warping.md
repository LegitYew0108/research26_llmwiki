---
title: "Subsequence DTW：部分軌跡の時間対応を取る検索"
type: concept
tags: [dynamic-time-warping, trajectory-retrieval, imitation-learning, sequence-alignment]
sources:
  - ../../raw/papers/2508.01131v2.pdf
updated: 2026-10-17
---

# Subsequence DTW：部分軌跡の時間対応を取る検索

## 目的

似た動作でも実行速度や開始時刻が違うと、同じframe番号の特徴同士を比べるだけでは対応がずれる。Dynamic Time Warping（DTW）は順序を保ちながら時間方向の対応を伸縮させ、累積コストの小さい対応を求める。Subsequence DTW（S-DTW）は、query列全体を長い参照列の中の連続部分へ対応付ける。[出典：Appendix A.4](../../raw/papers/2508.01131v2.pdf)

## 定式化

特徴列 $X=(x_1,\ldots,x_n)$ と $Y=(y_1,\ldots,y_m)$ に対し、COLLAGE付録では局所コストを $C(i,j)=\|x_i-y_j\|_2^2$ とする。DTWの累積コストは適切な境界初期化の下で計算する。

$$
D(i,j)=C(i,j)+\min\{D(i-1,j),D(i,j-1),D(i-1,j-1)\}.
$$

$n<m$ のとき、S-DTWは次の最小化を行う。

$$
\operatorname{S\text{-}DTW}(X,Y)=\min_{1\leq s\leq e\leq m}\operatorname{DTW}(X,Y_{s:e}).
$$

対応経路には単調性と連続性の制約を置く。部分列対応には任意の開始位置と終端を扱う設定が必要であり、通常のDTWの全列対応とは区別する。[出典：Appendix A.4](../../raw/papers/2508.01131v2.pdf)

## COLLAGEでの使い方と注意

end-effectorの停止点で対象デモを分割し、その特徴列をqueryとして既存軌跡の連続部分を検索する。視覚・動作・形状で独立して低コストなtop-Kを取得する。[出典：§3.1、Appendix A.1・A.4](../../raw/papers/2508.01131v2.pdf)

本文§3.1は局所コストをL2 norm、付録A.4はsquared L2 normで記している。本ページの式は付録に合わせたもので、再現時には実装確認が必要。付録の分割処理も「長さ20を超える部分軌跡をmergeする」と記しており、過分割への対処として具体的にどの区間を結合するかは、この記述だけでは確定できない。[出典：§3.1、Appendix A.1・A.4](../../raw/papers/2508.01131v2.pdf)

S-DTWは特徴列の時間対応を扱うため、単一ベクトルの近傍検索と同じ処理ではない。COLLAGEはグラフベースANNによる代替や高速化を検証していない。[出典：§3.1、Appendix A.4](../../raw/papers/2508.01131v2.pdf)

## 関連ページ

- [COLLAGEの論文要約](../sources/kumar_2025_collage.md)
- [Retrieval-augmented Imitation Learning](retrieval_augmented_imitation_learning.md)
