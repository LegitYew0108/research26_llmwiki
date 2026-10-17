---
title: 目次
type: index
tags: [index]
sources:
  - raw/papers/2304.08742v2.pdf
  - raw/papers/2508.01131v2.pdf
  - raw/papers/2401.17698v1.pdf
  - raw/papers/2507.03285v3.pdf
  - raw/papers/kernel_function_for_angle_testing.pdf
  - raw/papers/zhao_2023_act.pdf
  - raw/papers/sohn_2015_cvae.pdf
  - raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf
updated: 2026-10-18
---

# 目次

## 一次資料

- [論文・記事](raw/papers/)
- [調査資料の一時保管](raw/temp/)
- [ミーティング記録](raw/meeting/)

### Research候補と取り込み状況

- [FAISS公式資料：検索の基本とHNSW（2026-10-17）](raw/temp/research_faiss_20261017.md) — index一覧・距離・入門の公式HTML3件を一時保存。未ingest。

- [検索による模倣学習データ選択：既存研究調査（2026-10-17）](raw/temp/research_retrieval_imitation_20261017.md) — Behavior Retrieval、FlowRetrieval、DataMIL、ReMix、VINN。一次資料5件を一時保存。Behavior Retrievalはraw/papersに配置されたv2を取り込み済み、残る4件は未ingest。

- [ACTのためのCVAE：資料と学習ガイド](raw/temp/research_cvae_for_act_20261008.md) — CVAE原論文PDFを取得。条件付き生成・学習と実行の違い・ACTとの対応を説明。CVAE論文は取り込み済み。

- VAEの参照論文（個別ingestは未実施）：[Auto-Encoding Variational Bayes](raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)、[An Introduction to Variational Autoencoders（v3）](raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)。[概念の説明記事](wiki/concepts/variational_autoencoder.md)から原文にもリンク。

- [ロボットの模倣学習・強化学習：12本の候補と読む順番](raw/temp/research_robot_imitation_reinforcement_learning_20261003.md) — サーベイ、DAgger、ACT、Diffusion Policy、SAC、四足歩行、Offline RL、RLPD、SERL、HIL-SERL。ACTは取り込み済み（下記）。残りは未ingest。各PDFへのリンクは候補一覧に記載。

### Web記事の参照記録

- [MIT：Imitation Learning](raw/web/web_mit_imitation_learning_20261003.md)
- [Hugging Face：RL Framework](raw/web/web_huggingface_rl_framework_20261003.md)
- [Spinning Up：Kinds of RL Algorithms](raw/web/web_spinningup_rl_algorithms_20261003.md)

## Wiki

- [論文ごとの要約](wiki/sources/)
- [概念・手法](wiki/concepts/)
- [研究者・研究室・データセット](wiki/entities/)

## 研究活動

- [研究概要発表：Marpスライド案（2026-10-16）](lab/presentation/research_overview_20261016.md) — 30分・21枚。検索表現は空欄、追加の実験設計案は未採用として記載。

- [自分の理解・考察](mind/)
- [研究方針・実験記録](lab/)
- [依頼して保存した研究提案](lab/proposals/)

### 自分の理解・考察の記事

- [Behavior Cloning](<mind/IL/BC-Behavior Cloning.md>)
- [Imitation Learning](<mind/IL/IL-Imitation Learning(模倣学習).md>)
- [ACT論文の読書ノート](<mind/paper/Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware.md>)
- [Attention（ざっくり）](<mind/Transformer/Attention(ざっくり).md>)
- [VLAについての疑問](mind/Questionnaire/VLA.md)
- [マニピュレーションについての疑問](mind/Questionnaire/マニピュレーションって？.md)

### 研究方針・計画の記事

以下はユーザーの記録。日付の異なる計画や案は、最新の採用方針と同一とは限らない。

- [1008計画](lab/research_policy/1008計画.md)
- [1013計画](lab/research_policy/1013計画.md)
- [スライド計画](lab/research_policy/スライド計画.md)
- [検索拡張型ACTの研究計画（案）](lab/meeting/research_plan_retrieval_augmented_ACT.md)

## 進捗記録

