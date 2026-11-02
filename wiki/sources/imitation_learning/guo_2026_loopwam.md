---
title: "LoopWAM：実行時の成功・失敗から改善するWorld-Action Model"
type: source
tags: [robotics, imitation-learning, LoopWAM, world-action-model, flow-matching, quality-steering, deployment-rollout]
sources:
  - ../../../raw/papers/guo_2026_loopwam.pdf
updated: 2026-10-31
---

# LoopWAM：実行時の成功・失敗から改善するWorld-Action Model

## 書誌情報

Wenxuan Guo, Yingping Liang, Zhaoguo Wangほか（Tsinghua University・Dexmal・Loopeva）、**LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts**。保存版はarXiv:2610.18873v1、25ページ。arXiv表記は2026-10-13、表紙右上は2026-10-14。以下の節・図表番号は保存版に従う。[原論文・表紙](../../../raw/papers/guo_2026_loopwam.pdf)

## 何を解決するか

実行時のrolloutには成功、不完全な動作、失敗が混在する。すべての行動を模倣すると望ましくない動作も学び、成功だけを残すと失敗時の物理的相互作用を捨ててしまう。LoopWAMは、**行動の模倣に使う度合いを品質で調整し、未来観測の学習にはすべての品質を使う**。自分自身と他方策のrolloutを利用できる。[§1・§3](../../../raw/papers/guo_2026_loopwam.pdf)

## モデル：未来動画と行動列を同時生成する

現在画像$o_t$、ロボット状態$s_t$、言語指示$\ell$、軌跡品質$q$を条件として、action chunk $A_t$と未来動画latent $Z_t$の同時分布$p_\theta(A_t,Z_t\mid o_t,s_t,\ell,q)$を学ぶ。動画側はWan2.2-TI2V-5Bで初期化し、行動側はhidden dimension 1024のDiTを使う。二つのstreamは別のパラメータ・headを持ち、各層のjoint attentionで情報交換する。[§3.1・§4.1](../../../raw/papers/guo_2026_loopwam.pdf)

観測tokenは初期フレーム内だけを参照し、未来動画tokenと行動tokenは観測・未来動画・行動を参照する。動画・行動の双方が品質付き言語指示へcross-attentionし、ロボット状態は行動側を条件付ける。未来表現が行動生成に参加する構造だが、別のworld modelで複数候補を採点する段階は設けない。[§3.1・§3.3・Fig.2](../../../raw/papers/guo_2026_loopwam.pdf)

## 混在する品質を学ぶ三つの仕組み

### 1. データの出所によってnoise分布を変える

flow matchingでは$X_m^{\sigma_m}=(1-\sigma_m)X_m+\sigma_m\epsilon_m$とし、$\epsilon_m-X_m$を予測する。$m=v,a$は動画と行動、noise 0はclean、1は純noise。動画と行動のnoise levelは独立にサンプルする。[§3.1・式(2)](../../../raw/papers/guo_2026_loopwam.pdf)

| データの出所 | 動画noise | 行動noise | 意図 |
| --- | --- | --- | --- |
| expert demonstration | Beta(7,1) | 基本分布$P_0$ | 強く壊した未来動画の復元と行動生成 |
| rollout | 基本分布$P_0$ | Beta(1,7) | 記録行動を低noiseで残し、その結果の動画を予測 |

$P_0$は$u\sim U(0,1)$を$5u/(1+4u)$へ変換した分布。rolloutの行動を常に完全なclean条件に固定する方式ではない。出所によるnoise選択と、品質による模倣強度の調整は別の操作である。[§3.2・式(4)・Appendix A.2](../../../raw/papers/guo_2026_loopwam.pdf)

### 2. 品質を言語指示へ加える（quality steering）

指示に `Quality: q` を付ける。品質は軌跡全体へ与え、そのすべての学習segmentが同じ値を継承する。実機ではrolloutを1–10、失敗を1、expertを12とするepisode-level annotationを使う。シミュレーションでは方策全体の成功率と約0.7%の軌跡の手動確認から、成功rolloutに方策別の共有値2–4、失敗に1、expertに5を割り当てるcoarse-level annotationを使う。各成功軌跡の品質を個別推定する方式とは区別する。[§3.2・Appendix A.1](../../../raw/papers/guo_2026_loopwam.pdf)

推論時はexpert品質$q^\star$を指定する。品質ラベルは条件と損失の重み付けに利用され、保存版の更新手順はflow matchingによる教師あり学習として記述される。品質を使うことだけからactor-criticやTD学習と同一視しない。[§3.1–3.3・式(2)–(7)](../../../raw/papers/guo_2026_loopwam.pdf)

### 3. 動画lossは残し、行動lossを品質で重み付けする

