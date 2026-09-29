---
title: "Probabilistic Kernel Function for Fast Angle Testing"
type: source
tags: [ANNS, HNSW, angle-testing, random-projection, KS1, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-09-29
---

# Probabilistic Kernel Function for Fast Angle Testing

## 書誌情報と要点

- 著者：Kejing Lu、Chuan Xiao、Yoshiharu Ishikawa。
- 取り込んだ版：arXiv:2505.20274v3、2026年3月1日。PDFでは arXiv preprint と表記。
- 一次資料：[論文PDF](../../raw/papers/kernel_function_for_angle_testing.pdf)。著者が提示する実装：<https://github.com/KejingLu-810/KS>（本取り込みではコード未検証）。

高次元ベクトル間の角度を正確に計算する代わりに、「どちらの角度が小さいか」「角度が閾値以下か」を低コストで確率的に判定する。提案するKS₁は比較、KS₂は閾値判定に対応し、KS₂をHNSWの候補選別に用いて距離計算を削減する。中心となるのは、ベクトルとその代表的な射影ベクトルとの**参照角度**である。[出典：§1・3・6](../../raw/papers/kernel_function_for_angle_testing.pdf#page=1)

## 背景と提案

CEOsやPEOsが利用するガウス射影の理論には、射影ベクトル数が無限大へ向かう漸近条件がある。本論文は、固定した単位球面上の配置とランダム回転を用い、参照角度を条件とする有限次元の分布関係を導く。「漸近仮定が不要」とは判定が常に正しいという意味ではなく、誤判定確率の解析が漸近近似に依存しないという意味である。[出典：§1・3–4](../../raw/papers/kernel_function_for_angle_testing.pdf#page=2)

単位ベクトルの集合を $S$、ランダム回転を $H$ とし、

$$Z_S(v)=\arg\max_{u\in S}\langle u,v\rangle,\qquad A_S(v)=\langle v,Z_S(v)\rangle$$

と定義する。正規化した $q,v$ に対して提案関数は次のとおり。

$$K_{S1}(q,v)=\langle v,Z_{HS}(q)\rangle,$$
$$K_{S2}(q,v)=\frac{\langle Hq,Z_S(Hv)\rangle}{A_S(Hv)}.$$

KS₁はクエリ側の参照ベクトルへの射影値で候補を比較する。KS₂はデータ側の参照ベクトルを用い、参照角度の余弦で補正する。ここでいうkernelは本論文の確率的判定関数を指す。[出典：§3、式(2)–(3)](../../raw/papers/kernel_function_for_angle_testing.pdf#page=3)

## 理論と計算量

$d\ge3$ などの条件下で、KS₁の参照角度を条件としたCDFは正則化不完全ベータ関数で表される。参照角度が小さいほど比較成功確率が高まり、参照角度が $(0,\pi/2)$ にある場合、正しい順序を返す確率は $0.5$ を超える。KS₂についても同範囲の参照角度でangle-sensitive性を示すが、閾値内の候補を通す保証は少なくとも $0.5$ である。[出典：補題4.2・4.3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=4)

射影配置には、対蹠点対を使う $S_{sym}$ と、回転した複数のcross-polytopeを使う $S_{pol}$ を提案する。空間を $L$ 個に分割し、各部分空間の $m$ 個の射影を組み合わせて仮想的に $m^L$ 個の候補を表す。配置の一般的な大域最適性を証明したわけではない。[出典：§5、Algorithm 1–2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=5)

| 項目 | KS₁ | KS₂ |
| --- | --- | --- |
| インデックス時（データ数 $n$） | $O(nmd)$ | $O(nd\log d+nmd)$ |
| クエリごとの射影など | $O(md)$ | $O(d\log d+md)$ |
| 前計算後の候補1件の評価 | $O(1)$ | $O(L)$ |

表は補題5.1の一般的な計算量であり、$L\ll d$ を想定する。高速変換を使える配置では前処理をさらに短縮できる。**検索全体が $O(1)$ や $O(L)$ になるという主張ではない。** [出典：§5、補題5.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## HNSWへの組み込み

訪問中のノード $v$ から隣接ノード $w$ への辺 $e=w-v$ に射影情報を持たせる。探索中の結果リストから距離閾値を決め、KS₂テストに通った候補だけ正確な距離を計算する。1辺の判定は $L$ 回のテーブル参照と加算などで実行できる。実験では $S_{sym}(256,L)$ を使用し、各辺に $L$ bytesの射影IDと量子化した2スカラーを保存する。[出典：§6.2、式(9)、Algorithm 7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

系6.2の保証は $(\delta,0.5)$-routing、すなわち距離 $\delta$ 未満の候補がテストを通る確率の下限である。これは検索結果全体のRecallが0.5以上になる保証でも、候補を絶対に取りこぼさない保証でもない。[出典：定義6.1・系6.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

## 実験結果と条件

Intel Xeon Gold 6258R（2.70GHz）、C++実装で、ANNSの構築は64スレッド、検索はCPU 1スレッド。主実験は $k=10$ のRecall–QPS比較である。[出典：§7、図1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

| データセット | データ数 | 次元 | ANNSの距離 | KS₂の $L$ |
| --- | ---: | ---: | --- | ---: |
| SIFT | 10,000,000 | 128 | ℓ₂ | 8 |
| GloVe1M | 1,183,514 | 200 | angular | 10 |
| Word | 1,000,000 | 300 | ℓ₂ | 15 |
| GloVe2M | 2,196,017 | 300 | angular | 15 |
| Tiny | 5,000,000 | 384 | ℓ₂ | 16 |
| GIST | 1,000,000 | 960 | ℓ₂ | 20 |

HNSWは $M=32$、構築時の $ef_c$ はSIFT・Tiny・GISTで1000、他で2000。KS₂とPEOsの $L$ を揃え、PEOsは $\epsilon=0.2$、両者の $m=256$ として比較する。[出典：付録D.1、表3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=20)

- **ANNS**：著者はHNSW比2.5–3倍、HNSW+PEOs比1.1–1.3倍のQPSを報告する。ただし図1の実験条件における結果で、Wordの高Recall領域ではScaNNが上回る。[出典：§7.2、図1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=9)
- **KS₁**：CEOsに対する改善は小さい。例えばGloVe1MのProbe@10KではRecallが63.545%から64.355%となり、差は0.810パーセントポイント。全条件で改善するわけではない。[出典：表1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)
- **構築・容量**：KS₂追加構築時間は報告条件でグラフ構築時間の25%未満。PEOs比のインデックス容量削減は序論では5%と報告する一方、実際の容量は $L$ に依存する。[出典：§1・7.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=9)
- **$L$ の調整**：増やすと参照角度が小さくなる一方、容量と判定時間が増える。著者の実験では部分空間次元 $d/L$ が約16で良好だった。全データに通用する最適値という意味ではない。[出典：§7.2、図2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=9)

## 卒研との接点・読む順序

本論文が評価するのはベクトル検索であり、ロボット制御や強化学習の実験はない。応用案は[研究メモ](../research/ks2_for_robot_rl.md)に仮説として分けて記録する。[出典：§7・付録D](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

理解は[角度判定と参照角度](../concepts/angle_testing.md) → [確率的ルーティングとKS₂](../concepts/probabilistic_routing_ks2.md) → 原論文§6.2・Algorithm 7の順に進めるとよい。
