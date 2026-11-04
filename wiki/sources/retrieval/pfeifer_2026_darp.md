---
title: "DARP：Difference-Aware Retrieval Policies for Imitation Learning"
type: source
tags: [robotics, imitation-learning, behavior-cloning, nearest-neighbor, semi-parametric-policy, inference-time-retrieval, laplacian-regularization, permutation-invariance, compounding-error]
sources:
  - ../../../raw/papers/pfeifer_2026_darp.pdf
updated: 2026-11-04
---

# DARP：Difference-Aware Retrieval Policies for Imitation Learning

## 書誌情報と要点

Quinn Pfeifer、Ethan Pronovost、Paarth Shah、Khimya Khetarpal、Siddhartha Srinivasa、Abhishek Gupta（University of Washington、Toyota Research Institute、Google DeepMind、Mila）。ICLR 2026採録。arXiv版は2606.09758v1（2026-06-08）。[出典：表紙](../../../raw/papers/pfeifer_2026_darp.pdf)

**学習データを推論時にも使う、semi-parametricな模倣学習。** 通常のBehavior Cloning（BC）では、デモは学習に使った後で捨てられる。DARPは推論時にもデモからk近傍を検索する。各近傍について、(近傍の状態 $s^*_i$、その行動 $a^*_i$、クエリとの差分 $\Delta s_i=s^*_i-s_q$) をネットワークに入れ、近傍ごとの行動候補を出す。最後に候補を順序に依存しない方法（平均など）で集約する。[出典：Abstract、§1、Fig. 1](../../../raw/papers/pfeifer_2026_darp.pdf)

- 追加データ、オンラインのexpert、タスク固有の知識は要らない。BCと同じ前提で動く。[出典：Abstract](../../../raw/papers/pfeifer_2026_darp.pdf)
- 理論面では、近傍での集約がk-NNグラフ上のLaplacian smoothing（低域通過フィルタ）に対応すると主張する。[出典：§1、§2.3 Theorem 2](../../../raw/papers/pfeifer_2026_darp.pdf)
- 実験では、BCに対して15–46%の改善を報告している。[出典：Abstract、§5](../../../raw/papers/pfeifer_2026_darp.pdf)

[VINN](pari_2022_vinn.md)は近傍行動の重み付き平均をそのまま出力する（学習パラメータなし）。DARPは、近傍との**差分を見て行動を補正するネットワーク**を学習する点が異なる。論文中ではVINN方式を「LWR」としてbaselineに含めている。[出典：§3.1、§4](../../../raw/papers/pfeifer_2026_darp.pdf)

## 問題意識

