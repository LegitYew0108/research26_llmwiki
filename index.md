---
title: 目次
type: index
tags: [index]
sources:
  - raw/papers/2401.17698v1.pdf
  - raw/papers/2507.03285v3.pdf
  - raw/papers/kernel_function_for_angle_testing.pdf
  - raw/papers/zhao_2023_act.pdf
  - raw/papers/sohn_2015_cvae.pdf
  - raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf
updated: 2026-10-09
---

# 目次

## 一次資料

- [論文・記事](raw/papers/)
- [調査資料の一時保管](raw/temp/)
- [ミーティング記録](raw/meeting/)

### Research候補と取り込み状況

- [ACTのためのCVAE：資料と学習ガイド](raw/temp/research_cvae_for_act_20261008.md) — CVAE原論文PDFを取得。条件付き生成・学習と実行の違い・ACTとの対応を説明。CVAE論文は取り込み済み。

- VAEの参照論文（個別ingestは未実施）：[Auto-Encoding Variational Bayes](raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)、[An Introduction to Variational Autoencoders（v3）](raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)。[概念の説明記事](wiki/concepts/variational_autoencoder.md)から原文にもリンク。

- [ロボットの模倣学習・強化学習：12本の候補と読む順番](raw/temp/research_robot_imitation_reinforcement_learning_20261003.md) — サーベイ、DAgger、ACT、Diffusion Policy、SAC、四足歩行、Offline RL、RLPD、SERL、HIL-SERL。ACTは取り込み済み（下記）。残りは未ingest。各PDFへのリンクは候補一覧に記載。

### Web記事の参照記録

- [MIT：Imitation Learning](web_mit_imitation_learning_20261003.md)
- [Hugging Face：RL Framework](web_huggingface_rl_framework_20261003.md)
- [Spinning Up：Kinds of RL Algorithms](web_spinningup_rl_algorithms_20261003.md)

## Wiki

- [論文ごとの要約](wiki/sources/)
- [概念・手法](wiki/concepts/)
- [研究者・研究室・データセット](wiki/entities/)

## 研究活動

- [自分の理解・考察](mind/)
- [研究方針・実験記録](lab/)
- [依頼して保存した研究提案](lab/proposals/)

## 進捗記録

- [日次ログ](log/daily/)
- [週次ログ](log/weekly/)

## 取り込み済みの論文

- [Bi-ACT：Bilateral ControlとACTの統合](wiki/sources/buamanee_2024_biact.md) — [一次資料](raw/papers/2401.17698v1.pdf)

- [Memory Mosaics at scale（v2）](wiki/sources/zhang_2025_memory_mosaics_at_scale.md) — [一次資料](raw/papers/2507.03285v3.pdf)

- [Learning Structured Output Representation using Deep Conditional Generative Models（CVAE）](wiki/sources/sohn_2015_cvae.md) — [一次資料](raw/papers/sohn_2015_cvae.pdf)

- [ALVINN: An Autonomous Land Vehicle in a Neural Network（NIPS 1988）](wiki/sources/pomerleau_1988_alvinn.md) — [一次資料](raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

- [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware（ACT）](wiki/sources/zhao_2023_act.md) — [一次資料](raw/papers/zhao_2023_act.pdf)

- [Probabilistic Kernel Function for Fast Angle Testing](wiki/sources/kernel_function_for_angle_testing.md) — [一次資料](raw/papers/kernel_function_for_angle_testing.pdf)

## 概念・手法のページ

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

- [2026-10-09](log/daily/daily_20261009.md)

- [2026-10-08](log/daily/daily_20261008.md)

- [2026-10-05](log/daily/daily_20261005.md)

- [2026-09-29](log/daily/daily_20260929.md)
- [2026-10-01](log/daily/daily_20261001.md)
- [2026-10-03](log/daily/daily_20261003.md)
