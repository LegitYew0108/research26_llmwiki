---
title: "ロボットの模倣学習・強化学習：Research候補（2026-10-03）"
type: research
tags: [research, robotics, imitation-learning, reinforcement-learning, offline-rl, sim-to-real]
sources:
  - raw/temp/osa_2018_imitation_learning_survey.pdf
  - raw/temp/ross_2011_dagger.pdf
  - raw/papers/zhao_2023_act.pdf
  - raw/temp/chi_2023_diffusion_policy.pdf
  - raw/temp/kober_2013_robot_rl_survey.pdf
  - raw/temp/tang_2024_real_world_robot_rl_survey.pdf
  - raw/temp/haarnoja_2018_sac.pdf
  - raw/temp/lee_2020_quadrupedal_locomotion.pdf
  - raw/temp/levine_2020_offline_rl_tutorial.pdf
  - raw/temp/ball_2023_rlpd.pdf
  - raw/temp/luo_2024_serl.pdf
  - raw/temp/luo_2024_hil_serl.pdf
updated: 2026-10-03
---

# ロボットの模倣学習・強化学習：Research候補

## 調査範囲と資料の状態

入門用のサーベイ、基礎アルゴリズム、実機でのmanipulationとlocomotion、既存データ・demonstrationを使うRLの接点を対象に、12本を選定した。基礎理解を優先した候補集であり、最新論文の網羅調査ではない。選定理由と読む順番はLLMによる編集上の判断であり、ユーザーの研究方針を表すものではない。

PDFは公開元から取得した一次資料で、本ページは選択用の案内である。**未ingest**。ユーザーが必要なPDFを `raw/papers/` などへ移動し、ingestを指示する運用とする。

## 入口で区別したいこと

2026-10-03追記：ユーザーの追加依頼により、一部の候補論文とWeb解説を参照した[基礎概念の記事](../../wiki/concepts/imitation_and_reinforcement_learning.md)を作成した。各論文の個別要約は未ingestのまま、PDFもこのフォルダに保管している。

- 模倣学習には、expertの行動を直接学ぶBehavioral Cloningだけでなく、報酬を推定するInverse Reinforcement Learningなどもある。[Osaら・第3〜5章](osa_2018_imitation_learning_survey.pdf)。
- ロボットRLでは、報酬を用いた学習に加えて、実世界との相互作用のコストや学習の安定性が問題となる。[Koberら・Introduction](kober_2013_robot_rl_survey.pdf)、[Tangら・Abstract / Introduction](tang_2024_real_world_robot_rl_survey.pdf)。
- Offline RLは固定された既存データから学習する設定であり、SACのoff-policyという性質と同義ではない。RLPDは既存データを使いつつオンラインで相互作用する。[Offline RL tutorial・第2〜3章](levine_2020_offline_rl_tutorial.pdf)、[SAC・Abstract](haarnoja_2018_sac.pdf)、[RLPD・第3章](ball_2023_rlpd.pdf)。
- demonstrationの利用は模倣学習だけに限られず、実機RLに組み込む方法もある。[SERL・第4章](luo_2024_serl.pdf)、[HIL-SERL・Abstract / 手法](luo_2024_hil_serl.pdf)。

## 候補一覧

各行の説明の出典はその行のローカルPDF。サーベイは分野整理の資料、手法論文は各手法の一次報告として区別して読む。

