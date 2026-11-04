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
- Dockerイメージのビルド完了：`sha256:13e790fb80270caa3c35d656736f0332142b97fcdb0a8e0545ec1b2fc671c0c3`。
- 2026-11-04 17:11:11 JSTにコンテナ`act-official-gpu5-20261104`を起動。ID：`3fdc8181425c3a9daa55de7ba66b7534d52b616684bc767714810df0ba8959ec`。
- GPU 5の認識（Quadro RTX 8000）とMuJoCo EGL描画（480×640×3）が成功。
- 17:14 JST頃の確認でepisode 0〜10の保存完了、episode 11生成中。学習・評価はまだ開始していない。
- episode 0のHDF5を検査：action/qpos/qvelは各(400,14) float32、top画像は(400,480,640,3) uint8。
- 公式visualize_episodes.pyでepisode 0の動画・関節グラフを生成。ffprobeで640×480・50fps・400 frameを確認。
- ローカルにも`/home/wada-lab/Univ/research26_workspace/act_baseline_docker/artifacts/episode_0_video.mp4`と`episode_0_qpos.png`を回収。これはスクリプト方策のデモであり、学習済みACTの評価映像ではない。
- 途中で手元のDNSが研究室外DNSを選び、名前解決に失敗。設定済み研究室DNS 10.0.0.1へ直接照会してkubera=10.0.16.19を確認し、`HostName=10.0.16.19`・`HostKeyAlias=kubera.bigdata-lab`で既知のホスト鍵を検証して再接続。サーバーの処理は継続していた。

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

## デモ生成完了・学習開始（2026-11-04 17:24 JST頃）

- `demos.log`の最終結果は`Success: 50 / 50`。スクリプト方策による生成と関節軌道再生のログを保存。
- 全50 HDF5について画像400 frameを読み取り、画像形状・dtype、qpos/qvel/actionの形状・有限値を検証。検証プロセスはexit code 0。
- 総データサイズ：18,437,041,600 bytes。各ファイルのSHA-256と値域は`outputs/demo-validation.jsonl`。ローカルの`act_baseline_docker/artifacts/`にも回収。
- `outputs/upstream.sha256`と`outputs/container-source.sha256`を照合し、公式ソース全48ファイルがコンテナ内でも一致することを確認。
- 学習が自動開始。17:24 JST頃にはepoch 67/2000まで進行。GPU5は使用メモリ約3943MiB・使用率95%を観測。
- 初期のepoch時間は約1.5〜1.6秒。残り約50分の推定は実測途中の目安であり、終了時刻の保証ではない。
- 評価は学習完了後に自動実行予定。現時点でACTの評価成功率・評価動画は未取得。
