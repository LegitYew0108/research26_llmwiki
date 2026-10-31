---
title: "Cosmos Policy：動画モデルの追加学習によるロボット制御とplanning"
type: source
tags: [robotics, imitation-learning, Cosmos-Policy, video-diffusion, world-model, value-function, planning]
sources:
  - ../../../raw/temp/kim_2026_cosmos_policy.pdf
updated: 2026-10-31
---

# Cosmos Policy：動画モデルの追加学習によるロボット制御とplanning

## 書誌情報と対象

Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, Jinwei Gu（NVIDIA・Stanford）、**Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning**。対象は保存したarXiv:2601.16163v1、22ページ。節・表・図番号はこの保存版に従う。[表紙](../../../raw/temp/kim_2026_cosmos_policy.pdf)

- [保存PDF](../../../raw/temp/kim_2026_cosmos_policy.pdf)
- [一次情報の調査記録・公式リンク](../../../raw/temp/cosmos_policy_research_20261031.md)

## 要点

事前学習済み動画生成モデル **Cosmos-Predict2-2B-Video2World** を、ロボットのデモで追加学習して制御に使う。行動専用の新しいheadを設計する代わりに、固有受容情報・行動列・価値を動画のlatent frameと同じ形に埋め込み、同じdiffusion transformerで扱う。モデルのアーキテクチャを変更しないが、入力表現・条件付け・noise samplingは制御向けに変更している。[§3–4・Appendix A.1–A.2.1](../../../raw/temp/kim_2026_cosmos_policy.pdf)

方策・world model・価値関数を同一構造で学習でき、直接行動を出す使い方と、複数候補を未来予測で評価するplanningの使い方がある。初期方策は模倣学習であり、planning用の追加学習はrolloutの未来観測とMonte Carlo returnを教師にする。価値を扱うことを、そのままactor-criticやTD学習の実施と解釈しない。[§3–4](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## Latent frame injection

観測$s$は現在時刻の画像・固有受容情報で、完全な物理状態ではない。$a$は$K$ stepsのaction chunk、$s'$は$t+K$時点の未来観測。入力履歴も、chunk内の全時刻に対応する未来動画も使わない。[§3・§4.1](../../../raw/temp/kim_2026_cosmos_policy.pdf)

1. カメラ画像と非画像modality用の空画像を並べ、Wan2.1 VAE tokenizerでlatent化する。
2. 非画像用latentを、$[-1,1]$に正規化した固有受容ベクトル・flattenした行動列・価値の複製で上書きする。
3. 系列を$(s,a,s',V(s'))$の順に配置し、条件部分はclean、予測対象はGaussian noiseで汚す。
4. 生成した非画像latentの複製部分を平均し、元の尺度へ戻して行動や価値を取り出す。非画像の抽出にはVAE decoderを使わない。

出典：[§4.1・Appendix A.1・Figs. 2・8](../../../raw/temp/kim_2026_cosmos_policy.pdf)。VAEの時間圧縮に合わせ、先頭にblank frameを置き、各画像を4枚複製する。4枚は4時刻ではなく同じ時刻のコピーである。

## 学習する三つの条件付き分布

| バッチの比率 | cleanな条件 | denoiseする対象 | 役割 |
| --- | --- | --- | --- |
| 50% | $s$ | $a,s',V(s')$ | 方策＋未来状態・価値の補助教師 |
| 25% | $s,a$ | $s',V(s')$ | world model＋価値の補助教師 |
| 25% | $s,a,s'$ | $V(s')$ | 価値予測 |

初期学習では方策用に成功デモ、残りには失敗再生を含むデータを利用する。ALOHAには失敗デモがなく、初期の両データ集合は同じ。条件maskを変えることで同じネットワークに異なる予測を学ばせる。[§4.2・Fig. 12](../../../raw/temp/kim_2026_cosmos_policy.pdf)

