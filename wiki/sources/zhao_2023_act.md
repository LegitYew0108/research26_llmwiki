---
title: "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware"
type: source
tags: [robotics, imitation-learning, behavior-cloning, ACT, ALOHA, action-chunking, transformer, CVAE]
sources:
  - ../../raw/papers/zhao_2023_act.pdf
updated: 2026-10-03
---

# Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

## 書誌情報と要点

- 著者：Tony Z. Zhao、Vikash Kumar、Sergey Levine、Chelsea Finn。
- 取り込んだ版：arXiv:2304.13705v1、2023年4月23日。
- 一次資料：[論文PDF](../../raw/papers/zhao_2023_act.pdf)。本ページはこの版を対象とする。[出典：表紙](../../raw/papers/zhao_2023_act.pdf)

低価格の双腕遠隔操作システム **ALOHA** と、デモから将来の行動列を予測する **Action Chunking with Transformers（ACT）** を組み合わせ、精密な実機操作を学習する研究。ACTは報酬最大化によるRLではなく、デモの行動列を教師信号とする模倣学習である。action chunking、temporal ensembling、CVAEによる学習が主要な構成要素となる。[出典：§I・IV](../../raw/papers/zhao_2023_act.pdf)

## 背景：精密操作での誤差の累積

高頻度で長い軌道を実行すると、小さな行動予測の誤差が次の観測をデモの分布からずらし、さらに誤差を生む。双腕の受け渡しや挿入では数mmのずれでも失敗につながる。また、人のデモには停止や軌道のばらつきがあり、現在の観測だけから一時刻の行動を予測する方法では捉えにくい。著者らは、行動列をまとめて予測することでこれらの問題を軽減する。[出典：§I・IV-A](../../raw/papers/zhao_2023_act.pdf)

## ALOHAとデータの意味

ALOHAは2台のleader armを人が動かし、2台のfollower armが関節空間で追従する仕組み。既製のロボットと3Dプリント部品を使い、論文当時の全体費用は約18,000ドル、カメラ等の追加を含め約20,000ドルとされる。これは当該構成・時点の報告値である。[出典：§III・Appendix A](../../raw/papers/zhao_2023_act.pdf)

観測は4台のRGBカメラ画像（各480×640）とfollowerの関節位置14次元（左右それぞれ6関節＋gripper）。行動の教師信号には **leaderの関節位置** を使う。leaderとfollowerの位置差を通じて低レベルPIDが力を生むため、followerが実際に到達した位置を行動ラベルに置き換えると、操作者の指令と意味が変わる。方策の出力は左右の絶対目標関節位置であり、トルクや関節位置の差分ではない。[出典：§IV・IV-C](../../raw/papers/zhao_2023_act.pdf)

## ACTの学習と推論

1. 現在の観測と、その時刻からの長さ $k$ のデモ行動列をサンプリングする。
2. 学習時のCVAE encoderは、現在の関節位置と正解行動列から潜在変数 $z$ の分布を推定する。画像はこのencoderには入れない。
3. 方策であるCVAE decoderは、画像・関節位置・$z$ を入力して $k\times14$ の行動列を出力する。
4. 再構成損失と、潜在分布を標準正規分布へ近づけるKL項の和で学習する。
5. 推論時はCVAE encoderを使わず、$z=0$ に固定する。行動列を毎時刻予測し、同じ実行時刻に対応する複数の予測をtemporal ensemblingで統合する。

以上は§IV-B・C、Algorithms 1–2に基づく。生成モデルとして学習していても、この推論手順では $z$ をサンプリングせず、観測に対する出力は決定的になる。[出典](../../raw/papers/zhao_2023_act.pdf)

画像をResNet18で特徴化し、Transformer encoderでカメラ特徴・関節情報・潜在変数を統合する。Transformer decoderは固定の位置埋め込みをqueryとして、未来の行動列を生成する。**CVAE encoderと、方策内部のTransformer encoderは役割が異なる**。推論時に残るのは後者を含むCVAE decoderである。[出典：§IV-C・Appendix C](../../raw/papers/zhao_2023_act.pdf)

本文§IV-Cは再構成に **L1 loss** を使い、L2より精密な行動列を学習できたと記す。一方、Algorithm 1の9行目は **MSE** と表記する。取り込んだv1にはこの不一致があるため、本文の説明を整理しつつ、実装の再現にはコード確認が必要な点として残す。本ingestでは実装コードを検証していない。[出典：§IV-C・Algorithm 1](../../raw/papers/zhao_2023_act.pdf)

