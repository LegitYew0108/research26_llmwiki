---
title: "確率的ルーティングとKS₂テスト"
type: concept
tags: [ANNS, HNSW, probabilistic-routing, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-03
---

# 確率的ルーティングとKS₂テスト

## 距離計算の前に候補を選別する

グラフベースANNSでは、現在のノードの隣接候補を評価して探索を進める。KS₂テストは辺 $e=w-v$ の射影情報を使い、候補 $w$ が現在の結果リストを改善しそうかを判定する。通過した候補だけ正確な距離を計算することで探索を高速化する。[出典：§6.2、付録C.4・Algorithm 7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

1. クエリの射影テーブルを前計算する。
2. 訪問ノードの未訪問の隣接候補を列挙する。
3. 結果リストが満杯なら最遠候補の距離を閾値 $\delta$ とし、未充足なら $\delta=\infty$ とする。
4. KS₂テストを通った候補について正確な距離を求める。
5. 閾値より近ければ結果リストと探索キューへ追加し、探索を続ける。

これは論文Algorithm 7の流れの要約であり、そのまま完全な実装仕様ではない。実装時には訪問管理、結果リストの容量管理、停止条件なども扱う必要がある。[出典：付録C.4、Algorithm 7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=19)

## 保証の意味

$(\delta,1-\epsilon)$-routingは、$\operatorname{dist}(w,q)<\delta$ を満たす隣接候補が少なくとも $1-\epsilon$ の確率で通過するという局所的な保証である。論文のKS₂テストは $(\delta,0.5)$-routingを満たす。探索全体のRecall保証と解釈してはならず、複数辺での判定を独立と仮定して成功確率を掛け合わせる根拠も、この定義からは得られない。[出典：定義6.1・系6.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

## コストと調整

実験の $m=256$ では、各部分空間で選んだ射影ベクトルIDを1 byteで格納できる。各辺に $L$ bytesのIDと量子化した2スカラーを保存し、判定では $L$ 回の参照と $L-1$ 回の加算などを行う。候補ごとの $O(L)$ のコストだけでなく、クエリ射影の前計算、辺の追加情報、テストを通った候補の正確な距離計算も必要になる。[出典：§5–6、付録D.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

$L$ を増やせば常に速くなるわけではない。参照角度の改善と、判定時間・容量の増加のバランスを評価する必要がある。[出典：§7.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=9)

## 距離の条件が角度判定になる理由

以下は、原論文の式(9)を理解するために、ユークリッド距離の条件を展開した説明である。現在の結果リストの距離閾値を $\delta$ とすると、候補 $w$ を採用したい条件は

$$\|w-q\|^2<\delta^2
\iff \frac{\|w\|^2}{2}-w^\top q<\frac{\delta^2-\|q\|^2}{2}.$$

ここで $\tau=(\delta^2-\|q\|^2)/2$ と置き、$e=w-v$ により $w^\top q=v^\top q+e^\top q$ と分解すれば、

$$q^\top\frac e{\|e\|}>
\frac{\|w\|^2/2-\tau-v^\top q}{\|e\|}$$

となる。つまり既に訪問した $v$ の情報を再利用し、「クエリと辺方向の内積が閾値を超えるか」に置き換えられる。単位クエリでなければ両辺を $\|q\|$ で割ると余弦同士の比較になる。この展開は原論文のテスト式に対応する代数的な補足であり、原論文で曖昧に述べられる $\tau$ と距離閾値の関係を明示したものである。[出典：§6.2、式(9)、付録C.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

## KS₂テストの式と保存する情報

実装のテスト式は

$$\sum_{i=1}^{L}q_i^\top u_{i,e[i]}
\ge A_S(e)\frac{\|w\|^2/2-\tau-v^\top q}{\|e\|}.$$

$e[i]$ は辺方向について第 $i$ 部分空間で選んだ参照ベクトルのID、$u_{i,e[i]}$ はその部分ベクトルである。ここで $A_S(e)$ は、理論の単位球面の定義に合わせて**正規化した辺方向**に対する参照余弦として読む。式は回転後の座標系を用いた形であり、直交回転はノルム・内積を保つ。左辺を参照余弦で割った量がKS₂に対応する。[出典：式(3)・(9)、付録C.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

前計算・再利用する情報は次のように分かれる。

| 単位 | 情報 | 使い方 |
| --- | --- | --- |
| 辺ごと | $L$ 個の参照方向ID | クエリ射影テーブルの参照位置 |
| 辺ごと | $c_1=A_S(e)\|w\|^2/(2\|e\|)$ | 閾値の定数項 |
| 辺ごと | $c_2=A_S(e)/\|e\|$ | 動的閾値を掛ける係数 |
| クエリごと | $T[i,j]=q_i^\top u_{i,j}$ | 全候補で再利用 |
| 訪問ノードごと | $v^\top q$ | 同じ $v$ の隣接辺で再利用 |

右辺は $c_1-c_2(\tau+v^\top q)$ と書ける。候補ごとに高次元の辺との内積を直接求めず、$L$ 回のテーブル参照と加算、少数のスカラー演算で判定することが高速化の要点である。論文ではスカラーを量子化し、SIMDで16辺を同時にテストする。[出典：§6.2 Complexity analysis](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

## 通過・棄却によって何が起きるか

テストを通っても正確な距離で再評価するため、閾値外の候補が通る誤りは主に余分な距離計算となる。一方、閾値内の候補を棄却すると距離計算と探索キューへの追加が省かれるので、そのノードを経由する探索にも影響する。これはAlgorithm 7の動作から分かる帰結であり、候補の通過確率だけで検索全体のRecallを計算できない理由でもある。[出典：Algorithm 7、定義6.1・系6.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=19)

結果リストの容量は最終出力数 $k$ ではなく $ef_s\ge k$ であり、途中で保持する候補数を調節する。満杯になるまでは距離閾値を無限大とし、その後はリストの最遠候補を閾値にする。KS₂の $L$ はテストの精度とコスト、$ef_s$ は探索で保持する候補数を調節する別のパラメータである。[出典：付録C.4、Algorithm 7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=18)

PEOsと比べたKS₂の特徴は、参照角度を明示的に利用し、テスト式を単純化して保存スカラーも減らした点にある。ただし比較実験はPEOsの $\epsilon=0.2$ とKS₂の理論上の通過確率下限0.5を同一に設定したものではない。実験曲線では同じRecallにおける速度を見る必要がある。[出典：§6.2、付録D.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=20)

## 関連ページ

- [角度判定と参照角度](angle_testing.md)
- [参照角度による確率解析](reference_angle_probability.md)
- [射影配置と部分空間分割](projection_configuration_ks.md)
- [論文要約と実験条件](../sources/kernel_function_for_angle_testing.md)
