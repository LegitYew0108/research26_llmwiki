---
title: "VINN：The Surprising Effectiveness of Representation Learning for Visual Imitation"
type: source
tags: [robotics, imitation-learning, nearest-neighbor, locally-weighted-regression, self-supervised-learning, BYOL, non-parametric-policy, inference-time-retrieval]
sources:
  - ../../../raw/papers/pari_2022_vinn.pdf
  - ../../../raw/papers/zhao_2023_act.pdf
updated: 2026-11-04
---

# VINN：The Surprising Effectiveness of Representation Learning for Visual Imitation

## 書誌情報と要点

Jyothish Pari、Nur Muhammad (Mahi) Shafiullah（共同第一著者）、Sridhar Pandian Arunachalam、Lerrel Pinto（New York University）。Robotics: Science and Systems 2022（RSS 2022）の採録版を保存した。arXiv版は2112.01511。[出典：表紙](../../../raw/papers/pari_2022_vinn.pdf)

**視覚表現の学習と行動の学習を分ける。** 画像encoderは自己教師あり学習で事前に学ぶ。実行時は、現在の画像をencoderで埋め込み、デモ画像の埋め込みからk近傍を検索し、**近傍の行動を距離に応じて重み付き平均した値をそのまま行動にする**。行動側にパラメータを持つネットワークはなく、追加の学習も要らない。手法名VINNはVisual Imitation through Nearest Neighborsの略。[出典：§I、§III、Fig. 2](../../../raw/papers/pari_2022_vinn.pdf)

[Behavior Retrieval](du_2023_behavior_retrieval.md)や[SAILOR](nasiriany_2023_sailor.md)は、検索結果を方策の**学習データ**に加える。これに対しVINNは、**実行時の検索結果から行動を直接計算する**。同じ「検索」でも、使う段階が異なる。

## 問題意識

通常のBehavior Cloningは、CNNをend-to-endで学習する。このとき、次の2つを同時に解いている、と著者は指摘する。[出典：§I](../../../raw/papers/pari_2022_vinn.pdf)

- (a) **表現学習**：高次元の画像から、情報を保った低次元の埋め込みを得る
- (b) **行動学習**：その表現から行動を出す

両者を同時に学習すると互いに依存し、多くのデモが必要になる。VINNはこの2つを分離し、少数デモでも動く方策を目指す。

## 手法

### 1. 視覚表現の学習

- encoderはResNet-50の最終線形層を除いたもので、ImageNetの事前学習重みで初期化する。[出典：§III-A、§IV-C](../../../raw/papers/pari_2022_vinn.pdf)
- 次に、デモ画像の全フレームでBYOLにより自己教師ありfine-tuningを行う（100 epoch）。このとき行動ラベルは使わない。[出典：§III-A・C、§IV-C](../../../raw/papers/pari_2022_vinn.pdf)
- BYOLは、online networkと、その移動平均であるtarget networkを使う。同じ画像に異なるaugmentationをかけた2つの入力に対して、両者の出力の差を小さくする。[出典：§III-A、Fig. 2](../../../raw/papers/pari_2022_vinn.pdf)
- 学習後、全デモフレームを埋め込み、埋め込み集合 $E$ を作る。表現ベクトルは2048次元。[出典：§III-A、Appendix B-e](../../../raw/papers/pari_2022_vinn.pdf)
- 著者はSimCLR・VICRegなど他の自己教師あり手法でも動くとしている。[出典：§III-A、Table III](../../../raw/papers/pari_2022_vinn.pdf)

### 2. k近傍によるLocally Weighted Regression

現在の観測の埋め込み $e$ に対して、$E$ からL2距離 $\|e-e^{(i)}\|_2$ の近いk件を探す。それらの埋め込みと行動の組 $(e^{(i)},a^{(i)})$ から、次の式で行動を計算する。[出典：§III-B](../../../raw/papers/pari_2022_vinn.pdf)

$$
\hat a=\frac{\sum_{i=1}^{k}\exp\left(-\|e-e^{(i)}\|_2\right)a^{(i)}}{\sum_{i=1}^{k}\exp\left(-\|e-e^{(i)}\|_2\right)}
$$

これは、距離のSoftMinを重みとした近傍行動の平均である。疑似コードでも、上位k件の距離に `softmax(-距離)` をかけて行動を足し合わせている。[出典：§III-B、Appendix A](../../../raw/papers/pari_2022_vinn.pdf)

- **暗黙の前提**：似た観測には似た行動が対応する。[出典：§III-B](../../../raw/papers/pari_2022_vinn.pdf)
- **もう一つの前提**：有効な行動同士の局所的な重み付き平均も、有効な行動になる。著者はこれを明示したうえで、出力をそのまま任意の行動空間へ射影できる柔軟さを利点としている。[出典：§IV-G c](../../../raw/papers/pari_2022_vinn.pdf)
- 近傍1件の行動をそのまま使うのではなく平均する利点は、Fig. 3右下の例で示されている。[出典：Fig. 3](../../../raw/papers/pari_2022_vinn.pdf)
- 着想元は、状態推定値に対して使われてきたLocally Weighted Learning（LWL）。VINNは、状態推定値の代わりに自己教師ありの視覚表現の上でLWLを行う。著者は、直感的にはデモで学んだMixture-of-Expertsに近い振る舞いだと述べる。[出典：§I、§II-C](../../../raw/papers/pari_2022_vinn.pdf)

