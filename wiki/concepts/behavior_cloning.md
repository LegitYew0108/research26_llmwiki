---
title: "Behavior Cloning：学習方法と分布シフト"
type: concept
tags: [robotics, imitation-learning, behavior-cloning, supervised-learning, distribution-shift, compounding-error]
sources:
  - ../../raw/temp/osa_2018_imitation_learning_survey.pdf
  - ../../raw/temp/ross_2011_dagger.pdf
  - ../../raw/papers/zhao_2023_act.pdf
  - ../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf
updated: 2026-10-05
---

# Behavior Cloning：学習方法と分布シフト

## 何を学ぶのか

Behavior Cloning（BC）は、expertのデモに含まれる状態または観測と行動の組から、方策を教師あり学習する方法。入力が似た状況ならexpertに近い行動を出すことを目指すが、完全再現やタスク成功を保証するものではない。expertは人間に限らずcontrollerなどでもよい。[出典：Osaら §1.6・2.2・3](../../raw/temp/osa_2018_imitation_learning_survey.pdf)

カメラ画像や関節角などを観測 $o_i$、デモの行動を $a_i^*$ とし、データ $D=\{(o_i,a_i^*)\}$ に対して、例えば次の損失を小さくする。

$$
\min_\theta \frac{1}{|D|}\sum_{(o_i,a_i^*)\in D}\ell(\pi_\theta(o_i),a_i^*).
$$

$\pi_\theta$ はパラメータ $\theta$ を持つ方策、$\ell$ は予測と教師行動を比較する損失。これはBCの教師あり学習を説明するための一般形である。完全な状態を取得できる設定では $o_i$ の代わりに $s_i$ と書ける。[定式化の根拠：Osaら §3](../../raw/temp/osa_2018_imitation_learning_survey.pdf)、[DAgger §2](../../raw/temp/ross_2011_dagger.pdf)

連続行動の回帰では二乗誤差などを使えるが、BCという名前だけで損失やネットワーク構成が決まるわけではない。ACTは行動列を学び、本文ではL1 reconstruction lossとCVAEのKL項を用いる。一時刻の行動をMSEで予測する形はBCの一例である。[出典：Osaら §3](../../raw/temp/osa_2018_imitation_learning_survey.pdf)、[ACT §IV](../../raw/papers/zhao_2023_act.pdf)

## なぜ教師データ上で正確でも失敗するのか

固定されたデモで学習するときは、学習中の方策の出力によって学習入力が変わるわけではない。しかし実行時には、方策が出した行動が次の状態・観測を変える。小さな誤りによってexpertが訪れない状況へ移り、そこでさらに誤ることがある。expertと学習者の訪れる状態分布の違いがdistribution shift、誤りが後続の誤りを誘発することがcompounding errorにつながる。未見の状況で必ず失敗するという主張ではない。[出典：DAgger §1–2](../../raw/temp/ross_2011_dagger.pdf)

## ALVINNに見られる、回復例を学ぶ必要性

ALVINN（NIPS 1988）は、人間の運転画像から適応的に学習する将来構想について、正しい運転だけでなく、間違えた後に道路中央へ戻る例も必要だと記す。ただし、**この版で実施された学習は人工道路画像と教師信号によるものであり、人間のデモを用いた学習は将来構想である。** この論文を読む際には、教師ありの観測→行動学習という共通点と、教師データの生成元を分けて捉える。[出典：ALVINN、Training and Performance・Discussion and Extensions、pp.307–308・311](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

後年のDAggerは、学習者を実行して訪れた状態にexpertが適切な行動をラベル付けし、そのデータを既存データへ追加して学び直す。単に固定データ上の損失を減らすだけでなく、どの状態から学ぶかを変える方法である。[出典：DAgger §3・Algorithm 3.1](../../raw/temp/ross_2011_dagger.pdf)

## 関連ページ

- [ALVINNの論文要約](../sources/pomerleau_1988_alvinn.md)
- [ACTの論文要約](../sources/zhao_2023_act.md)
- [ロボットの模倣学習と強化学習](imitation_and_reinforcement_learning.md)
- [BC：自分の理解](<../../mind/IL/BC-Behavior Cloning.md>)
- [IL：自分の理解](<../../mind/IL/IL-Imitation Learning(模倣学習).md>)
