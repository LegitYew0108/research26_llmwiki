---
title: "KSの射影配置と部分空間分割"
type: concept
tags: [random-projection, spherical-covering, cross-polytope, KS1, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-01
---

# KSの射影配置と部分空間分割

## なぜ射影ベクトルの配置を設計するのか

KS₁・KS₂の判定精度は参照角度に左右される。そのため、射影数を固定したまま球面をできるだけよく覆う配置を選ぶことが設計課題となる。ランダム回転を入れているので、論文は球面上一様な $v$ に対する参照角度の余弦の期待値を

$$J(S)=\mathbb{E}_{v\sim U(\mathbb{S}^{d-1})}[A_S(v)]$$

と定義し、これを大きくする配置を考える。これは期待余弦の最大化であり、角度の期待値そのものの最小化と同一の目的関数ではない。[出典：§5、式(5)–(7)](../../raw/papers/kernel_function_for_angle_testing.pdf#page=5)

論文は期待値で良い配置に加え、最悪ケースの $\min_v\max_{u\in S}\langle u,v\rangle$ を最大化する配置も定義する。これは球面のbest covering問題に関係し、一般的な最適解を求めるのは難しい。そのため提案する2配置は実用的な構成法であり、任意の $m,d$ で大域最適という結論ではない。[出典：§5、式(6)](../../raw/papers/kernel_function_for_angle_testing.pdf#page=5)

## S_sym：ランダムな対蹠点対

各部分空間で球面上に $m/2$ 個の方向を生成し、それぞれの反対方向も追加して $m$ 個とする。方向 $u$ と $-u$ の内積は符号が反対なので、1回の内積計算から両方を評価できる。論文は、対蹠点を使うことで正の参照内積を確保し、KS₂の分母の条件を満たす構成として説明する。[出典：Algorithm 1、§5](../../raw/papers/kernel_function_for_angle_testing.pdf#page=5)

この配置の利点は生成が簡単なことに加え、$m,L,d$ と期待参照余弦の関係を解析できることである。付録Bの補題B.1は期待値の下界を与え、付録C.5の図5はそれを数値的に評価する。図の縦軸はラベルがReference Angleでも、実際に示す量は参照角度の**余弦**であり、上がるほど角度は小さくなる。[出典：付録B・C.5、図5](../../raw/papers/kernel_function_for_angle_testing.pdf#page=21)

## S_pol：複数のcross-polytope

$d'$ 次元のcross-polytopeは正負の座標軸方向 $\{\pm e_1,\ldots,\pm e_{d'}\}$ を頂点とする。これをランダム回転して複数組み合わせ、必要な $m$ 個の方向を作る。Algorithm 2は $m=2d'a+b$ とし、$a$ 組の完全なcross-polytopeと、余りがあれば追加の対蹠点対を用いる。[出典：Algorithm 2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

構成を最大 $R$ 回生成し、球面からサンプリングした $N$ 個のベクトルに対する経験平均 $\widetilde J(S,N)$ が最も大きい配置を残す。選んだ配置を各部分空間で回転して使用する。球面の覆い方を実用的に改善する手続きであり、有限サンプルの経験平均による選択なので厳密な最適性は保証しない。実験ではS_polがS_symより良いRecallを示す場合が多い。[出典：§5、Algorithm 2、表1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## L個の部分空間で m^L 個の方向を表現する

$d=Ld'$ として、各部分空間に $m$ 個の射影ベクトルを置く。各部分ベクトルのノルムを $1/\sqrt L$ にすると、各空間から1本ずつ選んで連結したベクトルは単位長になる。各空間で独立に最良の方向を選べるため、$m^L$ 通りの連結方向を列挙せずに参照ベクトルを決定できる。[出典：Algorithm 1–2、§5](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

実際に保存する配置は $mL$ 個の $d'$ 次元部分ベクトルであり、その成分数は $mLd'=md$ となる。一方、選ばれた参照方向は $L$ 個のIDで表せる。例えば $m=256,L=8$ なら、仮想的な方向数は $256^8$ だが、1本の方向のIDは8 bytesで表せる。この例は論文の構成と保存規則に基づく計算である。[出典：§5–6](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

部分空間分割はproduct quantizationに似た構成を利用しているが、ここで符号化する対象は角度判定に使う参照方向である。$L$ を増やすと各部分空間の次元が下がり、同じ $m$ で覆いやすくなる一方、候補1件のKS₂評価には $L$ 回の参照が必要となる。[出典：§5、補題5.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## 前処理と問い合わせのコスト

| 処理 | KS₁ | KS₂ |
| --- | --- | --- |
| データ $n$ 件の射影等 | $O(nmd)$ | $O(nd\log d+nmd)$ |
| クエリの準備 | $O(md)$ | $O(d\log d+md)$ |
| 前計算後の候補1件の関数評価 | $O(1)$ | $O(L)$ |

これは補題5.1の関数評価に関する計算量である。MIPS用の射影別リストをソートする処理やHNSWそのものの構築・探索コストをすべて含んだ表ではない。前計算を多数の候補に再利用することで、候補ごとの $O(d)$ の内積を安い判定へ置き換える。[出典：補題5.1、Algorithm 5–7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

S_polを $R=1$ で構成し、Fast Johnson–Lindenstrauss変換を利用する場合、論文は射影計算の高速化も述べる。KS₁のインデックス時コストは $O(\max(d,m)n\log d)$、KS₂は $O(nd\log d+nmL\log(d/L))$ にできる。複数配置から選ぶ $R>1$ の構成と、この高速化条件を同一視しない。[出典：§5、補題5.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## 実験での使い分け

KS₁のMIPS実験では $m=2048,L=1$ として両配置を比較する。KS₂のグラフ探索実験はS_sym、$m=256$ を採用し、IDを1 byteに収める。$L$ が大きいほど良いわけではなく、参照角度の改善と判定時間・容量の増加を合わせて判断する。部分空間次元 $d/L\approx16$ が良好だったという観察は、本論文の実験条件における傾向である。[出典：§7、付録D.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=20)

## 関連ページ

- [参照角度による確率解析](reference_angle_probability.md)
- [確率的ルーティングとKS₂テスト](probabilistic_routing_ks2.md)
- [論文全体の要約](../sources/kernel_function_for_angle_testing.md)
