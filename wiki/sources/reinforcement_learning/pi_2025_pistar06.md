---
title: π*0.6 / RECAP：実機経験と人の修正から学ぶVLA
type: source
tags: [robotics, VLA, reinforcement-learning, RECAP, advantage-conditioning]
sources:
  - ../../../raw/papers/pi_2025_pistar06.pdf
updated: 2026-10-31
---

# π*0.6 / RECAP：実機経験と人の修正から学ぶVLA

## 論文の位置づけ

Physical Intelligence, *π*0.6: a VLA That Learns From Experience*（2025）。保存PDFは18ページ。RECAPは **RL with Experience and Corrections via Advantage-conditioned Policies** の略。デモ、自律rollout、人の修正をまとめて使い、flow matchingで行動を生成する大規模VLAを改善する。π0.6は基盤VLA、π*0.6はRECAPで学習したモデルであり、同一ではない。[原論文 Abstract・§I・IV–V](../../../raw/papers/pi_2025_pistar06.pdf)

## 学習の流れ

1. 多タスクのデモでvalue functionを学習し、advantage conditioningを使ってVLAをoffline RLで事前学習する。
2. 対象タスクのデモでSFTする。この段階ではadvantageのindicatorをTrueに固定する。
3. 実機で自律rolloutを収集し、必要に応じて人がteleoperationで修正する。各episodeには成否ラベルを付ける。
4. それまでに集めたデータでvalue functionを学習し直し、更新したadvantageのindicatorを条件に方策を学習する。この収集・学習を反復する。

各反復のvalue functionと方策は、直前の反復モデルではなく**事前学習checkpointからfine-tune**する。収集と更新は交互であり、実機収集中の連続同時更新ではない。[§IV・V-D・VII・Algorithm 1](../../../raw/papers/pi_2025_pistar06.pdf)

## Value functionとadvantage conditioning

報酬は成功終了時0、失敗終了時に大きな負値、それ以外は毎step −1。成功までの速さと失敗回避を同時に評価する。returnをタスクごとに正規化し、201 binsの分布をcross entropyで学習するMonte Carlo型のvalue推定で、明示的なoff-policy Q-learningではない。[§IV-A・V-C・式(1)・(5)](../../../raw/papers/pi_2025_pistar06.pdf)

post-trainingでは概ね次のN-step推定を用い、N=50とする。

\[
\hat A_t=\sum_{k=t}^{t+N-1}r_k+V(o_{t+N},\ell)-V(o_t,\ell),\qquad I_t=\mathbf1[\hat A_t>\epsilon_\ell].
\]

方策は観測・指示・indicatorから行動列を予測する。負のindicatorのデータも捨てず、推論時に正のindicatorで条件付ける。人の修正行動はindicatorをTrueにするため、修正が良質という仮定を含む。indicatorは30%の確率でdropoutし、CFGも利用可能。[§IV-B・V-B・Appendices E–F](../../../raw/papers/pi_2025_pistar06.pdf)

**原文の注意点**：§V-Dには閾値をvalue予測の30th percentileとする記述がある一方、Appendix Fは「事前学習で約30%をpositive、fine-tuningで通常約40%、単純洗濯で約10%」と説明する。両者を同じ条件だと断定せず、再現時には実装との照合が必要。またAppendix Fの事前学習advantage式はreturnの総和開始が0と印字されており、post-training式と区別する。[§V-D・Appendix F](../../../raw/papers/pi_2025_pistar06.pdf)

## モデルと実機

π0.6はGemma 3 4Bと860Mのaction expertを使う。Knowledge Insulationではflow matching側からbackboneへの勾配をstop gradientで遮断し、離散token予測も併用する。value側は小さい670M VLM backbone。評価実機は6 DoFの双腕、parallel-jaw gripper、3台のcameraで、50 Hzの関節位置commandを生成する。[§V-A–C・Fig.5](../../../raw/papers/pi_2025_pistar06.pdf)

## 評価条件と結果

| タスク | 成功条件・時間制限 |
| --- | --- |
| T-shirt / shorts | 1着を畳んで所定位置に積む、200秒以内 |
| Diverse laundry | 11種類で学習し、定量評価は難しいbutton-up shirt、500秒以内 |
| Espresso | double shotを作り提供、重大なミスなし、200秒以内 |
| Box assembly | 平らな段ボールから組立・label・stack、600秒以内 |

成功率は人のannotationに基づく。**Throughputは1時間あたりの成功作業数**で、速度と成功率をまとめた指標。異なるタスクの制限時間や採点を揃えた共通benchmarkではない。[§VI-A・C](../../../raw/papers/pi_2025_pistar06.pdf)

- 最終方策はoffline RL + SFTに対し、難しい洗濯とespressoでthroughputが2倍以上、失敗率は約半分。多様な洗濯以外は成功率90%以上と報告する。
- 自律データだけを使う単純洗濯の2反復ではthroughputが約50%改善。箱組立では2反復後に約2倍となるが、最初の反復で単調に改善するわけではない。
- 襟の向きを厳しく判定する別の洗濯設定では、2反復後の成功率97%を報告。一般の衣類全体の成功率ではない。
- 同じ収集データによるAWR・PPO比較ではRECAPがthroughputで上回る。PPOはoff-policy設定で安定化の制約を加えており、あらゆるPPO実装の優劣を示す結果ではない。

出典：[§VI-C・Figs.7–12](../../../raw/papers/pi_2025_pistar06.pdf)。Figs.7–8は画像でも確認し、棒グラフの値を厳密な数表として転記していない。

## 限界と記述の食い違い

介入だけでは速度や微妙な品質を最適化できず、介入品質も一定ではない。評価対象は選ばれた実機タスクで、未知タスク全般の保証ではない。valueは混合データのbehaviorを近似し、理想的なvalueを仮定した改善式が学習済み実機モデルで常に成り立つという保証ではない。[§III・IV-A・V-D・VII](../../../raw/papers/pi_2025_pistar06.pdf)

収集量には本文と付録で差がある。箱組立の§VI-C.2は各反復600 autonomous trials + 360 intervention trialsだが、Appendix Fは600 demonstrations + 360 correction episodesと記す。失敗除去も本文は追加介入なしとする一方、付録はcorrection dataを記載する。単一の確定した内訳に統合しない。[§VI-C.2・4・Appendix F](../../../raw/papers/pi_2025_pistar06.pdf)

## 関連ページ

- [π0.7](../imitation_learning/pi_2026_pi07.md)
- [π*0.6とπ0.7の比較](../../concepts/imitation_learning/pi_recap_and_pi07.md)
- [HIL-SERL](luo_2024_hil_serl.md)
- [デモを併用する実機RL](../../concepts/reinforcement_learning/demonstration_augmented_robot_rl.md)
