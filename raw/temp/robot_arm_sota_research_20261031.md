---
title: ロボットアーム制御のSOTAと評価指標：2026-10-31調査
type: research-note
tags: [robotics, robot-learning, benchmark, success-rate, evaluation]
sources:
  - https://arxiv.org/html/2610.18873v1
  - https://robochallenge.ai/challenges
  - https://www.pi.website/download/pi07.pdf
  - https://www.pi.website/download/pistar06.pdf
  - ../papers/kim_2026_cosmos_policy.pdf
  - ../papers/luo_2024_hil_serl.pdf
updated: 2026-10-31
---

# ロボットアーム制御のSOTAと評価指標

2026-10-31（日本時間）に一次情報を確認した調査メモ。新規PDFはtempへの収集のみで、個別ingestは未実施。以下の分類と比較上の注意は資料を踏まえた編集上の整理であり、ユーザーの研究方針や採用決定ではない。

## SOTAの読み方

タスク成功率は、対象タスク、ロボット、初期条件、既知／未知条件、学習データ、時間制限、介入の有無が異なると直接比較できない。成功率は指定条件で完了した割合であり、位置誤差の精度や実世界のあらゆる作業への対応能力とは別。以下の数値は異なる評価条件の代表例であり、手法全体の順位表ではない。[比較条件の具体例：HIL-SERL §4・6](../papers/luo_2024_hil_serl.pdf)、[Cosmos Policy §5・Appendix A.3](../papers/kim_2026_cosmos_policy.pdf)、[LoopWAM §4](guo_2026_loopwam.pdf)

| 方向 | 研究と確認結果 | 留保 |
| --- | --- | --- |
| 限定した実機タスクの高成功率 | HIL-SERL（2024、保存版2025）：RAM挿入、USB挿入、ベルト組立など。Table 1(a)は各タスク100%、IKEA全体組立は10/10 | 通常100評価試行、タスクごとに学習。未知環境全般への汎化を実証した値ではない。2026年の総合首位と断定しない。 |
| 多タスク実機ベンチマーク | LoopWAM（2026-10-13）：Table30 V2で成功率43.33%、score 56.80。確認時の公式掲載首位。次点VLA-DM0.5は40.67%、54.42 | 30タスク・4種類の実機。ロボット種別ごとにmulti-taskモデルを学習。ランキングは変動する。scoreと成功率を区別。 |
| 汎用モデルの器用さと汎化 | π0.7（2026-04-16）：単一モデルが、洗濯物・エスプレッソ・箱組立などの既知作業で専門方策と同程度の性能。多様な衣類・箱組立ではthroughputも上回ると報告 | 主に著者独自評価。task-specific post-trainingなしは、対象作業の訓練データを使っていないという意味ではない。未知作業の実験とは分ける。 |
| シミュレーションの高成功率 | Cosmos Policy（2026-01）：LIBERO 98.5%、RoboCasa 67.1%。実機ALOHAは93.6/100の達成度スコア | 論文報告時のSOTA。2026-10-31の全後続研究中の首位を保証しない。RoboCasaとRoboCasa365も同一評価ではない。 |

出典：[HIL-SERL Table 1・§6](../papers/luo_2024_hil_serl.pdf)、[LoopWAM §4.2・Tables 1–3](guo_2026_loopwam.pdf)、[公式ランキング](https://robochallenge.ai/challenges)、[π0.7 §IX-A・Fig.6](pi_2026_pi07.pdf)、[Cosmos Policy Tables 1–3](../papers/kim_2026_cosmos_policy.pdf)。

LoopWAMは成功・不完全・失敗のrolloutを取り込むWorld-Action Model。失敗行動をそのまま模倣せず、失敗も未来観測の学習には使う。実機で3回の収集・学習を経て23.67%から43.33%へ改善した。報酬を扱うことだけを理由に、手順を一般的なactor-critic RLと同一視しない。[LoopWAM §3–4](guo_2026_loopwam.pdf)

π*0.6 / RECAP（2025）は、デモ・自律試行・人の修正を使ってVLAを改善する先行例。成功率とともに1時間あたりの成功作業数を評価し、難しい衣類・エスプレッソ作業で大きな改善を報告。π0.7での比較対象となる専門方策も含む。[RECAP §V-C・Figs.7–10](pi_2025_pistar06.pdf)、[π0.7 Fig.6](pi_2026_pi07.pdf)

## 成功率以外の指標

以下は論文での評価例をまとめたもの。すべての研究が同じ指標を報告するわけではない。

- **作業速度**：cycle time、完了時間。HIL-SERLは成功率とcycle timeを併記。[HIL-SERL Table 1](../papers/luo_2024_hil_serl.pdf)
- **Throughput**：単位時間あたりの成功作業数。速度と成功率を合わせて評価。計測に失敗・リセット・人の介入時間を含むかは条件確認が必要。[RECAP §V-C・Fig.7](pi_2025_pistar06.pdf)
- **汎化**：未知物体・背景・指示・ロボットでの成功率／達成度。測る数値は成功率でも、既知条件での性能と異なる問いを扱う。[π0.7 §IX-B–D](pi_2026_pi07.pdf)、[Cosmos Policy Table 3](../papers/kim_2026_cosmos_policy.pdf)
- **データ・試行効率**：必要なデモ本数、実機試行量、所定性能までの学習時間。実機学習時間と準備・デモ収集を含む総作業時間を分ける。[HIL-SERL §3–4・Appendix A](../papers/luo_2024_hil_serl.pdf)
- **人の負担**：学習中の介入step率など。デモ作成・報酬ラベル・リセットの負担も別に存在する。[HIL-SERL §3.5・Fig.5](../papers/luo_2024_hil_serl.pdf)
- **計算資源・応答性**：学習GPU数・時間、推論遅延。制御周期・chunk長・非同期実行との関係も確認する。[Cosmos Policy Appendix A.2–A.3・Table 5](../papers/kim_2026_cosmos_policy.pdf)
- **部分達成・出力品質**：中間工程の達成度、ソース塗布のcoverageやIoUなど、二値成功では捨てられる情報。[Cosmos Policy Table 3・Appendix A.3.2](../papers/kim_2026_cosmos_policy.pdf)、[Diffusion Policy §VI](../papers/chi_2023_diffusion_policy.pdf)

成功率が同じでも、作業速度、必要データ、人の介入、計算資源が異なれば有用性は異なる、というのが上記資料からの整理。検索技術の効果をこれらの研究結果だけから主張することはできない。

## 保存資料と参照URL

- [LoopWAM PDF](guo_2026_loopwam.pdf)：https://arxiv.org/pdf/2610.18873v1
- [π0.7 PDF](pi_2026_pi07.pdf)：https://www.pi.website/download/pi07.pdf
- [π*0.6 PDF](pi_2025_pistar06.pdf)：https://www.pi.website/download/pistar06.pdf
- [RoboChallenge公式](https://robochallenge.ai/challenges)：Web検索でランキング掲載を確認。HTMLダウンロードは403のため未保存。

上記3本は、混合品質の経験からの学習、汎用方策、実運用に近い指標を理解する資料としてingest候補。ただし今回の調査ではtempから移動しない。
