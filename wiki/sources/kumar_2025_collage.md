---
title: "COLLAGE：Adaptive Fusion-based Retrieval for Augmented Policy Learning"
type: source
tags: [robotics, imitation-learning, retrieval, few-shot-learning, multimodal-fusion]
sources:
  - ../../raw/papers/2508.01131v2.pdf
updated: 2026-10-17
---

# COLLAGE：Adaptive Fusion-based Retrieval for Augmented Policy Learning

## 書誌情報と要点

Sateesh Kumar、Shivin Dass、Georgios Pavlakos、Roberto Martín-Martín（The University of Texas at Austin）。対象はarXiv:2508.01131v2、2025年9月7日版。COLLAGEはCOLLective data AGgrEgationに由来する。[出典：表紙・Abstract](../../raw/papers/2508.01131v2.pdf)

**少数の対象デモを、既存データから検索したデモで補ってBehavior Cloningを学習する**。外観・動き・形状・言語でそれぞれ検索し、各検索集合だけで学習した参照方策が対象デモを説明できる程度に応じて、最終学習のサンプリング比率を変える。重み推定に環境rolloutは不要である。[出典：§1・3](../../raw/papers/2508.01131v2.pdf)

## 問題設定

少数の対象デモを $D_{target}$、多数の既存デモを $D_{prior}$ とする。外観が似ていても目的が異なる、動きが似ていても意味が異なるデモを追加するとnegative transferにつながりうる。単一の類似度に頼らず、検索集合の学習への有用性を推定するのが狙いである。[出典：§1、Fig. 1、§3](../../raw/papers/2508.01131v2.pdf)

## 手法

### 1. Modalityごとに検索する

end-effectorの速度に基づく停止点で対象デモを部分軌跡に分割する。視覚・動作・形状は特徴列の[Subsequence DTW](../concepts/subsequence_dynamic_time_warping.md)で既存軌跡の連続部分と対応付け、各queryについて低コストのtop-Kを取得する。取得した部分軌跡には元の言語指示も付ける。[出典：§3.1、Appendix A.1・A.4](../../raw/papers/2508.01131v2.pdf)

| Modality | 特徴 | 実装上の要点 |
| --- | --- | --- |
| Visual | DINOv2のRGB特徴 | patch・CLS tokenを平均し768次元 |
| Motion | GMFlowのoptical flowを再構成するencoder-decoder | simulationは5 frame差、256次元latent |
| Shape | foreground point cloudのPointNet++特徴 | simulationは正解depth・mask、実機はZED depthとDECOLA mask |
| Language | text-embedding-ada-002の指示文特徴 | cosine similarityが0.90を超えるデモを選択 |

言語は実装上デモ単位の検索であり、取得量を視覚検索に合わせて選択デモ間に配分する。「4つすべてに同じS-DTWを使う」とは読まない。実機ではDROIDの3 camera viewsそれぞれの特徴を平均する。[出典：§3.4・4.1、Appendix A.1・A.2](../../raw/papers/2508.01131v2.pdf)

### 2. 参照方策で検索集合を評価する

modality $f$ の検索集合 $D_{retrieved}^{f}$ だけで参照BC方策 $\pi_{ref}^{f}$ を学習し、対象デモ上の行動log-likelihoodを測る。

$$
S_f=\sum_{(s,a,\ell)\in D_{target}}\log\pi_{ref}^{f}(a\mid s,\ell),\qquad
w_f=\frac{\exp(S_f/\tau)}{\sum_{f'}\exp(S_{f'}/\tau)}.
$$

$\ell$ は言語指示、$\tau$ はtemperature。重みは検索集合単位で、個々のデモの成功確率ではない。論文はimportance samplingに着想を得た手法と説明しているが、この重みは確率密度比を直接計算したものではない。[出典：§3.2、式(1)–(2)](../../raw/papers/2508.01131v2.pdf)

参照方策は100 epochs学習し、60・70・80・90・100 epochsの5時点のスコアを平均する。初期の変動と長期学習によるoverfittingを避ける設定。temperatureはsimulationで2、実機で10。各参照方策の学習は約40分で4方策を並列実行し、追加の重み計算は約1.5分、最終方策学習は約2時間と報告する。検索・特徴抽出を含む全処理時間ではない。[出典：Appendix A.1–A.3](../../raw/papers/2508.01131v2.pdf)

