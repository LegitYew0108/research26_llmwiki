---
title: "Learning Structured Output Representation using Deep Conditional Generative Models"
type: source
tags: [CVAE, VAE, conditional-generation, structured-prediction, ELBO, GSNN, segmentation]
sources:
  - ../../raw/papers/sohn_2015_cvae.pdf
updated: 2026-10-08
---

# Learning Structured Output Representation using Deep Conditional Generative Models

## 書誌情報と要点

Kihyuk Sohn、Xinchen Yan、Honglak Lee、NeurIPS 2015。取り込んだ資料は9ページの本文PDFで、supplementary materialは含まない。[一次資料](../../raw/papers/sohn_2015_cvae.pdf)。

入力に対して複数の妥当な出力があるstructured output predictionを、Gaussian潜在変数を持つ **Conditional Variational Autoencoder（CVAE）** で扱う研究。条件付き尤度の変分下界で学習し、MNISTの部分画像補完、鳥のsegmentation、顔の領域ラベル付けで評価する。CVAEに加え、GSNNとhybrid objective、multi-scale prediction、入力への欠損ノイズも提案している。[出典：Abstract・§1・4–5](../../raw/papers/sohn_2015_cvae.pdf)

## 問題設定とモデル

原論文では入力を $x$、出力を $y$、潜在変数を $z$ とする。1つの入力から複数の出力があり得るone-to-many mappingを、条件付き分布として表現する。[出典：§1・4・Fig.1](../../raw/papers/sohn_2015_cvae.pdf)

$$z\sim p_\theta(z\mid x),\qquad y\sim p_\theta(y\mid x,z).$$

- **Recognition network（encoder）** $q_\phi(z\mid x,y)$：入力と正解出力を見て、潜在変数の事後分布を近似する。
- **Conditional prior network** $p_\theta(z\mid x)$：正解出力を見ず、入力から潜在変数の事前分布を決める。
- **Generation network（decoder）** $p_\theta(y\mid x,z)$：入力と潜在変数から出力の分布を決める。

以上は[§4・Fig.1](../../raw/papers/sohn_2015_cvae.pdf)に基づく。原論文は条件付き事前分布を学ぶが、$p_\theta(z\mid x)=p_\theta(z)$ として入力から独立にする構成も認める。CVAEは入力 $x$ 自体を復元するのではなく、**$x$ を条件として正解出力 $y$ を再構成する**という意味でautoencoderに対応する。[出典：§4・脚注1](../../raw/papers/sohn_2015_cvae.pdf)

CNNの初期予測 $\hat y$ もprior networkへ渡すrecurrent connectionを導入し、予測を改善する構成を検討している。ネットワークの詳細は本文がsupplementary materialを参照しているため、本取り込みではその詳細を補完しない。[出典：§4・Fig.1(d)](../../raw/papers/sohn_2015_cvae.pdf)

## 学習目的と推論

条件付き対数尤度の下界は次の通り。右辺を最大化する。[出典：§4・式(4)–(5)](../../raw/papers/sohn_2015_cvae.pdf)

$$\log p_\theta(y\mid x)\ge\mathbb E_{q_\phi(z\mid x,y)}[\log p_\theta(y\mid x,z)]-D_{\mathrm{KL}}\!\left(q_\phi(z\mid x,y)\Vert p_\theta(z\mid x)\right).$$

再構成の項は正解出力を説明する方向に働き、KL項は学習時のrecognition distributionと予測時のprior distributionの隔たりを抑える。Gaussian潜在変数はreparameterizationによって勾配を通し、ネットワークを学習する。[出典：§3–4.2](../../raw/papers/sohn_2015_cvae.pdf)

通常の生成では入力 $x$ からpriorを求めて $z$ をサンプリングし、decoderから出力を生成する。§4.1は、$z$ を事前分布の平均に固定して $p_\theta(y\mid x,z)$ を最大にする出力を選ぶ決定的な予測も説明する。条件付き尤度の評価にはMonte Carlo samplingまたはimportance samplingを使う。[出典：§4.1・式(6)–(7)](../../raw/papers/sohn_2015_cvae.pdf)

## GSNN・hybrid・学習の工夫

学習時は正解 $y$ を使って $z$ を推定する一方、予測時には $y$ がない。著者らはこの違いを問題とし、KL項の重みを増やす方法は本論文の実験では有効でなかったと報告する。代わりに $q_\phi(z\mid x,y)=p_\theta(z\mid x)$ とする **Gaussian stochastic neural network（GSNN）** を導入する。この場合、KL項は消え、priorからサンプリングした $z$ に対する出力尤度を学習する。[出典：§4.2・式(8)](../../raw/papers/sohn_2015_cvae.pdf)

さらに $\mathcal L_{\mathrm{hybrid}}=\alpha\mathcal L_{\mathrm{CVAE}}+(1-\alpha)\mathcal L_{\mathrm{GSNN}}$ として両目的を組み合わせる。segmentationでは複数解像度で出力を評価するmulti-scale predictionと、入力のランダムな矩形領域を0にするnoise injectionも用いる。[出典：§4.2–4.3・式(9)・Fig.2](../../raw/papers/sohn_2015_cvae.pdf)

## 実験結果と読み取れる範囲

- **MNIST部分画像補完**：画像を4象限に分け、一部を入力、残りを出力とする。Fig.3では決定的NNのぼやけた予測に対し、CVAEは多様な数字形状を生成する。Table 1でもCVAEのnegative conditional log-likelihood（negative CLL、低い方がよい）が小さい。観測部分が少ないほど画素当たりの改善幅が大きくなった。[出典：§5.1・Fig.3・Table 1](../../raw/papers/sohn_2015_cvae.pdf)
- **CUBのsegmentationとLFWの領域ラベル付け**：CVAE・GSNN・hybridなどを比較する。Table 2ではCUB testのIoUがCNN baselineの81.90からGSNN（multi-scale＋noise injection）の85.39になる。一方、Table 3のnegative CLLではCVAEが最良で、**点予測の精度と分布の評価で優位なモデルが異なる**。LFWではGDNNとの差が統計的に明確でないケースも記されている。[出典：§5.2・Tables 2–3](../../raw/papers/sohn_2015_cvae.pdf)
- **部分観測でのsegmentation**：入力の一部が欠損し、観測できた部分の出力ラベルも与えられる設定。未知の出力と $z$ を交互に更新して推論する。これは入力画像のみから一度で生成する設定とは異なるため、Table 4の改善を通常の画像segmentation全般へ一般化しない。[出典：§5.3・式(10)・Fig.4・Table 4](../../raw/papers/sohn_2015_cvae.pdf)

上記は画像タスクにおける報告であり、ロボットの行動予測の効果をこの論文自体が検証したものではない。[実験範囲：§5](../../raw/papers/sohn_2015_cvae.pdf)

## ACTとの接続

[ACT](zhao_2023_act.md)では画像・関節位置が条件、将来の行動列が出力に対応する。ただしACTは学習するconditional prior networkの代わりに固定の $\mathcal N(0,I)$ を使い、CVAE encoderから画像を省く。実行時は $z=0$ に固定する。これらはACT側の設計であり、本論文の画像実験の構成とは区別する。[出典：CVAE §4](../../raw/papers/sohn_2015_cvae.pdf)、[ACT §IV-B–C・Appendix C](../../raw/papers/zhao_2023_act.pdf)

- [CVAE：条件付き生成とACTでの使い方](../concepts/conditional_variational_autoencoder.md)
- [VAE：仕組みと学習の目的](../concepts/variational_autoencoder.md)
