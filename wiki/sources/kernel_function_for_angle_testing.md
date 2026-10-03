---
title: "Probabilistic Kernel Function for Fast Angle Testing"
type: source
tags: [ANNS, HNSW, angle-testing, random-projection, KS1, KS2]
sources:
  - ../../raw/papers/kernel_function_for_angle_testing.pdf
updated: 2026-10-03
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

## 論文全体の論理の流れ

この論文は、安い確率的な判定関数を設計する理論と、その関数を検索のどこに挿入するかという実装をつなぐ。正確な内積は候補1件につき $O(d)$ かかるが、欲しい情報が候補の順位や閾値との比較だけなら、すべての候補に対して正確な値を求める必要があるとは限らない。これがProblem 1.1・1.2の出発点である。[出典：§1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=1)

| 論文の段階 | 問い | 得られるもの |
| --- | --- | --- |
| §1–2 | 既存のガウス射影理論の制約は何か | 射影数が無限大へ向かう漸近条件への問題提起 |
| §3 | 何を使って判定するか | クエリ側の代表方向を使うKS₁、データ側を使うKS₂ |
| §4 | 何が判定精度を決めるか | 参照角度を条件とする有限次元の分布と成功確率 |
| §5 | 良い参照方向を安く表現できるか | 対蹠点・cross-polytope・部分空間分割 |
| §6 | 検索のどこを高速化するか | KS₁の候補抽出、KS₂のグラフrouting |
| §7・付録D | 実際にどれだけ改善するか | MIPSのRecallとANNSのRecall–QPS評価 |

表は論文の構成に沿った整理である。参照角度の理論だけでも、HNSWへの組み込みだけでもなく、その間にある射影配置の設計までが本論文の提案範囲となる。[出典：§1–7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=2)

## 関連手法の中での位置づけ

SimHashはランダム超平面による符号、Falconnは近い射影方向のIDをハッシュとして使う。CEOsは極端な射影値を持つ方向を利用し、その方向への別ベクトルの射影から内積を推定する。KS₁はこの候補順位の推定を参照角度の小さい配置で改善する。一方、PEOsはqueryとdataの役割の入れ替えと部分空間分割を用い、グラフ探索の候補選別を行う。KS₂は参照角度による補正を加えた閾値判定に対応する。[出典：§2–3、付録C.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=3)

