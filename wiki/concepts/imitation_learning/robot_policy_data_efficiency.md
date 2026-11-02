---
title: 高成功率ロボット方策のデータ効率を比較する
type: concept
tags: [robotics, data-efficiency, demonstrations, pretraining, evaluation]
sources:
  - ../../../raw/papers/luo_2024_hil_serl.pdf
  - ../../../raw/papers/kim_2026_cosmos_policy.pdf
  - ../../../raw/papers/guo_2026_loopwam.pdf
  - ../../../raw/papers/pi_2026_pi07.pdf
  - ../../../raw/papers/pi_2025_pistar06.pdf
updated: 2026-10-31
---

# 高成功率ロボット方策のデータ効率を比較する

## 比較の軸

以下は各論文の条件を踏まえた編集上の整理。データ効率を、初期の人のデモ、追加の実機試行・修正介入、事前学習に分ける。同じタスク・初期条件・目標成功率に必要なデータ量を比較するのが基本であり、異なる作業の成功率をデモ本数で割って順位付けしない。1 episodeの長さや、人が関与する時間も異なる。[条件の根拠：HIL-SERL §3–4](../../../raw/papers/luo_2024_hil_serl.pdf)、[Cosmos Policy §5・Appendix A](../../../raw/papers/kim_2026_cosmos_policy.pdf)、[RECAP §VI・Appendix F](../../../raw/papers/pi_2025_pistar06.pdf)

## 対象データと追加経験

| 研究 | 対象作業のデータ | 事前学習と留保 |
| --- | --- | --- |
| HIL-SERL | 通常20–30本の初期成功デモ＋自律試行＋人の修正。多くの作業は1–2.5時間の実機学習、ベルト組立は6時間 | ImageNet事前学習済みResNet-10。報酬classifierにも通常positive約200・negative約1000点を用意。初期デモだけで最終性能に達したわけではない。 |
| Cosmos Policy | LIBERO 40×50本、RoboCasa 24×50本。実機ALOHAは4タスク計185本（plate80、shirt15、bowl45、bag45）。planning版の追加学習は別途648 rollouts | Cosmos-Predict2の動画事前学習を利用。185本は4タスク合計。planning版のデータと直接実行版を分ける。 |
| LoopWAM | 実機Table30 V2は初期expertデータに加え、各タスク約100 rollouts／roundを3回収集。RoboTwin 2.0はexpert27,500本＋rollout22,500本 | Wan2.2-TI2V-5Bで初期化。追加embodied pretrainingなしは動画事前学習なしを意味しない。実機の初期expert総数は確認した記述から確定できない。 |
| π0.7 | 既知の器用さ評価ではtask-specific post-trainingなし。訓練には多ロボットのデモ・評価rollout・介入・公開ロボットデータ・人の動画・Webデータを含む | 対象作業データなしという意味ではない。π*0.6のRL過程のデータも含む。総データ量を統一単位で比較する情報は確認範囲で不足。 |
| π*0.6 / RECAP | espresso追加経験例：自律414 episodes＋correction429 episodes。初期タスクデモは別 | 事前学習は数万時間のロボットデモ。correctionと自律episodeの長さ・人手負担を同一視しない。 |

出典：[HIL-SERL §3・Table 1・Appendix A](../../../raw/papers/luo_2024_hil_serl.pdf)、[Cosmos Policy §5・Appendix A.2–A.4](../../../raw/papers/kim_2026_cosmos_policy.pdf)、[LoopWAM §4.1–4.2](../../../raw/papers/guo_2026_loopwam.pdf)、[π0.7 §VI-A・IX-A](../../../raw/papers/pi_2026_pi07.pdf)、[RECAP §IV・Appendix F](../../../raw/papers/pi_2025_pistar06.pdf)。

RECAPの箱組立は本文で600 autonomous trials＋360 intervention trials／反復、付録では600 demonstrations＋360 correction episodesと記載が異なる。内訳を単一の確定値に統合しない。[RECAP §VI-C.2・Appendix F](../../../raw/papers/pi_2025_pistar06.pdf)

## 何が言えるか

以下は上記のデータ構成からの整理であり、公平な直接比較の実験結果ではない。

- **HIL-SERL**：初期デモを少なくし、実機経験と人の介入で補う。少数デモと少数総試行は区別する。
- **Cosmos Policy**：動画事前学習の知識を、少量の対象作業デモに転用する。対象デモが少ないことと総事前学習が小さいことは別。
- **LoopWAM**：成功以外の経験も学習に利用する。ただし比較手法と追加rollout量を揃えた効率順位ではない。
- **π0.7**：広い訓練の負担を多タスクに共有し、対象タスク専用の追加学習を減らす方向。既知作業の追加学習なしと、未知作業データなしを区別する。

根拠：[HIL-SERL §3–4](../../../raw/papers/luo_2024_hil_serl.pdf)、[Cosmos Policy §4–5](../../../raw/papers/kim_2026_cosmos_policy.pdf)、[LoopWAM §3–4](../../../raw/papers/guo_2026_loopwam.pdf)、[π0.7 §VI・IX](../../../raw/papers/pi_2026_pi07.pdf)。

どれが同じ性能に最少の総データで達するかは、これらの異なるタスク・条件の報告だけでは結論できない。比較にはデモ量だけでなく、人の修正時間、実機相互作用量、目標成功率までの曲線、共有する事前学習条件が必要になる。これは比較上の整理であり、新しい研究方針の提案・採用決定ではない。

## 関連ページ

- [評価指標とSOTAの読み方](robot_policy_evaluation_metrics.md)
- [π*0.6からπ0.7へ](pi_recap_and_pi07.md)
- [デモを併用する実機RL](../reinforcement_learning/demonstration_augmented_robot_rl.md)
