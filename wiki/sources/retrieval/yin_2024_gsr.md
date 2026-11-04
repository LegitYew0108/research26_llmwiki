---
title: "GSR：Offline Imitation Learning Through Graph Search and Retrieval"
type: source
tags: [robotics, imitation-learning, offline-learning, suboptimal-demonstrations, graph-search, retrieval, sample-weighting, trajectory-stitching, diffusion-policy, R3M]
sources:
  - ../../../raw/papers/yin_2024_gsr.pdf
updated: 2026-11-04
---

# GSR：Offline Imitation Learning Through Graph Search and Retrieval

## 書誌情報と要点

Zhao-Heng Yin、Pieter Abbeel（UC Berkeley EECS）。[出典：表紙](../../../raw/papers/yin_2024_gsr.pdf)

- 保存したPDFには掲載先の記載がない。[arXiv（2407.15403、2024-07-22）](https://arxiv.org/abs/2407.15403)のコメント欄によると、RSS 2024採録論文である。
- 保存PDFは本文と参考文献の11ページで、本文中で参照される付録（実装の詳細、デモ数、追加の可視化）は含まれていない。

**質の低い部分を含む人のデモから、良い行動だけを強めて学習する。** 次の3段階で行う。[出典：Abstract、§I、Fig. 2](../../../raw/papers/yin_2024_gsr.pdf)

1. 事前学習済みの視覚表現で、似た状態をデモ間でつなぎ、データ全体をグラフにする。
2. グラフ上の最短経路でゴールまでの距離を求め、各遷移の良さ（value）とする。
3. 各状態の近傍を検索し、似ていて価値の高い遷移に重みを再配分する。その重み付きデータでBehavior Cloning（BC）を行う。

**グラフと検索を使うのは学習前の前処理だけ**で、実行時の方策はグラフを使わない。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)

## 問題設定

**データ**：オフライン方策学習の設定。データ $D$ はタスクに関係する人の操作軌跡 $\tau=(o_0,a_0,\dots,o_T,a_T)$ の集合で、**各軌跡は最終的にタスクに成功している**。ただし途中には、失敗した把持のやり直し、遅い動き、細かな修正など、質の低い行動が含まれ得る。学習にオンラインの環境操作は使わない。[出典：§I、§III-A](../../../raw/papers/yin_2024_gsr.pdf)

**ねらい**：デモ中の良い区間をつなげて、より良い方策を得ること。強化学習ではtrajectory stitchingと呼ばれる。[出典：§I](../../../raw/papers/yin_2024_gsr.pdf)

**既存手法への問題意識**：offline deep RLでも原理的には可能である。しかし著者は次のように述べる。[出典：§I、§II](../../../raw/papers/yin_2024_gsr.pdf)
- deadly triadにより不安定になりやすい。
- 画像入力で長いhorizonのタスクではBCを上回れないことが多い、という先行研究がある。

GSRはBellman更新による深い価値関数の学習を避け、グラフ探索で価値を直接求める。

**定式化**：多くのオフライン方策学習は、重み付き対数尤度 $L(\theta)=\mathbb E_{(o,a)\sim D}[w(o,a)\log\pi_\theta(a\mid o)]$ を最大化する形で書ける。[出典：§III-B、式(1)](../../../raw/papers/yin_2024_gsr.pdf)
- $w=1$ ならBC。
- $w=\exp(A(o,a))$ ならAWR・IQLの方策抽出。
- GSRはこの $w(o,a)$ を、グラフ探索と検索で決める。

## 手法

### 考え方（表形式の場合）

ゴール観測 $o_g$ へ最短で到達したいとき、各観測で選ぶべき行動は、遷移先からゴールまでの距離 $d(o_a,o_g)$ が最小のものである。$w(o,a)=\mathbf 1[a=a^*]$ とすれば、最適でない行動を落として最適な行動だけを学べる。[出典：§IV-A、式(2)](../../../raw/papers/yin_2024_gsr.pdf)

ただし連続制御のデータでは、各観測は一度しか現れない。このため次の2つの問題が生じる。[出典：§IV-A](../../../raw/papers/yin_2024_gsr.pdf)
1. 異なる軌跡上の似た状態がつながらず、距離の推定が不正確になる。
2. 各観測の候補行動が1つしかなく、argminが意味をなさない（全部の重みが1になる）。

GSRは、1をグラフ構築（似た状態の接続）で、2を近傍検索による候補集合の近似で解決する。

### 1. グラフの構築