- BCは、実行中の小さな誤差が積み重なり、デモにない状態へ入る（covariate shift、[Compounding Error](../../concepts/imitation_learning/compounding_error.md)）。分布外の状態では方策の出力が不安定でばらつく。[出典：§1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 既存の対策（DAggerなど）は、シミュレータ・対話的なexpert・大量の準最適データ・タスク固有の構造など、BC以上の前提を要する。著者は「デモだけでBCのばらつきを減らせるか」を問う。[出典：§1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 統計的には、BCはexpert状態での教師あり誤差だけを最小化する。データ密度の低い領域では、方策が任意に振動しうる。近い状態には近い行動を出す「滑らかさ」を課すのが自然な対策になる。[出典：§1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 著者の整理では、**global**な方策（ACT、Diffusion Policy、π0など）は全データを1つの関数に圧縮するため分布シフトに弱い。**local**な方法（VINNなど）は頑健だが、距離の選び方に依存し、平均すると異なる行動がぼやけ、近傍を絶対的な状態でしか扱わないため汎化が限られる。[出典：§1](../../../raw/papers/pfeifer_2026_darp.pdf)

## 手法

### 1. 準備：近傍で正則化したBC（MRIL）

BCの損失に、近傍のexpert状態どうしで予測行動が近くなるよう求める項を加える。[出典：§2.2 式(1)](../../../raw/papers/pfeifer_2026_darp.pdf)

$$
L_{\mathrm{MRIL}}(f)=\underbrace{\mathbb{E}\left[\ell(f(s^*),a^*)\right]}_{L_{\mathrm{BC}}}+\lambda\,\mathbb{E}_{s^*}\Big[\sum_{i\in N_k(s^*)} w_i(s^*)\,\|f(s^*)-f(s^*_i)\|_2^2\Big]
$$

- $N_k(s^*)$ はデモ内のk近傍、$w_i$ は状態差に基づくkernel重み。[出典：§2.2](../../../raw/papers/pfeifer_2026_darp.pdf)
- 第2項はk-NNグラフのLaplacianによる二次形式 $\mathrm{Tr}(F^\top LF)$ に等しい（manifold regularization）。[出典：Appendix A.1.1 Lemma 1](../../../raw/papers/pfeifer_2026_darp.pdf)
- **Theorem 1**：(i) 推定量の分散が減る、(ii) 局所Lipschitz定数が一様に抑えられる、(iii) 閉ループでの誤差の蓄積が、BCの線形に対してMRILでは劣線形になる、と主張する。前提は、真のexpert方策が $C^2$ 級に滑らかでコンパクトな状態空間上にあること。[出典：§2.2 Theorem 1、Appendix A.1.1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 欠点は、重み $\lambda$ の調整が必要なことと、目的関数を変えるので最適化の性質が変わりうること。[出典：§2.3](../../../raw/papers/pfeifer_2026_darp.pdf)

### 2. 目的関数ではなく構造で滑らかにする（iMRIL）

平均操作を損失からモデル構造へ移す。近傍での予測の平均 $\hat f(s)=\frac1k\sum_{i\in N_k(s)}f_\theta(s^*_i)$ を通常のBC損失で学習する。推論時も、新しい状態の近傍を検索して同じ平均を取る。[出典：§2.3 式(2)](../../../raw/papers/pfeifer_2026_darp.pdf)

**Theorem 2**：近傍平均は、random-walk行列 $S=D^{-1}A$ を掛ける操作に当たる。グラフLaplacianの固有値 $\mu$ に対して、固定の減衰 $1-\mu$ をかける。MRILの解の減衰 $1/(1+\lambda\mu)$ と同じく、変化の緩やかな成分を残し、近傍間で激しく変わる成分を抑える。著者は、iMRILを $\lambda\approx1$ の正則化に相当し、調整不要なものと位置づける。[出典：§2.3 Theorem 2、Appendix A.1.2](../../../raw/papers/pfeifer_2026_darp.pdf)

著者は役割を次のように分けて説明する。ネットワーク $f_\theta$ は局所的な補正で精度（bias）を担い、平均操作はばらつき（variance）を抑える。[出典：§2.3](../../../raw/papers/pfeifer_2026_darp.pdf)

### 3. DARP：差分を入力にする

iMRILの $f_\theta$ に、近傍の状態だけでなく、近傍の行動とクエリとの差分も与える。[出典：§2.4.1 式(3)(4)](../../../raw/papers/pfeifer_2026_darp.pdf)

$$
a'_i=f_\theta\left(s^*_i,\ a^*_i,\ \Delta s_i=s^*_i-s_q\right),\qquad
\hat a_q=\frac1k\sum_{i\in N_k(s_q)}a'_i
$$

- ねらい：「状態が少しずれたとき、expertの行動がどう変わるか」を学ばせる。[出典：§2.4.1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 学習損失は $\|\hat a_q-a^*_q\|^2$ の通常の回帰。$f_\theta$ はMLPやCNNでよい。[出典：§2.4.1 式(5)](../../../raw/papers/pfeifer_2026_darp.pdf)
- 学習時も、各クエリ $(s^*_q,a^*_q)$ についてデモ全体から近傍を検索する。[出典：Appendix A.3 Algorithm 1](../../../raw/papers/pfeifer_2026_darp.pdf)

### 4. 平均以外の集約

平均は、順序に依存しない集約関数 $g_\psi$ の特別な場合である。Set TransformerやDeepSetsで $g_\psi$ を学習でき、Gaussian Mixture Modelの係数やdiffusionのscoreなど、多峰的な行動分布のパラメータを出力させることもできる。[出典：§2.4.2 式(6)](../../../raw/papers/pfeifer_2026_darp.pdf)

### 5. 近傍検索の距離

- 事前学習済み埋め込み空間でのEuclidean距離を使う。[出典：§2.4.1 脚注3](../../../raw/papers/pfeifer_2026_darp.pdf)
- 実験では、過去の状態履歴も比べる。lookback $\ell$ と減衰率 $\gamma$ を使い、クエリ軌跡と、デモ軌跡上の対応時刻の状態を比較する。[出典：Appendix A.2.1](../../../raw/papers/pfeifer_2026_darp.pdf)

$$
d(s_q,s^*_i)=\sum_{n=0}^{\ell-1}\|s_{q,-n}-s^*_{j,t-n}\|\,e^{-\gamma n}
$$

- 近傍検索の実装（全件探索か、ANN索引か）は本文・付録に記載がない。[出典：§2.4、Appendix A.2.1、A.4](../../../raw/papers/pfeifer_2026_darp.pdf)

## 実験

### 設定

- **環境**：MuJoCo（Hopper、Walker、Ant、HalfCheetah）、Robosuite（Stack、Threading、Square Peg）、RoboCasa（Drawer、Door、Stove）、実機FurnitureBenchのsquare table組み立て。Robosuite・RoboCasaのデータはMimicGenで生成。[出典：§3.1、§3.2、Fig. 3–5](../../../raw/papers/pfeifer_2026_darp.pdf)
- **比較**：R&P（最近傍の行動をそのまま実行）、LWR（VINN方式の局所重み付き回帰）、BC、REGENT（検索した近傍を入れるTransformerのin-context学習）、MRIL。[出典：§3.1](../../../raw/papers/pfeifer_2026_darp.pdf)
- MuJoCo・Robosuiteのデモは、最適なRL方策で収集したもの。[出典：Appendix A.2.8](../../../raw/papers/pfeifer_2026_darp.pdf)

### 低次元状態での結果（Q1）

MuJoCo（スコア、100試行平均、95%信頼区間）[出典：Table 1](../../../raw/papers/pfeifer_2026_darp.pdf)

| 手法 | Hopper | Ant | Walker | HalfCheetah |
| --- | --- | --- | --- | --- |
| R&P | 711.82 | -305.97 | 419.18 | -178.64 |
| LWR（VINN方式） | 1703.78 | 846.59 | 1484.91 | 1945.82 |
| BC | 2313.65 | 2376.20 | 2658.40 | 1063.23 |
| REGENT | 1819.39 | -302.10 | 507.01 | 169.85 |
| MRIL | 2793.63 | 3869.08 | 4370.96 | 701.58 |
| **DARP** | **3545.57** | **4383.28** | **4894.01** | **5515.41** |
| DARP Set Transformer | 2965.86 | 4063.79 | 4752.42 | 3417.85 |

操作タスク（成功率%、シミュレーション100試行・実機50試行）[出典：Table 2](../../../raw/papers/pfeifer_2026_darp.pdf)

| 手法 | Drawer | Door | Stove | Stack | Threading | Peg | 実機Sq. Table |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC | 54 | 29 | 28 | 47 | 37 | 46 | 44 |
| DARP | 85 | 45 | 43 | 72 | 63 | 62 | 92 |

- この実験では集約関数 $g$ は単純平均。[出典：§3.2](../../../raw/papers/pfeifer_2026_darp.pdf)
- 純粋なnon-parametric手法（R&P・LWR）はBCより悪い。[出典：§3.2](../../../raw/papers/pfeifer_2026_darp.pdf)
- シミュレーションはMLP、実機はDiffusion Policyを使用。表の注は「Section 8」を参照先とするが、本文にSection 8は見当たらない。Diffusion Policyとの組み合わせはAppendix A.2.7で扱われている。[出典：Table 1・2注、Appendix A.2.7](../../../raw/papers/pfeifer_2026_darp.pdf)

### 画像特徴・多峰的な行動（Q2）

- R3MのRobosuite画像埋め込みを状態として使う。成功率はStack 44→75%、Threading 38→76%、Peg 17→52%（BC→DARP）。平均の改善幅（約35%）は、低次元状態のRobosuite（約22%）より大きい。[出典：§3.3、Table 3](../../../raw/papers/pfeifer_2026_darp.pdf)
- Push-T：Set TransformerでGMMの係数を出すDARPが、BC 48に対し70。[出典：Appendix A.2.2、Table 4](../../../raw/papers/pfeifer_2026_darp.pdf)

### 構成要素の検証（Q3、Robosuite Stack、100試行）

| 入力・構成 | 成功率 |
| --- | --- |
| $(s^*_i,a^*_i,s^*_i-s_q)$（DARP） | 0.72 |
| $(s^*_i,s^*_i-s_q)$（近傍行動なし） | 0.67 |
| BC 10個のensemble | 0.59 |
| ランダムなk件 | 0.58 |
| $(s^*_i,a^*_i,\|s^*_i-s_q\|_2)$（差分をノルムだけに） | 0.53 |
| BC | 0.47 |
| $(s^*_i,a^*_i,s_q)$（差分の代わりにクエリ状態） | 0.42 |
| 順序に依存する集約 | 0.19 |

[出典：Fig. 6](../../../raw/papers/pfeifer_2026_darp.pdf)（数値はFig. 6の棒グラフのラベル）

- 差分ベクトルと順序に依存しない集約の寄与が大きい。近傍行動の寄与は比較的小さい。[出典：§3.4](../../../raw/papers/pfeifer_2026_darp.pdf)
- 差分をノルムだけにすると大きく下がる。差分の**方向**の情報が効いていると読める（この解釈は本Wikiの推測であり、著者は差分ベクトルが重要とだけ述べる）。

### 分布外への頑健性

- BCが失敗しDARPが成功する試行で、両者の報酬が分かれる時点（SoD）を調べた。2タスク計6試行のすべてで、その時点の状態は学習データに対して低尤度（分布外）だが、差分 $\Delta s$ は学習時に見た範囲内（高尤度）だった。著者は、差分で表すことで「少し分布外」の状態でも予測できる、と解釈している。[出典：§3.4、Fig. 7](../../../raw/papers/pfeifer_2026_darp.pdf)
- BCを失敗するまで走らせ、10ステップごとに環境を複製してDARPに切り替える実験。BCがずれた状態からでも、DARPは途中まで高スコアに回復できた。[出典：Appendix A.2.4、Fig. 12](../../../raw/papers/pfeifer_2026_darp.pdf)
- 近い状態で正反対の行動が必要な迷路（D4RL Umazeの改変）でも、BC 25%に対しDARP 57%。[出典：Appendix A.2.3、Table 5](../../../raw/papers/pfeifer_2026_darp.pdf)

### その他の付録実験

- **CCILとの比較**（MuJoCo、BCからの相対改善。CCILの値はCCIL論文の報告値）：Hopper 32.6% vs 53.2%、Walker 84.1% vs 84.1%、Ant 12.6% vs 84.5%、HalfCheetah 5.4% vs 418.7%（CCIL vs DARP）。[出典：Appendix A.2.5、Table 6](../../../raw/papers/pfeifer_2026_darp.pdf)
- **距離の種類**：R3M特徴のStackで、Euclidean 75%、cosine 70%、BC 47%。[出典：Appendix A.2.6、Table 7](../../../raw/papers/pfeifer_2026_darp.pdf)
- **Diffusion Policyとの組み合わせ**（50試行、デモ数はTable 2より少ない）：[出典：Appendix A.2.7、Table 8](../../../raw/papers/pfeifer_2026_darp.pdf)

| 手法 | Stack | Threading | Peg |
| --- | --- | --- | --- |
| BC（MLP） | 34 | 12 | 28 |
| DARP（MLP） | 62 | 38 | 40 |
| Diffusion | 52 | 44 | 54 |
| DARP w/ Diffusion | 82 | 72 | 66 |

- **人のデモ**：Stackを人のデモで学習すると、BC 45%、DARP 60%。[出典：Appendix A.2.8、Table 10](../../../raw/papers/pfeifer_2026_darp.pdf)

### 検索のハイパーパラメータ

- 近傍数kが小さいと性能が悪い。Stackではk≈500で最大となり、kをデータ全体に近づけるとBCをわずかに上回る程度に落ち着く。[出典：Appendix A.2.1、Fig. 9](../../../raw/papers/pfeifer_2026_darp.pdf)
- 履歴（lookback）をほとんど使わない場合と、過去の減衰を強くしすぎた場合は、BCより悪くなる。[出典：Appendix A.2.1、Fig. 9](../../../raw/papers/pfeifer_2026_darp.pdf)
- 検証損失でエポックと検索ハイパーパラメータを選ぶと、BCより良い設定を選べた（Hopper 507.49→805.69、Stack 0.12→0.31）。[出典：Appendix A.2.9、Table 11](../../../raw/papers/pfeifer_2026_darp.pdf)

### 計算時間

| 環境（データ点数） | 設定 | 学習（s/epoch） | 推論（s/step） |
| --- | --- | --- | --- |
| Hopper（1,000） | BC | 0.102 | 0.00127 |
| | k=500 | 0.130 | 0.00419 |
| Stack（4,200） | BC | 0.431 | 0.00139 |
| | k=500 | 0.559 | 0.00437 |
| | k=2000 | 0.758 | 0.00451 |

- kを増やしても計算時間の増え方は緩やか。Stackでk=500のとき推論は約0.0044秒で、230 Hz超の制御周期に当たる。[出典：Appendix A.4、Table 12](../../../raw/papers/pfeifer_2026_darp.pdf)
- 同じ表のデータ点数は数千規模である。数十万点を超えるデータでの検索時間は評価されていない。[出典：Appendix A.4、Table 12](../../../raw/papers/pfeifer_2026_darp.pdf)
- DARP（MLP）はDiffusion Policyより学習で約10倍、推論で約36倍速い。[出典：Appendix A.2.7、Table 9](../../../raw/papers/pfeifer_2026_darp.pdf)

## 関連研究での位置づけ（著者の整理）

- **Non-parametric IL**：VINN、MiDiGaP、SEABO、FlowRetrieval、STRAP、[Behavior Retrieval](du_2023_behavior_retrieval.md)。DARPは $(s^*_i,a^*_i,s^*_i-s_q)$ の組で近傍を表し、semi-parametricな方策を学習する点で異なる。[出典：§4](../../../raw/papers/pfeifer_2026_darp.pdf)
- **滑らかさの制約**：L2C2、CCILなど。DARPは損失ではなく構造で滑らかさを課す。[出典：§4](../../../raw/papers/pfeifer_2026_darp.pdf)
- **In-context学習**：REGENT、DPT、ICRT、Instant Policy、KAT。これらは新タスクへの素早い適応が目的で、DARPは通常の模倣学習での性能と安定性が目的。[出典：§4](../../../raw/papers/pfeifer_2026_darp.pdf)

## 読むときの注意

- 理論（Theorem 1・2）は、近傍平均の形（iMRIL）について述べる。差分入力やSet Transformerの集約を加えたDARP全体に、同じ保証がそのまま成り立つとは示されていない。[出典：§2.3–2.4](../../../raw/papers/pfeifer_2026_darp.pdf)
- 主な比較相手はMLPのBCである。ACTのようなaction chunkingを持つ方策との比較はない。[出典：§3、Appendix A.2.7](../../../raw/papers/pfeifer_2026_darp.pdf)
- 定式化と疑似コードでは、1つのクエリ状態に1つの行動を予測する。行動列（chunk）を出す設定の記載はない。[出典：§2.4、Algorithm 1](../../../raw/papers/pfeifer_2026_darp.pdf)

## 研究計画との関係

[現在の研究計画](../../../lab/research_policy/20261104_inference_time_retrieval_act.md)の§12は、DARPを「検索とネットワークを併用するだけでは十分な差分にならない」根拠として挙げている。論文から確認できる事実は次のとおり。

- 推論時にデモから近傍を検索し、ネットワークと組み合わせて行動を出す方法として、DARPが既にある。[出典：§2.4、Algorithm 1](../../../raw/papers/pfeifer_2026_darp.pdf)
- DARPは毎ステップ必ず検索する。信頼度に応じて検索を起動する仕組みや、既存方策（ACTなど）との重み付き混合は扱っていない。[出典：§2.4、Algorithm 1](../../../raw/papers/pfeifer_2026_darp.pdf)
- 近傍検索の索引・高速化手法は記載がなく、データ規模も数千点まで。[出典：Appendix A.4](../../../raw/papers/pfeifer_2026_darp.pdf)

計画にとっての意味づけ（新規性・採否）は本Wikiでは判断しない。

## 関連ページ

- [推論時検索による行動推定：VINNとDARP](../../concepts/retrieval/inference_time_retrieval_policies.md)
- [VINN](pari_2022_vinn.md)
- [Behavior Cloning](../../concepts/imitation_learning/behavior_cloning.md)
- [Compounding Error](../../concepts/imitation_learning/compounding_error.md)
- [Diffusion Policy](../imitation_learning/chi_2023_diffusion_policy.md)
- [Retrieval-augmented Imitation Learning](../../concepts/retrieval/retrieval_augmented_imitation_learning.md)
- [HNSW](../../concepts/vector_search/hnsw.md)