保存版§3のEDM目的は、noisy latentからclean latentを復元する二乗誤差として記載される。価値ラベルは学習済みcriticからのbootstrapではなく、終端報酬を時間割引した経験return $G_t=\gamma^{H-t}R(s_H,a_H)$。終端報酬は$[0,1]$で、部分達成も表せる。$V(s')$という記号はラベルに対する簡略表記で、初期価値予測は実際には$s,a,s'$全体を条件に持つ。[§3・§4.2と脚注](../../../raw/temp/kim_2026_cosmos_policy.pdf)

noise分布は元のlog-normalを確率0.7、uniform $[1,85]$を確率0.3で混ぜ、高noise領域を増やす。推論は$\sigma_{max}=80,\sigma_{min}=4$とする。高noise領域と終盤の誤差に対する著者の説明は仮説を含み、改善の観察と原因の確定を区別する。[Appendix A.2.1・Fig. 9](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## 直接実行とplanning

直接実行では、$a,s',V(s')$を並列生成し、行動だけを使い、未来予測と価値は捨てる。従って「実行時に未来画像を評価して行動を選ぶ」とは限らない。[§4.2・Appendix A.3.1](../../../raw/temp/kim_2026_cosmos_policy.pdf)

planningでは、成功だけのデモでは予測できない失敗を学ぶため、追加のrolloutで再学習する。バッチを方策10%・world model45%・価値45%に変更し、元checkpointを候補生成用の**policy model**、追加学習checkpointを予測用の**planning model**として併用する。同じアーキテクチャだが、実験時は二つのcheckpointを使う。[§4.3](../../../raw/temp/kim_2026_cosmos_policy.pdf)

best-of-$N$の手順は次のとおり。[§4.3・Appendix A.3.1・A.4.2](../../../raw/temp/kim_2026_cosmos_policy.pdf)

1. 元方策から$N=8$個の行動列候補を生成する。
2. 各候補につき未来状態を3回生成する。
3. 各未来状態について価値を5回予測する。planning用の$V(s')$は$s,a$をmaskし、未来状態だけを条件とする。
4. 候補ごとの計15個の値を、閾値で成功／失敗側へ分け、多数側のみ平均する「majority mean」で集約する。
5. 最高値の候補を選び、chunk全体を実行して再観測する。

探索木は1層であり、多段先読みやデータベースの近傍検索ではない。比較するmodel-free版は、$s'$をmaskして$Q(s,a)$を直接予測し、world modelを介さず候補を評価する方式である。[§4.3・§5.3・§6・Fig. 12](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## 学習・制御の規模

| 環境 | デモ数 | gradient steps／H100数／時間 | 予測chunk／実行steps | 推論denoising |
| --- | --- | --- | --- | --- |
| LIBERO | 40タスク×50本（方策用は失敗を除外） | 40K／64基／48時間 | 16／16 | 5回 |
| RoboCasa | 24タスク×50本（同上） | 45K／32基／48時間 | 32／16 | 5回 |
| ALOHA | 4タスク計185本 | 50K／8基／48時間 | 50／50（25 Hzで2秒） | 10回 |

全重みをfine-tuneする。ALOHA入力は14 joint angles・上方1台と手首2台の画像・タスク文。ALOHAデモはplate 80、shirt 15、bowl 45、bag 45本で、全タスクを一つの方策で学習する。[§5.1・Appendix A.2.2–A.3.1](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## 直接実行の結果

| 評価 | Cosmos Policy | 比較・条件 |
| --- | --- | --- |
| LIBERO平均成功率 | 98.5% | Spatial 98.1、Object 100.0、Goal 98.2、Long 97.6。3 seeds・計6000 trials。Diffusion Policy平均72.4、π0.5 96.9。 |
| RoboCasa平均成功率 | 67.1% | 24タスク×50 trials×3 seeds＝3600 trials。各タスク50本の人間デモ。比較手法は50～3000本等、学習データ量が異なる。 |
| ALOHA平均達成度スコア | 93.6 / 100 | 4タスクの平均。各手法101 trials。π0.5 88.6、Diffusion Policy 33.6。 |

出典：[Tables 1–3・§5.1–5.2・Appendix A.3.2](../../../raw/temp/kim_2026_cosmos_policy.pdf)。論文報告時の比較であり、現在のランキングではない。RoboCasaは未知物体を使い、5評価scene中2つは未知style。事前学習データ・規模まで同一に揃えた比較ではない。

ALOHAのスコアは成功／失敗の二値ではなく、物体把持・移動・折り畳み段階などの達成度を採点する。本文Introductionは93.6%をsuccess rateとも呼ぶが、ここでは採点規定とTable 3に従いスコアと呼ぶ。OODだけの平均ではCosmos Policy 89.3に対しπ0.5は92.5で、全条件・全タスクで最良という結果ではない。[§1・Appendix A.3.2・Table 3](../../../raw/temp/kim_2026_cosmos_policy.pdf)

ALOHAではVLA系とCosmos Policyを8 H100・48時間で学習するが、stepsは手法ごとに異なる。小さいDiffusion Policyは1 H100・48時間であり、全手法のGPU計算量が同一という意味ではない。[Appendix A.2.4](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## Planningとablationの結果

planning用には、5手法の直接評価505 rolloutsとCosmos Policyのbag追加143 rolloutsの計648本を用いる。§4.3のon-policyという説明に対し、実験の学習集合には他方策のrolloutも含まれる。評価はbowl・bagの難しい初期条件であり、直接評価Table 3の平均と混ぜない。[§4.3・§5.3](../../../raw/temp/kim_2026_cosmos_policy.pdf)

| 難しい初期条件の達成度スコア | 直接実行 | Qによるmodel-free選択 | world model＋Vによる選択 |
| --- | --- | --- | --- |
| candies in bowl | 49.0 | 52.0 | 60.0 |
| candy in ziploc bag | 70.0 | 70.7 | 84.0 |
| 2タスク平均 | 59.5 | 61.3 | 72.0 |

出典：[Fig. 7・§5.3](../../../raw/temp/kim_2026_cosmos_policy.pdf#page=10)。改善は平均**12.5スコアポイント**で、成功率の相対12.5%増とはしない。§5.3は「three formulations」と書くが列挙は$V(s')$と$Q(s,a)$の2種類であり、第3の方式を補完しない。

LIBEROでは補助lossを外すと98.5→97.0、事前学習なしでは94.6。RoboCasaの段階的ablationは67.1→66.6→64.0→62.5→44.4で、順に価値学習用サンプル、world model学習用サンプル、方策の価値補助教師、未来状態補助教師を除く。最後の差が大きいが、複数変更を積み重ねた比較であり、全構成に共通する独立した効果量ではない。[Tables 4–5・Appendix A.4.1](../../../raw/temp/kim_2026_cosmos_policy.pdf)

Table 5の1-step推論は66.4%で、67.1%との差は0.7ポイント。一方captionは「-0.5%」と記載するため、数値差を混同しない。[Table 5](../../../raw/temp/kim_2026_cosmos_policy.pdf#page=22)

## 計算量・限界

1 H100でchunk生成は5 denoising stepsで0.61秒、10 stepsで0.95秒、1 stepで0.16秒。ALOHAは2秒間の動作を生成するために0.95秒停止する。planningは8 H100の並列処理でも4.9秒かかる。制御周波数25 Hzはモデルが毎秒25回推論する意味ではない。[Appendix A.4.2](../../../raw/temp/kim_2026_cosmos_policy.pdf)

動的manipulation・locomotionへの適用は遅延が制約となる。planningにはデモ分布外の結果を予測できるrolloutデータが必要で、探索は1層に限られる。graph-based ANNや検索による学習データ選択の効果は検証していない。[§6・Appendix A.4.2、実験範囲§5](../../../raw/temp/kim_2026_cosmos_policy.pdf)

## 関連ページ

- [Cosmos Policyの仕組み：動画モデル・world model・planning](../../concepts/imitation_learning/cosmos_policy.md)
- [Diffusion Policy](chi_2023_diffusion_policy.md)
- [Action ChunkingとTemporal Ensembling](../../concepts/imitation_learning/action_chunking_and_temporal_ensembling.md)
- [Behavior Cloning](../../concepts/imitation_learning/behavior_cloning.md)

注意：Related Workに登場するJain et al. (2025)のSAILORと、このWikiの[Nasiriany et al. (2023)のSAILOR](../retrieval/nasiriany_2023_sailor.md)は異なる文献である。[§2・References](../../../raw/temp/kim_2026_cosmos_policy.pdf)
