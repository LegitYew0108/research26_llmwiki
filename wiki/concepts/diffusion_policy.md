---
title: "Diffusion Policy：ノイズ予測から行動列を生成する仕組み"
type: concept
tags: [diffusion-policy, denoising, behavior-cloning, multimodal-action, receding-horizon-control]
sources:
  - ../../raw/papers/chi_2023_diffusion_policy.pdf
  - ../../raw/papers/zhao_2023_act.pdf
updated: 2026-10-31
---

# Diffusion Policy：ノイズ予測から行動列を生成する仕組み

## 一言でいうと

Diffusion Policyは、カメラ画像やロボットの状態を条件として、**ランダムなノイズ列を繰り返し修正し、実行可能な行動列を生成するBC方策**である。画像生成をするのではなく、画像を見ながら行動を生成する。[Diffusion Policy §2・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 学習では何が正解になるのか

説明用に、デモ中の連続した手先目標位置を「正解の行動列」と考える。学習では、その列に意図的にノイズを加える。ネットワークには観測・ノイズ付き行動列・ノイズ段階を渡し、追加したノイズを当てさせる。これは論文の学習手順を簡略化した説明であり、特定タスクの実験例ではない。[§2.2–2.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

本文の簡略表記では次の損失を使う。$A_t^0$がデモ行動列、$O_t$が観測履歴、$k$がdenoising段階、$\epsilon^k$がその段階で加えるノイズである。noise scheduleの係数はこの表記では省略されている。[式(3)–(5)・§3.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

$$\mathcal L=\operatorname{MSE}\left(\epsilon^k,\epsilon_\theta(O_t,A_t^0+\epsilon^k,k)\right).$$

正解ノイズを知っているのは、デモに自分で加えたからである。デモの代わりにランダムな行動を正解としているわけではない。デモ行動列を使ってノイズ除去を学ぶことが、観測条件に合う行動の分布を学ぶ方法になっている。[§2.2–2.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 実行時には正解行動を必要としない

学習後は、現在の観測を条件としてGaussian noiseからdenoisingを繰り返す。学習時のデモ行動列や、それに加えた正解ノイズを実行時に入力する必要はない。画像特徴は一度計算し、各denoising段階で共有できる。[§2.3・Fig.2](../../raw/papers/chi_2023_diffusion_policy.pdf)

同じ観測に左右どちらを回り込む動作もあり得る場合、単純な点予測では複数の行動を表しにくい。Diffusion Policyは分布を学び、ノイズから一つの行動列を生成する。Push-Tでは左右の回り込みを表現し、一回のrollout中は一方に沿う例を示す。ただし、あらゆる観測で全modeを等しく学習できるという保証ではない。[§4.1・Fig.3・§5.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

## 予測する長さと実行する長さは違う

| 記号 | 意味 | CNN版の代表的なsimulation設定 |
| --- | --- | --- |
| $T_o$ | 入力する観測履歴の長さ | 2 steps |
| $T_p$ | 予測する行動列の長さ | 16 steps |
| $T_a$ | 新しい観測で再予測する前に実行する長さ | 8 steps |

出典：[§2.3・Table 7](../../raw/papers/chi_2023_diffusion_policy.pdf)。例外タスクもあるため固定仕様ではない。

この例では、16 steps先まで予測して8 steps分を実行し、そこで新しい観測から予測を更新する。実行する区間が長いほどモデルを呼ぶ回数は減るが、予期しない変化に気付いて再予測するまでの時間も長くなる。行動列全体の整合性と反応性の間にtrade-offがある。[§2.3・§4.3・§5.3](../../raw/papers/chi_2023_diffusion_policy.pdf)

## ACTとの共通点と違い

下表は両原論文の記述を並べた整理で、同じ条件で両手法の性能を比較した結果ではない。[Diffusion Policy §2–3](../../raw/papers/chi_2023_diffusion_policy.pdf)、[ACT §IV](../../raw/papers/zhao_2023_act.pdf)

| 観点 | Diffusion Policy | ACT |
| --- | --- | --- |
| 共通する目的 | デモから観測に応じた行動列を学ぶBC | 同左 |
| 行動列の生成 | ノイズ列を反復denoisingする | CVAE decoderが行動列を予測する |
| 学習時 | デモ行動列に加えたノイズを予測する | 正解行動列からzを推定し、再構成損失とKL項で学習する |
| 論文の実行手順 | ノイズから行動列を生成し、一部を実行して再予測する | z=0、毎時刻chunkを予測し、同時刻に対応する過去予測をtemporal ensemblingする |
| 出力の表現 | タスクに応じた手先目標位置・姿勢など | ALOHAでは左右の目標関節位置14次元 |

列を出すことと、その列をいつ更新・統合するかは別の設計要素である。Diffusion Policyのreceding horizon実行を、ACTのtemporal ensemblingと同じ処理として説明しない。[Diffusion Policy §2.3](../../raw/papers/chi_2023_diffusion_policy.pdf)、[ACT §IV-A・Algorithm 2](../../raw/papers/zhao_2023_act.pdf)

## 読む際の注意

ノイズを反復除去するため推論は複数回のネットワーク評価を必要とする。BCとしてのデモ不足・分布シフトの問題も残り、生成モデルを使うだけで回復や成功が保証されるものではない。[§9](../../raw/papers/chi_2023_diffusion_policy.pdf)

- [論文要約：実験・評価条件・保存版の不一致](../sources/chi_2023_diffusion_policy.md)
- [Behavior Cloning](behavior_cloning.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
- [CVAEとACT](conditional_variational_autoencoder.md)
