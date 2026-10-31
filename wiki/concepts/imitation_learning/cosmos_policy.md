---
title: "Cosmos Policyの仕組み：動画モデル・world model・planning"
type: concept
tags: [Cosmos-Policy, video-diffusion, imitation-learning, world-model, value-function, planning, action-chunking]
sources:
  - ../../../raw/papers/kim_2026_cosmos_policy.pdf
  - ../../../raw/papers/chi_2023_diffusion_policy.pdf
updated: 2026-10-31
---

# Cosmos Policyの仕組み：動画モデル・world model・planning

## 動画生成モデルから行動を出すには

Cosmos Policyは、動画生成モデルが持つ時空間の事前学習をロボット制御へ利用する手法である。画像から行動を推論する新しい専用headを足す代わりに、ロボットの状態・行動・価値を、動画モデルが処理するlatent frameの形へ変換する。これを**latent frame injection**と呼ぶ。[Cosmos Policy §3–4.1](../../../raw/papers/kim_2026_cosmos_policy.pdf)

例えば行動列が「50時刻×14関節」の配列なら、正規化してflattenし、同じベクトルを複製して一つのlatent volumeを埋める。生成後は複製部分を平均して元の行動尺度に戻す。行動を画像に描いてからVAEで読み戻すわけではなく、非画像情報はVAE encode後のlatentを直接上書きする。[Cosmos Policy Appendix A.1](../../../raw/papers/kim_2026_cosmos_policy.pdf)

## 同じネットワークで何を学ぶか

$s$を現在観測、$a$をaction chunk、$s'$をchunk終端の未来観測とする。未来観測はカメラ画像と固有受容情報であり、完全な環境状態ではない。次の表のように、cleanな条件とnoisyな予測対象を変える。[Cosmos Policy §3–4.2・Fig. 12](../../../raw/papers/kim_2026_cosmos_policy.pdf)

| 役割 | 与えるもの | 生成するもの | 意味 |
| --- | --- | --- | --- |
| 方策 | 現在観測 | 行動列＋未来観測＋価値 | 今どの動きをするか |
| world model | 現在観測＋指定した行動列 | 未来観測＋価値 | その動きをすると何が見えるか |
| 価値予測（初期学習） | 現在観測＋行動列＋未来観測 | 価値 | どの程度タスクを達成できそうか |

学習ではcleanな正解latentへnoiseを加え、条件付きでdenoiseする。推論では正解の行動・未来観測は存在しないため、noiseから生成する。系列中の「未来」は、長い未来動画全体ではなく、$K$ steps後の一時点である。[Cosmos Policy §3–4.2](../../../raw/papers/kim_2026_cosmos_policy.pdf)

価値の教師はrolloutの終端報酬を時間割引したMonte Carlo returnであり、未来状態そのものの特徴量ではない。タスクが違えば評価すべき終端達成度も変わる。成功デモだけでは失敗が起こる状態・行動を十分学べないため、planningには実際の方策rolloutによる追加学習が必要になる。[Cosmos Policy §3・§4.3](../../../raw/papers/kim_2026_cosmos_policy.pdf)

## 直接実行とmodel-based planningの違い

直接実行は「現在観測 → 行動列を生成 → 実行 → 再観測」という流れ。未来観測・価値も並列生成するが、行動選択には使わない。[Cosmos Policy §4.2・Appendix A.3.1](../../../raw/papers/kim_2026_cosmos_policy.pdf)

model-based planningは「現在観測 → 行動候補を複数生成 → 各候補の未来観測を予測 → その未来観測の価値を推定 → 最良候補を実行」という流れ。planning用の価値関数は未来観測だけを見るようmaskを変更する。実験では、候補生成に元checkpoint、未来予測と価値評価にrolloutで改善した別checkpointを使う。[Cosmos Policy §4.3・§5.3・Fig. 12](../../../raw/papers/kim_2026_cosmos_policy.pdf)

候補は方策からサンプリングする。既存デモの最近傍をデータベースから引く検索ではない。また、実験のbest-of-Nは1層先読みであり、複数chunk先の探索木を展開する方式ではない。[Cosmos Policy §4.3・§6](../../../raw/papers/kim_2026_cosmos_policy.pdf)

## Diffusion Policyとの比較

| 観点 | Diffusion Policy | Cosmos Policy |
| --- | --- | --- |
| 分布として学ぶ主対象 | 観測条件付きの行動列 | 行動列・未来観測・価値と、それらの条件付き分布 |
| 事前学習の基盤 | 元論文の方策は主にタスクのデモから学ぶ | 事前学習済み動画生成モデルを全重みfine-tune |
| 視覚の役割 | 行動denoisingの条件 | 条件に加え未来観測の生成対象にもなる |
| 実行時の候補評価 | 元論文の基本方式は生成したchunkの一部を実行 | 直接実行、またはworld modelと価値による候補評価 |

出典：[Diffusion Policy §2–3](../../../raw/papers/chi_2023_diffusion_policy.pdf)、[Cosmos Policy §3–4](../../../raw/papers/kim_2026_cosmos_policy.pdf)。どちらもdiffusionで行動列を扱うが、事前学習・予測対象・実行方法が異なる。Cosmos Policyのアーキテクチャ変更不要という性質を、入力処理や学習設定の変更も不要という意味に広げない。

## 理解するときの注意

- action chunkはモデルの推論間隔とロボットの制御間隔を分ける。ALOHAの25 Hz制御は50 stepsで2秒の動作となり、その生成に1 H100で0.95秒停止する。planningでは8 H100でも4.9秒を要する。[Cosmos Policy Appendix A.4.2](../../../raw/papers/kim_2026_cosmos_policy.pdf)
- 複数候補の最良値を選べても、予測が正しくなければ良い行動を選べるとは限らない。論文はデモだけのworld modelが失敗を見落とす例を示し、rollout追加学習で改善している。[Cosmos Policy §4.3・Fig. 6](../../../raw/papers/kim_2026_cosmos_policy.pdf)
- 実機評価はタスクの部分達成を含むスコアであり、成功率と区別する。planningの平均12.5ポイント改善もスコアの差である。[Cosmos Policy Fig. 7・Appendix A.3.2](../../../raw/papers/kim_2026_cosmos_policy.pdf)

## 関連ページ

- [Cosmos Policy論文要約：実験条件・ablation・限界](../../sources/imitation_learning/kim_2026_cosmos_policy.md)
- [Diffusion Policyの仕組み](diffusion_policy.md)
- [Action ChunkingとTemporal Ensembling](action_chunking_and_temporal_ensembling.md)
- [Behavior Cloning](behavior_cloning.md)
