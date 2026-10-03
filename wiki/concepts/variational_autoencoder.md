---
title: "VAE（Variational Autoencoder）：仕組みと学習の目的"
type: concept
tags: [VAE, CVAE, generative-model, latent-variable, variational-inference, ELBO, representation-learning]
sources:
  - ../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf
  - ../../raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf
  - ../../raw/papers/zhao_2023_act.pdf
updated: 2026-10-03
---

# VAE（Variational Autoencoder）

## まず直感で理解する

**VAEは、観測データを潜在変数の確率分布に変換するencoderと、潜在変数からデータの分布を作るdecoderを一緒に学習する生成モデル**である。日本語では「変分オートエンコーダ」と呼ばれる。入力を復元するだけでなく、学習後には潜在変数をサンプリングして新しいデータを生成できる。[原論文：§2–3](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)・[原文リンク](https://arxiv.org/abs/1312.6114)

説明用に手書き数字の画像を考える。画像をそのまま扱う代わりに、潜在変数 $z$ を通して画像の特徴を表現し、そこから画像を復元する。[潜在表現の出典：原論文§3・5](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)。説明上の注意として、$z$ の各成分が「傾き」「線の太さ」など、人が理解できる意味に必ず対応すると解釈してはいけない。解説論文でも、そのようなdisentangled representationの学習は研究課題として位置づけられている。[出典：解説論文§1.1](../../raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)

通常の決定的なAutoencoderとの主な違いは次のとおり。[出典：解説論文§2.1–2.4](../../raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)・[解説の原文](https://arxiv.org/html/1906.02691v3)

| 観点 | 通常のAutoencoder | 基本的なVAE |
|---|---|---|
| encoderの出力 | 入力に対応する1つのベクトル | 潜在変数の分布のパラメータ（平均・分散など） |
| decoderへの入力 | encoderが出したベクトル | 分布からサンプリングした潜在変数 |
| 学習の目的 | 主に入力の再構成 | 再構成と、潜在分布を事前分布に近づける項 |
| 新しいデータの生成 | 再構成の学習だけでは、コードのサンプリング方法が定まらない | 定義した事前分布から $z$ をサンプリングして生成する |

## 構成：encoder、潜在変数、decoder

ここでは、観測データを $x$、潜在変数を $z$、encoderの学習パラメータを $\phi$、decoderの学習パラメータを $\theta$ とする。基本的なVAEは、次の生成過程を仮定する。[出典：原論文§2.1・3](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

$$z\sim p(z),\qquad x\sim p_\theta(x\mid z).$$

- **事前分布 $p(z)$**：データを見る前の潜在変数の分布。よく使う選択は標準正規分布 $\mathcal N(0,I)$。
- **decoder $p_\theta(x\mid z)$**：$z$ を受け取り、データの分布のパラメータを出すニューラルネットワーク。例えば画像の各画素に対するBernoulli分布の確率や、Gaussian分布の平均などを出す。
- **encoder $q_\phi(z\mid x)$**：入力 $x$ から、その入力を生成した可能性のある $z$ の分布を推定する。計算が難しい真の事後分布 $p_\theta(z\mid x)$ を近似する役割を持つ。

この3つの役割と分布の選択は[原論文§2.1・3](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)に基づく。Gaussianや標準正規分布は典型的な選択であり、VAE全般の必須条件ではない。

対角共分散のGaussian encoderの場合、

$$q_\phi(z\mid x)=\mathcal N\!\left(\mu_\phi(x),\operatorname{diag}(\sigma_\phi^2(x))\right).$$

encoderが出すのは $z$ 自体ではなく、平均 $\mu$ と分散 $\sigma^2$ を決める値である。実装では分散が正になるよう、$\log\sigma^2$ を出力する形がよく使われる。[出典：原論文§3・Appendix C](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

## 学習：再構成だけでなく潜在分布も整える

モデルが実際のデータに高い尤度を与えるようにしたいが、

$$p_\theta(x)=\int p_\theta(x\mid z)p(z)\,dz$$

の積分は一般に直接計算するのが難しい。そこで、対数尤度の下界である **ELBO（Evidence Lower Bound）** を最大化する。[出典：原論文§2.1–2.2](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

$$\mathcal L_{\mathrm{ELBO}}(x)=\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]-D_{\mathrm{KL}}\!\left(q_\phi(z\mid x)\Vert p(z)\right).$$

損失を最小化する表記にすると、符号を反転して、

$$\mathcal J(x)=\underbrace{-\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]}_{\text{再構成損失}}+\underbrace{D_{\mathrm{KL}}\!\left(q_\phi(z\mid x)\Vert p(z)\right)}_{\text{KL項}}.$$

**再構成損失**は、サンプリングした $z$ から元の入力 $x$ をどれだけ説明できるかを評価する。固定分散のGaussian decoderなら二乗誤差に対応し、Bernoulli decoderならbinary cross entropyに対応する。したがって「VAEの再構成損失は必ずMSE」とは限らない。[出典：原論文§3・Appendix C](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

**KL項**は、入力ごとの潜在分布 $q_\phi(z\mid x)$ が事前分布 $p(z)$ から離れることへのペナルティである。再構成のために入力の情報を保持することと、事前分布に近づけることの間にトレードオフが生じる。KL項だけを最小化すると入力に依存しない分布になり得るため、両方の項が必要になる。[出典：原論文§2.3・3](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

標準正規事前分布と対角Gaussian encoderの場合、KL項は次のように計算できる。$d$ は潜在変数の次元数である。[出典：原論文Appendix B](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

$$D_{\mathrm{KL}}(q_\phi\Vert p)=\frac12\sum_{j=1}^{d}\left(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2\right).$$

## なぜ「変分」なのか

「変分」は、計算しにくい真の事後分布を、扱いやすい分布族 $q_\phi(z\mid x)$ で近似し、そのパラメータを最適化する **variational inference（変分推論）** に由来する。ELBOと対数尤度の関係は、

$$\log p_\theta(x)=\mathcal L_{\mathrm{ELBO}}(x)+D_{\mathrm{KL}}\!\left(q_\phi(z\mid x)\Vert p_\theta(z\mid x)\right)$$

である。KL divergenceは非負なのでELBOは下界となる。ここに現れる「真の事後分布とのKL」と、損失に現れる「事前分布とのKL」は比較対象が異なる点に注意する。[出典：原論文§2.2、式(1)–(3)](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

## Reparameterization trick：サンプリングを通して学習する

encoderの分布から単純にサンプリングする操作では、その出力を通常の決定的な演算と同じように扱ってencoderへ勾配を伝えることはできない。Gaussianの場合には、サンプリングを次の形に書き換える。[出典：原論文§2.3–2.4](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

$$\epsilon\sim\mathcal N(0,I),\qquad z=\mu_\phi(x)+\sigma_\phi(x)\odot\epsilon.$$

ここで $\odot$ は要素ごとの積である。乱数 $\epsilon$ の分布を学習パラメータから切り離し、$\mu$ と $\sigma$ を使う微分可能な演算で $z$ を作る。これにより、decoderの再構成損失からencoderへも勾配を伝えられる。この方法を **reparameterization trick** と呼ぶ。[出典：原論文§2.4・3](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

## 学習時と生成時の違い

学習時は `入力x → encoder → 分布q(z|x) → zをサンプリング → decoder → 再構成損失` という流れで、KL項も加えて両ネットワークを更新する。新しいデータを生成する時は入力画像もencoderも必要なく、`事前分布p(z) → zをサンプリング → decoder → データを生成` となる。decoderの分布からのサンプリングと、その分布の平均を表示することは区別する。[出典：原論文§2–3・Algorithm 1](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)

## CVAEとACTとの関係

**CVAE（Conditional VAE）** は、観測やラベルなどの条件 $c$ を与え、$p_\theta(x\mid z,c)$ を学習する拡張である。encoderも $q_\phi(z\mid x,c)$ のように条件を使う。条件付きの生成モデルとして扱うことで、同じ条件下のデータのばらつきを潜在変数で表せる。[出典：解説論文§1.3.1・1.7.2](../../raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)

既存の[ACT論文の要約](../sources/zhao_2023_act.md)では、この枠組みを行動列の予測に使う。ACTの学習時のCVAE encoderは関節位置と正解行動列から $z$ の分布を推定し、decoderは画像・関節位置・$z$ から行動列を予測する。推論時は $z=0$ に固定するので、基本的なVAEの「事前分布からランダムに生成する」手順とは異なる。またACTはL1再構成損失と重み付きKL項を用いるため、上の基本VAEの式と区別して読む。[出典：ACT §IV-B–C・Appendix C](../../raw/papers/zhao_2023_act.pdf)・[ACT原文](https://arxiv.org/abs/2304.13705)

## 出典と関連ページ

1. Diederik P. Kingma, Max Welling, **Auto-Encoding Variational Bayes**（2013公開、ICLR 2014）。[論文ページ](https://arxiv.org/abs/1312.6114) / [ローカルPDF](../../raw/temp/kingma_2013_auto_encoding_variational_bayes.pdf)。VAEの生成モデル、ELBO、reparameterization trickの原論文。
2. Diederik P. Kingma, Max Welling, **An Introduction to Variational Autoencoders**（2019）。[論文ページ](https://arxiv.org/abs/1906.02691) / [Webで読める本文](https://arxiv.org/html/1906.02691v3) / [ローカルPDF（v3）](../../raw/temp/kingma_2019_introduction_to_variational_autoencoders.pdf)。確率モデルの基礎からVAEを説明する解説論文。
3. Tony Z. Zhao et al., **Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware**（2023）。[論文ページ](https://arxiv.org/abs/2304.13705) / [ローカルPDF](../../raw/papers/zhao_2023_act.pdf)。ロボット模倣学習でのCVAE利用例。

新規に参照したVAEのPDFは `raw/temp/` に保管している。本記事は依頼された概念の説明として作成したもので、これらの論文の個別ingestは行っていない。

- [ACT：Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
- [ロボットの模倣学習と強化学習](imitation_and_reinforcement_learning.md)
