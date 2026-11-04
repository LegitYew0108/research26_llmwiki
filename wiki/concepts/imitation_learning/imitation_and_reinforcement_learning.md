---
title: "ロボットの模倣学習：基本的な仕組みとRLとの違い"
type: concept
tags: [robotics, imitation-learning, behavior-cloning, observation, action, policy]
sources:
  - ../../../raw/papers/zhao_2023_act.pdf
  - ../../../raw/papers/chi_2023_diffusion_policy.pdf
  - ../../../raw/papers/du_2023_behavior_retrieval.pdf
  - ../../../raw/web/web_mit_imitation_learning_20261003.md
  - ../../../raw/web/web_huggingface_rl_framework_20261003.md
  - ../../../raw/papers/luo_2024_hil_serl.pdf
updated: 2026-10-31
---

# ロボットの模倣学習：基本的な仕組みとRLとの違い

## 何を学ぶのか

模倣学習（Imitation Learning, IL）は、お手本であるdemonstrationから、観測に応じて行動を選ぶ方策（policy）を学ぶ。毎回同じ軌道を再生するだけでなく、カメラ画像や関節情報に応じて操作を変えることが目的になる。[模倣学習の参照記録：MIT](../../../raw/web/web_mit_imitation_learning_20261003.md)、[実例：ACT §III–IV](../../../raw/papers/zhao_2023_act.pdf)

説明用に、机の上の物を箱に入れる場面を考える。人が操作した画像・関節情報と、そのときの操作を記録し、新しい観測に対してもお手本に近い操作を出すように学ぶ。これは仕組みを示す仮想例で、論文の特定実験の再現ではない。[学習の仕組み：ACT §IV](../../../raw/papers/zhao_2023_act.pdf)

## 入力・出力・方策

| 用語 | 意味 |
| --- | --- |
| observation $o_t$ | 時刻$t$に取得する画像や関節情報など。 |
| state $s_t$ | 環境の状態。観測だけでは、その全体が分かるとは限らない。 |
| action $a_t$ | ロボットへ与える操作。目標関節位置や手先の指令など。 |
| policy $\pi$ | 観測から行動、または行動の分布を決めるモデル。 |
| demonstration | 観測・操作などを時系列で記録したお手本。 |

用語の整理は[保存したRL Frameworkの参照記録](../../../raw/web/web_huggingface_rl_framework_20261003.md)と[MITの参照記録](../../../raw/web/web_mit_imitation_learning_20261003.md)、行動表現の具体例は[ACT §IV](../../../raw/papers/zhao_2023_act.pdf)に基づく。Web参照記録は全文保存ではなく、2026-10-03の参照内容の記録である。

方策が直接モータのトルクを出す必要はない。ACTは目標関節位置、Diffusion Policyの実機例は手先の目標位置・姿勢などを出し、下位のcontrollerが実行する。入力・出力の仕様は手法やロボットによって異なる。[ACT §IV-C](../../../raw/papers/zhao_2023_act.pdf)、[Diffusion Policy §6–7・Appendix D](../../../raw/papers/chi_2023_diffusion_policy.pdf)

## Behavior Cloning：行動を教師信号にする

BCは、デモの観測を入力、記録されたexpertの行動を教師信号にして方策を学ぶ。例えば、観測$o_i$と教師行動$a_i^*$の組に対し、予測行動とのずれを小さくする。次式はその学習を説明するための一般形で、すべての手法が同じ損失を使うという意味ではない。[BCの参照記録：MIT](../../../raw/web/web_mit_imitation_learning_20261003.md)、[具体的な目的関数：Behavior Retrieval §III-E](../../../raw/papers/du_2023_behavior_retrieval.pdf)

$$\min_\theta\;\frac1{|D|}\sum_{(o_i,a_i^*)\in D}\ell(\pi_\theta(o_i),a_i^*).$$

BCの構成は一時刻の行動を二乗誤差で回帰するものに限らない。ACTはCVAEで行動列を学び、Diffusion Policyは行動列のノイズ予測を学ぶ。ネットワークや損失が違っても、デモから振る舞いを学ぶBCの設定である。[ACT §IV](../../../raw/papers/zhao_2023_act.pdf)、[Diffusion Policy §2・§5](../../../raw/papers/chi_2023_diffusion_policy.pdf)

## なぜお手本に合うだけでは失敗するのか

学習時の観測はお手本に含まれる状況だが、実行時は学習した方策の行動が次の状況を作る。小さな誤りでデモに少ない状態へ移ると、さらに誤ることがある。このdistribution shiftとcompounding errorのため、データ上の行動予測が正確でも、タスクの成功が保証されるわけではない。[ACT §II・IV-A](../../../raw/papers/zhao_2023_act.pdf)

デモ収集の負担も課題である。Behavior Retrievalは、少数の対象デモに似た状態・行動を既存データから選んでBCの訓練に加える。一方、無関係なデータを混ぜれば常に改善するとは限らない。[Behavior Retrieval §I・III・V](../../../raw/papers/du_2023_behavior_retrieval.pdf)

## RLとの違いは学習の基準

| 観点 | 標準的なBC | RL |
| --- | --- | --- |
| 学習の基準 | デモに記録された行動へ合わせる。 | 将来にわたる報酬を大きくする。 |
| 主な教師・評価信号 | expertの行動。 | 行動の結果に対する報酬。 |

BCの定義は[MITの参照記録](../../../raw/web/web_mit_imitation_learning_20261003.md)、RLの目的は[RL Frameworkの参照記録](../../../raw/web/web_huggingface_rl_framework_20261003.md)に基づく。ここではBCとの違いを理解する範囲に絞り、RLの価値関数・アルゴリズム分類・目的関数の詳説は扱わない。

デモや人の修正を使う方法でも、報酬に基づいて方策を改善するものはある。HIL-SERLはその例であり、「デモを使う」だけでBCと同じ学習になるわけではない。[HIL-SERL §III・IV-C](../../../raw/papers/luo_2024_hil_serl.pdf)

また、IL全体をBCだけで定義しない。IRLはデモからcostを推定する方法として区別される。このページは、行動を教師信号にするBCと、その行動列予測・データ選択を中心とする。[MITの参照記録](../../../raw/web/web_mit_imitation_learning_20261003.md)

## 関連ページ

- [Behavior Cloning](behavior_cloning.md)
- [Compounding Error](compounding_error.md)
- [ACTの論文要約](../../sources/imitation_learning/zhao_2023_act.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
- [Diffusion Policy](diffusion_policy.md)
- [検索による模倣学習データ選択](../retrieval/retrieval_based_imitation_data_selection.md)
- [ロボットアームの模倣学習：基礎資料と読む観点](robot_arm_imitation_learning_reading_guide.md)