- [日次ログ](log/daily/)
- [週次ログ](log/weekly/)
- [2026-10-17 Wiki Lint結果](log/lint/lint_20261017.md)

## 取り込み済みの論文

- [Behavior Retrieval：少数デモによる既存データ検索とBC](wiki/sources/du_2023_behavior_retrieval.md) — [一次資料（v2）](raw/papers/2304.08742v2.pdf)

- [COLLAGE：Adaptive Fusion-based Retrieval for Augmented Policy Learning](wiki/sources/kumar_2025_collage.md) — [一次資料（v2）](raw/papers/2508.01131v2.pdf)

- [Bi-ACT：Bilateral ControlとACTの統合](wiki/sources/buamanee_2024_biact.md) — [一次資料](raw/papers/2401.17698v1.pdf)

- [Memory Mosaics at scale（モデルv2／arXiv v3）](wiki/sources/zhang_2025_memory_mosaics_at_scale.md) — [一次資料](raw/papers/2507.03285v3.pdf)

- [Learning Structured Output Representation using Deep Conditional Generative Models（CVAE）](wiki/sources/sohn_2015_cvae.md) — [一次資料](raw/papers/sohn_2015_cvae.pdf)

- [ALVINN: An Autonomous Land Vehicle in a Neural Network（NIPS 1988）](wiki/sources/pomerleau_1988_alvinn.md) — [一次資料](raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

- [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware（ACT）](wiki/sources/zhao_2023_act.md) — [一次資料](raw/papers/zhao_2023_act.pdf)

- [Probabilistic Kernel Function for Fast Angle Testing](wiki/sources/kernel_function_for_angle_testing.md) — [一次資料](raw/papers/kernel_function_for_angle_testing.pdf)

## 概念・手法のページ

- [Behavior RetrievalのVAE：基礎から検索手順まで](wiki/concepts/behavior_retrieval_vae_search.md)

- [検索による模倣学習データ選択](wiki/concepts/retrieval_based_imitation_data_selection.md)

- [Retrieval-augmented Imitation Learning：検索による学習データ拡張](wiki/concepts/retrieval_augmented_imitation_learning.md)
- [Subsequence DTW：部分軌跡の時間対応を取る検索](wiki/concepts/subsequence_dynamic_time_warping.md)

- [ACTのinfer z：学習時に正解行動列を使う理由](wiki/concepts/act_infer_z.md)

- [Bilateral Controlに基づく模倣学習](wiki/concepts/bilateral_control_based_imitation_learning.md)

- [Associative MemoryとKernel Regression](wiki/concepts/associative_memory_and_kernel_regression.md)

- [CVAE：条件付き生成とACTでの使い方](wiki/concepts/conditional_variational_autoencoder.md)

- [Behavior Cloning：学習方法と分布シフト](wiki/concepts/behavior_cloning.md)

- [VAE（Variational Autoencoder）：仕組みと学習の目的](wiki/concepts/variational_autoencoder.md)

- [Action ChunkingとTemporal Ensembling](wiki/concepts/action_chunking_and_temporal_ensembling.md)

- [ロボットの模倣学習と強化学習：基本的な仕組みと違い](wiki/concepts/imitation_and_reinforcement_learning.md)
- [角度判定と参照角度](wiki/concepts/angle_testing.md)
- [参照角度によるKS₁・KS₂の確率解析](wiki/concepts/reference_angle_probability.md)
- [KSの射影配置と部分空間分割](wiki/concepts/projection_configuration_ks.md)
- [確率的ルーティングとKS₂テスト](wiki/concepts/probabilistic_routing_ks2.md)

## 日次ログ一覧

- [2026-10-18](log/daily/daily_20261018.md)

- [2026-10-17](log/daily/daily_20261017.md)

- [2026-10-16](log/daily/daily_20261016.md)

- [2026-10-09](log/daily/daily_20261009.md)

- [2026-10-08](log/daily/daily_20261008.md)

- [2026-10-05](log/daily/daily_20261005.md)

- [2026-09-29](log/daily/daily_20260929.md)
- [2026-10-01](log/daily/daily_20261001.md)
- [2026-10-03](log/daily/daily_20261003.md)
