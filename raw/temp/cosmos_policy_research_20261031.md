---
title: "Cosmos Policy：一次情報の調査記録"
type: research
tags: [research, Cosmos-Policy, world-model, imitation-learning, planning]
sources:
  - kim_2026_cosmos_policy.pdf
  - nvidia_cosmos_policy_project_20261031.html
updated: 2026-10-31
---

# Cosmos Policy：一次情報の調査記録

Researchとして候補資料を保存。Wikiへのingestは未実施。

## 論文

**Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning** — Moo Jin Kimほか、NVIDIA・Stanford、ICLR 2026。

- [arXiv書誌ページ](https://arxiv.org/abs/2601.16163)：初回公開2026-01-22。
- [保存PDF（arXiv v1、22ページ）](kim_2026_cosmos_policy.pdf)
- [ICLR版PDF](https://openreview.net/pdf?id=wPEIStHxYH)

Cosmos-Predict2をロボットのデモで単一段階のpost-trainingにより適応する。行動・未来状態・価値をlatent framesとして扱い、動画モデルのアーキテクチャを変更せず、方策・world model・value functionを統合する。直接の行動生成に加え、候補の未来状態と価値を用いたmodel-based planningを行う。[出典：論文Abstract・Fig. 1](kim_2026_cosmos_policy.pdf)

論文報告の平均成功率はLIBERO 98.5%、RoboCasa 67.1%。実機ではALOHAの双腕操作を評価している。これらは当該論文の評価条件での結果であり、現時点の全手法に対する順位を示すものではない。[出典：論文Abstract](kim_2026_cosmos_policy.pdf)、[公式ページ保存版](nvidia_cosmos_policy_project_20261031.html)

## 開発者による一次情報

1. [NVIDIA公式プロジェクトページ](https://research.nvidia.com/labs/cosmos-lab/cosmos-policy/) — 概要、評価表、LIBERO・RoboCasa・ALOHAの実行動画。旧URL `labs/dir/cosmos-policy/` はこちらへ移転。[保存HTML](nvidia_cosmos_policy_project_20261031.html)。ページはJavaScriptで内容を読み込むため、保存HTMLだけでは全文を閲覧できない場合がある。
2. [公式実装：NVlabs/cosmos-policy](https://github.com/NVlabs/cosmos-policy) — セットアップ、学習・評価、GPU要件、モデル・データへの入口。
3. [NVIDIA執筆の紹介記事](https://huggingface.co/blog/nvidia/cosmos-policy-for-robot-control) — 2026-01-29公開。行動・未来観測・価値の統合と、直接実行／planningの違いを説明。
4. [公式Cosmos Cookbook](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/post_training/predict2/cosmos_policy/post_training.html) — latent frame injection、学習目的、学習設定の実装寄りの解説。

読む順の提案：公式紹介記事 → 論文 → GitHub／Cookbook。これは理解の進め方についての提案であり、研究方針の決定ではない。
