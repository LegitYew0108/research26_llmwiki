---
title: "推論時検索による行動推定：VINNとDARP"
type: concept
tags: [imitation-learning, inference-time-retrieval, nearest-neighbor, non-parametric-policy, semi-parametric-policy, VINN, DARP]
sources:
  - ../../../raw/papers/pari_2022_vinn.pdf
  - ../../../raw/papers/pfeifer_2026_darp.pdf
  - ../../../raw/papers/du_2023_behavior_retrieval.pdf
updated: 2026-11-04
---

# 推論時検索による行動推定：VINNとDARP

## 何の話か

検索を模倣学習に使う方法は、**いつ検索結果を使うか**で2つに分けられる。

| 使う段階 | やること | 例 |
| --- | --- | --- |
| 学習前（データ選択） | 大きなデータから関連する部分を検索し、方策の学習データに加える | [Behavior Retrieval](../../sources/retrieval/du_2023_behavior_retrieval.md)、[SAILOR](../../sources/retrieval/nasiriany_2023_sailor.md) |
| 推論時（行動推定） | 実行中の毎ステップ、現在の状態に近いデモを検索し、その情報から行動を決める | [VINN](../../sources/retrieval/pari_2022_vinn.md)、[DARP](../../sources/retrieval/pfeifer_2026_darp.md) |

本ページは後者を扱う。学習前の検索は[検索による模倣学習データ選択](retrieval_based_imitation_data_selection.md)を参照。

推論時検索では、通常のBehavior Cloningと違い、デモを学習後も手元に残して使う。[出典：DARP §1、Fig. 1](../../../raw/papers/pfeifer_2026_darp.pdf)

## 共通の流れ

1. デモの各時刻の状態（または画像の埋め込み）と行動を保存しておく。
2. 実行時、現在の状態に近いk件をデモから検索する。
3. 近傍の情報から行動を計算する。

違いは3の計算方法にある。

## VINN：近傍行動の重み付き平均（non-parametric）

近傍の行動を、距離が近いほど大きい重みで平均し、そのまま出力する。行動を出すためのネットワークは学習しない。[出典：VINN §III-B](../../../raw/papers/pari_2022_vinn.pdf)

$$
\hat a=\frac{\sum_i \exp(-\|e-e^{(i)}\|_2)\,a^{(i)}}{\sum_i \exp(-\|e-e^{(i)}\|_2)}
$$

- 前提：似た観測には似た行動が対応し、有効な行動の平均も有効な行動である。[出典：VINN §III-B、§IV-G](../../../raw/papers/pari_2022_vinn.pdf)
- 出力は常にデモ行動の重み付き平均なので、デモにない補正（「少しずれているから少し戻す」など）は作れない（本Wikiによる整理）。

## DARP：差分を見て近傍ごとに補正する（semi-parametric）

近傍ごとに $(s^*_i,\ a^*_i,\ s^*_i-s_q)$ をネットワーク $f_\theta$ に入れ、近傍ごとの行動候補 $a'_i$ を出す。それらを平均（または順序に依存しない学習済み関数）でまとめる。[出典：DARP §2.4、式(3)(4)](../../../raw/papers/pfeifer_2026_darp.pdf)

$$
\hat a_q=\frac1k\sum_{i\in N_k(s_q)} f_\theta\left(s^*_i,a^*_i,s^*_i-s_q\right)
$$

- ネットワークは「状態がこれだけずれたら、行動をこう変える」を学ぶ。著者は、平均が滑らかさ（ばらつきの抑制）を、ネットワークが局所的な補正（精度）を担う、と説明する。[出典：DARP §2.3–2.4.1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 近傍での平均は、k-NNグラフ上のLaplacian smoothingに相当すると主張している。[出典：DARP Theorem 2](../../../raw/papers/pfeifer_2026_darp.pdf)

## 比較

| 観点 | VINN | DARP |
| --- | --- | --- |
| 行動の計算 | 近傍行動の距離重み付き平均 | 近傍ごとに差分から補正した候補を集約 |
| 学習するもの | 表現（BYOLによるencoder）のみ | 表現は事前学習済みを利用。行動予測ネットワーク $f_\theta$（と集約関数）を学習 |
| 学習時の検索 | なし | あり（各学習サンプルの近傍を検索） |
| 距離 | 埋め込みのL2距離 | 埋め込みのEuclidean距離＋過去状態の履歴（減衰付き） |
| 典型的なk | k≈10–20 | Stackでk≈500が最良 |
| 多峰的な行動 | 平均でぼやける | GMMなどの分布を出す集約で対応可 |

出典：VINN [§III、§IV-G](../../../raw/papers/pari_2022_vinn.pdf)、DARP [§2.4、Appendix A.2.1・A.2.2](../../../raw/papers/pfeifer_2026_darp.pdf)

- DARP論文では、VINN方式（LWR）はMuJoCoで多くの場合BCより低いスコアだった。[出典：DARP Table 1](../../../raw/papers/pfeifer_2026_darp.pdf)
- ただしVINNの原論文は、少数デモ・実機・画像入力の設定で、BCより良い結果を報告している。設定が大きく異なるので、単純な優劣とは読めない。[出典：VINN §IV-E](../../../raw/papers/pari_2022_vinn.pdf)

## DARPの検証で効いていた要素

Robosuite Stackでの構成の比較では、次が性能に大きく効いた。[出典：DARP §3.4、Fig. 6](../../../raw/papers/pfeifer_2026_darp.pdf)

- 差分ベクトル $s^*_i-s_q$ を入力すること（ノルムだけ、またはクエリ状態そのものに替えると低下）
- 順序に依存しない集約（順序に依存する集約では大きく低下）
- 距離による近傍の選択（ランダムなk件では低下）

## 推論時検索の実用上の論点

- **検索時間**：毎ステップ検索するため、制御周期内に終わる必要がある。VINNは線形探索で近傍回帰に約0.038秒。[出典：VINN §IV-H](../../../raw/papers/pari_2022_vinn.pdf) DARPは数千点のデータで推論約0.0044秒/step。[出典：DARP Appendix A.4](../../../raw/papers/pfeifer_2026_darp.pdf) どちらも大規模データでのANN索引（[HNSW](../vector_search/hnsw.md)など）の効果は評価していない。
- **表現の質**：距離が意味を持つ表現でないと、近傍が役に立たない。VINNは表現のfine-tuningを外すと実機で失敗した。[出典：VINN §IV-G b](../../../raw/papers/pari_2022_vinn.pdf)
- **近傍数k**：DARPではkが小さすぎるとBCより悪くなり、検証損失での選択が有効だった。[出典：DARP Appendix A.2.1、A.2.9](../../../raw/papers/pfeifer_2026_darp.pdf)

## 関連ページ

- [VINNの論文要約](../../sources/retrieval/pari_2022_vinn.md)
- [DARPの論文要約](../../sources/retrieval/pfeifer_2026_darp.md)
- [Retrieval-augmented Imitation Learning](retrieval_augmented_imitation_learning.md)
- [Behavior Cloning](../imitation_learning/behavior_cloning.md)
- [Compounding Error](../imitation_learning/compounding_error.md)
- [HNSW](../vector_search/hnsw.md)
- [FAISS](../vector_search/faiss_vector_search.md)
