---
title: "KS₂のロボット強化学習への応用検討"
type: research
tags: [research, robot, reinforcement-learning, ANNS, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-09-29
---

# KS₂のロボット強化学習への応用検討

## 論文から確認できる範囲

KS₂はHNSWなどのグラフ探索で候補の正確な距離計算を削減する手法である。評価対象はテキスト・画像由来のベクトル検索であり、ロボットの強化学習における性能は実証していない。[出典：§6–7、付録D](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

## 応用仮説（未検証）

以下は本Wikiでの研究案であり、原論文の結論ではない。

- 状態や観測の埋め込みから過去の遷移・類似経験を検索する構成を採るなら、その検索部分をHNSW+KS₂で高速化できる可能性がある。
- 検索の取りこぼしは、強化学習側で使用する経験や推定値を変える可能性があるため、検索Recallだけでなくタスク性能の測定が必要になる。
- 埋め込みを学習中に更新する場合、保存ベクトルや辺の射影情報をいつ更新するかが課題になり得る。

これらの着想の根拠は原論文の検索高速化機構と辺ごとの前計算である。強化学習での有効性や更新コストは未検証である。[着想元：§5–7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## 次に行う検証案（未実施）

1. 強化学習のどの処理が検索を使うのかを定義する。対象ベクトル、距離尺度、件数、次元、更新頻度、必要な検索精度を決める。
2. 埋め込みを固定し、同じデータ・クエリ・ハードウェアで厳密検索、HNSW、HNSW+KS₂を比較する。
3. Recall@kを揃えてQPS、レイテンシ、正確な距離の計算回数、メモリ、構築時間を測る。
4. 強化学習に組み込み、複数seedでリターン・成功率・学習の実時間を比較する。動的更新を必要とする場合は追加測定する。

上記は研究計画案であり、実験済みの結果ではない。原論文の比較条件は[論文要約](../sources/kernel_function_for_angle_testing.md)を参照。論文の2.5–3倍という検索QPSの向上を、そのまま学習全体の高速化率とみなさない。[着想元：§7・付録D.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

## 関連ページ

- [確率的ルーティングとKS₂](../concepts/probabilistic_routing_ks2.md)
- [角度判定と参照角度](../concepts/angle_testing.md)
