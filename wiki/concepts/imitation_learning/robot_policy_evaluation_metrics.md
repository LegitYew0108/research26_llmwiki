---
title: ロボット方策の評価指標とSOTAの読み方
type: concept
tags: [robotics, evaluation, benchmark, success-rate, generalization]
sources:
  - ../../../raw/papers/pi_2025_pistar06.pdf
  - ../../../raw/papers/pi_2026_pi07.pdf
  - ../../../raw/papers/luo_2024_hil_serl.pdf
  - ../../../raw/papers/kim_2026_cosmos_policy.pdf
  - ../../../raw/papers/chi_2023_diffusion_policy.pdf
updated: 2026-10-31
---

# ロボット方策の評価指標とSOTAの読み方

## 成功率だけでは比較できない理由

以下は保存済み論文に基づく整理。成功率は定義された作業を完了した割合であり、手先の位置誤差や達成度スコアとは区別する。HIL-SERLのタスク別成功率と、Cosmos PolicyのALOHA達成度スコアは同じ尺度ではない。[HIL-SERL Table 1](../../../raw/papers/luo_2024_hil_serl.pdf)、[Cosmos Policy Table 3・Appendix A.3.2](../../../raw/papers/kim_2026_cosmos_policy.pdf)

異なる手法の比較では、タスク・実機／シミュレーション・ロボット・初期条件・既知／未知条件・データ量・評価試行数を確認する。各論文の比較対象内で最良であることと、現在の全研究中で最良であることは別。例えばHIL-SERLはタスクごとの学習で非構造環境の広範な汎化を検証せず、Cosmos Policyも全条件で最良ではない。[HIL-SERL §4・6](../../../raw/papers/luo_2024_hil_serl.pdf)、[Cosmos Policy §5・Table 3](../../../raw/papers/kim_2026_cosmos_policy.pdf)

## 評価する方向と具体例

| 方向 | 指標・確認する量 | 一次資料 |
| --- | --- | --- |
| 完了できるか | タスク成功率、試行数 | [HIL-SERL Table 1](../../../raw/papers/luo_2024_hil_serl.pdf) |
| 速くできるか | cycle time | [HIL-SERL Table 1](../../../raw/papers/luo_2024_hil_serl.pdf) |
| どこまで進むか・品質 | 部分達成スコア、IoU、coverage | [Cosmos Policy Table 3](../../../raw/papers/kim_2026_cosmos_policy.pdf)、[Diffusion Policy §6](../../../raw/papers/chi_2023_diffusion_policy.pdf) |
| 条件が変わってもできるか | 未知物体・配置・sceneでの成功率やスコア | [Cosmos Policy §5・Table 3・Appendix A.3.2](../../../raw/papers/kim_2026_cosmos_policy.pdf) |
| 少ない経験で学べるか | デモ数、実機学習時間、学習曲線 | [HIL-SERL §3–4・Fig.5](../../../raw/papers/luo_2024_hil_serl.pdf) |
| 人の手助けを減らせるか | 学習中の介入step率。デモ・ラベル・リセット工数とは区別 | [HIL-SERL §3.5・Fig.5](../../../raw/papers/luo_2024_hil_serl.pdf) |
| 計算負担と応答性 | 学習GPU数・時間、推論遅延、chunk長 | [Cosmos Policy Appendix A.2–A.3・Table 5](../../../raw/papers/kim_2026_cosmos_policy.pdf) |

汎化を成功率で測る場合もある。「異なる指標」には、数式が異なる量だけでなく、同じ成功率を異なる条件で測る評価軸も含む。これは上記の実験条件を踏まえた整理。

## Throughputと汎化の追加例

RECAPは1時間あたりの成功作業数をthroughputとして評価し、成功率と速度の両方を捉える。π0.7 Fig.6上段のthroughputは専門方策に対して正規化され、下段はtask progressなので数値をそのまま比較しない。また、学習で見たタスクの専門方策との比較と、未知タスク・未知task–robot組合せへの転移を区別する。[RECAP §VI-C・Fig.7](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §IX・Fig.6](../../../raw/papers/pi_2026_pi07.pdf)

詳しくは[π*0.6からπ0.7へ](pi_recap_and_pi07.md)を参照。

## 記述上の注意

100回中100回の成功は、将来の失敗率が0である保証ではない。学習曲線に人の介入で得た成功を含む場合、最終方策の評価結果と分ける。また、学習時間と初期デモ収集・準備を含めた総工数も分ける。[HIL-SERL §4・6・Fig.5・Table 1](../../../raw/papers/luo_2024_hil_serl.pdf)

## 関連ページ

- [ロボット学習の動機](robot_learning_motivation.md)
- [HIL-SERL](../../sources/reinforcement_learning/luo_2024_hil_serl.md)
- [Cosmos Policy](../../sources/imitation_learning/kim_2026_cosmos_policy.md)
- [Diffusion Policy](../../sources/imitation_learning/chi_2023_diffusion_policy.md)
