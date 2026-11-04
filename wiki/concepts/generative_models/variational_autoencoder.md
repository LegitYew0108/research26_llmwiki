---
title: "VAE（Variational Autoencoder）：仕組みと学習の目的"
type: concept
tags: [VAE, generative-model, latent-variable, ELBO, reparameterization, representation-learning]
sources:
  - ../../../raw/papers/sohn_2015_cvae.pdf
  - ../../../raw/papers/zhao_2023_act.pdf
  - ../../../raw/papers/du_2023_behavior_retrieval.pdf
updated: 2026-10-31
---

# VAE（Variational Autoencoder）

## 何をするモデルか

**VAEは、データを説明する潜在変数の分布を学ぶ生成モデル**である。学習では入力を潜在変数を通して復元し、生成時には事前分布から選んだ潜在変数を使ってデータを作る。「小さなベクトルに圧縮する」だけでなく、確率分布として扱うことが特徴になる。[基礎となる生成過程・学習：CVAE論文 §3](../../../raw/papers/sohn_2015_cvae.pdf)

このページは特定論文の要約ではなく、基本的なVAEの理解を目的とする。生成過程、学習目的、サンプリングの説明は、取り込み済みのCVAE論文の基礎節に基づく。以下の例や図は理解のための説明であり、特定の学習結果ではない。[基礎の出典：§3・式(1)–(3)](../../../raw/papers/sohn_2015_cvae.pdf)

## EncoderとDecoderの役割

入力データを$x$、潜在変数を$z$とする。例えば「入力画像の特徴を少数の数値で表し、その数値から画像を復元する」という説明用の場面を考える。学習では次の3つを区別する。[モデルの定義：CVAE論文 §3](../../../raw/papers/sohn_2015_cvae.pdf)

| 要素 | 役割 |
| --- | --- |
| encoder $q_\phi(z\mid x)$ | 入力$x$を説明する潜在変数$z$の分布を推定する。recognition modelとも呼ぶ。 |
| decoder $p_\theta(x\mid z)$ | $z$から、データ$x$の分布を決める。generation modelとも呼ぶ。 |
| 事前分布 $p(z)$ | 入力$x$を見る前に定める、潜在変数の分布。 |

encoderとdecoderのパラメータ$\phi,\theta$を一緒に学ぶ。encoderの分布は、計算が難しい真の事後分布$p_\theta(z\mid x)$を近似する役割を持つ。[CVAE論文 §3](../../../raw/papers/sohn_2015_cvae.pdf)

```text
学習：入力x → encoder → zの分布 → zを取り出す → decoder → 入力の復元
        └──────────────────── 復元の正解 ───────────────────┘

生成：事前分布 → zを取り出す → decoder → データの生成
```

図は生成過程と学習時のrecognition modelを簡略化したもの。KL項とパラメータ更新の経路は省略している。decoderは厳密にはデータの分布を定めるため、その分布から値を取り出すことと代表値を表示することは区別する。[モデル定義からの説明：CVAE論文 §3](../../../raw/papers/sohn_2015_cvae.pdf)

## 「分布を出す」とは

Gaussianを使う場合、分布は平均$\mu$と分散$\sigma^2$で表せる。encoderが決めるのは入力に対応したこれらの値で、そこから取り出した一つの$z$とは別物である。[Gaussian latent variableの基礎：CVAE論文 §3](../../../raw/papers/sohn_2015_cvae.pdf)、[平均・分散を推定する具体例：ACT §IV-B](../../../raw/papers/zhao_2023_act.pdf)

説明用に1次元の例を置く。平均が$1.0$、標準偏差が$0.2$なら、$z$は1.0付近を取りやすいが、常に1.0になるわけではない。標準正規乱数$\epsilon$を使って、

$$z=\mu+\sigma\epsilon$$

と書ける。例えば$\epsilon=0.5$なら$z=1.1$になる。これはGaussianの変数変換による計算例で、実験値ではない。ベクトルの場合は各成分について$z=\mu+\sigma\odot\epsilon$とする。[微分可能な変換によるサンプリング：CVAE論文 §3・式(3)直後](../../../raw/papers/sohn_2015_cvae.pdf)

## 学習では何を小さくするか

基本的なVAEの損失は、次の2項の和として理解できる。ここでは学習目的の符号を反転し、最小化する形で表す。[CVAE論文 §3・式(2)–(3)](../../../raw/papers/sohn_2015_cvae.pdf)

$$
\mathcal J(x)=
\underbrace{-\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]}_{\text{再構成損失}}
+\underbrace{D_{\mathrm{KL}}(q_\phi(z\mid x)\Vert p(z))}_{\text{KL項}}.
$$

- **再構成損失**：取り出した$z$から、元の入力をどれだけよく説明できるかを評価する。
- **KL項**：入力から推定した潜在分布が、事前分布からどれだけ離れているかを評価する。

片方は入力を復元するための情報を保持する役割、もう片方は事前分布とのずれを抑える役割を持つ。KL項だけでは入力を復元する要求がなくなり、再構成だけでは事前分布との整合を求めなくなる。これは上の目的関数の各項を取り除いた場合の数学的な読み方である。[元の目的関数：CVAE論文 §3・式(2)–(3)](../../../raw/papers/sohn_2015_cvae.pdf)

この目的関数の符号を逆にした量が、対数尤度の下界であるELBO（Evidence Lower Bound）。計算しにくい真の事後分布を、扱える分布で近似しながら学習する変分推論の考え方に基づく。[CVAE論文 §3・式(1)–(3)](../../../raw/papers/sohn_2015_cvae.pdf)

## 乱数を使っても学習できる理由

上の$z=\mu+\sigma\odot\epsilon$では、乱数$\epsilon$と、encoderが決める$\mu,\sigma$を分けている。$\epsilon$を与えれば$z$は$\mu,\sigma$の微分可能な式になるため、decoderの復元誤差をencoderまで伝えて両方を更新できる。この考え方がreparameterization trickである。[CVAE論文 §3・式(3)直後](../../../raw/papers/sohn_2015_cvae.pdf)

## CVAE・ロボット学習とのつながり

CVAEは観測やラベルなどの条件$c$を加え、条件に合う出力の分布を学ぶ拡張である。条件だけでは出力が一つに決まらない場合を潜在変数で表す。[CVAE論文 §4・式(4)–(5)](../../../raw/papers/sohn_2015_cvae.pdf)

ACTでは現在の画像・関節位置を条件として行動列を予測する。学習時のencoderは関節位置と正解行動列から$z$の分布を推定するが、実行時はencoderを使わず$z=0$に固定する。したがって、VAEの一般的な生成手順と、個々の方策の実行手順は分けて読む。[ACT §IV-B–C・Appendix C](../../../raw/papers/zhao_2023_act.pdf)

Behavior Retrievalでは状態と行動を復元するVAEを学び、encoderの表現を既存データの検索に使う。VAEの復元学習と、検索後のBCによる方策学習は別の段階である。[Behavior Retrieval §III-C–E・Algorithm 1](../../../raw/papers/du_2023_behavior_retrieval.pdf)

## 関連ページ

- [CVAE：条件付き生成とACTでの使い方](conditional_variational_autoencoder.md)
- [ACT用CVAEガイド](cvae_for_act_reading_guide.md)
- [Behavior RetrievalのVAE：基礎から検索手順まで](../retrieval/behavior_retrieval_vae_search.md)
- [ACTのCVAE：KL項と正解情報への依存](../imitation_learning/act_cvae_kl_regularization.md)
