---
title: "ACTのためのCVAE：資料と学習ガイド"
type: research
tags: [CVAE, VAE, ACT, latent-variable, conditional-generation, ELBO]
sources:
  - ../papers/sohn_2015_cvae.pdf
  - kingma_2013_auto_encoding_variational_bayes.pdf
  - kingma_2019_introduction_to_variational_autoencoders.pdf
  - ../papers/zhao_2023_act.pdf
updated: 2026-10-08
---

# ACTのためのCVAE：資料と学習ガイド

## 資料と読む順番

読む順番は理解を助けるためのLLMによる提案であり、研究方針ではない。2026-10-08：ユーザーがCVAE論文を `raw/papers/` に移動し、ingest済み。[論文要約](../../wiki/sources/sohn_2015_cvae.md)・[概念ページ](../../wiki/concepts/conditional_variational_autoencoder.md)を参照。このページはResearchの案内と依頼された説明を兼ねる。

1. **VAEの復習**：[既存の日本語解説](../../wiki/concepts/variational_autoencoder.md)。encoderが平均・分散を出すこと、再構成損失、KL項、reparameterization trickを確認する。一次資料は[Auto-Encoding Variational Bayes（Kingma & Welling、2013）](kingma_2013_auto_encoding_variational_bayes.pdf) §2–3、および[An Introduction to Variational Autoencoders（2019）](kingma_2019_introduction_to_variational_autoencoders.pdf)。後者は[公開本文](https://arxiv.org/html/1906.02691v3)でも読める。
2. **CVAEの原論文**：Sohn, Yan, Lee（NeurIPS 2015）、*Learning Structured Output Representation using Deep Conditional Generative Models*。[保存PDF](../papers/sohn_2015_cvae.pdf) / [公式PDF](https://proceedings.neurips.cc/paper_files/paper/2015/file/8d55a249e6baa5c06772297520da2051-Paper.pdf)。§3でVAEを復習し、§4冒頭・式(4)–(5)・Fig.1で条件付き生成と学習を読む。直感には§5.1・Fig.3の「数字画像の一部から残りを生成する」実験が役立つ。画像の一部が同じでも、残りの形には複数の可能性がある。[出典：同論文§3–5.1](../papers/sohn_2015_cvae.pdf)
3. **ACTへの対応**：Zhao et al.（2023）、*Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware*。[既存PDF](../papers/zhao_2023_act.pdf) / [公開ページ](https://arxiv.org/abs/2304.13705)。§IV-B、Fig.4、Algorithms 1–2、Appendix Cを読む。CVAE encoderと方策の構成、学習時と実行時の違いがまとまっている。[出典：ACT](../papers/zhao_2023_act.pdf)

## CVAEとは何か

**CVAE（Conditional Variational Autoencoder）は、条件を与えて、その条件に合う出力の分布を学ぶ生成モデル**。VAEがデータそのものの分布を学ぶのに対し、CVAEは「この入力が与えられたとき、どの出力があり得るか」を学ぶ。1つの入力に複数の出力が対応するone-to-many mappingを潜在変数で表現する。[出典：Sohnら§3–4](../papers/sohn_2015_cvae.pdf)

ここでは条件を $c$、生成する出力を $y$、潜在変数を $z$ と書く。原論文の入力 $x$ を $c$ に読み替えた表記である。

$$p_\theta(y\mid c)=\int p_\theta(y\mid c,z)p_\theta(z\mid c)\,dz.$$

- **条件 $c$**：生成時にも与えられる情報。
- **事前分布 $p_\theta(z\mid c)$**：正解出力を見る前の $z$ の分布。条件付きの分布を学習する構成も、条件によらない固定分布を使う構成もある。
- **decoder $p_\theta(y\mid c,z)$**：条件と潜在変数から出力の分布を決める。
- **encoder $q_\phi(z\mid c,y)$**：学習時に条件と正解出力を見て、潜在変数の事後分布を近似する。

以上は[原論文§4・Fig.1・式(4)–(5)](../papers/sohn_2015_cvae.pdf)に基づく。$z$ は条件だけでは決まらない出力のばらつきを表すための変数だが、各成分に人が解釈できる意味が自動的に割り当てられる保証はない。[解説論文§1.1](kingma_2019_introduction_to_variational_autoencoders.pdf)

## 学習時と生成時

学習時は正解 $y$ があるので、encoderで $q_\phi(z\mid c,y)$ を求め、そこから $z$ をサンプリングし、decoderで $y$ を再構成する。生成時は正解 $y$ がないためencoderを使わず、事前分布から $z$ を選び、条件とともにdecoderへ渡す。[出典：原論文§4–4.2](../papers/sohn_2015_cvae.pdf)

最小化する損失は、条件付きELBOの符号を反転したものになる。

$$\mathcal J=-\mathbb E_{q_\phi(z\mid c,y)}[\log p_\theta(y\mid c,z)]+D_{\mathrm{KL}}\!\left(q_\phi(z\mid c,y)\Vert p_\theta(z\mid c)\right).$$

第1項は正解を説明するための再構成損失、第2項は学習時の潜在分布を生成時の事前分布に近づける項。正解を見て得た $z$ だけに依存すると、正解のない生成時との隔たりが大きくなる。この隔たりを抑える役割をKL項が担う。[出典：原論文式(4)–(5)・§4.2](../papers/sohn_2015_cvae.pdf)

Gaussian encoderでは $z=\mu+\sigma\odot\epsilon$、$\epsilon\sim\mathcal N(0,I)$ としてサンプリングし、encoderとdecoderを勾配で同時に学習する。[出典：VAE原論文§2.4・3](kingma_2013_auto_encoding_variational_bayes.pdf)

## ACTでは何が条件・出力・潜在変数になるか

| 要素 | ACTでの対応 |
| --- | --- |
| 条件 | 現在のカメラ画像と関節位置 |
| 出力 | 将来の $k$ ステップの目標関節位置（action chunk） |
| 潜在変数 $z$ | 論文では行動列のstyle variableと呼ぶ |
| CVAE encoder | 現在の関節位置と正解行動列から $z$ の平均・分散を推定。画像は入力しない |
| CVAE decoder | 画像・関節位置・$z$ から行動列を予測する方策 |
| 事前分布 | 固定の標準正規分布 $\mathcal N(0,I)$ |

表の出典：[ACT §IV-B–C・Fig.4・Appendix C](../papers/zhao_2023_act.pdf)。一般式のencoderは条件全体を使う表記だが、ACTのencoderは高速化のため条件のうち画像を省く。

**学習時**：`関節位置＋正解行動列 → CVAE encoder → 平均・分散 → zをサンプリング`、続いて `画像＋関節位置＋z → CVAE decoder → 行動列`。損失は再構成損失と重み付きKL項の和である。本文§IV-CではL1再構成損失を用いる。一方、保存版v1のAlgorithm 1にはMSEとあり、表記が一致しないため、本説明は本文に従う。[出典：ACT §IV-B–C・Algorithm 1](../papers/zhao_2023_act.pdf)

$$\mathcal J_{\mathrm{ACT}}=\mathcal L_{\mathrm{reconst}}+\beta D_{\mathrm{KL}}\!\left(q_\phi(z\mid \text{関節位置},\text{正解行動列})\Vert\mathcal N(0,I)\right).$$

**実行時**：`画像＋関節位置＋z=0 → CVAE decoder → 行動列`。CVAE encoderは使わない。したがってACTは、CVAEとしてデモのばらつきを扱って学習するが、論文の実行手順では毎回ランダムなstyleを選ばず、観測に対して決定的な出力を返す。[出典：ACT §IV-B・Algorithm 2・Appendix C](../papers/zhao_2023_act.pdf)

$z=0$ は**潜在変数の事前分布の平均**である。「平均的な行動列」を出す保証はない。decoderは非線形なので、一般に平均の $z$ に対する出力と、$z$ を変えた出力の平均は一致しない。これはACTの手順と非線形モデルからの数学的な注意であり、実験結果の主張ではない。[前提の出典：ACT Appendix C](../papers/zhao_2023_act.pdf)

また、実行時に捨てるCVAE encoderと、CVAE decoder内部のTransformer encoderは別物。画像などを処理する後者は実行時にも必要になる。[出典：ACT Fig.4・Appendix C](../papers/zhao_2023_act.pdf)

## 取得記録

新規取得：`../papers/sohn_2015_cvae.pdf`、2026-10-08、NeurIPS公式PDF、9ページ。PDF本文のタイトル・著者と§4の内容を確認した。VAEの2本とACTは既存ファイルを再利用した。
