---
title: "Diffusion Policy：Action Diffusionによる視覚ベースの模倣学習"
type: source
tags: [robotics, imitation-learning, behavior-cloning, diffusion-model, action-sequence, receding-horizon-control]
sources:
  - ../../raw/papers/chi_2023_diffusion_policy.pdf
updated: 2026-10-31
---

# Diffusion Policy：Action Diffusionによる視覚ベースの模倣学習

## 書誌情報と保存版

Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, Shuran Song, **Diffusion Policy: Visuomotor Policy Learning via Action Diffusion**。2023年のRSS会議論文を拡張した **arXiv:2303.04137v5、2024-03-14、19ページ**を取り込んだ。著者一覧もこの拡張版に従う。以下の節番号・結果は保存v5のもの。[表紙・§1・References](../../raw/papers/chi_2023_diffusion_policy.pdf)

- [保存PDF](../../raw/papers/chi_2023_diffusion_policy.pdf)
- [arXiv書誌ページ](https://arxiv.org/abs/2303.04137)、[著者プロジェクト](https://diffusion-policy.cs.columbia.edu/)。外部ページ・公開コードは今回新たに検証していない。

## 何を解決する手法か

同じ観測から物体の左右どちらを回り込むかなど、デモには複数の有効な行動がある。さらに、長い動作では時間的に整合する行動列が必要になる。本論文は観測を条件とする行動列の分布をdenoising diffusionで学ぶ。学習設定はBehavior Cloningであり、報酬最大化やデータ検索を主目的とする手法ではない。[§1–2・§8](../../raw/papers/chi_2023_diffusion_policy.pdf)

単一の行動を直接回帰する代わりに、ノイズの多い行動列からノイズを取り除くネットワークを学び、実行時にはランダムなノイズ列を繰り返し修正して行動列を得る。生成するのは画像ではなく行動で、画像は条件として使う。[§2・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 観測・学習・実行

時刻$t$までの$T_o$ stepsの観測を$O_t$、予測する$T_p$ stepsの行動列を$A_t$、再予測までに実行する長さを$T_a$とする。物理時刻$t$と、denoisingの反復段階$k$は異なる添字である。[§2.3・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

学習ではデモの行動列$A_t^0$を取り出し、ランダムな段階$k$に応じたノイズ$\epsilon^k$を加え、ネットワーク$\epsilon_\theta$にそのノイズを予測させる。本文の簡略表記に従うと、損失は次式となる。実装用の完全なnoise scheduleをこの式だけで指定するものではない。[§2.2–2.3・式(3)–(5)・§3.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

$$
\mathcal L=\operatorname{MSE}\!\left(\epsilon^k,\epsilon_\theta(O_t,A_t^0+\epsilon^k,k)\right).
$$

したがって、**教師行動列を利用するBCだが、損失で直接比較するのは追加ノイズと予測ノイズ**である。行動と無関係なノイズを覚えるのではなく、観測条件に合うデモ行動列へ戻すための学習になる。[§2.2–2.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

実行手順は次のとおり。[§2.3・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

1. 直近の観測履歴を取得し、視覚特徴を計算する。
2. Gaussian noiseから行動列を初期化する。
3. 観測を条件にdenoisingを繰り返し、$T_p$ stepsの行動列を生成する。
4. そのうち$T_a$ stepsを実行し、新しい観測から再予測する。

このreceding horizon方式は、行動列の整合性と観測への反応性の両立を狙う。列の一部を実行している間は方策を再予測しないため、「毎時刻新しい画像から行動列を出す」ことと同一ではない。論文は前回の予測列によるwarm startも可能と述べるが、全実験でそれを使用したとは確定しない。[§2.3・§4.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

## ネットワークと設計上の選択

| 要素 | 保存版での設計・結果 |
| --- | --- |
| CNN版（DiffusionPolicy-C） | 1D temporal CNNに、観測特徴とdenoising段階をFiLMで条件付ける。多くのタスクで調整が比較的少なく済んだ。 |
| Transformer版（DiffusionPolicy-T） | ノイズ付き行動のtokenとdenoising段階を使い、観測特徴へcross-attentionする。行動token間はcausal maskを使う。急な行動変化を扱いやすい一方、hyperparameterに敏感。 |
| 視覚encoder | 基本構成はResNet-18。spatial softmax pooling、GroupNormを使い、方策とend-to-endに学習。カメラごとに別encoder、各時刻を個別にencodeする。 |
| 観測の条件付け | 観測と行動の同時分布ではなく$p(A_t\mid O_t)$を学ぶ。denoising中に視覚特徴を毎回計算し直さなくてよい。 |
| 推論高速化 | 実機ではDDIMでdenoising反復を減らす。回数については後述の本文・付録差に注意。 |

出典：[§2.3・§3・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)。CNNを最初に試すという記述は著者の実験に基づく推奨であり、あらゆる条件でCNNが優れるという保証ではない。

CNN版の代表的なsimulation設定は$T_o=2,T_a=8,T_p=16$。実機Push-Tは$T_a=6$、BlockPushは$T_o=3,T_a=1,T_p=12$など例外がある。Transformer版では予測長も異なる。[Appendix A.4・Tables 7–8](../../raw/papers/chi_2023_diffusion_policy.pdf)

## シミュレーション実験と読み方

RoboMimic、Push-T、Multimodal Block Pushing、Franka Kitchenで評価する。RoboMimicには熟練者データPHと複数人データMHの条件があり、状態入力と画像入力を分ける。以下は**画像入力・PH条件の抜粋**で、値は「最大checkpoint／最後10 checkpoint平均」。[§5・Tables 1–4](../../raw/papers/chi_2023_diffusion_policy.pdf)

| タスク | LSTM-GMM | DiffusionPolicy-C | DiffusionPolicy-T |
| --- | --- | --- | --- |
| Square | 0.82 / 0.59 | 0.98 / 0.92 | 1.00 / 0.90 |
| Transport | 0.88 / 0.62 | 1.00 / 0.93 | 0.98 / 0.81 |
| ToolHang | 0.68 / 0.49 | 0.95 / 0.73 | 0.76 / 0.47 |
| Push-T | 0.69 / 0.54 | 0.91 / 0.84 | 0.78 / 0.66 |

出典：[Table 2](../../raw/papers/chi_2023_diffusion_policy.pdf#page=7)。RoboMimicの値は成功率、simulation Push-Tはtarget area coverageであり、すべてを同じ成功率と呼ばない。CNNとTransformerの優劣もタスク・観測条件によって異なる。[§5.2–5.3・Tables 1–2](../../raw/papers/chi_2023_diffusion_policy.pdf)

評価条件の注意点：[§5.2・p.7脚注・Tables 1–2](../../raw/papers/chi_2023_diffusion_policy.pdf)

- 原則3 training seeds、50初期条件、50 epochsごとのcheckpointを使う。状態入力4500 epochs、画像入力3000 epochs。
- ただし脚注は、評価コードのbugによりRoboMimicでは**22初期条件**のみと明記する。captionの50条件と区別する。
- Diffusion Policyは基本的に位置制御、baselineは速度制御という、各手法に有利な行動表現で比較する。生成モデルだけの完全な条件統一比較ではない。
- 最大checkpointと最後10 checkpoint平均を混同しない。表には分散・信頼区間が示されていないため、平均値から有意差までは判断しない。

**平均46.9%改善**は、Tables 1・2・4のMHを除く対象列について、baseline各手法の最大値$b_i$とCNN/Transformerの最大値$d_i$を選び、相対改善$(d_i-b_i)/b_i$を平均したもの。単一の固定モデル同士の比較や、成功率46.9 percentage points増加ではない。[Appendix B.2](../../raw/papers/chi_2023_diffusion_policy.pdf#page=17)

## 実機と拡張版の双腕実験

単腕系のPush-T、Mug Flipping、Sauce Pouring・Spreadingに加え、拡張版では双腕3タスクがある。下表の指標・試行数を区別する。[§6–7](../../raw/papers/chi_2023_diffusion_policy.pdf)

| タスク | Diffusion Policyの報告結果 | 条件・注記 |
| --- | --- | --- |
| Push-T | 成功率95%、最終IoU 0.80 | 20試行、訓練デモ136本。LSTM-GMMの最良成功率20%、IBC 0%。 |
| Mug Flipping | 成功率90% | Fig.9。試行数を他タスクから推定して補わない。 |
| Sauce Pouring | IoU 0.74、成功率0.79 | Fig.10の値。coverageと成功率は別指標で、0.79を整数試行数に換算しない。 |
| Sauce Spreading | coverage 0.77、成功率1.00 | Fig.10。 |
| Bimanual Egg Beater | 成功率55% | 210デモ、20試行。 |
| Bimanual Mat Unrolling | 成功率75% | 162デモ、20試行。 |
| Bimanual Shirt Folding | 成功率75% | 284デモ、20試行。 |

出典：[Push-T §6.1・Table 6・Appendix C.1、Mug §6.2・Fig.9、Sauce §6.3・Fig.10、双腕 §7.3–7.5](../../raw/papers/chi_2023_diffusion_policy.pdf)。Push-Tは12時間の固定訓練後の最終checkpointを使用するが、IBCは訓練データの行動予測MSE最小checkpointを使用する。simulationの最大checkpoint指標とは条件が違う。[Appendix C.1](../../raw/papers/chi_2023_diffusion_policy.pdf)

Egg Beaterでは触覚feedbackを使ったテレオペがデモ収集に有効だった。ただし、それを理由に「方策が力覚を観測する」「実行時もhaptic controllerを使う」と解釈しない。方策の入力は§7.1の画像・固有受容情報で、推論にはnon-haptic controlを使うと記す。[§7.1–7.3・Appendix D.1](../../raw/papers/chi_2023_diffusion_policy.pdf)

## Ablation・実装で重要な点

- $T_a$が短すぎると時間的整合性、長すぎると反応性が損なわれる。多くの検証タスクで8 stepsが良かったという結果であり、全タスク共通の最適値ではない。[§4.3・§5.3・Fig.5・Tables 7–8](../../raw/papers/chi_2023_diffusion_policy.pdf)
- 位置制御が速度制御より良いという傾向を報告するが、理由に関する説明の一部は著者の推測である。一般的なロボット制御則として確定しない。[§4.2・Fig.4](../../raw/papers/chi_2023_diffusion_policy.pdf)
- 視覚encoderの事前学習を固定しただけでは弱く、SquareのablationではCLIP ViTを低い学習率でfinetuneする構成が良かった。実機Push-Tのencoder比較とは別条件。[§5.4・Table 5、§6.1・Table 6](../../raw/papers/chi_2023_diffusion_policy.pdf)
- 行動の各次元を原則$[-1,1]$へmin-max正規化する。ほぼ定数の次元、回転表現は例外を設ける。実装詳細を確認せず全次元に同一処理を適用しない。[Appendix A.1–A.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 保存PDF内の不一致・留保

| 箇所 | 不一致と本記事の扱い |
| --- | --- |
| denoising回数 | §3.4は実機で訓練100・推論10回によりRTX 3080上約0.1秒とする。一方Appendix A.4・Tables 7–8は実機推論16回。10と16を統一せず併記し、0.1秒を16回の測定値として転用しない。 |
| Sauceのデモ数 | Table 3はPour/Spread各90本。一方Appendix C.2.1は各50本収集・90%を訓練とする。保存PDFだけでは整合しないため、単一の確定本数としてまとめない。 |
| Kitchenデモ数 | §5.1は566本、Table 3は656本。どちらかへ無根拠に訂正しない。 |
| タスク数 | Abstractは「15 tasks / 4 benchmarks」とする一方、拡張版§7に双腕3タスクが追加されている。15という見出し数を全実験の単純な合計として使わない。 |

出典：[§1・§3.4・§5.1・§7・Table 3・Appendix A.4・C.2・Tables 7–8](../../raw/papers/chi_2023_diffusion_policy.pdf)。再現用コードやデータによる解消は今回の取り込み範囲に含めない。

## 限界と関連研究への位置付け

BCに由来するデモ不足・品質の問題は残り、単純な方策より計算量・推論遅延が大きい。行動列による緩和だけでは高周波制御に不十分な可能性がある。RLへの拡張や高速化は論文の将来方向として区別する。[§9](../../raw/papers/chi_2023_diffusion_policy.pdf)

この論文はグラフベースANNによるデータ選択や検索高速化の効果を検証していない。検索による学習データ選択と、最終的に行動列を生成する方策モデルを区別して読む。[本論文の範囲：§2・§5–9](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 関連ページ

- [Diffusion Policyの仕組み：ノイズ予測から行動列へ](../concepts/diffusion_policy.md)
- [Behavior Cloning](../concepts/behavior_cloning.md)
- [Action ChunkingとTemporal Ensembling](../concepts/action_chunking_and_temporal_ensembling.md)
- [ACT](zhao_2023_act.md)
- [模倣学習データ選択の関連研究：FlowRetrieval等](../concepts/imitation_data_selection_related_work.md)
