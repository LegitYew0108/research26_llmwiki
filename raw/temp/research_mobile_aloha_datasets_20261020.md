---
title: Mobile ALOHAの観測・動作データセット候補調査
type: research
tags: [dataset, Mobile-ALOHA, ACT, imitation-learning, retrieval]
sources:
  - raw/temp/mobile_aloha_project.html
  - raw/temp/mobile_aloha_record_episodes.py
  - raw/temp/mobile_aloha_constants.py
  - raw/temp/mobile_aloha_real_env.py
  - raw/temp/tfds_aloha_mobile.md
  - raw/temp/lerobot_aloha_mobile_cabinet_card.md
  - raw/temp/lerobot_aloha_mobile_chair_card.md
  - raw/temp/lerobot_aloha_mobile_elevator_card.md
  - raw/temp/lerobot_aloha_mobile_shrimp_card.md
  - raw/temp/lerobot_aloha_mobile_wash_pan_card.md
  - raw/temp/lerobot_aloha_mobile_wipe_wine_card.md
updated: 2026-10-20
---

# Mobile ALOHAの観測・動作データセット候補

調査日：2026-10-20。Researchの一時資料。未ingest。公開ページ・スキーマ・記録コードを確認した段階であり、実データの全件ダウンロード・HDF5内部検査は未実施。

## 結論

Mobile ALOHAの公開デモは条件に合う。**台車を含む動作を扱う場合は公式HDF5版を優先**する。記録コードには画像・関節位置・速度・effortと、腕14次元action・台車2次元base_actionがある。一方、下記LeRobot版の公開スキーマではactionは14次元で、base_actionは掲載されていない。[記録コード](mobile_aloha_record_episodes.py)、[環境コード](mobile_aloha_real_env.py)、下表のカード。

研究への適合度は以下では調査者の判断として示す。研究方針の採用・実験計画の決定を意味しない。

## タスク別候補

