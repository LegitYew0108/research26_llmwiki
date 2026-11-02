---
title: "Skill-based Imitation Learning：skill表現と階層方策"
type: concept
tags: [imitation-learning, skill-learning, temporal-abstraction, VAE, retrieval]
sources:
  - ../../../raw/papers/nasiriany_2023_sailor.pdf
updated: 2026-10-31
---

# Skill-based Imitation Learning：skill表現と階層方策

## Skillと方策の役割

Skill-based Imitation Learningでは、短い観測・行動の部分軌跡を潜在変数 $z$ に圧縮し、複数タスクで再利用できる短時間の行動を表す。上位の方策は観測から次のskillを予測し、下位のdecoderはskillと観測から行動を生成する。skillは必ずしも「把持」などの人間のラベルで区切られるものではなく、SAILORでは固定長の部分軌跡から学ぶ。[出典：§3–4](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 表現学習と方策学習を分けて考える

[SAILOR](../../sources/retrieval/nasiriany_2023_sailor.md)では、まず既存データの部分軌跡をVAEで学習する。decoderの行動再構成だけでなく、開始・終了観測に条件付けたpriorへのKL項と、同一軌道内の2部分軌跡間の時間差を予測する補助損失を用いる。後者は、下流の方策が扱いやすいskill表現を学ぶための工夫である。[出典：§4.1、式(1)–(3)](../../../raw/papers/nasiriany_2023_sailor.pdf)

次に対象タスクの観測履歴からskillを回帰する。既存データはskill表現の事前学習に使うだけでなく、対象デモに近い部分軌跡を検索し、上位方策の教師データとしても利用する。したがって「既存データを使う」ときには、表現学習への利用と方策学習への利用を分けて確認する。[出典：§4.2、Table 2、Algorithm 2](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 実行時の時間抽象化

SAILORの標準設定は $H=10$。上位方策は10 stepsごとにskillを更新する一方、decoderは毎stepの最新観測に応じて行動を生成する。skillを一定時間保持しても、10個の行動を観測なしで再生するopen-loop制御を意味しない。[出典：§4.2、Appendix C.3・D](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 検索単位の違い

SAILORが比較するのは部分軌跡のskill平均であり、各既存候補から対象集合への最小L2距離で候補全体を順位付けする。検索結果を使うのは学習時で、実行時は学習済み方策とdecoderで行動する。時間的なまとまりを検索することと、実行時に近傍検索でskillを選ぶことは別の設計事項である。[出典：§4.2、Algorithm 2、Appendix C.3](../../../raw/papers/nasiriany_2023_sailor.pdf)

## 関連ページ

- [SAILOR：手法・実験・限界](../../sources/retrieval/nasiriany_2023_sailor.md)
- [検索による模倣学習データ選択](../retrieval/retrieval_based_imitation_data_selection.md)
- [VAE](../generative_models/variational_autoencoder.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