### 3. 重み付きサンプリングで最終方策を学習する

各 $D_{aug}^{f}=D_{retrieved}^{f}\cup D_{target}$ から $w_f$ に従ってサンプリングする。最終方策は言語条件付きTransformerで、過去の観測から複数ステップの将来行動をGMM headで予測する。目的関数は行動のnegative log-likelihoodとパラメータのL2正則化。参照方策の出力行動を混ぜる方式ではなく、**学習データ集合をlate fusionする**。[出典：§3.3、式(3)、Fig. 2](../../raw/papers/2508.01131v2.pdf)

## 実験条件

simulationはLIBERO-10の各タスク5デモを対象とし、LIBERO-90の4,500デモから検索する。最終学習は60k steps、batch size 32、評価は3 seeds・50 trials。実機はFRANKA Pandaで6タスク・各5デモ。検索元はDROIDの成功50k episodesから無作為抽出した言語指示付き30k episodesで、最終学習50k steps、各手法・各タスク15 trialsで評価する。[出典：§4.1、Tables 1–2、Appendix A.1–A.2](../../raw/papers/2508.01131v2.pdf)

## 結果と集計の注意

| 手法 | LIBERO-10平均成功率（%） | 実機6タスク平均成功率（%、原表表記） |
| --- | ---: | ---: |
| 対象デモのみのBC | 34.8 | 6.7 |
| 全データ併用のMT | 35.8 | 3.3 |
| STRAP（引用結果） | 45.6 | — |
| Visual（著者らのSTRAP再現） | 45.4 | 28.9 |
| NA-Fusion（非適応の統合） | 46.9 | — |
| COLLAGE | 50.5 | 45.5 |

simulation平均には全手法0%のMoka-Mokaを含む10タスクが入り、Table 1の個別列は残る9タスクのみ。STRAPの引用値とVisualの再現値は区別する。[出典：Tables 1–2、Appendix A.1・Table 5](../../raw/papers/2508.01131v2.pdf)

- Visual比は**5.1 percentage points、相対約11.2%**の改善。STRAP引用値45.6に対しては相対約10.7%であり、abstractの「best baseline比11.2%」は比較基準に注意する。[出典：Abstract、§4.2、Table 1](../../raw/papers/2508.01131v2.pdf)
- 実機COLLAGEの成功数は6・6・9・7・6・7で、計41/90＝約45.56%。Table 2は45.5と表記し、Visualは26/90＝約28.89%。abstractの相対57.4%改善は表記値45.5と28.9からの計算に対応する。[出典：Abstract、Table 2](../../raw/papers/2508.01131v2.pdf)
- §4.2はNA-Fusionを「across all tasks」で上回ると述べるが、Table 1ではMug-Mug・Mug-Puddingで下回り、Bookは同率。確認できるのは平均での改善である。[出典：§4.2、Table 1](../../raw/papers/2508.01131v2.pdf)
- 取得量を揃えた追加比較では、VisualをK=400、COLLAGEを4 modalities×100とし、約25k sequencesで平均46.9対50.5を報告する。ただしTable 6のVisual個別9列の合計を10タスクで割ると約46.4で、平均欄46.9と一致しない。[出典：Appendix A.1、Table 6](../../raw/papers/2508.01131v2.pdf)

## 限界と研究テーマとの関係

すべてのmodalityが有用なデモを取得できない場合は改善が限定され、modalityごとの参照方策学習には追加費用がある。対象デモ上の予測能力は有用性の代理指標であり、タスク成功を保証するものではない。[出典：§3.2・6、Appendix A.3](../../raw/papers/2508.01131v2.pdf)

評価対象は検索による学習データ拡張を伴う**模倣学習**で、報酬による強化学習ではない。特徴抽出・S-DTW・検索集合の重み付けを扱うが、グラフベースANN indexや、その速度・近似誤差と制御性能の関係は評価していない。[出典：§3–4、Appendix A.4](../../raw/papers/2508.01131v2.pdf)

## 関連ページ

- [Retrieval-augmented Imitation Learning](../concepts/retrieval_augmented_imitation_learning.md)
- [Subsequence DTW](../concepts/subsequence_dynamic_time_warping.md)
- [Behavior Cloning](../concepts/behavior_cloning.md)