| 区分             | 論文・著者・初稿年                                                                                                                          | 選定理由・着眼点                                                                                                       | 一次資料・書誌ページ                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 模倣学習の全体像       | An Algorithmic Perspective on Imitation Learning — Osa et al.（2018）                                                                | Behavioral CloningとInverse Reinforcement Learningを整理するサーベイ。まず目次・Introduction・第5章を読み、必要に応じて各手法に進む。              | [PDF](osa_2018_imitation_learning_survey.pdf) / [公開元](https://arxiv.org/abs/1811.06711)   |
| 模倣学習の基礎        | A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning — Ross, Gordon, Bagnell（2011）             | 学習した方策の行動が次の観測分布を変える問題を扱うDAggerの原論文。学習者の訪問状態へのexpertのラベル付けとデータ集約を読む。ロボット専用論文ではない。                              | [PDF](ross_2011_dagger.pdf) / [公開元](https://proceedings.mlr.press/v15/ross11a.html)       |
| 実機での模倣学習       | Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware — Zhao et al.（2023）                                             | ALOHAによる双腕遠隔操作データ収集とAction Chunking with Transformers（ACT）を扱う。行動列の予測とtemporal ensemblingに着目する。                 | [PDF](../papers/zhao_2023_act.pdf) / [公開元](https://arxiv.org/abs/2304.13705)                        |
| 実機での模倣学習       | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — Chi et al.（2023）                                               | 観測を条件とするdiffusion modelで行動列を生成する手法。多峰性のある行動分布とreceding horizon controlに着目する。保存PDFは2024年の拡張版v5。                 | [PDF](chi_2023_diffusion_policy.pdf) / [公開元](https://arxiv.org/abs/2303.04137)            |
| ロボットRLの基礎      | Reinforcement Learning in Robotics: A Survey — Kober, Bagnell, Peters（2013）                                                        | ロボットへのRL適用を、model-based / model-free、value function / policy searchなどの観点で整理するサーベイ。2013年の文献として読む。               | [PDF](kober_2013_robot_rl_survey.pdf) / [公開元](https://doi.org/10.1177/0278364913495721)   |
| 実機RLの全体像       | Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes — Tang et al.（2024）                                     | Deep RLの実世界ロボットでの成功事例と成立要因を整理するサーベイ。Koberらの基礎的な整理を、Deep RL時代の実機事例で補うために選定。                                     | [PDF](tang_2024_real_world_robot_rl_survey.pdf) / [公開元](https://arxiv.org/abs/2408.03539) |
| RLアルゴリズム       | Soft Actor-Critic Algorithms and Applications — Haarnoja et al.（2018）                                                              | maximum entropy RLに基づくoff-policy actor-criticであるSACを扱う。温度の自動調整、連続行動、実機への適用を読む。初稿2018年、保存版は2019年のv2。            | [PDF](haarnoja_2018_sac.pdf) / [公開元](https://arxiv.org/abs/1812.05905)                    |
| 歩行・sim-to-real | Learning Quadrupedal Locomotion over Challenging Terrain — Lee et al.（2020）                                                        | シミュレーションでRLにより学習した四足歩行制御をANYmalの実環境に移す。privileged teacherからproprioceptionのみを使うstudentへの蒸留も着眼点。                 | [PDF](lee_2020_quadrupedal_locomotion.pdf) / [公開元](https://arxiv.org/abs/2010.11251)      |
| 既存データを使うRLの基礎  | Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems — Levine et al.（2020）                          | 追加のオンライン収集をせず既存データから学習するoffline RLのチュートリアル。分布シフトと、通常のoff-policy RLをそのまま使う難しさを読む。ロボット専用ではない。                    | [PDF](levine_2020_offline_rl_tutorial.pdf) / [公開元](https://arxiv.org/abs/2005.01643)      |
| 既存データとオンラインRL  | Efficient Online Reinforcement Learning with Offline Data — Ball et al.（2023）                                                      | 既存データをオンラインoff-policy RLに取り込むRLPD。prior dataとonline dataのsampling、criticの設計などのablationに着目する。純粋なoffline RLではない。 | [PDF](ball_2023_rlpd.pdf) / [公開元](https://arxiv.org/abs/2302.02948)                       |
| 実機RLの実装        | SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning — Luo et al.（2024）                                      | RLPDに基づく学習、報酬の計算、環境リセット、ロボット制御を含む実機RLのソフトウェア体系。アルゴリズム以外の実装条件も確認する。                                             | [PDF](luo_2024_serl.pdf) / [公開元](https://arxiv.org/abs/2401.16013)                        |
| デモ・人間介入とRL     | Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning — Luo et al.（2024 preprint / 2025 journal） | demonstrationと人間の修正介入を組み込む実機の視覚ベースRL。論文内の模倣学習baselineとの比較と、学習時間の条件を読む。初稿2024年、保存版v3は2025年。                     | [PDF](luo_2024_hil_serl.pdf) / [公開元](https://arxiv.org/abs/2410.21845)                    |


## 読む順番の提案

1. **全体像**：Osaらの模倣学習サーベイとTangらの実機RLサーベイ。RLの分類を補いたい場合はKoberらも読む。
2. **模倣学習の基礎と実機例**：DAgger → ACT → Diffusion Policy。
3. **RLの基礎とデータ利用**：SAC → Offline RL tutorial → RLPD。
4. **実機での成立条件**：SERL → HIL-SERL。歩行・sim-to-realにも関心があればLeeらを読む。

この順序は上記資料の内容に基づく編集上の提案。まず2本のサーベイのIntroductionと結論だけを読む選び方でもよい。

## 読む際の注意

論文間で成功率や学習時間を比較する際は、タスク、観測、ロボット、データ収集、人間介入、リセット等の条件も確認する。SERLとHIL-SERLが報告する学習時間は各論文の実験条件での結果として扱う。[SERL・第5章](luo_2024_serl.pdf)、[HIL-SERL・実験](luo_2024_hil_serl.pdf)。

本調査では、グラフベースベクトル検索をこれらの手法へ導入する有効性は検証していない。研究テーマや実験計画の提案は含めていない。

## 取得記録

取得日：2026-10-03。全PDFで `%PDF` の形式と `pdftotext` による本文抽出を確認。arXiv番号のないPDFは、本文から版番号を特定していない。ファイル名の年は原則として初稿年であり、取得版の年とは異なる場合がある。

| ファイル | 保存版のPDF内表示 | サイズ（bytes） | ダウンロード元 |
| --- | --- | ---: | --- |
| [osa_2018_imitation_learning_survey.pdf](osa_2018_imitation_learning_survey.pdf) | 版番号表示なし | 5461618 | [PDF公開元](https://arxiv.org/pdf/1811.06711) |
| [ross_2011_dagger.pdf](ross_2011_dagger.pdf) | 版番号表示なし | 1174501 | [PDF公開元](https://proceedings.mlr.press/v15/ross11a/ross11a.pdf) |
| [zhao_2023_act.pdf](../papers/zhao_2023_act.pdf) | arXiv:2304.13705v1 | 5353485 | [PDF公開元](https://arxiv.org/pdf/2304.13705) |
| [chi_2023_diffusion_policy.pdf](chi_2023_diffusion_policy.pdf) | arXiv:2303.04137v5 | 6192199 | [PDF公開元](https://arxiv.org/pdf/2303.04137) |
| [kober_2013_robot_rl_survey.pdf](kober_2013_robot_rl_survey.pdf) | 版番号表示なし | 1438064 | [PDF公開元](https://publications.ri.cmu.edu/storage/publications/pub_files/2013/7/Kober_IJRR_2013.pdf) |
| [tang_2024_real_world_robot_rl_survey.pdf](tang_2024_real_world_robot_rl_survey.pdf) | arXiv:2408.03539v3 | 4550170 | [PDF公開元](https://arxiv.org/pdf/2408.03539) |
| [haarnoja_2018_sac.pdf](haarnoja_2018_sac.pdf) | arXiv:1812.05905v2 | 6750542 | [PDF公開元](https://arxiv.org/pdf/1812.05905) |
| [lee_2020_quadrupedal_locomotion.pdf](lee_2020_quadrupedal_locomotion.pdf) | arXiv:2010.11251v1 | 2112594 | [PDF公開元](https://arxiv.org/pdf/2010.11251) |
| [levine_2020_offline_rl_tutorial.pdf](levine_2020_offline_rl_tutorial.pdf) | arXiv:2005.01643v3 | 1968659 | [PDF公開元](https://arxiv.org/pdf/2005.01643) |
| [ball_2023_rlpd.pdf](ball_2023_rlpd.pdf) | arXiv:2302.02948v4 | 3702811 | [PDF公開元](https://arxiv.org/pdf/2302.02948) |
| [luo_2024_serl.pdf](luo_2024_serl.pdf) | arXiv:2401.16013v4 | 16336867 | [PDF公開元](https://arxiv.org/pdf/2401.16013) |
| [luo_2024_hil_serl.pdf](luo_2024_hil_serl.pdf) | arXiv:2410.21845v3 | 23020066 | [PDF公開元](https://arxiv.org/pdf/2410.21845) |


### SHA-256

```text
ee5bfa62e65712a1d8b60e7598d53b738748cef5a2cc29db97ae304f83702df9  osa_2018_imitation_learning_survey.pdf
17bdd6e049e64f09010b322f9e2d4fb5c744c33ff7ac99b4c4561e39bd9082a7  ross_2011_dagger.pdf
2e2fe25860f5f9cee9e655a2714e9f2264a7a5078bcd267c16d3f39af461345a  zhao_2023_act.pdf
b65c474b696a4802d8f1457d86b637ce2c5521412570d3aa928cd54563babc8f  chi_2023_diffusion_policy.pdf
afe949ac5ee4c624537bf97cef312353cc12460436affc7b2cb5fa9878739bd4  kober_2013_robot_rl_survey.pdf
61e9e3dba24c9c90d3908cb627a4efab15bffe89fc486667ad85679fa2d1517b  tang_2024_real_world_robot_rl_survey.pdf
30df4c4ff7c878aa2938ecaf651eb5cc05dc224eb0e3b5bcc8981dbf30d7a9bd  haarnoja_2018_sac.pdf
07c5607c708ffe0b33e9c02792c699b7084895bac0e296c6895e31b18da83af3  lee_2020_quadrupedal_locomotion.pdf
3c5e18cbf6efeeb129e0b6fc6f2b076c4349291b7d34e5920913744df1411342  levine_2020_offline_rl_tutorial.pdf
a87cb856a5294e71c21474006106fd7cadcff0e986da494535f44b13117c10d0  ball_2023_rlpd.pdf
4a45bc106add1571a0f5e02f295522ce8ae75186943f66c9339a5954a81bac16  luo_2024_serl.pdf
547a4d5d9440a3f70a773798813db1c8a612f006a6994398bbee2a566daab526  luo_2024_hil_serl.pdf
```

## 取り込み状況（2026-10-03）

ACTはユーザーが `raw/papers/` に移動し、ingest済み。[論文要約](../../wiki/sources/zhao_2023_act.md)を参照。上記の取得情報は当初のResearch時点の記録。
