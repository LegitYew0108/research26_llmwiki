---
title: "Bi-ACT: Bilateral Control-Based Imitation Learning via Action Chunking with Transformer"
type: source
tags: [robotics, imitation-learning, Bi-ACT, ACT, bilateral-control, force-feedback, action-chunking]
sources:
  - ../../raw/papers/2401.17698v1.pdf
updated: 2026-10-09
---

# Bi-ACT: Bilateral Control-Based Imitation Learning via Action Chunking with Transformer

## 書誌情報と要点

著者はThanpimon Buamanee、Masato Kobayashi、Yuki Uranishi、Haruo Takemura（前2名はequal contribution）。対象はarXiv:2401.17698v1、2024年1月31日。一次資料は[保存したPDF](../../raw/papers/2401.17698v1.pdf)。[出典：表紙](../../raw/papers/2401.17698v1.pdf)

**Bi-ACT**は、[ACT](zhao_2023_act.md)の行動列予測に、[Bilateral Control](../concepts/bilateral_control_based_imitation_learning.md)による位置・力の扱いを組み合わせる模倣学習手法。followerの画像・関節角度・角速度・トルクから、leaderの将来の角度・角速度・トルク列を予測し、低レベル制御器を介してfollowerを動かす。報酬最大化による強化学習の手法ではない。[出典：§I・III–IV](../../raw/papers/2401.17698v1.pdf)

## なぜ力情報を加えるか

位置追従を中心とするALOHA/ACTに対して、Bi-ACTでは操作者へ接触の反力を返すbilateral controlでデモを集める。画像・位置だけでは扱いにくい物体の硬さや重さの違いに対応することが狙いである。ただし、物性を明示的に推定して入力する構成ではなく、関節応答と画像を使って行動列を学習する。[出典：§I・III–IV](../../raw/papers/2401.17698v1.pdf)

## デモ収集と制御

人がleaderを操作し、followerが環境で作業する。目標は関節角度の一致 $\theta_l-\theta_f=0$ と、作用・反作用に対応するトルクの関係 $\tau_l+\tau_f=0$。角度はencoderで取得し、角速度はその微分から計算する。disturbance observer（DOB）を使い、反力トルク応答はreaction force observer（RFOB）で推定する。論文がforceと呼ぶ入力は、関節空間ではtorqueとして扱われており、手先の力センサの直接測定と読み替えない。[出典：§III、式(1)–(2)、Fig. 3](../../raw/papers/2401.17698v1.pdf)

自律実行時は学習モデルがleaderの応答を代替する。モデル出力そのものをmotor currentとして与えるのではなく、予測したleader応答とfollower応答を用いる制御器が必要な電流を決める。[出典：§III-B・IV-D、Fig. 2](../../raw/papers/2401.17698v1.pdf)

## 入出力とAction Chunking

| 項目 | Bi-ACTの構成 |
| --- | --- |
| 画像入力 | followerのgripperとoverheadのRGB画像2枚、各360×640 |
| 関節入力 | followerの5関節×角度・角速度・トルク＝15次元 |
| 出力 | leaderの将来 $k$ stepsの角度・角速度・トルク、$k\times15$ |
| 実機 | OpenMANIPULATOR-X、arm 4 DOF＋gripper 1 DOF |

以上は§IV-C・V-Aに基づく。[出典](../../raw/papers/2401.17698v1.pdf)

ACT由来のCVAEとTransformerを使い、Fig. 4はfollower関節情報・教師行動列から潜在変数 $z$ を得る経路と、画像・関節情報・$z$ から行動列を生成する経路を示す。ただし、このv1は具体的なchunk長 $k$、損失の係数、optimizer、学習時間、推論時の $z$ の扱いなどを詳述していない。ACT原論文の設定をそのままBi-ACTの確定設定として補わない。[出典：§II-B・IV-C、Fig. 4](../../raw/papers/2401.17698v1.pdf)

### 100Hzと1000Hzを区別する

低レベルのロボット制御は1000Hz、カメラは約200Hzで動作し、学習データは100Hzへ揃える。行動の更新は100Hzで、§IV-Dではモデルを **$k$ stepsごと** に実行して次の $k$ stepsを生成すると説明する。この説明に従えば、100Hzの行動列を消費する場合のモデル呼び出し頻度は $100/k$ Hzとなる（記述からの換算）。100Hzで毎回画像からchunkを再予測すると断定しない。[出典：§IV-D・V-A・V-C](../../raw/papers/2401.17698v1.pdf)

