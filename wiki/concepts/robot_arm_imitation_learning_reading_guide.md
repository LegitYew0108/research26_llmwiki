---
title: "ロボットアームの模倣学習：基礎資料と読む観点"
type: concept
tags: [robot-arm, imitation-learning, ACT, diffusion-policy, reading-guide]
sources:
  - ../../raw/temp/osa_2018_imitation_learning_survey.pdf
  - ../../raw/temp/ross_2011_dagger.pdf
  - ../../raw/papers/zhao_2023_act.pdf
  - ../../raw/papers/chi_2023_diffusion_policy.pdf
  - ../../raw/temp/levine_2020_offline_rl_tutorial.pdf
  - ../../raw/temp/luo_2024_serl.pdf
  - ../../raw/temp/luo_2024_hil_serl.pdf
updated: 2026-10-31
---

# ロボットアームの模倣学習：基礎資料と読む観点

## 模倣学習の基礎と行動列の予測

以下は2026-10-03の調査から、ロボットアームの模倣学習に関係する資料を整理し直したもの。読む順序は理解のための編集上の案内で、研究計画ではない。全文の個別要約が未作成の資料も含む。

| 資料 | 読む観点・一次資料 |
| --- | --- |
| Osa et al., An Algorithmic Perspective on Imitation Learning（2018） | BCとIRLの違い、デモの表現、学習の分類。[§2–5](../../raw/temp/osa_2018_imitation_learning_survey.pdf) |
| Ross et al., DAgger（2011） | 学習者の行動が訪問状態を変えること、expertによる追加ラベルとデータ集約。[§1–3](../../raw/temp/ross_2011_dagger.pdf) |
| Zhao et al., ACT（2023） | 双腕テレオペ、action chunk、CVAE、temporal ensembling。[§III–IV](../../raw/papers/zhao_2023_act.pdf)／[既存要約](../sources/zhao_2023_act.md) |
| Chi et al., Diffusion Policy（2023初稿、保存版v5） | 観測を条件とするdiffusion modelによる行動列生成とreceding horizon control。[§3](../../raw/papers/chi_2023_diffusion_policy.pdf)／[取り込み済み要約](../sources/chi_2023_diffusion_policy.md) |

まず[BC](behavior_cloning.md)と[Compounding Error](compounding_error.md)を確認し、ACTとDiffusion Policyの行動列予測を読むと、単一時刻の回帰と系列出力の関係を整理できる。この順序は上記資料に基づく編集上の判断。

## デモを使うRLとの区別

固定データから報酬を基準に方策を学ぶoffline RLは、expert行動を直接教師信号にするBCと目的が異なる。データが固定されていることだけではBCかRLかを判別できない。[Offline RL tutorial §2](../../raw/temp/levine_2020_offline_rl_tutorial.pdf)

SERLとHIL-SERLは、デモ利用や人間介入と実機manipulationのRLを理解する隣接資料として残す。デモを使うこと自体を、学習全体がBCである根拠にはしない。[SERL §4](../../raw/temp/luo_2024_serl.pdf)、[HIL-SERL 手法・実験](../../raw/temp/luo_2024_hil_serl.pdf)

## 関連ページ

- [模倣学習と強化学習の基本](imitation_and_reinforcement_learning.md)
- [検索による模倣学習データ選択の関連研究](imitation_data_selection_related_work.md)
- [ACTのためのCVAE学習ガイド](cvae_for_act_reading_guide.md)

- [SERL論文要約：デモを併用する実機RLの構成と結果](../sources/luo_2024_serl.md)
- [デモを併用する実機RL：学習とデータの流れ](demonstration_augmented_robot_rl.md)
