---
title: "検索による模倣学習データ選択：既存研究調査"
type: concept
tags: [imitation-learning, data-selection, retrieval, ACT, ANNS]
sources:
  - ../../raw/temp/nasiriany_2023_sailor.pdf
  - ../../raw/temp/du_2023_behavior_retrieval.html
  - ../../raw/temp/lin_2024_flowretrieval.html
  - ../../raw/temp/dass_datamil_project.html
  - ../../raw/temp/hejna_remix_proceedings.html
  - ../../raw/temp/pari_vinn_abstract.html
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-31
---

# 検索による模倣学習データ選択：既存研究調査

2026-10-17に確認した資料に基づく整理に、2026-10-31のSAILOR原論文ingestを追加。Behavior RetrievalとFlowRetrievalは保存全文、DataMILは著者ページ、ReMixは出版ページ、VINNはabstractが確認範囲であり、網羅的なサーベイではない。出版情報や実装の最新性は再確認していない。

| 研究 | 確認できた内容 | 参照先 |
| --- | --- | --- |
| SAILOR（CoRL 2022） | 部分軌跡のVAE skill表現と時間差予測を学習し、対象集合への最小L2距離で既存候補の上位割合を取得。観測履歴からskillを予測するLSTM方策を学ぶ。 | [保存PDF §4・Appendix C](../../raw/temp/nasiriany_2023_sailor.pdf)、[個別要約](../sources/nasiriany_2023_sailor.md) |
| Behavior Retrieval（2023） | 少数の対象デモを使って既存データから関連する状態・行動を選び、両者を共同学習する。状態・行動のVAE表現とL2距離を利用。方策はLSTM–GMM。 | [保存全文](../../raw/temp/du_2023_behavior_retrieval.html)、[原文 §III・付録A](https://arxiv.org/html/2304.08742v2) |
| FlowRetrieval（2024） | Optical flowをVAEで表現して関連区間を選び、flow予測の補助損失を加えて学習する。実験の方策はDiffusion Policy。 | [保存全文](../../raw/temp/lin_2024_flowretrieval.html)、[原文 §4](https://arxiv.org/html/2408.16944v1) |
| DataMIL（preprint 2025／ICLR 2026） | 類似性だけでなく方策への影響を推定して選択。対象デモのvalidation lossを代理指標にし、trajectory/sub-trajectory単位のclusteringを使う。 | [保存著者ページ](../../raw/temp/dass_datamil_project.html)、[著者ページ](https://robin-lab.cs.utexas.edu/datamodels4imitation/)、[論文](https://arxiv.org/abs/2505.09603)、[出版情報](https://proceedings.iclr.cc/paper_files/paper/2026/hash/033d9e8dbbbc0ad90e59222cf1db0fc2-Abstract-Conference.html) |
| ReMix（CoRL第8回／PMLR 2025） | 事前学習のデータdomainの重みをDROにより調整する。BridgeとOpenXで評価。 | [保存出版ページ](../../raw/temp/hejna_remix_proceedings.html)、[出版ページ](https://proceedings.mlr.press/v270/hejna25a.html) |
| VINN（preprint 2021） | 表現学習と行動の対応付けを分離し、Locally Weighted Regressionで行動を予測する。学習前の追加データ選択とは用途が異なる。 | [保存abstract](../../raw/temp/pari_vinn_abstract.html)、[原文](https://arxiv.org/abs/2112.01511) |

## 方式を比較するときの注意

- Behavior Retrievalの実装はpriorとtargetの埋め込み間のバッチL2距離を計算する。検索条件は正規化した類似度の閾値であり、単純なクエリごとのtop-Kではない。[出典：§III-D、付録A-G](../../raw/temp/du_2023_behavior_retrieval.html)
- FlowRetrievalはpriorの各候補からtarget集合への最小L2距離で採点し、prior全体の上位割合を選ぶ。状態から将来フレームまでの間隔は行動予測長に対応する。時間区間を扱うこと自体は既に実施されている。[出典：§4.1–4.2、式(3)–(5)](../../raw/temp/lin_2024_flowretrieval.html)
- 両手法はtargetとretrievedの両データを共同学習する。FlowRetrievalはbatch内で同量をサンプルするため、単純な全データ結合とは学習時の比率が異なり得る。[出典：Behavior Retrieval Algorithm 1](../../raw/temp/du_2023_behavior_retrieval.html)、[FlowRetrieval §4.3](../../raw/temp/lin_2024_flowretrieval.html)
- KS₂はHNSWのroutingに組み込む候補選別法であり、ロボットの学習に有益な距離を定義する手法ではない。保存論文の実験は静的ベクトル検索である。[出典：§6–7](../../raw/papers/kernel_function_for_angle_testing.pdf)

読む順序の提案：Behavior Retrieval §III → FlowRetrieval §4 → DataMIL全文 → KS §6–7。これは調査上の提案であり、ユーザーが採用した研究計画ではない。

## 関連ページ

- [検索による模倣学習データ選択](retrieval_based_imitation_data_selection.md)
- [Behavior Retrievalの要約](../sources/du_2023_behavior_retrieval.md)

- [Diffusion Policy：ノイズから行動列を生成するBC](diffusion_policy.md)