一方、§V-Cにはmodel inference cycleが約100Hzとの表現もあり、モデル呼び出し頻度について本文に曖昧さが残る。temporal aggregationは関連研究で説明されるが、Bi-ACT実験での具体的な重みや実行手順は示されない。[Action ChunkingとTemporal Ensembling](../concepts/action_chunking_and_temporal_ensembling.md)で説明するACTの毎時刻再予測を、本論文の実行方式と同一視しない。[出典：§II-B・IV-D・V-C](../../raw/papers/2401.17698v1.pdf)

## データと実験条件

- **Pick-and-Place**：foam ballとsoftballで各25 episodes、合計50 episodes。1本8.4–9.3秒、44,184 time steps以上。評価は学習済み2物体と未学習7物体で、各10試行。指定のplace area外へ落とすと失敗とする。
- **Put-in-Drawer**：50 episodes、1本19.5–22.4秒、97,972 time steps。引き出しを開く→物体を掴む→運ぶ→中へ置く→閉める。評価は5試行。

以上は§V-B–Dに基づく。複数seedによるばらつきや信頼区間は報告されていない。[出典](../../raw/papers/2401.17698v1.pdf)

## 結果

Pick-and-Placeの最終成功率（Table IIのTotal、%）は次の通り。[出典：§V-D・Table II](../../raw/papers/2401.17698v1.pdf)

| 物体 | 学習に使用 | Bi-ACT | w/o Force |
| --- | --- | ---: | ---: |
| Softball | あり | 100 | 80 |
| Foam ball | あり | 100 | 100 |
| Table tennis | なし | 100 | 100 |
| Eye cream | なし | 100 | 50 |
| Canele | なし | 80 | 80 |
| Soccer ball | なし | 90 | 80 |
| Honey bottle | なし | 90 | 90 |
| Plastic bell pepper | なし | 80 | 70 |
| Glue jar | なし | 80 | 50 |

各10試行なので、例えば100%は10/10、80%は8/10である。eye creamは50 percentage points、glue jarは30 points改善する一方、差がない物体もある。これは表の値と試行数からの換算であり、統計的有意差を示すものではない。[出典：§V-D・Table II](../../raw/papers/2401.17698v1.pdf)

Put-in-Drawerでは全段階100%、本文では5試行すべて成功と報告する。Table IIIには提案手法のみが載っており、このタスクで力情報なしより優れるとは比較できない。[出典：§V-D・Table III](../../raw/papers/2401.17698v1.pdf)

## 限界と読み方

比較対象はBi-ACTのw/o Forceであり、元のALOHA/ACTを同じ条件で直接比較した表ではない。また本文は「force controlなし」「force dataなし」という表現を使うが、デモ収集、入出力、低レベル制御のどこを変更したかの詳細は十分でない。したがって、トルク入力だけの効果やbilateral controlだけの効果を独立に測定したとは断定できない。[出典：§V-D・Table II](../../raw/papers/2401.17698v1.pdf)

eye creamやglue jarの液体による重量分布の変化がw/o Forceを難しくしたという説明は、著者の考察であり独立に検証した原因ではない。硬さ・形・重さも物体間で同時に異なる。少数試行・単一ロボット構成での結果を、任意の物体や環境への適応の保証へ一般化しない。[出典：Table I、§V-D・VI](../../raw/papers/2401.17698v1.pdf)

この論文は接触情報を使う模倣学習の研究であり、検索器・グラフベースANN・RL更新を組み込んだ評価は行っていない。照明変化、動的環境、異なるロボットへの一般化は今後の課題として挙げられる。[出典：§IV–VI](../../raw/papers/2401.17698v1.pdf)

## 関連ページ

- [Bilateral Controlに基づく模倣学習](../concepts/bilateral_control_based_imitation_learning.md)
- [ACT原論文](zhao_2023_act.md)
- [Action ChunkingとTemporal Ensembling](../concepts/action_chunking_and_temporal_ensembling.md)
- [CVAE：条件付き生成とACTでの使い方](../concepts/conditional_variational_autoencoder.md)