**頂点**：各軌跡から $n$ ステップおきに観測を取り、頂点 $v_0,v_1,\dots$ とする。間引くのは、隣接頂点の見た目が同じにならないようにするため。仮想的なゴール頂点 $g$ も加える。[出典：§IV-B-1](../../../raw/papers/yin_2024_gsr.pdf)

**dataset edge**：同じ軌跡の次の頂点へつなぐ有向辺で、重みは1。成功した軌跡の最後の頂点は $g$ へつなぐ。世界のダイナミクスの近似にあたる。[出典：§IV-B-2](../../../raw/papers/yin_2024_gsr.pdf)

**augmented edge**：軌跡をまたいで似た状態を双方向につなぐ辺。[出典：§IV-B-2、式(3)–(5)、Fig. 3](../../../raw/papers/yin_2024_gsr.pdf)
- 事前学習済みencoder $f_\theta$ の特徴 $f_v$ を使う。類似度は負のL2距離 $\mathrm{sim}(x,y)=-\|x-y\|_2$。
- まず各頂点について、1ステップ前後の頂点との類似度の小さい方を $\mathrm{Tol}_{raw}$ とする。それを特徴空間のM近傍で平均し、許容範囲 $\mathrm{Tol}(v_i)$ とする。M近傍は全軌跡から求める。
- $\mathrm{sim}(f_{v_i},f_{v_j})>\alpha\max\{\mathrm{Tol}(v_i),\mathrm{Tol}(v_j)\}$ のとき2頂点をつなぐ。つまり互いの許容範囲に入る場合である。
- $\alpha$ は1前後に設定する。直感的には「互いに1ステップで届く範囲」を意味する。
- augmented edgeの距離重みは、保存本文には明記されていない。

**グラフの位置づけ**：このグラフは**ノンパラメトリックなworld model**として働き、ある区間がゴールへ効率よく到達するかを推論できる。[出典：§I](../../../raw/papers/yin_2024_gsr.pdf)

### 2. グラフ探索による価値

遷移 $v_i\to v_{i+1}$ の価値を、グラフ上の最短距離で $\tilde Q(v_i)=-1-d(v_{i+1},g)$ と定義する。[出典：§IV-C](../../../raw/papers/yin_2024_gsr.pdf)

### 3. 検索による重みの再配分

各頂点 $v$ について、特徴空間のK近傍 $N_K(v)$ を検索し、$N(v)=\{v\}\cup N_K(v)$ とする。$v$ が本来持つ重み1を、$N(v)$ の各頂点 $u$ に次の比率で配る。[出典：§IV-C、式(6)–(7)、Algorithm 1](../../../raw/papers/yin_2024_gsr.pdf)

