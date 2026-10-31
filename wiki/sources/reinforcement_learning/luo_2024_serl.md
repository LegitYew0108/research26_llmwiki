---
title: "SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning"
type: source
tags: [robotics, reinforcement-learning, SERL, RLPD, demonstrations, off-policy, impedance-control, reset-free]
sources:
  - ../../../raw/temp/luo_2024_serl.pdf
updated: 2026-10-31
---

# SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning

## 書誌情報と要点

- 著者：Jianlan Luo、Zheyuan Hu（同等貢献）、Charles Xu、You Liang Tan、Jacob Berg、Archit Sharma、Stefan Schaal、Chelsea Finn、Abhishek Gupta、Sergey Levine。
- 対象版：arXiv:2401.16013v4、2025年3月20日。PDF冒頭の「January 2024」やファイル名の2024と、取り込んだ版の更新日は区別する。
- 一次資料：[保存済みPDF・表紙](../../../raw/temp/luo_2024_serl.pdf)。今回の明示的な依頼に従い、資料は `raw/temp/` に保持した。

**SERLは、新しいRLアルゴリズム単体ではなく、実機で効率よくRLを行うためのソフトウェア基盤**である。RLPDに基づく学習、画像からの報酬判定、forward/backward方策によるリセット、非同期の学習・行動実行、接触操作向けのimpedance controllerをまとめて提供する。著者らの中心的な主張は、アルゴリズムの選択に加えて、その実装と実機システムの設計が性能を大きく左右するというもの。[出典：§1・4](../../../raw/temp/luo_2024_serl.pdf)

## デモをどう使い、何を学習するのか

中核は、Soft Actor-Critic（SAC）に基づくoff-policy actor-critic手法であるRLPD。actorは行動を選ぶ方策、criticは状態と行動の将来の価値を推定するQ-functionである。デモ等のprior dataと、現在の方策が実機から集めた経験を使い、報酬に基づいて両者を更新する。**デモの行動を正解ラベルとして再現するBCとは学習目的が異なる**。[出典：§4.1・5のBC比較](../../../raw/temp/luo_2024_serl.pdf)

SERLが採用するRLPDの主な構成は次の3点。ここでの説明はSERL論文に基づき、RLPD原論文そのものを取り込んだ要約ではない。[出典：§4.1](../../../raw/temp/luo_2024_serl.pdf)

1. **高いupdate-to-data（UTD）ratio**：実機の環境1 stepに対して複数回のgradient updateを行い、取得した経験を繰り返し使う。
2. **symmetric sampling**：学習batchの半分をprior data、残り半分をonline replay bufferから取る。類似度で近いデモを選ぶ検索手順ではない。
3. **criticのlayer normalization**：高いUTD ratioでの学習を支えるregularizationとして使う。

方策の学習にはentropy regularizationも含まれる。SERLはprior dataなしの学習にも対応するが、主実験では各タスク20本の遠隔操作デモを用いてRLを開始している。[出典：§4.1・5](../../../raw/temp/luo_2024_serl.pdf)

## 報酬・リセット・制御を含むシステム

### 報酬：成功をどう判定するか

- ロボットの状態から成功を判定できる場合は、手で定義した報酬を使う。PCB挿入では、物体がgripper内で固定されている前提のもと、手先位置による成功判定を利用する。
- 画像によるbinary classifierを使う場合は、成功eventの確率から $r(s)=\log p(e\mid s)$ とする。
- VICEも選択肢として実装される。方策が報酬classifierをだます状態を見つける問題に対し、方策の訪問状態をnegativeとして追加し、classifierを更新する。

これらは選択可能な報酬の方式であり、全実験でVICEを使ったわけではない。[出典：§4.2・Table 2](../../../raw/temp/luo_2024_serl.pdf)

### リセット：次の試行をどう始めるか

object relocationでは、物体を一方のbinから他方へ移すforward方策と、元に戻すbackward方策を同時に学ぶ。各agentは独立の方策・Q-function・報酬を持つ。ここでのreset-freeは、戻す操作自体を学習して人手を減らす構成を指し、環境を初期状態へ戻す工程が存在しないという意味ではない。[出典：§4.3・5](../../../raw/temp/luo_2024_serl.pdf)

### 学習と行動実行を分ける

Gym-likeな環境adapterを介し、actor、learner、robot environmentを並行して動かす。高UTDの学習計算と行動推論を分けることで、実機の制御周期を維持する。Franka向けの環境を提供するが、設計上は他のロボット環境も接続できる。[出典：§4.4・Fig. 2](../../../raw/temp/luo_2024_serl.pdf)

### 接触時のimpedance control

低頻度の方策が目標を出し、高頻度の低レベルcontrollerが追従する。論文の説明例は方策10 Hz、低レベル1 kHz。接触で手先が止まったとき、目標と実位置が離れすぎると大きな力が生じるため、**低レベル側で目標と実位置の差を制限する**。方策の移動量だけを極端に小さくする方法では自由空間の移動まで遅くなるため、この制限を実時間制御側に置く。[出典：§4.5・Figs. 3–4](../../../raw/temp/luo_2024_serl.pdf)

