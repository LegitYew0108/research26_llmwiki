---
title: "Associative MemoryとKernel Regression"
type: concept
tags: [associative-memory, kernel-regression, attention, memory-mosaics, in-context-learning]
sources:
  - ../../raw/papers/2507.03285v3.pdf
updated: 2026-10-09
---

# Associative MemoryとKernel Regression

## keyからvalueを取り出す

Associative Memory（連想記憶）はkey-valueの組 $\{(k_i,v_i)\}_{i=1}^n$ を保存し、query key $k$ から対応するvalueを取り出す仕組み。Memory Mosaicsでは、保存した組から条件付き期待値 $\mathbb E[V\mid K=k]$ を推定するものとして捉える。単一の最近傍を返すのではなく、複数valueの重み付き平均を使う。[出典：§2、式(1)–(3)](../../raw/papers/2507.03285v3.pdf)

Gaussian kernel regressionの読み出しは次の形になる。[出典：式(3)](../../raw/papers/2507.03285v3.pdf)

$$
f(k)=\sum_{i=1}^n w_i(k)v_i,\qquad
w_i(k)=\frac{\exp(-\beta\lVert k-k_i\rVert^2)}{\sum_j\exp(-\beta\lVert k-k_j\rVert^2)}.
$$

近いkeyほど大きな重みを受ける。$\beta$ が大きいほど重みが集中し、小さいほど広い範囲のvalueを平均する。論文ではbandwidthを $1/\sqrt{\beta}$ と表す。v2は $\beta=\beta_1n^\alpha+\beta_0$ として記憶数に応じて調整する。[出典：§3.1](../../raw/papers/2507.03285v3.pdf)

## Attentionとの関係

$\lVert k-k_i\rVert^2=\lVert k\rVert^2+\lVert k_i\rVert^2-2k^\top k_i$ なので、保存keyが等ノルムなら共通項が正規化で消え、重みは $\operatorname{softmax}_i(2\beta k^\top k_i)$ になる。論文の式(4)は係数2を $\beta$ に吸収した形で表す。これは距離によるkernel regressionと内積によるattentionのつながりである。[出典：§2、式(3)–(4)](../../raw/papers/2507.03285v3.pdf)

Memory MosaicsではkeyをL2正規化し、queryとkeyに同じ抽出関数を使い、明示的なposition encodingを使わない。保存集合の読み出しは組の並べ替えに不変だが、抽出するkeyは過去の再帰処理、valueは隣接時刻を使うため、入力列の順序を無視するモデルではない。[出典：§2–3、式(5)–(9)](../../raw/papers/2507.03285v3.pdf)

## 文脈から学ぶことと重みの学習

事前学習では特徴抽出などのパラメータを更新する。推論時は文脈のkey-valueを保存して読み出し、その例示を予測に使う。したがってICLと、optimizerによるfine-tuningは区別する。また、long-term memoryは文脈内の古い情報で、persistent memoryは学習済みのnetwork weightsに対応する。[出典：§3–5・7](../../raw/papers/2507.03285v3.pdf)

この読み出しは全key-valueを保持する方式であり、top-k最近傍検索やグラフベースANNを採用した結果ではない。検索高速化については将来課題として扱う。[出典：§3.2脚注6・§8](../../raw/papers/2507.03285v3.pdf)

## 関連ページ

- [Memory Mosaics at scale：論文要約](../sources/zhang_2025_memory_mosaics_at_scale.md)
