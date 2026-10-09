---
title: "Bilateral Controlに基づく模倣学習"
type: concept
tags: [robotics, bilateral-control, imitation-learning, force-feedback, torque, Bi-ACT]
sources:
  - ../../raw/papers/2401.17698v1.pdf
updated: 2026-10-09
---

# Bilateral Controlに基づく模倣学習

## 操作する側へ反力を返す

Bilateral Controlは、操作者が動かすleaderと、環境に接触するfollowerとの間で位置・力などを双方向に共有する制御。Bi-ACTで説明するfour-channel bilateral controlでは、leaderとfollowerの関節角度を一致させ、トルクを作用・反作用の関係へ近づけることを目標とする。[出典：§III-B・Fig. 2](../../raw/papers/2401.17698v1.pdf)

$$
\theta_l-\theta_f=0,\qquad \tau_l+\tau_f=0.
$$

これは制御の目標であり、実機で常に誤差ゼロという測定結果ではない。位置追従に加えて環境の反力を操作者へ返すことで、接触を感じながらデモを収集できる。[出典：§III-B・IV-B、式(1)–(2)](../../raw/papers/2401.17698v1.pdf)

## 模倣学習への使い方

1. 人がleaderを操作し、bilateral controlでfollowerに作業を実行させる。
2. leader・followerの関節角度、角速度、トルクと、follower側の画像を記録する。
3. followerの観測からleaderの将来の応答を予測するモデルを学習する。
4. 自律実行時はモデルがleaderの応答を代替し、followerの制御器へ指令を与える。

この手順はBi-ACTの構成に基づく。モデルが予測するのはleaderの応答で、最終的なmotor currentは低レベル制御器が計算する。[出典：§III-B・IV](../../raw/papers/2401.17698v1.pdf)

## forceとtorqueの区別

Bi-ACTの関節情報は5関節それぞれの角度・角速度・トルクで15次元。本文のforceという説明は、ここでは関節トルク情報として具体化される。角度をencoderで測定し、角速度を微分で求め、反力トルクはRFOBで推定する。手先の外力ベクトルや接触圧をそのまま測って入力する構成ではない。[出典：§III-A・IV-C](../../raw/papers/2401.17698v1.pdf)

## 制御周期と方策の更新周期

Bi-ACTは低レベル制御1000Hz、学習データと行動更新100Hzを使う。§IV-Dではchunkを $k$ stepsごとに予測すると記載するので、低レベル制御のfeedbackと、画像を使う方策の再予測のタイミングは区別する。§V-Cの約100Hzというinference cycleの記述との関係には曖昧さがある。[出典：§IV-D・V-A・V-C](../../raw/papers/2401.17698v1.pdf)

力情報を含むことで接触を扱う狙いはあるが、硬さを明示的に推定するモデルや、安定性を保証する学習則が提示されたわけではない。Bi-ACTの物体別成功率と比較の限界は[論文要約](../sources/buamanee_2024_biact.md)を参照。[出典：§IV–V](../../raw/papers/2401.17698v1.pdf)

## 関連ページ

- [Bi-ACT論文要約](../sources/buamanee_2024_biact.md)
- [ACT論文要約](../sources/zhao_2023_act.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
- [Behavior Cloning](behavior_cloning.md)