動画lossは全品質について学習する。行動lossには単調非減少の$\lambda(q)\in[0,1]$を掛け、expertでは1、失敗では0とする。minibatch内での目的は次式。[§3.2・式(5)–(6)](../../../raw/papers/guo_2026_loopwam.pdf#page=6)

$$
\mathcal L=\frac1B\sum_{i=1}^{B}\ell_{v,i}
+\frac{\sum_{i=1}^{B}\lambda(q_i)\ell_{a,i}}
{\max(1,\sum_{i=1}^{B}\lambda(q_i))}.
$$

失敗では行動の直接の教師lossを除くが、記録行動自体を入力から捨てるわけではない。joint attentionを通じた動画lossの勾配は行動生成に用いる表現にも伝わる。初期観測latentとpaddingは予測lossの対象外。中間品質の$\lambda$について、本文は一般的な条件を定めるが、具体的な対応表は示していない。[§3.2・Appendix A](../../../raw/papers/guo_2026_loopwam.pdf)

## 実行と再学習

expertのみで学習した方策を実行し、rolloutを採点し、元のexpertと累積rolloutで更新して再実行する。推論では観測latentを固定し、動画と行動をGaussian noiseから並列にdenoiseして行動を利用する。これはデータ収集と再学習のループであり、各制御stepでオンラインに重みを更新するという記述ではない。[§3.3](../../../raw/papers/guo_2026_loopwam.pdf)

学習segmentは64-stepの行動列と、8 control stepsごとのRGB画像9枚（初期観測込み）。複数カメラを1画像へ連結し、expert統計で状態・行動を正規化する。Table30-V2では関節targetはchunk開始時の状態に対する相対値、gripperは絶対値。4タスクではQwen2.5-VL-7Bによるsubtask segmentationを使い、オンライン実行中に段階別指示を切り替える。[§4.1・Appendix A.2–A.4・Table 5](../../../raw/papers/guo_2026_loopwam.pdf)

## 実験条件と結果

| 評価 | 条件 | 主な結果 |
| --- | --- | --- |
| RoboChallenge Table30-V2（実機） | 30タスク、ALOHA・DOS-W1・ARX5・UR5。ロボット種別ごとにmulti-taskモデル。各収集roundは各タスク約100 rollouts | 成功率23.67→28.00→37.67→43.33%。score 36.10→42.63→51.65→56.80 |
| シャツ折り畳み（実機） | DOS-W1のmulti-taskモデルを新規expertで単一タスクへ追加学習後、2回の収集・更新 | 成功率13.20→32.54→55.56%。score 14.44→38.89→67.78 |
| RoboTwin 2.0（simulation） | 50タスク。expert 27,500本と、LoopWAM・X-VLA・π0.5のrollout計22,500本 | clean 94.58%、randomized 94.42%、平均94.50% |
| RoboCasa365（simulation） | 50タスクのHuman300 split。LoopWAMとRLDX-1のrolloutを併用。16 Composite-Unseenタスクを学習から除外 | Atomic-Seen 79.7%、Composite-Seen 50.3%、Composite-Unseen 14.9%、全体49.5% |

出典：[§4.2–4.4・Tables 1–3・Fig.3・Appendix A.1](../../../raw/papers/guo_2026_loopwam.pdf)。Table30-V2の改善は丸めて19.7**パーセントポイント**。score 56.80は成功率56.80%という意味ではない。シミュレーションでは収集と評価でrandom seedを分ける。[§4.2–4.4](../../../raw/papers/guo_2026_loopwam.pdf)

## Ablationと結果の読み方

RoboTwin 2.0のTable 4では、steeringなし・rollout行動教師なしで平均72.3%、成功／失敗だけのextra-coarse steeringで92.8%、coarse steeringで92.7%。品質を考慮したrollout行動教師を加えると、それぞれ93.6%、94.5%になる。全行でexpert行動教師と動画教師は維持する。この表が直接比較するのはsteeringとrollout行動教師であり、noise samplingやjoint attentionの独立した効果量ではない。[§4.5・Table 4](../../../raw/papers/guo_2026_loopwam.pdf)

Table30-V2の全体成功率・scoreは掲載比較中で首位だが、ロボット別ではARX5成功率55.71%がVLA-DM0.5の58.57%を下回る。RoboCasa365の未知複合タスクも14.9%で、PRTSの18.8%を下回る。全条件で最良という意味ではない。順位は保存論文の比較とsnapshotに限定し、現在のランキングとは扱わない。[Tables 1・3・Appendix B](../../../raw/papers/guo_2026_loopwam.pdf)

「追加のembodied pretrainingなし」は、動画事前学習もないという意味ではない。Wan2.2で初期化し、さらにexpert以外のrolloutを利用しているため、expertのみの手法とデータ量を揃えた比較ではない。保存版には具体的な学習GPU数・所要時間、固定の推論step数・遅延、評価試行数の詳細な一覧がなく、計算効率や統計的不確実性の比較には情報が不足する。[§4・Appendix A](../../../raw/papers/guo_2026_loopwam.pdf)

グラフベース近傍検索や検索による学習データ選択を検証した研究ではない。本記事では、品質に基づく学習信号の使い分けと、rolloutからの方策改善という実施範囲を整理する。[§3–4](../../../raw/papers/guo_2026_loopwam.pdf)

## 関連ページ

- [Cosmos Policy：動画モデルによる制御とplanning](kim_2026_cosmos_policy.md)
- [Diffusion Policy](chi_2023_diffusion_policy.md)
- [Behavior Cloning](../../concepts/imitation_learning/behavior_cloning.md)
- [Action ChunkingとTemporal Ensembling](../../concepts/imitation_learning/action_chunking_and_temporal_ensembling.md)
- [ロボット方策の評価指標とSOTAの読み方](../../concepts/imitation_learning/robot_policy_evaluation_metrics.md)
