---
title: "Retrieval-augmented Imitation Learning：検索による学習データ拡張"
type: concept
tags: [robotics, imitation-learning, retrieval, behavior-cloning, data-selection]
sources:
  - ../../../raw/papers/2508.01131v2.pdf
updated: 2026-10-31
---

# Retrieval-augmented Imitation Learning：検索による学習データ拡張

## 何を検索し、いつ使うのか

少数の対象タスクデモを、大規模な既存デモから検索したデータで補い、Behavior Cloningの学習データを増やす方法。COLLAGEでは検索結果を使って最終方策を訓練する。実行時の観測に応じて検索した行動を直接再生するzero-shot retrievalとは設定が異なる。[出典：§2–3](../../../raw/papers/2508.01131v2.pdf)

## 類似度と学習への有用性

外観・動作・形状・指示文はそれぞれ異なる共通性を捉える。外観が似ても目的が異なる、動きが似ても意味が異なるデモを追加するとnegative transferにつながりうる。特徴の類似度だけで学習への有用性を保証することはできない。[出典：§1、Fig. 1](../../../raw/papers/2508.01131v2.pdf)

[COLLAGE](../../sources/retrieval/kumar_2025_collage.md)は、各特徴で検索した集合のみから参照方策を学習し、対象デモ上の行動log-likelihoodを測る。そのスコアをsoftmaxで重みにし、対象デモと検索集合を合わせたデータからのサンプリング比率を調整する。検索時の特徴距離と、検索後の集合の有用性の代理指標を分けている。重み推定には環境rolloutは不要である。[出典：§3.1–3.3](../../../raw/papers/2508.01131v2.pdf)

## 比較時に確認すること

検索単位（状態・部分軌跡・デモ全体）、特徴、取得量、対象デモ数、最終方策の構成を確認する。COLLAGEでは視覚・動作・形状は[Subsequence DTW](subsequence_dynamic_time_warping.md)による部分軌跡検索、言語はデモ単位検索で、特徴以外にも実装差がある。[出典：§3–4、Appendix A.1](../../../raw/papers/2508.01131v2.pdf)

本ページはCOLLAGEに基づく整理で、先行研究を個別に検証したサーベイではない。報酬最大化ではなく、デモ行動を教師信号とする[Behavior Cloning](../imitation_learning/behavior_cloning.md)のデータ選択として位置付ける。[出典：§2–3](../../../raw/papers/2508.01131v2.pdf)
