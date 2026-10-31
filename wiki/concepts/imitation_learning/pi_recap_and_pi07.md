---
title: π*0.6からπ0.7へ：経験による改善と多様な条件付け
type: concept
tags: [robotics, VLA, RECAP, advantage-conditioning, generalization, metadata]
sources:
  - ../../../raw/papers/pi_2025_pistar06.pdf
  - ../../../raw/papers/pi_2026_pi07.pdf
updated: 2026-10-31
---

# π*0.6からπ0.7へ：経験による改善と多様な条件付け

## 2本をつなぐ見方

π*0.6 / RECAPは、実機経験に報酬とvalueを与えてタスク方策を改善する方法。π0.7は、そのような専門方策のrolloutも学習し、詳細なpromptで多様な品質・タスクのbehaviorを1つの汎用方策から引き出す。以下の対比は2本の記述に基づく編集上の整理であり、新たな研究方針の提案ではない。[RECAP §IV–V](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §V–VI](../../../raw/papers/pi_2026_pi07.pdf)

| 観点 | π*0.6 / RECAP | π0.7 |
| --- | --- | --- |
| 中心課題 | 対象タスクの成功率・速度を経験で改善 | 単一モデルの器用さ・指示追従・組合せ汎化 |
| データの扱い | デモ・自律rollout・人の修正を集約し反復学習 | それらに動画・Web等を混ぜ、専門方策の経験も蒸留 |
| 品質の条件 | value由来のadvantageを二値化したindicator | 速度・品質・ミスのmetadata、subtask、画像subgoal |
| 推論時の誘導 | positive indicator、必要に応じCFG | 高品質metadata、言語・画像subgoal、必要に応じCFG |
| 追加の対象タスク学習 | SFTと実機データによる改善を評価 | 既知タスクはtask-specific post-trainingなしで評価。未知長期タスクのcoaching後のhigh-level学習は別設定 |
| 主な注意 | 介入品質・value近似・反復収集の工数 | 学習済みタスクと未知タスク、coachingと自律実行を区別 |

出典：[RECAP §IV–VII](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §V–X](../../../raw/papers/pi_2026_pi07.pdf)。

## 「悪いデータも使う」は同じだが、ラベルの意味が違う

RECAPはvalueから求めたadvantageの正負を入力にして、低advantageの行動も条件付き学習に残す。π0.7はepisode全体の品質・長さと局所的ミスを条件にする。π0.7のmetadataをそのままRECAPのvalue推定やadvantageと同一視しない。[RECAP §IV-B・V-B](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §V-C・VI-A・IX-E](../../../raw/papers/pi_2026_pi07.pdf)

この2本の主な学習機構は、近傍検索で類似データだけを取り出す方法ではない。混合データから条件に合うbehaviorを引き出す方式として記述されており、ベクトル検索・グラフ検索を使った性能改善は両論文の実験結果ではない。[RECAP §IV・Algorithm 1](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §V–VII](../../../raw/papers/pi_2026_pi07.pdf)

## 結果を比較するとき

π0.7 Fig.6は、洗濯・espresso・箱組立のRL specialistと汎用モデルを同じ図内で比較するため、2本の関係を読む入口になる。ただし、π0.7は専門方策の自律データも学習に使う。またFig.6上段のthroughputは専門方策に対する正規化で、RECAP Fig.7のsuccesses/hourそのものとは違う。[π0.7 §VI-A・IX-A・Fig.6](../../../raw/papers/pi_2026_pi07.pdf)、[RECAP §VI-C・Fig.7](../../../raw/papers/pi_2025_pistar06.pdf)

Throughputは成功作業数/時間。成功率が同じでも速くなれば改善し、成功率だけでは作業能力を捉え切れない。一方、異なるタスクの時間制限、リセット等の扱い、既知／未知条件を揃えないまま数値だけで全体順位を作らない。[RECAP §VI-A・C](../../../raw/papers/pi_2025_pistar06.pdf)、[π0.7 §IX・Fig.6](../../../raw/papers/pi_2026_pi07.pdf)

## 読む順番・関連ページ

1. [π*0.6 / RECAP要約](../../sources/reinforcement_learning/pi_2025_pistar06.md)：収集→value→advantage条件付け。
2. [π0.7要約](../../sources/imitation_learning/pi_2026_pi07.md)：promptの拡張と専門方策の蒸留。
3. [評価指標の読み方](robot_policy_evaluation_metrics.md)：成功率・throughput・task progressの区別。
4. [Cosmos Policy](cosmos_policy.md)：画像生成を使う別方式。π0.7のsubgoal画像と、Cosmos Policyのaction・future・valueの共同予測を区別する。