## 実験条件と結果

実機6タスクとMuJoCoのシミュレーション2タスクで評価。実機デモは各タスク50本、Thread Velcroのみ100本。1本8–14秒、50Hzで記録し、デモの合計は約10–20分だが、リセット・操作失敗を含む収集の実時間は約30–60分。シミュレーションはscripted / humanそれぞれ50本の成功デモを使う。[出典：§V-A・B](../../raw/papers/zhao_2023_act.pdf)

| 実機タスク | 最終成功率（ACT） |
| --- | ---: |
| Slide Ziploc：袋のsliderを操作して開ける | 88% |
| Slot Battery：電池を挿入する | 96% |
| Open Cup：半透明容器の蓋を開ける | 84% |
| Thread Velcro：面ファスナーの端をloopへ通す | 20% |
| Prep Tape：テープを切り、受け渡して箱に掛ける | 64% |
| Put On Shoe：靴を履かせてstrapを留める | 92% |

実機は1 seed・25試行。最初の2タスクではBC-ConvMLP、BeT、RT-1、VINNと比較し、4手法とも最終成功率は0%。残る4タスクはBeTとの比較で、その最終成功率も0%。これは本論文のデータ・調整・評価条件における結果である。Table IIのcaptionと本文は「remaining 3」と記すが、表に載るのは4タスクである。[出典：§V-C・Tables I–II](../../raw/papers/zhao_2023_act.pdf)

| シミュレーションタスク | scriptedで学習 | humanで学習 |
| --- | ---: | ---: |
| Cube Transfer | 86% | 50% |
| Bimanual Insertion | 32% | 20% |

シミュレーションは3 seeds・各50試行。humanデータで性能が下がる点も重要で、実機の高い成功率を全タスクへ一般化することはできない。[出典：§V-C・Table I](../../raw/papers/zhao_2023_act.pdf)

## Ablationと計算資源

- temporal ensemblingなしの比較では、シミュレーション4条件の平均成功率は $k=1$ の約1%から $k=100$ の約44%へ向上。さらに長いchunkではやや低下し、著者らは反応性の低下と長い行動列のモデル化の難しさを理由として挙げる。
- temporal ensemblingによるACTの改善は約3.3 percentage points。VINNでは低下しており、どの方法にも一律に有効とはいえない。
- CVAEを除くと、humanデータによるシミュレーション2タスクの平均成功率は35.3%から2%へ低下。scriptedデータでは差は小さい。

以上の比較条件・数値は§VI-A・B、Fig. 8に基づく。[出典](../../raw/papers/zhao_2023_act.pdf)

モデルは約80M parameters。各タスクで学習し、11GB RTX 2080 Ti 1枚で約5時間、推論は約0.01秒と報告。Table IIIの設定はchunk size 100、$\beta=10$、batch size 8、learning rate $10^{-5}$、hidden dimension 512、encoder 4層、decoder 7層である。論文の実機制御50Hzでは100 stepsは約2秒の行動列に相当するが、temporal ensembling使用時はその2秒間を観測なしで実行するわけではない。[出典：§IV-C・V-B・Table III](../../raw/papers/zhao_2023_act.pdf)

## 限界と読む際の注意

ALOHAのparallel-jaw gripperでは多指操作や大きな力を要する操作に限界がある。学習面でも、追加検討したキャンディ包装の開封は初期評価で最終成功0/10、小さな袋を机上から開けるタスクは把持後の操作を学習できなかった。知覚の難しさやデータ不足は著者らの考察であり、原因を独立に実証した結果とは区別する。[出典：Appendix F](../../raw/papers/zhao_2023_act.pdf)

概要の「10分のデモで80–90%」だけでは、タスク間の成功率差や収集実時間が見えない。上のタスク別結果と条件を併せて読む必要がある。また、ALOHAで人が遠隔操作できる技能と、ACTが自律実行できた技能は区別する。ACT自体に検索器やRLの更新を組み込んだ評価はなく、検索ベースのVINNは比較対象として登場する。[出典：§III–VI・Appendix F](../../raw/papers/zhao_2023_act.pdf)

## 関連ページ

- [Action ChunkingとTemporal Ensembling](../concepts/action_chunking_and_temporal_ensembling.md)
- [ロボットの模倣学習と強化学習](../concepts/imitation_and_reinforcement_learning.md)