### 観測と行動の座標系

proprioceptionはepisode開始時の手先座標系を基準に表し、行動は現在の手先座標系に対する6D twistとして出す。開始位置のrandomizationと相対表現を組み合わせ、特定のglobal位置への過適合を避ける設計である。§5では行動を6D end-effector delta poseとも記述している。[出典：§4.6・5・Appendix 7.1](../../../raw/temp/luo_2024_serl.pdf)

## 実験条件と結果

Franka Pandaで、PCB挿入、cable routing、object relocationを評価。画像と手先pose・twist・force・torque等を観測し、ImageNet事前学習済みResNet-10と2層MLPを使う。学習はNvidia RTX 4090 1枚。RLにはSpace Mouseで収集した20本のデモと追加の実機経験、BCには100本の高品質デモを使う。したがって、デモ数だけで両者の全データ量・収集費用が同じとはいえない。[出典：§5](../../../raw/temp/luo_2024_serl.pdf)

| タスク | 学習時間（Table 2） | 報酬 | カメラ（Table 2） | 成功数 RL / BC（各100試行） | cycle time RL / BC |
| --- | ---: | --- | --- | ---: | ---: |
| PCB挿入 | 20分 | Ground Truth | 手首2台 | 100 / 10 | 5.22 / 10.14秒 |
| Cable routing | 31分 | Binary Classifier | 手首2台 | 100 / 19 | 4.08 / 13.58秒 |
| Object relocation | 105分（forward/backward合計） | Binary Classifier | 手首1台・側方1台 | 100 / 58 | 7.53 / 18.94秒 |

出典：[§5・Table 2・Figs. 6–7](../../../raw/temp/luo_2024_serl.pdf)。105分は2方策を学ぶ合計であり、1方策105分という値ではない。Fig. 6のobject relocationは集約表示で、forward/backwardそれぞれの成功数を個別には示していない。

PCBとcableではepisode開始時の手先位置を所定領域内で一様にrandomizeする。object relocationでは各bin中央上へ戻す。論文は学習実時間に計算・リセット・意図した停止を含むと記すが、デモ収集や初期セットアップも含めた総作業時間とは区別する。[出典：§5・Table 2](../../../raw/temp/luo_2024_serl.pdf)

別拠点での再現例として、University of Washingtonのpeg insertionでは、初期デモ20本、準備3時間未満、学習19分、成功100/100を報告している。これは同論文内の再現報告である。[出典：§5 Reproducibility・Fig. 8](../../../raw/temp/luo_2024_serl.pdf)

## 数値・比較を読む際の注意

- §5本文はPCBとcableが「30分未満」と記すが、Table 2のcableは31分。本ページは具体的なタスク別の表を採用した。
- Fig. 7 captionは全タスクでBCより「少なくとも2倍」速いとするが、PCBの図中値は $10.14/5.22\approx1.94$ 倍。正確には約1.94倍として読む。
- §5冒頭は手首カメラ2台と説明するが、Table 2のobject relocationは手首1台・側方1台。本ページはタスク別の表を採用した。

以上は取り込んだv4内の記述差であり、別の版や実装によって補完したものではない。[出典：§5・Table 2・Fig. 7](../../../raw/temp/luo_2024_serl.pdf)

Table 1の既存研究との比較は、類似した挿入タスクについて他論文の報告値を並べたもの。装置・タスク・報酬等が統一された直接比較ではなく、著者らも比較の難しさを認める。100/100の成功は当該条件での評価であり、未知の物体・環境での普遍的な成功保証ではない。[出典：§5・Table 1・6](../../../raw/temp/luo_2024_serl.pdf)

## 限界と関連知識

著者らは、全RL手法や非manipulationタスクを網羅するlibraryではないこと、classifier報酬とforward/backwardリセットが全設定に適するとは限らないことを挙げる。部品の統合による有効性は示すが、主実験は各部品の寄与をすべて独立に切り分けるablationではない。[出典：§4–6](../../../raw/temp/luo_2024_serl.pdf)

本論文のbatch構成はprior/onlineの混合であり、グラフベースの近傍検索によるデモ選択を評価したものではない。SERLの実験結果を、そのような検索手法の有効性の根拠として扱わない。[出典：§4.1・5](../../../raw/temp/luo_2024_serl.pdf)

- [デモを併用する実機RL：SERLの学習とデータの流れ](../../concepts/reinforcement_learning/demonstration_augmented_robot_rl.md)
- [模倣学習と強化学習の基本](../../concepts/imitation_learning/imitation_and_reinforcement_learning.md)
- [ロボットアームの模倣学習：基礎資料と読む観点](../../concepts/imitation_learning/robot_arm_imitation_learning_reading_guide.md)
