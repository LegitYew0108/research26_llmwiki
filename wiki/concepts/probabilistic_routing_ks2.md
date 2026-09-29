---
title: "確率的ルーティングとKS₂テスト"
type: concept
tags: [ANNS, HNSW, probabilistic-routing, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-09-29
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

## 関連ページ

- [角度判定と参照角度](angle_testing.md)
- [論文要約と実験条件](../sources/kernel_function_for_angle_testing.md)
- [ロボット強化学習への応用仮説](../research/ks2_for_robot_rl.md)
