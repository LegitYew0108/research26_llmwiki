---
title: "デモを併用する実機RL：SERLの学習とデータの流れ"
type: concept
tags: [reinforcement-learning, robotics, demonstrations, SERL, RLPD, replay-buffer, UTD]
sources:
  - ../../../raw/papers/luo_2024_hil_serl.pdf
  - ../../../raw/papers/luo_2024_serl.pdf
updated: 2026-10-31
---

# デモを併用する実機RL：SERLの学習とデータの流れ

## デモを使っても、学習目的がBCとは限らない

SERLでは、人のデモをprior dataとして保持し、方策自身が実機で集める経験と混ぜて学習する。デモの行動を直接正解として合わせるBCと異なり、criticは報酬と次状態からQ-functionを学び、actorはcriticの評価とentropy regularizationに基づいて改善する。したがって、SERLは固定デモだけで完結するBCでも、固定データだけで学ぶoffline RLでもなく、prior dataを併用してオンラインの実機経験から改善するRLである。[出典：SERL §4.1・5](../../../raw/papers/luo_2024_serl.pdf)

## データと更新の流れ

1. 初期デモをprior dataとして用意する。SERLの主実験では各タスク20本。
2. actorが観測から行動を出し、robot environmentが実行する。
3. 観測・行動・報酬・次の観測をonline replay bufferへ蓄積する。
4. prior dataとonline bufferから半分ずつbatchを取り、criticとactorを更新する。
5. 更新された方策でさらに経験を集める。actorとlearnerを分けて、制御と学習を並行する。

以上は[SERL §4.1・4.4・5、Fig. 2](../../../raw/papers/luo_2024_serl.pdf)に基づく。ここでのsamplingはデモとの距離に基づく近傍検索ではない。

## UTD ratio：1回の経験を何回の更新に使うか

update-to-data（UTD）ratioは、環境の1 stepに対して何回gradient updateを行うかを表す。**説明用の仮想例**としてUTDが10なら、環境1 stepあたり10回更新する。これはデモを10本使う意味でも、方策を10倍の制御周波数で動かす意味でもない。SERLは高UTDとcriticのlayer normalizationを採用するが、ここでの10は同論文の実験設定値を示すものではない。[定義と構成の出典：SERL §4.1・4.4](../../../raw/papers/luo_2024_serl.pdf)

実機経験を繰り返し利用するには計算が必要で、学習が行動出力を妨げない仕組みも重要になる。SERLはactorとlearnerを分離し、学習中も制御周期を維持する。[出典：SERL §4.4](../../../raw/papers/luo_2024_serl.pdf)

## 実機では報酬とリセットも必要

デモを与えるだけでは、オンライン試行の成功判定や次の試行の準備は解決しない。SERLは状態に基づく報酬、画像classifier、VICEを選択肢として用意し、object relocationではforward/backward方策で戻し操作も学ぶ。これらの方式がすべての環境に適するわけではない。[出典：SERL §4.2–4.3・6](../../../raw/papers/luo_2024_serl.pdf)

## 関連ページ

- [SERL論文要約：構成・タスク別結果・限界](../../sources/reinforcement_learning/luo_2024_serl.md)
- [模倣学習と強化学習の基本](../imitation_learning/imitation_and_reinforcement_learning.md)
- [Behavior CloningのCompounding Error](../imitation_learning/compounding_error.md)

## HIL-SERL：オンラインの修正を追加する

HIL-SERL（Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning）は、SERLに対して、初期デモに加え、学習中の人間による修正介入を組み込んだ実機の視覚ベースRLシステム。人が必要な場面で制御を引き継ぎ、その介入データをdemo bufferとRL bufferの両方へ入れる。方策自身の遷移はRL bufferにのみ入れる。修正行動への教師あり学習だけでなく、報酬に基づくoff-policy RLで方策を改善する。[出典：HIL-SERL §2–3・Fig. 2](../../../raw/papers/luo_2024_hil_serl.pdf)

精密挿入、双腕での受け渡しやtiming belt組立、物体をフライパンで返す動作などを扱う。多くは1–2.5時間で学習するが、Table 1(a)のtiming belt組立は6時間。Jenga whippingでは実時間の人間修正を使わないため、全タスクが同じ介入条件ではない。[出典：HIL-SERL §4・Table 1](../../../raw/papers/luo_2024_hil_serl.pdf)

個別の手法・実験・ablationは[HIL-SERL論文要約](../../sources/reinforcement_learning/luo_2024_hil_serl.md)を参照。対象はarXiv:2410.21845v3（2025-03-20）。[版の出典：表紙](../../../raw/papers/luo_2024_hil_serl.pdf)

### 介入データとHG-DAggerの違い

| 観点 | HIL-SERL | HG-DAgger（論文内の比較） |
| --- | --- | --- |
| 人の関わり | 必要時に制御を引き継いで修正 | 必要時に制御を引き継いで修正 |
| 学習目的 | 報酬に基づくQ-function・方策の改善 | 人の修正行動に合わせる教師あり学習 |
| 自律試行 | 成功・失敗ともRLの遷移として利用 | 人のラベルを中心に方策を学ぶ |

出典：[HIL-SERL §3.4・4.3](../../../raw/papers/luo_2024_hil_serl.pdf)。同じ「人が修正する」方式でも、学習の目的は異なる。

### 介入の有効性はタスクごとに見る

初期デモを増やしてオンライン介入を除くablationでは、RAM挿入48%、dashboard組立0%に対し、HIL-SERLは各100%。一方、object flippingでは介入なしでも100%だった。したがって、介入は難しい操作の探索を助けるが、全タスクで必須と一般化しない。また、各試行のリセットはscriptまたは人手であり、人の介入とreset-free学習は別の仕組みである。[出典：HIL-SERL §3.5・4.5・Table 1(b)](../../../raw/papers/luo_2024_hil_serl.pdf)
