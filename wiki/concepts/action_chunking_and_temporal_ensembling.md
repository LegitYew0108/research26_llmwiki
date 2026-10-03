---
title: "Action ChunkingとTemporal Ensembling"
type: concept
tags: [robotics, imitation-learning, ACT, action-chunking, temporal-ensembling, closed-loop-control]
sources:
  - ../../raw/papers/zhao_2023_act.pdf
updated: 2026-10-03
---

# Action ChunkingとTemporal Ensembling

## Action Chunking：一時刻ではなく行動列を予測する

ACTのaction chunkingは、現在の観測 $o_t$ から次の $k$ stepsの行動をまとめて予測する。ここでは添字の終点を含め、

$$\hat a_{t:t+k-1}=\pi_\theta(o_t,z)$$

と書く。これは長さ $k$ の列である。論文の $a_{t:t+k}$ も長さ $k$ のchunkを表すため、本ページでは終点の曖昧さを避けて表記した。ACTの各行動は左右の絶対目標関節位置14次元である。[出典：§IV-A・C](../../raw/papers/zhao_2023_act.pdf)

単純な実行方法は、観測から $k$ 個の行動を予測し、それを順に実行してから再び観測する方法。このとき、全長 $T$ stepsの軌道に対し観測から行動列を決める回数はおよそ $T/k$ となり、著者らはeffective horizonが $k$ 分の1になると説明する。これは誤差の累積を軽減する動機であり、誤差が消える保証ではない。人の一時的な停止など、chunk内で時間的につながる振る舞いのモデル化にも役立つとされる。[出典：§IV-A](../../raw/papers/zhao_2023_act.pdf)

## Temporal Ensembling：同じ実行時刻の予測を統合する

ACTでは反応性と滑らかさのため、毎時刻新しい観測からchunkを予測する。実行時刻 $t$ の行動に対して、過去の複数の観測から出された予測が重なるため、それらを重み付き平均する。**異なる時刻の行動を平均するのではなく、同じ時刻を対象とする予測を平均する**。[出典：§IV-A・Fig. 5・Algorithm 2](../../raw/papers/zhao_2023_act.pdf)

同じ時刻 $t$ の候補を、予測が生成された順に古いものから $A_t[0], A_t[1],\ldots$ と並べると、

$$a_t=\frac{\sum_i w_i A_t[i]}{\sum_i w_i},\qquad w_i=\exp(-mi).$$

論文では $w_0$ が最も古い予測への重みである。したがって $m>0$ では古い予測を強く重視し、$m$ を小さくすると新しい観測の予測が相対的に反映されやすくなる。「新しい予測ほど大きい重み」と読み替えないよう注意する。[出典：§IV-A・Algorithm 2](../../raw/papers/zhao_2023_act.pdf)

**説明用の例**：$k=3$ なら、時刻2で実行する行動は、時刻0のchunkの3番目、時刻1のchunkの2番目、時刻2のchunkの1番目を平均する。この例は論文の手順を示すためのもので、実験値ではない。[手順の出典：Fig. 5・Algorithm 2](../../raw/papers/zhao_2023_act.pdf)

## Chunkの長さとclosed-loopの関係

chunkが長いほど良いとは限らない。temporal ensemblingなしのablationでは $k=100$ 付近まで改善するが、$k=200,400$ ではやや低下した。著者らは観測への反応性と長い列のモデル化の難しさを理由として挙げる。一方、毎時刻chunkを更新する構成では、$k=100$ は100 stepsを観測なしで動かすことを意味しない。先の行動列を予測しつつ、観測に基づいて実行行動を更新する。[出典：§IV-A・VI-A](../../raw/papers/zhao_2023_act.pdf)

temporal ensemblingは学習を追加せず推論時の計算を増やす。論文ではACTとBC-ConvMLPを改善する一方、検索型のVINNでは性能が低下した。「chunking」と「複数chunkの統合」は別の構成要素として評価する必要がある。[出典：§IV-A・VI-A・Fig. 8](../../raw/papers/zhao_2023_act.pdf)

## 関連ページ

- [ACT論文の要約：モデル・データ・実験条件](../sources/zhao_2023_act.md)
- [ロボットの模倣学習と強化学習](imitation_and_reinforcement_learning.md)