件数・フレーム数は**確認したLeRobot配布版**の値。公式原データ全体の件数と同一とは限らない。全6件のカードで3視点640×480画像、14次元state・effort・action、50 fpsを確認した。名称にMobileがあっても、この変換版だけでは台車動作を学習できるとは扱わない。[各カード](#一次資料の所在)

|タスク／配布先|episodes|frames|形式版|参照候補としての評価（推測）|ローカル出典|
|---|---:|---:|---|---|---|
|[cabinet](https://huggingface.co/datasets/lerobot/aloha_mobile_cabinet)：キャビネット・鍋の収納|85|127,500|v3.0|最優先候補。候補中最多の軌跡数があり、把持・扉操作の動作検索を調べやすそう|[カード](lerobot_aloha_mobile_cabinet_card.md)|
|[wash_pan](https://huggingface.co/datasets/lerobot/aloha_mobile_wash_pan)：フライパンのすすぎ|50|55,000|v2.0|最初のデータ処理確認に適しそう。比較的短い系列|[カード](lerobot_aloha_mobile_wash_pan_card.md)|
|[wipe_wine](https://huggingface.co/datasets/lerobot/aloha_mobile_wipe_wine)：こぼれたワインを拭く|50|65,000|v2.0|拭き動作の反復や部分軌跡検索の参照候補|[カード](lerobot_aloha_mobile_wipe_wine_card.md)|
|[chair](https://huggingface.co/datasets/lerobot/aloha_mobile_chair)：椅子を扱うタスク|55|110,000|v2.0|台車を含む協調動作の参照候補。全身動作の確認にはHDF5を使う|[カード](lerobot_aloha_mobile_chair_card.md)|
|[shrimp](https://huggingface.co/datasets/lerobot/aloha_mobile_shrimp)：エビの調理・配膳|18|67,500|v3.0|長い複合動作の参照候補。ただしこの配布版は軌跡数が少ない|[カード](lerobot_aloha_mobile_shrimp_card.md)|
|[elevator](https://huggingface.co/datasets/lerobot/aloha_mobile_elevator)：エレベータ操作・移動|20|45,000|v2.0|移動＋操作を調べる候補。配布版の範囲・切り詰めを要確認|[カード](lerobot_aloha_mobile_elevator_card.md)|

タスク名と設定は[公式constants.py](mobile_aloha_constants.py)、調理・収納・エレベータ・すすぎの説明は[公式ページ](mobile_aloha_project.html)にも基づく。公式設定にはhigh_fiveなどもあるが、設定の存在のみを公開実データの確認とは扱わず、主要一覧には含めなかった。

## 入手形式を選ぶ

### 1. 公式HDF5版：全身動作の第一候補

- [公式プロジェクト](https://mobile-aloha.github.io/)のDatasetsリンク → [Google Drive](https://drive.google.com/drive/folders/1FP5eakcxQrsHyiWBRDsMRvUfSxeykiDc)。リンク先到達は確認したが、今回のWeb取得ではフォルダ内部の全件数を検証できなかった。[保存した公式ページ](mobile_aloha_project.html)
- observations/images以下にカメラ画像、qpos・qvel・effort各14次元、action 14次元、base_action 2次元を記録する。圧縮時はJPEGバイト列とcompress_lenを保存するため、生の画像テンソルとは読み方が異なる。[記録コード](mobile_aloha_record_episodes.py)
- 腕actionは左右それぞれ6関節＋gripper。台車は線速度・角速度。base_actionは記録時に観測のbase_velから保存されているため、「操作指令そのもの」と決めつけず、遅延・同期の扱いも確認する。[環境コード](mobile_aloha_real_env.py)、[記録コード](mobile_aloha_record_episodes.py)
- effortの名前だけから校正済み接触力やBi-ACTの力覚教師と同一とは判断できない。単位・センサ由来は別途確認が必要（調査上の留保）。

### 2. LeRobot版：画像＋腕の状態・動作を扱いやすい候補

上表のHugging Faceリンクから取得できる。MP4動画とParquetの形式。state・effort・action各14次元で、base_actionとqvelは公開スキーマに掲載されていない。今回の条件を腕の動作に限るなら適合するが、台車の動作も必須ならこの版だけでは不足する。[6件のカード](#一次資料の所在)

cabinet・shrimpはv3.0、残る4件はカード上v2.0なので、読み込みコードとの互換性と使用revisionを固定する必要がある（スキーマからの判断）。カードのライセンス表示はcabinet・shrimpがApache-2.0、残る4件はMIT。原配布と変換版の条件を同一と仮定しない。[各カード](#一次資料の所在)

### 3. TensorFlow Datasets / RLDSのaloha_mobile：統一形式の候補

[公式カタログ](https://www.tensorflow.org/datasets/catalog/aloha_mobile)では276 episodes、47.42 GiB。観測は3視点画像とstate 14次元、actionは16次元。原HDF5・LeRobot版とは別収集のコーパスと数えず、Mobile ALOHAの別形式として扱う。16次元の各成分・変換方法、取得経路の動作は変換コードと実ファイルで別途確認が必要。[カタログ保存版](tfds_aloha_mobile.md)

## 今回の研究との関係と限界

**調査者の判断**：観測と動作のペアを検索しACTの学習資料を選ぶ用途では、同じロボットで複数タスクがあり、形式が共通する点で有望。まずcabinet、wash_pan、wipe_wineが参照候補となる。ただし件数は数十〜数百episodes規模であり、フレームや重なった部分系列を大量に作っても独立したデモ数が増えるわけではない。[カード](#一次資料の所在)

これらは実機のデモデータである。[公式ページ](mobile_aloha_project.html)、[TFDS](tfds_aloha_mobile.md)。したがって、既存のMuJoCo環境にそのまま投入して同じタスクの成功率を評価できるとは確認していない。検索速度やオフラインの予測誤差と、閉ループ実行時の成功率は区別する必要がある（方法上の判断）。既存のユーザー研究計画は変更していない。

## 一次資料の所在

2026-10-20に以下の公開原文を取得した。Python・HTMLは原形式、カードは原Markdownを保存。個別原文ファイルにはfrontmatterを付けず、原文を保全する。

- [公式ページ](mobile_aloha_project.html)：https://mobile-aloha.github.io/
- [記録コード](mobile_aloha_record_episodes.py)：https://github.com/MarkFzp/mobile-aloha/blob/main/aloha_scripts/record_episodes.py
- [設定コード](mobile_aloha_constants.py)：https://github.com/MarkFzp/mobile-aloha/blob/main/aloha_scripts/constants.py
- [環境コード](mobile_aloha_real_env.py)：https://github.com/MarkFzp/mobile-aloha/blob/main/aloha_scripts/real_env.py
- [TFDSカタログ](tfds_aloha_mobile.md)：https://github.com/tensorflow/datasets/blob/master/docs/catalog/aloha_mobile.md
- [cabinet](lerobot_aloha_mobile_cabinet_card.md)、[chair](lerobot_aloha_mobile_chair_card.md)、[elevator](lerobot_aloha_mobile_elevator_card.md)、[shrimp](lerobot_aloha_mobile_shrimp_card.md)、[wash_pan](lerobot_aloha_mobile_wash_pan_card.md)、[wipe_wine](lerobot_aloha_mobile_wipe_wine_card.md)：上表の各Hugging FaceページのREADME.md。