$$
w_{alloc}(u)\mid_v=\frac{\exp[\beta_1S(u,v)+\beta_2\tilde Q(u)]}{\sum_{u'\in N(v)}\exp[\beta_1S(u',v)+\beta_2\tilde Q(u')]}
$$

- $S(u,v)=\frac12\left(\frac1{|\mathrm{Tol}(u)|}+\frac1{|\mathrm{Tol}(v)|}\right)\mathrm{sim}(f_u,f_v)\le0$ は、1ステップ近傍の距離で正規化した類似度。
- 着想元はLocally Weighted Regressionで、重みは「類似度×価値の指数」に比例する。
- 全頂点について配り終えた合計 $w[v_i]$ を、区間 $(o_{in:(i+1)n},a_{in:(i+1)n})$ のデータ重みにし、式(1)で方策を学習する。
- $\beta_1\to\infty$ かつ $\beta_2\to0$ のとき、重みは $v$ 自身に集中し、通常のBCに戻る。$\beta_1$・$\beta_2$ により、積極的な方策改善とBCの間を連続的に調整できる。

### 実装と計算量

- **特徴**：R3Mを使う。著者は、contrastiveな目的で事前学習されていて細かな動きをよく表せるため、と説明する。複数カメラの場合は各画像の埋め込みを連結する。[出典：§IV-D](../../../raw/papers/yin_2024_gsr.pdf)
- **fine-tuning（任意）**：デモデータでtime-contrastive学習による追加学習もできる。シミュレーション実験では、ハイパーパラメータ選択への頑健性が上がったという。[出典：§IV-D、Algorithm 1](../../../raw/papers/yin_2024_gsr.pdf)
- **計算量**：$O(N\log N+|E|)$（$N$ はデータ数、$|E|$ は辺数）。[出典：§IV-D](../../../raw/papers/yin_2024_gsr.pdf)
- **追加時間**：fine-tuningなしの場合、BCに比べた追加時間（Algorithm 1の2–9行）は、実験では概ね10分未満。§Iは前処理の追加時間をデータセット次第で10〜30分と記しており、条件の違いに注意する。[出典：§I、§IV-D](../../../raw/papers/yin_2024_gsr.pdf)
- **近傍探索の方法**：K近傍・M近傍の検索方法（全探索かANN索引か）は保存本文に記載がない。

## 実験

**比較の条件**：方策モデルは、DPとIQL-DPとGSRですべて同じDiffusion Policy（DP）を使う。[出典：§V-B](../../../raw/papers/yin_2024_gsr.pdf)
- 画像ごとにResNet-18で処理し、関節位置と連結して、Transformerのdenoiserで行動を生成する。
- 推論はDDIMで行う。
- 比較手法：DP（BC）、IQL-DP（R3M特徴でIQLを学び、方策をDPにしたもの）。

### シミュレーション：robomimic（画像入力）

- **タスク**：Can（Worse-Okay20／Worse-Better20）、Nut Assembly（Worse-Okay50／Worse-Better50）、Transport（MH）。WorseなどはデモをWorse・Okay・Betterの質で分けたもので、数字は質の高いデータを混ぜた割合（%）。[出典：§V-A-1](../../../raw/papers/yin_2024_gsr.pdf)
- **評価**：3 seed、各seedで最後の5 checkpointを各50試行で評価。評価指標は次の3つ。[出典：§V-A-3、Table I](../../../raw/papers/yin_2024_gsr.pdf)
  - 成功率（SR）
  - Time-to-success（TTS）：成功した試行だけの平均完了時間
  - Normalized Proficiency（NP）：最も速い操作者のTTSを1、最も遅い操作者を0として正規化したもの

| タスク | DP SR | IQL-DP SR | GSR SR | DP NP | GSR NP |
| --- | --- | --- | --- | --- | --- |
| Can (WO) | 0.77 | 0.77 | 0.85 | 0.46 | 0.86 |
| Can (WB) | 0.80 | 0.81 | 0.87 | 0.47 | 0.76 |
| Nut Assembly (WO) | 0.44 | 0.40 | 0.53 | 0.48 | 1.16 |
| Nut Assembly (WB) | 0.48 | 0.46 | 0.57 | 0.62 | 0.88 |
| Transport | 0.53 | 0.53 | 0.67 | 0.54 | 0.63 |

[出典：Table I](../../../raw/papers/yin_2024_gsr.pdf)

著者の解釈：[出典：§V-C](../../../raw/papers/yin_2024_gsr.pdf)
- NPの改善はCan・Nut Assemblyで30〜50%。
- 成功率の改善は、最も難しい双腕・長horizonのTransportで最大（約14%）。Nut Assemblyなどでは5〜10%と小さい。
- 使ったデモはすべて最終的に成功しており、質の低さは主に遅い動きや小さな修正によるものなので、成功率への悪影響が小さい、と推測している。

### 実機：UR5＋Robotiq gripper

- **タスク**：Pushing、Spoon Scooping、Tying a Rubber Band、Tweezer Manipulation。[出典：§V-A-2、Fig. 4–5](../../../raw/papers/yin_2024_gsr.pdf)
- **データ**：デモはGELLOで収集。カメラは2〜3台（256×256 RGB）で、関節位置も入力に使う。デモ数は付録にあり、保存PDFには含まれない。
- **評価**：3 seedの最後のcheckpointを、各30試行で評価。[出典：Table II](../../../raw/papers/yin_2024_gsr.pdf)

| タスク | DP SR | IQL-DP SR | GSR SR | DP TTS（秒） | GSR TTS（秒） |
| --- | --- | --- | --- | --- | --- |
| Pushing | 0.58 | 0.82 | 0.95 | 12.0 | 7.8 |
| Spoon Scooping | 0.63 | 0.67 | 0.81 | 30.2 | 24.0 |
| Band Tying | 0.57 | 0.57 | 0.86 | 34.8 | 22.5 |
| Tweezer | 0.48 | 0.46 | 0.76 | 41.2 | 29.7 |

[出典：Table II](../../../raw/papers/yin_2024_gsr.pdf)

著者の観察：baselineは、デモ収集中の人の失敗動作を繰り返すことが多い。人のやり直し動作をまねて回復する場合もあるが、行き詰まったり分布外に出たりして失敗することも多い。[出典：§V-D](../../../raw/papers/yin_2024_gsr.pdf)

### 重みの可視化とハイパーパラメータ

- **重みの可視化**：[出典：§V-E、Fig. 8](../../../raw/papers/yin_2024_gsr.pdf)
  - 失敗につながる区間は重みが下がる。
  - 失敗からの回復動作は、その状態ではデータどおりに進むのが最善なので、弱められない。
  - 熟練した区間は強められ、遅い動きの区間はやや弱められる。
- **$\beta_1$・$\beta_2$**：$\beta_1$ を下げる（似ていない候補も使う）、または $\beta_2$ を上げる（価値の高い候補に寄せる）と、広い範囲で成功率・熟練度が上がった。ただし極端にすると、学習に使うデータが減って成功率が下がる。著者は、データが覆う狭い範囲では熟練しても、そこから外れると解けなくなる、と説明する。[出典：§V-F-a、Fig. 6–7](../../../raw/papers/yin_2024_gsr.pdf)
- **$\alpha$**：[出典：§V-F-b、Fig. 9](../../../raw/papers/yin_2024_gsr.pdf)
  - 小さすぎるとaugmented edgeの多くが消え、大きすぎると遠い状態までつながる。どちらも距離推定を悪くする。
  - 調整法として、誤った辺（大きく異なる状態の接続）を可視化で確認し、誤り率が閾値以下となる大きめの $\alpha$ を選ぶ方法を挙げている。

## 関連研究との違い（著者の整理）

- **グラフを方策に組み込む研究との違い**：そうした研究は、推論時にグラフ上でエージェントの位置を特定し、次のsubgoalを探索する（グラフを高レベルのplannerとして使う）。GSRはグラフをオフラインの価値推定だけに使い、推論時のplannerにはしない。著者は、plannerは展開時に不適切な次のゴールを選ぶなど、汎化や頑健性に欠けることがあると述べる。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)
- **グラフの作り方の違い**：既存研究は、収集データで到達可能性を判定するネットワークを専用に学習してグラフを作る。GSRは事前学習済み表現でグラフを作り、著者はこれを初めての試みと位置づける。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)
- **[VINN](pari_2022_vinn.md)などとの違い**：VINNなどは、検索を学習済みBC方策の一部として使う。GSRは検索をサンプルの重み付けに使う。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)
- **[Behavior Retrieval](du_2023_behavior_retrieval.md)との違い**：Behavior Retrievalは、タスク非依存のデータから関連する遷移を探す。GSRは、検索を方策改善の操作として使う点で踏み込んでいる、と著者は述べる。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)

