---
title: "角度判定と参照角度"
type: concept
tags: [angle-testing, random-projection, KS1, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-01
---

# 角度判定と参照角度

## 何を判定するか

単位ベクトルでは内積が角度の余弦に等しいため、内積が大きいほど角度は小さい。angle testingは角度そのものの精密な推定ではなく、候補同士の角度の比較、または所定の角度閾値との比較を行う問題である。原論文は前者にKS₁、後者にKS₂を提案する。[出典：§1・3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=1)

## 参照角度

単位球面上の射影ベクトル集合 $S$ から、対象 $v$ と内積が最大の $Z_S(v)$ を選ぶ。$v$ も単位ベクトルなら、$A_S(v)=\langle v,Z_S(v)\rangle=\cos\psi$ の $\psi$ が参照角度である。**クエリと検索候補の角度 $\phi$ と、候補などと参照ベクトルの角度 $\psi$ は異なる。** [出典：§3–4](../../raw/papers/kernel_function_for_angle_testing.pdf#page=3)

直感的には、代表として選んだ射影方向が対象ベクトルに近いほど、その射影値を使った角度判定が正確になる。論文はランダム回転と参照角度を条件とした分布解析により、この関係を有限の射影数で扱う。ただし正確なのは確率分布の関係であり、個々の判定には誤りが残る。[出典：補題4.2・4.3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

## 射影配置と部分空間

$S_{sym}$ は各方向と反対方向を対にして配置する。$S_{pol}$ はcross-polytope（座標軸の正負方向を頂点とする多面体）を回転して組み合わせる。後者は参照角度を小さくする配置を複数試行から選べるが、一般の場合の最適配置が既知というわけではない。[出典：§5、Algorithm 1–2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=5)

$d$ 次元を $L$ 個の部分空間へ分け、各部分空間に $m$ 個を配置すると、組合せとして $m^L$ 個の射影方向を表現できる。実際に保持するのは $mL$ 個の部分ベクトルである。$L$ を増やすと精度向上が期待できる一方、KS₂の候補判定にかかる $O(L)$ の時間と記憶容量も増える。[出典：§5・7.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## 詳細を読む

判定値の分布と確率保証は[参照角度による確率解析](reference_angle_probability.md)、配置の目的関数・構成手順・計算量は[射影配置と部分空間分割](projection_configuration_ks.md)にまとめる。

## 関連ページ

- [論文要約](../sources/kernel_function_for_angle_testing.md)
- [確率的ルーティングとKS₂](probabilistic_routing_ks2.md)
