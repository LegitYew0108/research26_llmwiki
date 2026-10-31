---
title: "Behavior Retrieval: Few-Shot Imitation Learning by Querying Unlabeled Datasets"
type: source
tags: [robotics, imitation-learning, behavior-cloning, retrieval, few-shot-learning, VAE, offline-data]
sources:
  - ../../../raw/papers/2304.08742v2.pdf
updated: 2026-10-31
---

# Behavior Retrieval: Few-Shot Imitation Learning by Querying Unlabeled Datasets

## 書誌情報と要点

Maximilian Du、Suraj Nair、Dorsa Sadigh、Chelsea Finn（Stanford University）。対象はarXiv:2304.08742v2、2023年5月13日版。[出典：表紙](../../../raw/papers/2304.08742v2.pdf)

**少数のタスク固有デモを、方策の教師データとしてだけでなく、既存データから学習に役立つ状態・行動の組を選ぶ検索クエリとして使う。** VAEで状態・行動の埋め込みを学び、関連データを検索し、デモと検索結果の両方でBehavior Cloning（BC）を行う。検索は学習用データの選択であり、実行時に検索した行動を直接出力する手順ではない。[出典：§III、Fig. 2、Algorithm 1](../../../raw/papers/2304.08742v2.pdf)

## 問題設定：「ラベルなし」の意味

- $D_t$：対象タスクのexpertによる状態・行動 $(s,a)$ の組。デモまたはonline interventionから得る。主なデモ実験では各タスク10本。
- $D_{prior}$：複数タスク・成功・失敗などが混ざる既存データ。対象タスクと無関係、あるいは逆方向の行動も含み得る。
- 両データは共通の状態空間・行動空間を持つ。「unlabeled」はタスクの分類・区切りが与えられないという意味で、**行動 $a$ の記録は必要**。行動を含まない動画だけをそのまま検索してBCする設定ではない。

以上は[§III-A・IV-A](../../../raw/papers/2304.08742v2.pdf)に基づく。オンライン介入を使う設定も報酬最大化によるRLではなく、expertの行動を模倣する。Appendix A-Hの実験では、学習者とexpertの行動差が閾値を超えると介入し、直近1000件の介入を用いる。[出典：Appendix A-H](../../../raw/papers/2304.08742v2.pdf)

## 手法

### 1. 状態と行動を一緒に埋め込む

$D_{prior}$ でVAEを学習し、状態と行動を再構成する。論文の目的関数は次の重み付きELBOである。[出典：§III-C、式(1)](../../../raw/papers/2304.08742v2.pdf)

$$
\mathbb E_{q_\phi(z_{sa}\mid s,a)}[\log p_\theta(s,a\mid z_{sa})]
-\beta D_{KL}(q_\phi(z_{sa}\mid s,a)\Vert p(z_{sa})).
$$

さらに行動を連結して $z=[z_{sa},a]$ とし、類似度を $F(s_1,a_1,s_2,a_2)=-\|z_1-z_2\|_2$ とする。状態が似ていても、右のpegへ運ぶ行動と左へ運ぶ行動は対象タスクへの有用性が異なるため、行動も距離に反映する。[出典：§III-C、式(2)](../../../raw/papers/2304.08742v2.pdf)

### 2. デモに近い組を選択する

各候補 $x=(s^*,a^*)\in D_{prior}$ に対し、$D_t$ 内の最も近い組との類似度を $m(x)=\max_{(s,a)\in D_t}F(s^*,a^*,s,a)$ とする。$F^+=\max_xm(x)$、$F^-=\min_xm(x)$ とおき、

$$\frac{m(x)-F^-}{F^+-F^-}>\delta$$

を満たす候補を $D_{ret}$ に入れる。これは論文式(3)を記号整理したもの。通常の実験では $\delta\in[0.6,0.8]$ を使う。軌道全体を採否判定するのではなく、別タスクの軌道からも、共通する把持部分などを取り出せる。[出典：§III-D、Fig. 8](../../../raw/papers/2304.08742v2.pdf)

**式の読解上の注意：** 本文には「top $1-\delta$%」を検索する趣旨の記述があるが、式(3)はmin-max正規化したスコアへの閾値であり、順位の分位点ではない。したがって、$\delta=0.75$ がデータの上位25%取得を保証するとは読めない。これは式からの解釈であり、実装の検証結果ではない。[対象記述：§III-D、式(3)](../../../raw/papers/2304.08742v2.pdf)

### 3. 対象デモと検索結果でBCする

$$\min_\psi\;\mathbb E_{D_t}[-\log\pi_\psi(a\mid s)]+\mathbb E_{D_{ret}}[-\log\pi_\psi(a\mid s)].$$

Algorithm 1ではそれぞれのデータから同じbatch sizeでサンプリングする。単純に結合してデータ件数に比例して学ぶ手順とは重みが異なる。方策はResNet-18、2層LSTM、5成分GMMからなり、推論では分散を小さくしたGMMから行動をサンプリングする。LSTMの履歴長は10で、選ばれた組の過去10 stepsも関連すると仮定する。[出典：§III-E、式(4)、Algorithm 1、Appendix A-B・G](../../../raw/papers/2304.08742v2.pdf)

