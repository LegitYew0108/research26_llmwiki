---
title: "ACTのinfer z：学習時に正解行動列を使う理由"
type: concept
tags: [ACT, CVAE, transformer, latent-variable, CLS, imitation-learning]
sources:
  - ../../../raw/papers/zhao_2023_act.pdf
  - ../../../raw/papers/sohn_2015_cvae.pdf
updated: 2026-10-31
---

# ACTのinfer z：学習時に正解行動列を使う理由

infer zは、学習データの正解行動列と現在の関節位置から、その行動列を説明する潜在変数の分布を推定する段階である。未来の行動を観測から予測する方策そのものとは役割が違う。[出典：ACT §IV-B・C、Appendix C・Fig.11](../../../raw/papers/zhao_2023_act.pdf)

## 入力と処理

現在時刻をtとし、現在の画像I_t・followerの関節位置q_tと、その時刻からの正解行動列A_t = (a_t, ..., a_{t+k-1})をデモから取り出す。ALOHAの行動はleader側の目標関節位置14次元で、左右それぞれ6関節とgripperを含む。現在の観測関節位置と行動ラベルは区別する。[出典：ACT §IV-C・Appendix C](../../../raw/papers/zhao_2023_act.pdf)

1. 各行動を共有の線形層で14→512次元へ写し、k×512の列にする。現在の関節位置も別の線形層で14→512次元へ写す。
2. 学習可能な512次元の[CLS] tokenを先頭に加え、(k+2)×512の列にする。位置埋め込みとともにCVAE encoderのTransformer encoderへ入力する。
3. 出力のうち[CLS]位置の512次元ベクトルを取り出し、線形層で潜在分布のパラメータへ写す。
4. 対角Gaussianの平均と分散を使い、reparameterizationでzをサンプリングする。

以上は[ACT Appendix C・Fig.11・Table III](../../../raw/papers/zhao_2023_act.pdf)に基づく。512次元への射影は学習する特徴表現であり、元データの独立な情報量が増えるという意味ではない（次元拡張に関する説明）。

図の「Weight matrix」はランダム初期化された学習可能な[CLS]の重みであり、データから別途生成する行列ではない。[CLS]入力は各サンプルで共通だが、Transformer処理後の[CLS]出力は関節位置と行動列に依存する。[出典：ACT Appendix C・Fig.11](../../../raw/papers/zhao_2023_act.pdf)

実装確認の補足：著者公開の[det r_vae.py](https://github.com/tonyzhaozh/act/blob/main/detr/models/detr_vae.py)では`nn.Embedding(1, hidden_dim)`を使用する。潜在次元は32で、512→64の線形層の出力を平均32次元とlog variance 32次元へ分け、σ = exp(logvar/2)、z = μ + σ⊙ε、ε ~ N(0,I)とする。論文は平均・分散と記すが、実装で直接出すのは平均・対数分散である。[対応する一次資料：ACT Fig.11](../../../raw/papers/zhao_2023_act.pdf)。コードは2026-10-16時点のmainを参照し、rawへの取り込みは行っていない。

## 画像はどこで使うか

画像はinfer zのCVAE encoderには入らない。画像・現在の関節位置・zを入力するCVAE decoder、すなわち方策側で使う。画像をResNet18で特徴化し、方策内部の別のTransformer encoderで関節情報とzを統合し、Transformer decoderがk個の行動を出力する。CVAE decoderの中にもTransformer encoderが存在する点に注意する。[出典：ACT §IV-C・Appendix C・Fig.11](../../../raw/papers/zhao_2023_act.pdf)

## なぜ未来の正解行動列を入れるか

CVAEのrecognition networkは、条件と正解出力を見て潜在変数の事後分布を近似する。ACTではq_φ(z | q_t, A_t)を推定し、方策が画像・関節位置・zから同じA_tを再構成するよう学習する。したがって正解行動列は、過去の履歴としてではなく再構成対象として入力される。[出典：ACT §IV-B・C](../../../raw/papers/zhao_2023_act.pdf)、[CVAE §4](../../../raw/papers/sohn_2015_cvae.pdf)

Transformer encoderという名称は、入力を過去に限定する規則ではない。この学習用encoderは既に記録された正解列全体を表現へ変換する。実行時には正解の未来列がないためCVAE encoderを使わず、z=0を与え、現在の画像と関節位置から行動列を予測する。[出典：ACT Appendix C・Algorithms 1–2](../../../raw/papers/zhao_2023_act.pdf)

## zの目的と限界

ACTでは人のデモに含まれる行動のばらつきを「style」として潜在変数で表現する。学習は行動列の再構成誤差と、推定分布を標準正規分布へ近づけるKL項を組み合わせる。これにより正解列の情報を際限なくzへ詰め込むことを抑え、正解列のない実行時の事前分布との隔たりを抑える。[出典：ACT §IV-B・C](../../../raw/papers/zhao_2023_act.pdf)、[CVAE §4](../../../raw/papers/sohn_2015_cvae.pdf)

理解のための例（説明用の仮定）：似た観測でもデモの動作速度や経路が異なる場合、zを通じてその違いを説明できる。ただし、zの各成分に速度などの意味が明示的に割り当てられるわけではない。また、実行時のz=0は事前分布の平均であり、成功行動の平均や最適な行動を保証する値ではない。ACTの実行はzをサンプリングしないため、この設定で毎回異なるstyleを生成するわけではない。[根拠：ACT §IV-B・Appendix C](../../../raw/papers/zhao_2023_act.pdf)

## 関連

- [ACT原論文の要約](../../sources/imitation_learning/zhao_2023_act.md)
- [CVAE：条件付き生成とACTでの使い方](../generative_models/conditional_variational_autoencoder.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