### 3. 実機での実行

- 実機（Hello Robot Stretch）では閉ループで動かす。毎ステップ観測を取得してモデルに問い合わせる。[出典：§III-C、Appendix C](../../../raw/papers/pari_2022_vinn.pdf)
- 出力は並進の行動 $\hat a$ とgripper状態 $g$。ロボットは $c\odot\hat a$ だけ動く。$c$ は各要素が1未満のハイパーパラメータで、SfMの誤差を抑え、人のデモからロボットへの移行を助ける。$g$ をgripperの状態へ変換するハイパーパラメータは、実験ごとに調整した。[出典：§III-C](../../../raw/papers/pari_2022_vinn.pdf)
- 並進 $\Delta(x,y,z)$ は逆運動学で関節の動きに変換する。[出典：Appendix C](../../../raw/papers/pari_2022_vinn.pdf)
- デモは、GoPro付きのreacher-grabber（DemoAT）で人が収集する。行動は、SfMで復元したカメラ位置の、フレーム間の並進である。[出典：§III-C、Appendix D](../../../raw/papers/pari_2022_vinn.pdf)

## 実験

### データと比較手法

- **Pushing・Stacking**：既存データを利用（各約930本・約750本）。行動はフレーム間のend-effector並進。[出典：§IV-A](../../../raw/papers/pari_2022_vinn.pdf)
- **Door Opening**：3人がそれぞれの台所で収集し、学習71本・テスト21本。他の2タスクも学習71本・テスト21本に間引いて揃えた。行動はSfMのスケール曖昧性に対応するため正規化した。評価指標は正解行動とのMSE。[出典：§IV-A](../../../raw/papers/pari_2022_vinn.pdf)
- **比較手法**：Random Action、Open Loop（時刻tの平均行動）、BC end-to-end（ResNet-50）、BC on Representations（BYOL表現を固定してMLPを学習）、Implicit BC、ImageNet features + NN（fine-tuningなし）、自己教師あり手法 + NN（BYOL・SimCLR・VICReg）。[出典：§IV-B](../../../raw/papers/pari_2022_vinn.pdf)

### 結果

**オフラインMSE**
- デモ数を変えた比較では、デモが多いとImageNet初期化のBC end-to-endも良い。少数デモでは近傍法が同等以上だった。[出典：§IV-D、Fig. 4](../../../raw/papers/pari_2022_vinn.pdf)
- StackingとDoor Openingでは、デモ20本未満でVINNが大きく優れる。Pushingは少数デモでは難しく、VICReg + NNの方が良い。[出典：§IV-D、Table III](../../../raw/papers/pari_2022_vinn.pdf)

**実機のドア開け（3つのキャビネット×10試行＝30試行）**

| 手法 | ハンドル把持 | ドア開放 |
| --- | --- | --- |
| BC end-to-end | 0% | 0% |
| BC on representations | 56.7% | 53.3% |
| ImageNet features + NN | 20% | 0% |
| VINN（BYOL + NN） | 80% | 80% |

[出典：§IV-E、Table I](../../../raw/papers/pari_2022_vinn.pdf)

著者の解釈：BCはロボットが誤った動きをすると観測がすぐ分布外になる。VINNは近傍の事前情報により、ある程度のずれから回復できる。並進の行動はロボットを分布の中心へ戻す傾向がある。[出典：§IV-E](../../../raw/papers/pari_2022_vinn.pdf)

**見た目を変えたキャビネット（各10試行）**

| 変更 | BC-rep | VINN |
| --- | --- | --- |
| 変更なし | 90% | 80% |
| 標識・ハンドルを覆う | 10% | 70% |
| ＋片方のbinを覆う | 0% | 50% |
| ＋両方のbinを覆う | 0% | 0% |

[出典：§IV-F、Table II](../../../raw/papers/pari_2022_vinn.pdf)

- §Iの「新しい場面で40%、最強のbaselineは3.3%」は、変更ありの3条件の平均に一致する。[出典：§I](../../../raw/papers/pari_2022_vinn.pdf)
- 変更なしの条件では、BC-repの方が高い。
- 見た目の手がかりをすべて覆うと、encoderが情報を伝えられず、k-NNも失敗する。[出典：§IV-F](../../../raw/papers/pari_2022_vinn.pdf)
- 著者は、MSEが低いことは実機で成功する必要条件に見えるが、十分条件ではないと述べる。[出典：§IV-F](../../../raw/papers/pari_2022_vinn.pdf)

### 設計の検証

