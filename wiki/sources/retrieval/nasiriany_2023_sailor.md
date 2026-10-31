---
title: "SAILOR：Learning and Retrieval from Prior Data for Skill-based Imitation Learning"
type: source
tags: [robotics, imitation-learning, skill-learning, retrieval, VAE, temporal-abstraction]
sources:
  - ../../../raw/papers/nasiriany_2023_sailor.pdf
updated: 2026-10-31
---

# SAILOR：Learning and Retrieval from Prior Data for Skill-based Imitation Learning

## 書誌情報と要点

著者はSoroush Nasiriany、Tian Gao、Ajay Mandlekar、Yuke Zhu。保存PDFの表紙はCoRL 2022と記載する。ファイル名の2023と会議年は区別する。本ページは保存PDFの本文・付録を対象とし、実装は検証していない。[出典：表紙](../../../raw/papers/nasiriany_2023_sailor.pdf)

**SAILOR（Skill-Augmented Imitation Learning with prior Retrieval）は、既存データから短い部分軌跡のskill表現を学び、対象デモに近いskillを検索して、対象タスクの方策学習にも既存データを利用する。** 主な工夫は、skill表現にtemporal predictabilityの補助目的を加えることと、検索による方策学習データの拡張である。SAILOR自体は模倣学習であり、比較対象にoffline RLを含む。[出典：§1・3–4、Fig. 1–2](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 問題設定

大規模な既存軌道集合 $D_{prior}$ と、少数の対象タスクデモ $D_{target}$ を使う。軌道には観測と行動が必要であり、既存データは関連タスクのデモやtask-agnosticなplay dataを想定する。skillは固定長 $H$ の部分軌跡を表す潜在変数で、方策は対象タスクを解くために次のskillを選ぶ。[出典：§3](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 1. Skill表現の事前学習

LSTM encoder $q_\phi(z\mid\tau)$ は部分軌跡 $\tau$ をGaussian分布に変換する。LSTM decoder $p_\psi(a_t\mid z,o_t)$ はskillと各時刻の観測から行動を再構成する。開始・終了観測で条件付けた学習可能なprior $p_\theta(z\mid o_0,o_H)$ を使い、次の損失を最小化する。実装上の再構成は決定論的decoderによるL2損失と記されている。[出典：§4.1、式(1)、脚注1](../../../raw/papers/nasiriany_2023_sailor.pdf)

$$
\mathcal L_{VAE}=-\mathbb E_{q_\phi}\left[\sum_{t=0}^{H-1}\log p_\psi(a_t\mid z,o_t)\right]
+\beta D_{KL}\left(q_\phi(z\mid\tau)\Vert p_\theta(z\mid o_0,o_H)\right).
$$

同じ軌道内の2部分軌跡の潜在平均を $\mu_1,\mu_2$、時間差を $d$ として、$\mathcal L_{TP}=(m_\omega(\mu_1,\mu_2)-d)^2$ を加える。全体は $\mathcal L_{Skill}=\mathcal L_{VAE}+\alpha\mathcal L_{TP}$。Algorithm 1では時間offsetを $[-50,50]$ からサンプリングする。これは潜在表現から時間差を予測する目的であり、将来画像を生成する損失ではない。[出典：§4.1、式(2)–(3)、Algorithm 1](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 2. 部分軌跡の検索

既存データから $N$ 個、対象デモから $M$ 個の部分軌跡をランダムに採り、encoderの分布の平均 $z_i^{prior},z_j^{target}$ を計算する。各既存候補について

$$s_i=\min_{j=1,\ldots,M}\|z_i^{prior}-z_j^{target}\|_2$$

を求め、$s_i$ が小さい順に全候補から $n$ 個を選ぶ。**クエリごとにtop-Kを選んで結合する手順ではなく、各候補の対象集合への最小距離で全体を順位付けする。** 取得するのはskill埋め込みと、その直前の観測履歴である。[出典：§4.2、式(4)、Algorithm 2](../../../raw/papers/nasiriany_2023_sailor.pdf)

標準設定はskill長 $H=10$、潜在次元64、観測履歴 $F=10$。候補数の上限はsimulationで $N=250{,}000$、実機で $300{,}000$、対象側は $M=2{,}500$。候補のうちsimulationでは10%、実機では5%を取得する。これらはランダムに採った候補集合に対する割合である。[出典：Appendix A.4・D、Table 7](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 3. 方策学習と実行

LSTM方策は直前の観測履歴からskill平均を回帰する。対象と検索データの損失を $\mathcal L_{Policy}=\mathbb E_{D_{target}}\|\pi(o_{fs},0)-z\|^2+\gamma\mathbb E_{D_{ret}}\|\pi(o_{fs},1)-z\|^2$ として学習する。dataset IDで両者を区別し、実行時はID=0を使う。$\gamma$ はsimulationで1、実機で0.15。skill modelも同時にfine-tuningする。[出典：Appendix C.1–C.3、Algorithm 2、Table 7](../../../raw/papers/nasiriany_2023_sailor.pdf)

実行時は方策が出したskillを $H$ steps保持し、decoderが各stepの最新観測を受けて行動を出すclosed-loop制御を行い、その後skillを更新する。実行時に既存データを再検索する構成ではない。[出典：§4.2、Appendix C.3](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 実験条件と主要結果

Franka Kitchenでは対象デモ18本、既存デモ584本（Kitchen-All）または235本（microwave操作を除外）。CALVINでは既存play dataが230万transitions、対象2タスクは各30デモ。どちらもvision-based policyを評価する。[出典：§5.1](../../../raw/papers/nasiriany_2023_sailor.pdf)

| 条件 | BC-RNN | BC-RNN (FT) | SAILOR |
| --- | ---: | ---: | ---: |
| Kitchen-All | 32.3 ± 9.0 | 93.0 ± 2.3 | 95.7 ± 1.7 |
| Kitchen-No Microwave | 32.3 ± 9.0 | 77.7 ± 7.6 | 95.0 ± 2.2 |
| CALVIN-Setting Up | 33.0 ± 2.2 | 72.8 ± 5.4 | 77.3 ± 3.1 |
| CALVIN-Cleaning Up | 41.0 ± 1.6 | 61.8 ± 9.1 | 88.0 ± 5.1 |

単位は成功率%。平均±標準偏差で、通常3 seeds、BC-RNN (FT)は分散が大きいため6 seeds。KitchenのBC-RNNはpriorを使わない共通条件。simulationでは各評価checkpointで100 rolloutsを行い、seedごとに最良checkpointの成功率を採用する。[出典：Table 1、Appendix C.3](../../../raw/papers/nasiriany_2023_sailor.pdf)

実機では各タスク30デモを用い、BC-RNN (FT)／SAILORの成功率はBreakfastで76.7／76.7%、Cookで23.3／73.3%、Cook-Panで46.7／76.7%。各手法1 seedで、有望なcheckpointを選んで30 rolloutsを評価するため、simulationと同じ統計条件ではない。[出典：§5.4、Appendix C.3](../../../raw/papers/nasiriany_2023_sailor.pdf)

## Ablation：検索はどの程度役立つか

| CALVINタスク | SAILOR | No TP | No Retrieval | All Retrieval | Random Retrieval |
| --- | ---: | ---: | ---: | ---: | ---: |
| Setting Up | 77.3 ± 3.1 | 68.0 ± 3.7 | 65.0 ± 2.2 | 64.3 ± 10.8 | 82.0 ± 3.7 |
| Cleaning Up | 88.0 ± 5.1 | 74.7 ± 7.9 | 70.0 ± 0.8 | 65.3 ± 7.3 | 55.3 ± 7.3 |

成功率%、平均±標準偏差。No Retrievalはpriorによるskill学習を残し、方策をtargetのみで学習する。All Retrievalはprior全体を使用し、Random Retrievalは標準設定と同じ取得量をランダムに選ぶ。**Cleaning Upでは関連データの選別が有効だが、Setting Upではランダム選択も同程度であり、検索の重要性はタスク・データセットに依存する**というのが付録の結論である。[出典：§5.3、Tables 2・6、Appendix A.4](../../../raw/papers/nasiriany_2023_sailor.pdf)

距離を対称化KL divergenceへ置き換えた比較では、Setting Upが79.3 ± 5.7%、Cleaning Upが80.7 ± 0.9%。著者は標準L2との明確な差を見いだしていない。取得量を増やせば一貫して改善するわけでもなく、Cleaning Upの90%取得は46.3 ± 20.0%となる。[出典：Tables 4・6、Appendix A.2・A.4](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 限界と原文の注意点

- 既存データ収集に費用がかかり、対象タスク数も限られる。BC-RNNよりnetwork・損失が多く計算負荷が高い。priorとtargetが比較的近いdomainでの検証が中心で、未知物体への汎化は評価していない。[出典：§6](../../../raw/papers/nasiriany_2023_sailor.pdf)
- 検索は全候補間のL2距離計算として記述され、HNSWなどのグラフ型ANN索引や検索高速化の効果を検証した論文とは扱わない。[出典：§4.2、Algorithm 2](../../../raw/papers/nasiriany_2023_sailor.pdf)
- Algorithm 2の4行目は距離の両辺がprior、6行目のコメントはtargetのindexと記されるが、本文§4.2と後続処理に沿い、本ページではprior–target間距離とprior側の選択indexとして読んだ（原文の不整合に対する解釈）。[出典：§4.2、Algorithm 2](../../../raw/papers/nasiriany_2023_sailor.pdf)
- skillのfine-tuningは本文§4.2ではtarget、付録C.2・Algorithm 2ではpriorとtargetと記される。本ページの手順は付録に従う。またNo Prior DataのSetting Up成功率はTable 2で50.7 ± 6.5%、Table 3で53.3 ± 4.0%と異なり、同一値に統合しない。[出典：§4.2、Tables 2–3、Appendix C.2、Algorithm 2](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 関連ページ

- [Skill-based Imitation Learning：skill表現と階層方策](../../concepts/imitation_learning/skill_based_imitation_learning.md)
- [Behavior Retrieval](du_2023_behavior_retrieval.md)
- [検索による模倣学習データ選択](../../concepts/retrieval/retrieval_based_imitation_data_selection.md)
- [VAE](../../concepts/generative_models/variational_autoencoder.md)
- [ACT](../imitation_learning/zhao_2023_act.md)
