---
title: "Mobile ALOHA：観測・行動データの構造"
type: entity
tags: [Mobile-ALOHA, dataset, robot-arm, imitation-learning]
sources:
  - ../../raw/temp/mobile_aloha_project.html
  - ../../raw/temp/mobile_aloha_record_episodes.py
  - ../../raw/temp/mobile_aloha_real_env.py
  - ../../raw/temp/mobile_aloha_constants.py
  - ../../raw/temp/tfds_aloha_mobile_snapshot.txt
updated: 2026-10-31
---

# Mobile ALOHA：観測・行動データの構造

## 資料の範囲

2026-10-20に保存した公式ページ、記録・環境コード、TFDSカタログの整理。実機の双腕移動manipulationを扱う。実データ全件の取得やHDF5内部検査は行っていない。[公式ページ](../../raw/temp/mobile_aloha_project.html)、[TFDS保存原文](../../raw/temp/tfds_aloha_mobile_snapshot.txt)

LeRobot配布版の件数表・カード由来の説明は、2026-10-31のユーザー指示により整理対象から除外した。

## 公式HDF5の記録構造

| 項目 | 保存コード上の内容 |
| --- | --- |
| observations/images | 複数カメラの画像 |
| observations/qpos・qvel・effort | それぞれ14次元 |
| action | 左右の腕それぞれ6関節＋gripperの計14次元 |
| base_action | 台車の2次元データ |

出典：[record_episodes.py](../../raw/temp/mobile_aloha_record_episodes.py)、[real_env.py](../../raw/temp/mobile_aloha_real_env.py)。圧縮時はJPEGバイト列とcompress_lenを使う。base_actionは観測のbase_velを記録しているため、記録値をそのまま操作指令と同一視しない。[記録処理](../../raw/temp/mobile_aloha_record_episodes.py)

`effort`という名前だけでは校正済みの接触力やBi-ACTの力覚教師と同じとは確認できない。これはコードから読み取れる範囲の留保であり、センサ校正を検証した結果ではない。[環境コード](../../raw/temp/mobile_aloha_real_env.py)

公式ページにはデータ配布先へのリンクがあるが、フォルダ内の全件数は今回再確認していない。タスク設定には調理・収納などが含まれるが、設定の存在だけを公開実データの確認とは扱わない。[公式ページ](../../raw/temp/mobile_aloha_project.html)、[constants.py](../../raw/temp/mobile_aloha_constants.py)

## TFDS / RLDS表現

保存カタログではtrainは276 episodes、47.42 GiB。観測は3視点の480×640 RGB画像と14次元state、actionは16次元。stepsにreward・discount・is_first・is_last・is_terminal・language_instructionを持つ。[保存カタログ](../../raw/temp/tfds_aloha_mobile_snapshot.txt)

16次元の各成分や変換方法を、このスキーマだけで確定しない。原HDF5と別の独立収集コーパスとも数えない。保存カタログ原文はMarkdown記事整理に伴って拡張子をtxtへ変更し、本文のバイト列は維持した。[原文](../../raw/temp/tfds_aloha_mobile_snapshot.txt)

実機データを既存MuJoCoタスクにそのまま投入して閉ループ成功率を評価できるかは未確認。これは資料の確認範囲の留保であり、使用する実験環境の決定ではない。

## 関連ページ

- [ACTとALOHA](../sources/imitation_learning/zhao_2023_act.md)
- [Action Chunking](../concepts/imitation_learning/action_chunking_and_temporal_ensembling.md)
