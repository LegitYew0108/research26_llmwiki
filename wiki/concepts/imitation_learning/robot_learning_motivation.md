---
title: ロボットの動作に機械学習を使う動機
type: concept
tags: [robotics, robot-learning, motivation, imitation-learning, reinforcement-learning]
sources:
  - ../../../raw/papers/zhao_2023_act.pdf
  - ../../../raw/papers/chi_2023_diffusion_policy.pdf
  - ../../../raw/papers/luo_2024_hil_serl.pdf
updated: 2026-10-31
---

# ロボットの動作に機械学習を使う動機

## 何を学習に任せたいのか

ロボット学習の一つの動機は、接触・変形・視覚を伴う作業で、環境の精密なモデルや状況ごとの動作規則を設計する負担を減らし、観測に応じた動作を経験から獲得することにある。ACTは、容器を押して蓋を開く際の接触や変形をモデル化するより、位置の変化に反応する閉ループ方策を学ぶほうが単純になり得ると説明する。これはACT著者の動機であり、すべての作業で学習が優れるという証明ではない。[ACT §I](../../../raw/papers/zhao_2023_act.pdf)

例えば、容器の位置が変わったときに同じ関節軌道を再生するだけではなく、画像を見て次の動作を調整する。ACTの入力は画像・関節位置で、出力は目標関節位置の列である。ただし、観測に応じて動作を変えること自体は学習に固有ではなく、ACTが目指すのはその方策をデモから得ることである。後半は制御と学習を区別するための整理。[ACT §I・IV](../../../raw/papers/zhao_2023_act.pdf)

## 想定する利用場面

| 場面 | 学習に期待する役割 | 一次資料 |
| --- | --- | --- |
| 日用品の精密な双腕操作：容器の開封、電池の挿入 | 接触を含む手順と視覚に基づく修正をデモから学ぶ | [ACT §I・V](../../../raw/papers/zhao_2023_act.pdf) |
| 布・液体を含む操作：シャツを畳む、ソースを注ぐ・広げる | 複雑な観測から時間的に整合した行動列を生成する | [Diffusion Policy §I・VI–VII](../../../raw/papers/chi_2023_diffusion_policy.pdf) |
| 精密組立・動的操作：RAM挿入、ベルト組立、物体の反転 | 実機の試行結果を使い、成功率や動作速度を改善する | [HIL-SERL §I・IV](../../../raw/papers/luo_2024_hil_serl.pdf) |
| 安価で誤差のあるハードウェアによる精密操作 | 高精度な機材だけに依存せず、視覚フィードバックから誤差を補う方策を学ぶ | [ACT §I](../../../raw/papers/zhao_2023_act.pdf) |

これらは論文の実験対象・想定用途であり、家庭や工場での長期運用が実証済みという意味ではない。HIL-SERLもタスクごとの学習であり、非構造環境での広範な汎化や、非常に長い作業への拡張には制約がある。[HIL-SERL §VI](../../../raw/papers/luo_2024_hil_serl.pdf)

## 模倣学習と強化学習で動機はどう違うか

- **模倣学習**：人ができる作業を実演し、観測から動作への対応を学ばせる。ACTは安価な遠隔操作システムでデモを集め、精密操作を学ぶ。[ACT §I・III–IV](../../../raw/papers/zhao_2023_act.pdf)
- **強化学習**：実行結果の報酬から、対象の実機・作業に適した動作へ改善する。HIL-SERLは初期デモと人の修正を併用するため、「自力の試行錯誤だけで学ぶ」とは限らない。[HIL-SERL §I・III](../../../raw/papers/luo_2024_hil_serl.pdf)

学習と従来制御は組み合わせられる。HIL-SERLでは学習方策の下に低レベルcontrollerを置く。したがって、機械学習の導入をモーター制御全体の置換と捉える必要はない。[HIL-SERL §III・Appendix D](../../../raw/papers/luo_2024_hil_serl.pdf)

## 読み取れる判断軸

以下は資料を踏まえた整理であり、特定手法の優位性を保証する基準ではない。環境を固定し、既知のモデルや規則で必要な性能を得られる場合、学習の導入自体を目的にする必要はない。状況ごとの規則設計や物理モデル化が難しい場合に、データ収集・訓練の負担を払う価値があるかを考える。学習は設計の負担を消すのではなく、デモ・報酬・試行環境・評価の設計へ移す側面もある。[整理の根拠：ACT §I、HIL-SERL §I・III・VI](../../../raw/papers/zhao_2023_act.pdf)、[HIL-SERL](../../../raw/papers/luo_2024_hil_serl.pdf)

## 関連ページ

- [模倣学習と強化学習の基本](imitation_and_reinforcement_learning.md)
- [ACT論文](../../sources/imitation_learning/zhao_2023_act.md)
- [Diffusion Policy論文](../../sources/imitation_learning/chi_2023_diffusion_policy.md)
- [HIL-SERL論文](../../sources/reinforcement_learning/luo_2024_hil_serl.md)
