---
title: "参照角度によるKS₁・KS₂の確率解析"
type: concept
tags: [angle-testing, reference-angle, KS1, KS2, probability]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-01
---

# 参照角度によるKS₁・KS₂の確率解析

## このページの位置づけ

[角度判定と参照角度](angle_testing.md)の定義を前提に、なぜ参照角度を小さくすると判定が改善するのかを説明する。論文の中核は「角度の推定値が常に正しい」という保証ではなく、参照角度を条件にした推定値の分布を有限次元で記述できる点にある。[出典：§3–4、補題4.2・4.3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

## 幾何学的な分解

単位クエリ $q$ と候補 $v$ の角度を $\phi$、クエリと参照ベクトル $z=Z_{HS}(q)$ の角度を $\psi$ とする。$q$ に直交する単位方向 $a,b$ を使うと、

$$v=\cos\phi\,q+\sin\phi\,a,\qquad z=\cos\psi\,q+\sin\psi\,b$$

と分解できる。このため

$$K_{S1}(q,v)=\langle v,z\rangle
=\cos\phi\cos\psi+\sin\phi\sin\psi\,T,\qquad T=\langle a,b\rangle.$$

ランダム回転と参照角度の条件付けのもとで、残る直交方向が球面上に一様に分布することを使って $T$ の分布を求める。ここでは論文付録Aの議論を幾何学的な形に書き直している。中心は真の余弦 $\cos\phi$ に $\cos\psi$ を掛けた値で、揺らぎの係数は $\sin\phi\sin\psi$ となる。[出典：補題4.2、付録A](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

$\psi$ が小さければ参照方向はクエリに近く、中心の縮小も揺らぎも小さい。$\psi=0$ では参照ベクトルがクエリ自身になるので、KS₁は正確な内積に一致する。ただし比較成功確率は2候補の差にも依存し、参照角度だけから一律の高精度を保証するわけではない。[出典：補題4.2、§4 Remarks](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

## 有限次元の分布をどう表すか

$d\ge3$、$\phi,\psi\in(0,\pi)$ では、$B=(T+1)/2$ が対称なBeta分布に従うことから、論文は次の条件付きCDFを示す。

$$F(x\mid\psi)=I_t\left(\frac{d-2}{2},\frac{d-2}{2}\right),\qquad
 t=\frac12+\frac{x-\cos\phi\cos\psi}{2\sin\phi\sin\psi}.$$

$I_t$ は正則化不完全ベータ関数で、CDFは「KS₁の値が $x$ 以下になる確率」を表す。値の範囲は $[\cos(\phi+\psi),\cos(\phi-\psi)]$ であり、その外側ではCDFは0または1となる。この関係は射影数 $m\to\infty$ を必要としない。[出典：補題4.2(1)、式(4)](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

CEOsの理論はガウス射影の極値に関する漸近分布を使う。本論文では、射影配置から参照方向を選び、その参照角度を条件にして分布を解析する。有限の $m$ の影響は参照角度や配置を通じて現れる。「漸近条件を不要にした」ことと「ランダム性をなくした」ことは別である。[出典：補題1.3、§3–4](../../raw/papers/kernel_function_for_angle_testing.pdf#page=2)

## KS₁：2候補の順序を判定する

KS₁は同じクエリの参照ベクトルを使って $v_1,v_2$ を評価する。差は $\langle v_1-v_2,z\rangle$ なので、比較は差ベクトルと参照方向の関係として扱える。補題4.2(2)は、$\langle q,v_1\rangle>\langle q,v_2\rangle$ なら、参照角度を小さくすると正しい順序を返す確率が高まり、$\psi\in(0,\pi/2)$ ではその確率が0.5より大きいと示す。2つのスコアは同じ射影方向を使うため、独立な推定値として扱う根拠はない。[出典：補題4.2(2)、付録A](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

## KS₂：参照角度で補正し、閾値と比較する

KS₂ではデータ側 $Hv$ に近い参照ベクトルを選び、その参照角度の余弦で割る。前述の分解の役割を入れ替えると、

$$K_{S2}(q,v)=\cos\phi+\sin\phi\tan\psi\,T$$

という形で理解できる。中心が真の余弦に一致し、参照角度が揺らぎの幅を制御する。これは補題4.3の分布関係を説明する書き換えである。分母が正になる $\psi\in(0,\pi/2)$ が重要な条件となる。[出典：式(3)、補題4.3、付録A](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

角度閾値を $\theta$ とすると、$K_{S2}\ge\cos\theta$ を満たす候補を通す。真の角度が $\phi\le\theta$ なら通過確率は少なくとも0.5であり、$\phi>\theta$ なら0.5未満となる。後者の確率は

$$I_{t'}\left(\frac{d-2}{2},\frac{d-2}{2}\right),\qquad
 t'=\frac12-\frac{\cos\theta-\cos\phi}{2\sin\phi\tan\psi}$$

で表され、$t'<0$ なら0とする。閾値のすぐ外の候補は通る可能性が残るが、角度が大きくなるほど通過しにくい、というangle-sensitive性を持つ。[出典：定義4.1、補題4.3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

## 保証を読むときの注意

この確率はランダム回転などに対するもので、同じ固定済みインデックスへの同じ問い合わせを繰り返すたびに新しい独立な判定を引く、という意味ではない。また、理論の関数と、スカラー量子化・高速変換などを含む実装とは区別して読む必要がある。原論文の局所的なrouting保証から、量子化後の検索全体のRecallの下限を直接導くことはできない。[出典：§3–6、系6.2、付録C.4](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

## 関連ページ

- [射影配置と部分空間分割](projection_configuration_ks.md)
- [確率的ルーティングとKS₂テスト](probabilistic_routing_ks2.md)
- [論文全体の要約](../sources/kernel_function_for_angle_testing.md)
