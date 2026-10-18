---
title: Behavior RetrievalとSAILORの実験結果比較
type: research-comparison
tags: [behavior-retrieval, sailor, evaluation, imitation-learning]
sources:
  - ../raw/papers/2304.08742v2.pdf
  - ../raw/temp/nasiriany_2023_sailor.pdf
updated: 2026-10-19
---

# Behavior RetrievalとSAILORの実験結果

別々のタスク・実験条件で評価されているため、両手法の成功率から直接優劣は比較できない。以下は各論文内の比較。単位は成功率%。ppはpercentage points。差分は掲載平均値からの計算であり、有意差検定ではない。[BR Table I・Fig.10](../raw/papers/2304.08742v2.pdf)、[SAILOR Table 1・§5.4](../raw/temp/nasiriany_2023_sailor.pdf)

## Behavior Retrieval：シミュレーション

| タスク・入力 | GCBC事前学習 | GCBC＋FT | Behavior Retrieval | 最良の比較手法との差（pp） |
|---|---:|---:|---:|---:|
| CanPick・画像 | 68 ± 14 | 62 ± 2 | 74 ± 1 | +6 |
| CanPick・状態 | 33 ± 1 | 45 ± 1 | 73 ± 1 | +28 |
| NutAssembly・画像 | 22 ± 4 | 10 ± 1 | 58 ± 9 | +36 |
| NutAssembly・状態 | 15 ± 1 | 10 ± 1 | 75 ± 5 | +60 |
| Office・画像 | 0 ± 0 | 10 ± 4 | 64 ± 3 | +54 |
| Office・状態 | 76 ± 5 | 76 ± 1 | 85 ± 4 | +9 |
| 論文の平均 | 35 ± 4 | 36 ± 2 | 72 ± 2 | +36 |

100試行、3 seeds、±標準誤差。GCBCはgoal-conditioned BC、FTはfine-tuning。対象デモ10本。[出典：Table I、§IV](../raw/papers/2304.08742v2.pdf)

実機のNutAssembly・Pickle・SoapはFig.10の棒グラフから概ね50%、58%、65%。表に掲載された厳密値ではなく図の読取概数。対象デモ10本、各40評価。Ground Truthは同じタスク名の軌道を選ぶ比較であり理論上限ではない。[出典：Fig.10](../raw/papers/2304.08742v2.pdf)

## SAILOR：シミュレーション

| タスク・既存データ条件 | BC-RNN | BC-RNN FT | BC-RNN R3M | IQL | IQL UDS | FIST | SAILOR |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kitchen-All | 32.3 ± 9.0 | 93.0 ± 2.3 | 83.3 ± 2.1 | 65.0 ± 7.1 | 78.3 ± 7.0 | 68.7 ± 2.5 | 95.7 ± 1.7 |
| Kitchen-No Microwave | 32.3 ± 9.0 | 77.7 ± 7.6 | 83.3 ± 2.1 | 65.0 ± 7.1 | 70.3 ± 7.3 | 83.0 ± 0.8 | 95.0 ± 2.2 |
| CALVIN-Setting Up | 33.0 ± 2.2 | 72.8 ± 5.4 | 26.0 ± 1.4 | 7.7 ± 1.7 | 16.3 ± 2.6 | 3.7 ± 2.4 | 77.3 ± 3.1 |
| CALVIN-Cleaning Up | 41.0 ± 1.6 | 61.8 ± 9.1 | 28.0 ± 2.2 | 14.7 ± 2.1 | 20.0 ± 3.7 | 9.3 ± 5.0 | 88.0 ± 5.1 |

原表のKitchenで統合されたセルは両行に繰り返した。±標準偏差、原則3 seeds、BC-RNN FTのみ6 seeds。各checkpointで100試行し、seedごとの最高成功率を集計。Kitchenの対象デモ18本、CALVINは各30本。[出典：Table 1、§5.1、Appendix C.3](../raw/temp/nasiriany_2023_sailor.pdf)

Kitchenの対象タスクは電子レンジ・ケトル・照明・引き戸を含む複数段階の操作。No Microwaveは既存データから電子レンジを操作するデモを除いた条件。CALVINはSetting Upが照明をつけてブロックを机に配置、Cleaning Upがブロックを引き出しへ片付けて消灯するタスク。[出典：§5.1](../raw/temp/nasiriany_2023_sailor.pdf)

## SAILOR：実機

| タスク | BC-RNN FT | SAILOR | 差（pp） |
|---|---:|---:|---:|
| Real-Breakfast | 76.7 | 76.7 | 0 |
| Real-Cook | 23.3 | 73.3 | +50.0 |
| Real-Cook-Pan | 46.7 | 76.7 | +30.0 |

各30試行、1 seed。複数checkpointを少数試行で確認し、有望なものを選んで30試行する。Real-Breakfastは朝食の配膳、Real-Cookは食材をフライパンへ入れる、Real-Cook-Panはフライパンをコンロへ置く操作も含む。[出典：§5.4、Appendix B.3・C.3](../raw/temp/nasiriany_2023_sailor.pdf)

## SAILORの検索による寄与

| タスク | 検索なし | 全既存データを使用 | SAILOR | 検索なしとの差（pp） |
|---|---:|---:|---:|---:|
| CALVIN-Setting Up | 65.0 ± 2.2 | 64.3 ± 10.8 | 77.3 ± 3.1 | +12.3 |
| CALVIN-Cleaning Up | 70.0 ± 0.8 | 65.3 ± 7.3 | 88.0 ± 5.1 | +18.0 |

既存手法との比較だけでなく、同じ枠組みから検索を除くablationでも改善する。ただし、グラフ型ANNで検索を近似・高速化した場合の効果を示す結果ではない。[出典：Table 2、§4.2・5.3](../raw/temp/nasiriany_2023_sailor.pdf)

SAILORはraw/tempの一次資料を参照した回答用資料であり、wikiへのingestは行っていない。