## 実験条件と結果

シミュレーションはCanPick、NutAssembly、Officeの3タスクを画像／低次元状態で評価する。既存データは順に400、400、1200軌道。実機はWidowXのNutAssembly、Pickle、Soapで、既存データは160、285、485軌道。PickleとSoapはBridge Dataのsubsetを使い、Soapには対象タスクそのものの既存デモがない。[出典：§IV-A](../../../raw/papers/2304.08742v2.pdf)

### GCBCとの比較（シミュレーション）

| 条件 | GCBC事前学習 | GCBC＋fine-tuning | Behavior Retrieval |
| --- | ---: | ---: | ---: |
| CanPick・画像 | 68 ± 14% | 62 ± 2% | 74 ± 1% |
| CanPick・状態 | 33 ± 1% | 45 ± 1% | 73 ± 1% |
| NutAssembly・画像 | 22 ± 4% | 10 ± 1% | 58 ± 9% |
| NutAssembly・状態 | 15 ± 1% | 10 ± 1% | 75 ± 5% |
| Office・画像 | 0 ± 0% | 10 ± 4% | 64 ± 3% |
| Office・状態 | 76 ± 5% | 76 ± 1% | 85 ± 4% |
| 平均 | 35 ± 4% | 36 ± 2% | 72 ± 2% |

各条件100試行、3 random seedsの平均とstandard error。平均72%と36%の差は36 percentage pointsであり、相対改善率36%という意味ではない。GCBCのfine-tuning比較は既存データと対象デモのbalanced batchesを使う。[出典：Table I、§IV-C1、Appendix A-F](../../../raw/papers/2304.08742v2.pdf)

他のデータ選択法との比較では、対象デモのみ、全既存データとの混合、正解タスクラベルによる軌道選別（Ground Truth）を評価した。Behavior Retrievalは別タスクの有用部分も利用でき、実機ではGround Truthを上回ると報告する。Ground Truthはタスク名で選ぶ比較であり、あらゆる有用な組を知る理論的上限ではない。実機の主評価は各タスク40試行で、Fig. 10は成功率改善を示す。[出典：§IV-C2・3、Figs. 9–10](../../../raw/papers/2304.08742v2.pdf)

### Ablation・追加検証

- 埋め込みをcontrastive RLへ置き換える比較では、Table IIIの平均は38 ± 2%、VAEは72 ± 2%。ただしcontrastive側のOffice画像条件は学習が発散しN/Aであり、全6条件の揃った平均比較とは扱わない。
- NutAssemblyの閾値比較では $\delta\approx0.75$ が良好。閾値が高すぎると有用データも除いて性能が急落する。
- Pickleの分布変化テスト（各10試行）は、カップ色変更6/10、実物pickle 4/10、distractors 4/10、物理的摂動4/10。対象デモだけでは順に1/10、0/10、0/10、3/10。
- 全Bridge Datasetを使った追加のcup操作では、20試行で55%、対象デモのみ30%、全既存データとの混合35%。この条件の閾値は0.9。
- LMPへの組合せも検証され、CanPickで55 ± 2%（LMP事前学習）、56 ± 2%（対象デモでfine-tuning）、67 ± 4%（検索を利用）と報告する。

以上は[§IV-D・E、Tables II–III、Fig. 11、Appendix D-B・C、Table V](../../../raw/papers/2304.08742v2.pdf)に基づく。本文§Vには他の事前学習法との組合せが未検証という一般的記述もあるが、このv2のAppendix D-BにはLMPとの検証が載っているため、「組合せはすべて未検証」とはまとめない。

## 限界と再現上の注意

圧縮された状態・行動の距離は、視覚的類似性に偏り、タスクに重要な違いを捉えない可能性がある。新タスク学習時にも既存データへのアクセスが必要。主実験のBridge subsetは対象に視覚的に近い場面を選んでおり、任意の環境差で有効とは示していない。共通の状態・行動空間という前提にも注意する。[出典：§III-A・V、Appendix D-C](../../../raw/papers/2304.08742v2.pdf)

実機制御について、本文§IV-Aは4DOFと記す一方、Appendix B-Bは3DoF delta control・3Hzと記し、Bridge Dataの姿勢成分を除いたと説明する。gripperの数え方を含む詳細は本ingestでは実装未確認。検索についてもAppendix A-Gは埋め込みの事前計算とbatchの負のL2距離計算を述べるが、グラフ型ANN索引や検索高速化の性能比較を報告しているわけではない。[出典：§IV-A、Appendix A-G・B-B](../../../raw/papers/2304.08742v2.pdf)

## 関連ページ

- [検索による模倣学習データ選択](../../concepts/retrieval/retrieval_based_imitation_data_selection.md)
- [Behavior Cloning](../../concepts/imitation_learning/behavior_cloning.md)
- [VAE](../../concepts/generative_models/variational_autoencoder.md)
- [ACTの論文要約](../imitation_learning/zhao_2023_act.md)
