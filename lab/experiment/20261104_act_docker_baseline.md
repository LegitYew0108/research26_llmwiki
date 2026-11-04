---
title: "kubera GPU5：公式ACT Docker基準実験"
type: experiment
tags: [experiment, ACT, Docker, MuJoCo, kubera]
sources:
  - ../../raw/papers/zhao_2023_act.pdf
updated: 2026-11-04
---

# kubera GPU5：公式ACT Docker基準実験

## 目的と条件

ユーザーの指示により、公式ACTコードを変更せず、Docker内でTransfer Cubeのデモ生成・学習・評価を行う。映像および公式で保存される動作データを残す。

- 公式実装：https://github.com/tonyzhaozh/act
- 使用commit：`742c753c0d4a5d87076c8f69e5628c79a8cc5488`。
- 接続先：`wadaharuto@kubera.bigdata-lab`。
- ホストGPU 5：Quadro RTX 8000、UUID `GPU-ac104ebf-b388-4675-65d2-9893921908ed`。開始前確認では使用メモリ0MiB・使用率0%。
- 保存先：`/home/wadaharuto/research26_workspace/act_baseline_docker/`。ホーム領域の空き32Tを確認。
- Dockerベース：`pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime`。MuJoCo 2.3.7、dm_control 1.0.14。実依存一覧は`outputs/pip-freeze.txt`へ保存予定。
- データパスは公式constants.pyを編集せず、コンテナ内のシンボリックリンクで解決。

## 実施状況

- SSH接続・GPU確認を実施。
- 公式ソースをgit archiveで転送し、Dockerビルドを開始。
- 現時点でデモ生成・学習・評価の結果は未取得。実行状況に応じて追記する。

## 実行する公式手順

1. GPU演算・MuJoCoヘッドレス描画を確認。
2. `record_sim_episodes.py`で`sim_transfer_cube_scripted`を50 episode生成。
3. `visualize_episodes.py`でepisode 0を動画化。
4. ACTを2000 epoch学習。seed=0、batch=8、lr=1e-5、KL=10、chunk=100、hidden=512、feedforward=3200。
5. 最良検証checkpointを`--eval --temporal_agg`で50 rollout評価。

公式の学習・検証分割と全50件からの正規化統計計算を維持する。厳密な検証分離を導入した実装とは区別する。生成デモのseedは公式CLIに指定がなく、固定しない。

## 成果物と限界

- `data/sim_transfer_cube_scripted/episode_*.hdf5`：デモの画像、qpos、qvel、教師行動。
- 同ディレクトリ：episode 0の動画・関節グラフ。
- `outputs/checkpoints/`：学習モデル・統計・曲線・評価動画・集計結果。
- `outputs/`：build、smoke、demos、train、evalのログ。全工程成功時だけ`COMPLETED`を作成。
- 評価時の予測Chunk・実行行動配列は公式コードでは保存されない。デモの教師行動と評価時の実行軌跡を区別する。

技術的背景：[ACT原論文](../../raw/papers/zhao_2023_act.pdf)。実行結果の一次記録は上記kuberaのログと成果物であり、未実行の処理を実績として扱わない。
