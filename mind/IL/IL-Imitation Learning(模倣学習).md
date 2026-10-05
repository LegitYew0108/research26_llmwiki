---
title: "Imitation Learning（模倣学習）：自分の理解"
type: mind
tags: [mind, imitation-learning, reinforcement-learning, policy, behavior-cloning, inverse-reinforcement-learning]
sources:
  - ../../raw/temp/osa_2018_imitation_learning_survey.pdf
  - ../../raw/temp/ross_2011_dagger.pdf
  - ../../raw/temp/levine_2020_offline_rl_tutorial.pdf
updated: 2026-10-05
---

# 解く問題
基本的には、強化学習などの機械学習と同じ。
観測`Observation`から、いかにして次の行動`Action`を導出するかの方策`Policy`を学習する手法。

# 学習方法
お手本となる`demonstration` のデータを基に、それに近づくように学習していく。
完全な正解データがあるというよりは、多数の状況の違い(ボールが転がったり)に対応した行動を学び、デモで示された観測・状態と行動の関係などを利用し、状況に応じて行動を選ぶ方策を学ぶ。

### RL(Reinforcement Learning ; 強化学習)との違い
RLにおいては正解データはなく、適切に決定された報酬関数に対して、不明な系(シミュレーターなどで再現したり、現実世界で行う)を動作し、最大化するようにパラメーターを変化させながら近づけていく。

# 代表的手法
- Behavior Cloning(BC)
- Dataset Aggregation(DAgger)
- Generative Adversarial Imitation Learning(GAIL)
- Adversarial Inverse Reinforcement Learning(AIRL)
- Inverse Reinforcement Learning(IRL)

## 関連ページ・出典

- [Behavior Cloning：自分の理解](<BC-Behavior Cloning.md>)
- [模倣学習と強化学習の基礎](../../wiki/concepts/imitation_and_reinforcement_learning.md)
- [模倣学習のサーベイ：§2.2・4・5.1](../../raw/temp/osa_2018_imitation_learning_survey.pdf)
- [DAgger：§3（expertによる追加ラベルとデータ集約）](../../raw/temp/ross_2011_dagger.pdf)
- [Offline RL tutorial：§2.1–2.2](../../raw/temp/levine_2020_offline_rl_tutorial.pdf)
