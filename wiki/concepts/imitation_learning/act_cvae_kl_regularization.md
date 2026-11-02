---
title: "ACTのCVAE：KL項と正解情報への依存"
type: concept
tags: [ACT, CVAE, KL-divergence, regularization, latent-variable]
sources:
  - ../../../raw/papers/zhao_2023_act.pdf
  - ../../../raw/papers/sohn_2015_cvae.pdf
updated: 2026-10-31
---

# ACTのCVAE：KL項と正解情報への依存

## 「過度な正解データの混入を防ぐ」という理解

「正解行動列の情報を潜在変数zに詰め込みすぎ、方策がそれに依存することを抑える」という意味なら、おおむね正しい。ただし正解データそのものを除去したり、encoderへの入力を遮断したりする仕組みではない。学習時に正解行動列をencoderへ与えることはCVAEの設計である。[出典：ACT §IV-B–C・Algorithm 1](../../../raw/papers/zhao_2023_act.pdf)、[CVAE §4](../../../raw/papers/sohn_2015_cvae.pdf)

## どこに制約をかけるか

現在の関節位置をs、正解行動列をAとすると、ACTの損失は次の構成になる。[出典：ACT §IV-B・Algorithm 1](../../../raw/papers/zhao_2023_act.pdf)

$$\mathcal L=\mathcal L_{\mathrm{reconst}}+\beta D_{\mathrm{KL}}\bigl(q_\phi(z\mid s,A)\Vert\mathcal N(0,I)\bigr).$$

- 再構成損失は、画像・関節位置・zから正解行動列を再現するよう促す。
- KL項は、各学習例から推定した潜在分布を、共通の標準正規事前分布へ近づける。ACT論文も、βを大きくするとzを通じて伝わる情報が少なくなると説明している。

以上の出典：[ACT §IV-B–C](../../../raw/papers/zhao_2023_act.pdf)。以下はこの目的関数からの解釈：KL制約が弱いと、正解ごとに区別しやすいzを作り、観測を十分に使わずに正解を復元する近道が生じ得る。KL項はその近道を使いにくくする。ただし、KL項がなければ必ずこの問題が起きるという主張ではない。

## 実行時との関係と限界

ACTの実行時には正解行動列がなく、CVAE encoderを使わずz=0を方策に与える。そのため、正解から得たzへの過度な依存は学習時と実行時の隔たりになり得る。KL項は事前分布との隔たりを抑えるが、z=0での予測精度を直接保証する項ではない。[手順の出典：ACT §IV-B・Algorithm 2](../../../raw/papers/zhao_2023_act.pdf)、[学習と生成の分布の違い：CVAE §4.2](../../../raw/papers/sohn_2015_cvae.pdf)。保証についての注意は目的関数と実行手順からの解釈である。

また、完全に情報を消すことが目的ではない。仮にすべての学習例で潜在分布が厳密にN(0,I)なら、zの分布は正解行動列によらなくなる。これはKL=0の場合の数学的帰結であり、実際の学習で必ずそうなるという主張ではない。再構成と正則化の両方を考える必要がある。[目的関数の出典：ACT §IV-B・Algorithm 1](../../../raw/papers/zhao_2023_act.pdf)

## 関連

- [ACTのinfer z：学習時に正解行動列を使う理由](act_infer_z.md)
- [CVAE：条件付き生成とACTでの使い方](../generative_models/conditional_variational_autoencoder.md)