## 限界と今後の課題（著者の記述）

- 方法の性能は表現の質に依存する。[出典：§VI](../../../raw/papers/yin_2024_gsr.pdf)
- 同じ作業空間で集めたデモを対象としており、背景などの異なる文脈をつなぐ表現は今後の課題。[出典：§VI](../../../raw/papers/yin_2024_gsr.pdf)
- 接続は1ステップの範囲に限られる。事前学習済みの順方向予測モデルで、より長い接続を作ることが今後の候補。[出典：§VI](../../../raw/papers/yin_2024_gsr.pdf)
- 価値はゴールまでのグラフ距離で定義する、goal-conditionedな設定を主に扱う。[出典：§II](../../../raw/papers/yin_2024_gsr.pdf)

## 研究計画との関係

[現在の研究計画](../../../lab/research_policy/20261104_inference_time_retrieval_act.md)で「グラフ」は、HNSWなどのベクトル索引を指す（計画§3）。保存本文から確認できる事実は次のとおり。

- GSRのグラフは、デモの状態をつないで遷移を表すworld modelであり、近傍探索を高速化するための索引ではない。[出典：§I、§IV-B](../../../raw/papers/yin_2024_gsr.pdf)
- 検索とグラフ探索は学習前のデータ重み付けに使い、実行時の行動決定には使わない。[出典：§II、Algorithm 1](../../../raw/papers/yin_2024_gsr.pdf)
- K近傍・M近傍の検索の実装方式と速度は報告されていない。[出典：§IV-D](../../../raw/papers/yin_2024_gsr.pdf)

計画にとっての意味づけ（採否・新規性）は本Wikiでは判断しない。

## 関連ページ

- [VINN](pari_2022_vinn.md)
- [Behavior Retrieval](du_2023_behavior_retrieval.md)
- [検索による模倣学習データ選択の関連研究](../../concepts/retrieval/imitation_data_selection_related_work.md)
- [検索による模倣学習データ選択](../../concepts/retrieval/retrieval_based_imitation_data_selection.md)
- [Diffusion Policy](../imitation_learning/chi_2023_diffusion_policy.md)
- [ロボットの模倣学習と強化学習](../../concepts/imitation_learning/imitation_and_reinforcement_learning.md)
- [HNSW](../../concepts/vector_search/hnsw.md)