- **事前学習・fine-tuning**：ImageNet初期化を外すとMSEが大きく悪化する。BYOLのfine-tuningを外したImageNet features + NNは、MSEでは僅差だが、実機では悪い（ドア開放0%）。方策の性能は表現の質に依存する。[出典：§IV-G b、Tables I・III](../../../raw/papers/pari_2022_vinn.pdf)
- **BC-repとの差**：訓練とテストの差が大きいほど、また方策のhorizonが長いほど、BC-repとの差が開く。[出典：§IV-G d](../../../raw/papers/pari_2022_vinn.pdf)
- **kの選び方**：kが小さすぎると行動が滑らかでなくなり、大きすぎると無関係な例が混ざる。検証損失ではk≈10が良く、k=20を超えると目立った改善はなかった。[出典：§IV-G e、Fig. 6](../../../raw/papers/pari_2022_vinn.pdf)

### 計算時間と検索

- 画像のencodeに約0.074秒、近傍回帰に約0.038秒。[出典：§IV-H](../../../raw/papers/pari_2022_vinn.pdf)
- 実装は全件を線形に比較する素朴な方法で、データ数nに対してO(n)。少数デモの設定ではnが小さいこと、FAISSなどの索引で高速化できることを、実用上の根拠として挙げている。ANN索引を使った実験はしていない。[出典：§IV-H、Appendix A](../../../raw/papers/pari_2022_vinn.pdf)

## 限界（著者の記述）

- 大きな見た目の手がかりをすべて取り除くと失敗する。デモの追加は簡単だが、場面の大きな変化に表現を適応させるのは難しい。[出典：§V](../../../raw/papers/pari_2022_vinn.pdf)
- 自己教師あり学習はタスク関連データで行っており、タスク非依存の事前学習は今後の課題。[出典：§V](../../../raw/papers/pari_2022_vinn.pdf)
- 単一タスクの設定に限られる。[出典：§V](../../../raw/papers/pari_2022_vinn.pdf)

## ACT論文でのVINN

[ACT原論文](../imitation_learning/zhao_2023_act.md)は、VINNをbaselineとして比較している。

- **シミュレーションの成功率（%）**：VINNのCube Transferは、Transfer段階でscripted data 3%、human data 0%。Bimanual InsertionのInsert段階は1%・1%。同じ条件のACTは、Cube Transfer 86%・50%、Bimanual Insertion 32%・20%。いずれも3 seed×50評価。[出典：ACT Table I](../../../raw/papers/zhao_2023_act.pdf)
- **Action Chunkingの効果**：ACTはVINNを、次のk個の行動を取得する形にも拡張した。chunkを大きくすると性能が上がる傾向がある。[出典：ACT §VI、Fig. 8(a)](../../../raw/papers/zhao_2023_act.pdf)
- **Temporal Ensemblingの効果**：VINNでは性能が下がった。ACTの著者は、temporal ensembleは主にパラメトリック手法のモデル誤差を平滑化する一方、VINNはデータセットの正解行動を取得するのでその恩恵がない、と仮説を述べている。[出典：ACT §VI、Fig. 8(b)](../../../raw/papers/zhao_2023_act.pdf)
- **実装上の調整**：ACTの実験では、近傍数kを検証損失で選んだ。action chunkingなしの場合は、視覚特徴の類似度に関節位置の差を加えると性能が上がったと報告している。[出典：ACT Appendix](../../../raw/papers/zhao_2023_act.pdf)

これらはACT論文の実装・データ・調整条件での結果であり、VINN原論文の実験条件（3次元の並進行動、ドア開けなど）とは異なる。

## 研究計画との関係

[現在の研究計画](../../../lab/research_policy/20261104_inference_time_retrieval_act.md)の§12は、VINNを「複数候補の平均それ自体は独自の要素ではない」根拠として挙げている。論文から確認できる事実は次のとおり。

- 実行時に近傍の行動を重み付き平均する手法として、VINNが既にある。
- VINNは検索結果だけで行動を決める。パラメトリック方策との混合、信頼度に応じた検索の起動、候補の再評価は扱っていない。[出典：§III](../../../raw/papers/pari_2022_vinn.pdf)
- 近傍探索は線形探索で、グラフ型ANN索引の効果は評価していない。[出典：§IV-H](../../../raw/papers/pari_2022_vinn.pdf)
- 対象のCube Transfer（ACTのシミュレーション）では、検索だけで動くVINNの成功率は低い。[出典：ACT Table I](../../../raw/papers/zhao_2023_act.pdf)

計画にとっての意味づけ（新規性・採否）は本Wikiでは判断しない。

## 関連ページ

- [検索による模倣学習データ選択の関連研究](../../concepts/retrieval/imitation_data_selection_related_work.md)
- [Retrieval-augmented Imitation Learning](../../concepts/retrieval/retrieval_augmented_imitation_learning.md)
- [Behavior Cloning](../../concepts/imitation_learning/behavior_cloning.md)
- [Action ChunkingとTemporal Ensembling](../../concepts/imitation_learning/action_chunking_and_temporal_ensembling.md)
- [ACTの論文要約](../imitation_learning/zhao_2023_act.md)
- [FAISS](../../concepts/vector_search/faiss_vector_search.md)
- [HNSW](../../concepts/vector_search/hnsw.md)