RaBitQについても、論文はKS₂との関連を述べる。射影構造を $m=2,L=d$ とした場合に対応し、超立方体とスカラー量子化を選ぶと関連する推定器に帰着する。ただしこの構造上の対応から、実装全体や検索性能が同じとは言えない。論文は $L$ による記憶容量と検索速度のバランスを重視する。[出典：§3 Remarks、付録C.3](../../raw/papers/kernel_function_for_angle_testing.pdf#page=18)

## 理論から実装へ：2つの利用方法

### KS₁によるMIPS候補抽出

Algorithm 5では各射影方向に対し、全データを射影値の大きい順に並べたリストを構築する。Algorithm 6ではクエリに近い上位 $s_0$ 個の射影方向を選び、それぞれのリストから上位Probe件を走査する。走査した候補の内積は正確に計算し、その中からtop-kを返す。KS₁の役割は有望な候補を先に集めることで、最終的な内積計算を全面的に置き換えることではない。[出典：§6.1、Algorithm 5–6](../../raw/papers/kernel_function_for_angle_testing.pdf#page=19)

主実験は $m=2048,L=1,s_0=5,k=10$、ランダム射影の偏りを抑えるため10回の平均を報告する。例えばWordのProbe@100ではCEOsの71.471%に対してS_polのKS₁は72.078%で、改善は0.607パーセントポイント。GloVe1MのProbe@10Kでは0.810パーセントポイントとなる。この改善量はANNSのQPSの2.5–3倍という結果と別の評価である。[出典：表1、§7.1](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

### KS₂によるグラフ探索の選別

KS₂はデータベクトル自体だけでなく、訪問ノードから隣接ノードへの辺方向に適用する。現在の結果リストを改善する距離条件を辺とクエリの内積閾値に変換し、射影テーブルから計算したKS₂で選別する。通過した候補は正確な距離で評価し、必要なら結果リスト・探索キューに加える。[出典：§6.2、式(9)、Algorithm 7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

したがって、KS₂は既存グラフのroutingを変える提案である。付録C.3はグラフ検索の改善を辺選択・routing・ベクトル量子化に整理し、これらは一般に組み合わせ得るとしている。今回の実験はHNSWに加えNSSGにも組み込むが、新しいグラフ構築法やロボットの学習アルゴリズムを提案しているわけではない。[出典：付録C.3・D.5](../../raw/papers/kernel_function_for_angle_testing.pdf#page=18)

## 付録まで含めた実験の読み方

主実験の $k=10$ だけでなく、付録D.3は $k=1,100$ のRecall–QPS曲線を示す。$k=1$ ではWord・GloVe1M・GloVe2M・TinyでScaNNが良好で、著者はHNSWの接続性の問題が一因と説明する。この結果から、本論文の高速化率をすべてのkやRecall領域へ一律に拡張することはできない。[出典：付録D.3、図6–7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=20)

付録D.5のNSSG実験では、GISTを除くデータセットでNSSG+KS₂がNSSG+PEOsを上回ると著者は述べる。HNSW以外でも利用できることを支持するが、全条件で優位という結果ではない。付録D.2ではKS₁の $s_0$ を2・10に変えた追加評価を行い、S_polが多くの条件で高いRecallを示す。[出典：付録D.2・D.5、表4–5、図9](../../raw/papers/kernel_function_for_angle_testing.pdf#page=20)

追加構築時間はWord 42秒、GloVe1M 164秒、GIST 165秒、GloVe2M 188秒、SIFT 366秒、Tiny 508秒と報告する。これはグラフ構築後の辺の整列・KS₂テスト構造の追加に必要な時間である。検索速度を比較する際は、前処理時間と追加インデックス容量も含めて利用状況に合うか考える必要がある。[出典：§7.2](../../raw/papers/kernel_function_for_angle_testing.pdf#page=9)

図5は参照角度の余弦の下界を数値計算した図であり、検索Recallを直接測った実験ではない。射影数 $m$ の線形増加に比べ、部分空間数 $L$ の増加が参照余弦を大きくするという設計理由を示す。一方、図2・8は実際の容量と検索速度のトレードオフを示す。この2種類の図を合わせて、理論上の判定精度と実装コストを評価する。[出典：付録C.5、図2・5・8](../../raw/papers/kernel_function_for_angle_testing.pdf#page=19)

## 本論文から言えることと残る課題

論文が示したのは、参照角度によって有限次元の判定分布を記述できること、配置の工夫でその判定を改善できること、そして評価した静的ベクトル検索でグラフroutingを高速化できることである。一方、$(\delta,0.5)$-routingは閾値内の隣接候補に関する局所的保証であり、量子化を含む実装の検索全体やロボットタスクの成功率を保証するものではない。[出典：補題4.2–4.3、系6.2、§7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=7)

卒研への接続では、検索部分が学習時間のどれだけを占めるか、必要なRecall、埋め込みの更新頻度を先に調べるとよい、というのが本Wikiの研究上の提案である。これは本論文の実証結果ではなく、辺ごとの前計算と確率的な候補棄却を強化学習に持ち込む際の未検証の検討事項である。[着想元：§5–7](../../raw/papers/kernel_function_for_angle_testing.pdf#page=6)

## 卒研との接点・読む順序

本論文が評価するのはベクトル検索であり、ロボット制御や強化学習の実験はない。[出典：§7・付録D](../../raw/papers/kernel_function_for_angle_testing.pdf#page=8)

理解は[角度判定と参照角度](../concepts/angle_testing.md) → [参照角度による確率解析](../concepts/reference_angle_probability.md) → [射影配置と部分空間分割](../concepts/projection_configuration_ks.md) → [確率的ルーティングとKS₂](../concepts/probabilistic_routing_ks2.md)の順に進めるとよい。原論文は§3–6を対応させて読み、付録A・Bで理論、付録C.4・Dでアルゴリズムと実験を確認する。
