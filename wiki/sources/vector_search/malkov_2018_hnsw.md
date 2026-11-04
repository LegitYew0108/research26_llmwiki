---
title: "HNSW：Efficient and robust approximate nearest neighbor search"
type: source
tags: [HNSW, ANNS, vector-search, proximity-graph, NSW]
sources:
  - ../../../raw/papers/malkov_2018_hnsw.pdf
  - ../../../raw/papers/lu_2025_ks_angle_testing.pdf
updated: 2026-11-02
---

# HNSW：Efficient and robust approximate nearest neighbor search

## 書誌情報と要点

- 正式題名：Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs。
- 著者：Yu. A. Malkov、D. A. Yashunin。
- 取り込んだ版：arXiv:1603.09320v4。一次資料：[原論文PDF](../../../raw/papers/malkov_2018_hnsw.pdf)。

HNSWは、データをノードとする近傍グラフを複数の層に分け、上位層で探索開始位置を絞ってから最下層で近傍候補を探索する、逐次構築可能な近似k近傍検索の手法である。提案の柱は階層による距離スケールの分離、明示的なentry point、多様な方向への接続を残す近傍選択heuristicである。[出典：Abstract・§1・3、Fig.1–2](../../../raw/papers/malkov_2018_hnsw.pdf#page=1)

## 解く問題とNSWからの変更

k近傍検索は、クエリに対する距離が小さいデータをk件探す問題である。全データとの距離を計算する全探索に対し、近似検索は真の近傍の取りこぼしを許容して探索を減らす。論文のRecallは、返したk件に含まれる真のk近傍の割合である。[出典：§1](../../../raw/papers/malkov_2018_hnsw.pdf#page=1)

従来のNSWでは単一のグラフに異なる長さの接続が混在する。HNSWはデータの入れ子の部分集合ごとに層を作り、疎な上位層から密な下位層へ進む。各ノードの最高層をランダムに決め、その層から最下層まで同じノードを含める。上位層のノードは学習した代表点やクラスタ中心ではない。[出典：§3–4、Fig.1、Algorithm 1](../../../raw/papers/malkov_2018_hnsw.pdf#page=3)

## 検索の流れ

1. 最上位層のentry pointから開始する。
2. 上位層では `ef=1` のgreedy searchを行い、得られた最も近いノードを次の層の開始点にする。
3. 最下層（layer 0）では `ef` を使って複数の有望な候補を保持しながら探索する。
4. 最後に見つかった候補からクエリに近いk件を返す。

以上はAlgorithm 5の処理である。上位層のgreedy searchと、最下層の候補を複数保持する探索を区別して読む。[出典：§4、Algorithm 5](../../../raw/papers/malkov_2018_hnsw.pdf#page=5)

層内探索のAlgorithm 2は、訪問済み集合、未展開の候補キュー `C`、発見済みの近いノードの集合 `W` を持つ。`C` の最も近いノードを取り出して隣接ノードを調べ、`W` が未充足または現在の最遠候補より近ければ候補を追加する。`W` は最大 `ef` 件に制限する。次に展開する候補が `W` の最遠候補より遠い場合に終了する。この終了条件は未訪問の全ノードに対する最適性の証明ではなく、近似探索の停止条件である。[出典：§4、Algorithm 2](../../../raw/papers/malkov_2018_hnsw.pdf#page=4)

## 構築と近傍選択

挿入ノードの最高層は $l=\lfloor-\ln(U)m_L\rfloor$、$U\sim\mathrm{Uniform}(0,1)$ で決める。既存の最上位層から探索し、挿入ノードが属する層に到達したら `efConstruction` を使って接続候補を集め、近傍を選んで接続する。既存ノードの接続数が上限を超えた場合も近傍選択で絞り直す。[出典：§4、Algorithm 1](../../../raw/papers/malkov_2018_hnsw.pdf#page=4)

単純に近いM件だけを選ぶと、同じクラスタ内のノードで接続が埋まる場合がある。heuristicは候補を挿入点qに近い順に調べ、候補eが選択済みの各ノードrよりもqに近い、すなわち $d(e,q)<d(e,r)$ をすべてのrについて満たす場合に採用する。既に選んだ方向と重複する接続を抑え、別方向やクラスタ間の接続を残す意図がある。`extendCandidates` は候補の隣接ノードも候補に追加し、`keepPrunedConnections` は枠が余れば棄却した候補を補充する。[出典：§3–4、Fig.2、Algorithm 4](../../../raw/papers/malkov_2018_hnsw.pdf#page=5)

## パラメータ

| パラメータ | 役割 |
| --- | --- |
| M | 挿入時に各層で選ぶ接続数。大きいと接続と容量が増え、検索性能にも影響する |
| Mmax / Mmax0 | 上位層／最下層で保持する接続数の上限 |
| efConstruction | 構築時の候補保持数。構築時間とグラフの品質に関係する |
| ef | 検索時の候補保持数。速度とRecallの調整に使う。返すk件を保持できる値が必要 |
| mL | 最高層の分布を決める。層間の重複と各層の探索量に関係する |

原論文の検索時パラメータ名は `ef` である。著者は `mL=1/ln(M)`、上位層の `Mmax=M`、最下層の `Mmax0=2M` を選択肢として検討しているが、全データに対する最適値の保証ではない。`ef` は訪問ノード数や距離計算回数そのものの上限ではない。[出典：§4–4.1、Algorithms 1–5、Fig.3–10](../../../raw/papers/malkov_2018_hnsw.pdf#page=5)

## 計算量と制約

著者は層数と各層の探索量に関する議論から対数的な検索スケーリングを説明し、低次元のランダムデータで実験する。一方、層内で使うDelaunay graphの近似が高次元でも同様に機能するかについて、追加の解析が必要と述べている。したがって任意のデータ・次元・必要Recallで最悪計算量が必ず $O(\log N)$ になる、と読むべきではない。構築についても少なくとも比較的低次元のデータで $O(N\log N)$ のスケーリングと述べる。[出典：§4.2.1–4.2.2](../../../raw/papers/malkov_2018_hnsw.pdf#page=7)

グラフ接続の保存に追加メモリが必要である。§4.2.3では典型的な設定でデータ本体を除き1要素あたり約60–450 bytesと見積もる。これは論文の接続表現と設定における見積もりで、現在のライブラリの総使用メモリを示す値ではない。[出典：§4.2.3](../../../raw/papers/malkov_2018_hnsw.pdf#page=8)

## 実験と結果の読み方

- NSWとの比較では、低次元ランダムベクトル上で距離計算回数と検索時間を評価し、HNSWの改善と対数的なスケーリングを示す。[出典：§5.1、Fig.12](../../../raw/papers/malkov_2018_hnsw.pdf#page=8)
- SIFT・GloVe・CoPhIRなどでRecallと検索時間を比較する。比較対象には当時のNSW・FLANN・Annoyなどを含む。現在の実装や任意のデータで常に最速だという結果ではない。[出典：§5.2、Table 1、Fig.13](../../../raw/papers/malkov_2018_hnsw.pdf#page=9)
- 一般の距離を使うデータでも評価し、200M SIFTではPQ系と比較する。後者では高い精度と速度を示す一方で、より多くのRAMを必要とする。[出典：§5.3–5.4、Tables 2–3、Fig.14–15](../../../raw/papers/malkov_2018_hnsw.pdf#page=10)
- 逐次挿入には対応するが、この版の§6では要素の更新・削除への対応を今後の課題としている。現在の実装の対応状況とは分ける。[出典：§6](../../../raw/papers/malkov_2018_hnsw.pdf#page=11)

## 関連ページ

- [HNSWの仕組み](../../concepts/vector_search/hnsw.md)：探索・構築の読み分け。
- [Probabilistic Kernel Function for Fast Angle Testing](lu_2025_ks_angle_testing.md)：HNSWの探索中にKS₂で候補を選別する別論文。原論文HNSW自体の構成要素ではない。[出典：KS論文§6.2](../../../raw/papers/lu_2025_ks_angle_testing.pdf#page=7)

HNSW原論文の評価対象は近傍検索であり、ロボット制御や強化学習の学習性能を実証した論文ではない。[出典：§5](../../../raw/papers/malkov_2018_hnsw.pdf#page=8)
