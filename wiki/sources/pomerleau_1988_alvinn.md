---
title: "ALVINN: An Autonomous Land Vehicle in a Neural Network"
type: source
tags: [robotics, autonomous-driving, road-following, supervised-learning, neural-network, synthetic-data, ALVINN]
sources:
  - ../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf
updated: 2026-10-05
---

# ALVINN: An Autonomous Land Vehicle in a Neural Network

## 書誌情報と要点

- 著者：Dean A. Pomerleau（Carnegie Mellon University）。
- 取り込んだ版：NIPS 1988、Advances in Neural Information Processing Systems 1、pp.305–313。
- 一次資料：[保存済みPDF](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)。本文の参照ページは冊子のページ番号であり、PDFでは1–9ページに対応する。

著者・ページは[原論文](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)、会議・巻は[公式掲載ページ](https://proceedings.neurips.cc/paper/1988/hash/812b4ba287f5ee0bc9d43bbf5bbe87fb-Abstract.html)で確認した。

ALVINN（Autonomous Land Vehicle In a Neural Network）は、カメラとlaser range finderの入力から、道路を追従するための旋回方向を出力するニューラルネットワーク。**本論文の学習データは人工生成した道路画像と教師信号であり、人間の運転デモで学習した実験ではない。** シミュレーションで学んだネットワークをNAVLAB実車へ適用し、限定された環境条件で道路追従を示した。[出典：Abstract・Training and Performance、pp.305・307–309](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## 何を学ぶのか

対象は道路の中央へ向かうroad followingである。教師の旋回曲率は「現在位置から7m先の道路中央へ車両を向かわせる曲率」と定義される。報酬の最大化による強化学習ではなく、人工画像に対応する望ましい出力をback-propagationで学ぶ。[出典：Network Architecture・Training and Performance、pp.306–308](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## ネットワーク構成

入力層・隠れ層・出力層からなる3層ネットワークで、隠れ層は1層。各入力から隠れ層、隠れ層から出力層へ全結合する。[出典：Network Architecture・Fig.1、pp.305–306](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

| 部分 | 次元・役割 |
| --- | --- |
| カメラ入力 | 30×32＝960 units。画像のblue bandの明るさを入力する |
| range finder入力 | 8×32＝256 units。対応する領域の近さを入力する |
| feedback入力 | 1 unit。前の画像で道路が周囲より明るいか暗いかを表す |
| 隠れ層 | 29 units |
| 旋回出力 | 45 units。中央が直進、左右へ行くほど急な左右旋回を表す |
| feedback出力 | 1 unit。現在の画像で道路が周囲より明るいか暗いかを表す |

入力は合計1217、出力は合計46 units。blue bandは道路と周囲のcontrastが高いとして選ばれている。実行時にはfeedback出力を次の入力へ戻すため、画像1枚だけを独立に処理する構成ではない。OCRで崩れたカメラ入力の次元はPDF画像のFig.1と本文で確認した。[出典：Network Architecture、pp.306–307](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

### 正解出力の表現

旋回方向を単一の数値へ直接回帰するのではなく、45個の出力unitで表す。正解の曲率を表すunitの周囲9個に、0.10、0.32、0.61、0.89、1.00、0.89、0.61、0.32、0.10という山形の教師信号を与え、それ以外は0とする。実行時は**最大activationのunitが表す曲率**を採用する。近い曲率にも教師信号を与えるが、この出力は総和1の確率分布として定義されてはいない。[出典：Network Architecture、pp.306–307](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## 学習データと手順

実道路の画像を多様な条件で収集する負担や、カメラの向きを変更すると再収集が必要になる問題を避けるため、人工道路画像のgeneratorを使う。generatorはカメラ画像だけでなくrange finder画像も生成する。学習セットは道路の画像内の位置・向き、照明、現実的なnoiseを変化させた1200 snapshotsである。[出典：Training and Performance、pp.307–308](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

学習初期にはfeedback入力をランダムに与え、feedback入力をそのまま出力へコピーするだけの学習を防ぐ。画像から道路の明暗関係を判定する表現を獲得した後、前画像での道路と周囲の明暗関係を入力する。学習にはWarp上のback-propagation simulatorを使う。[出典：Training and Performance、pp.307–308](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## 評価結果と、その読み方

| 評価 | 報告内容 | 条件・注意 |
| --- | --- | --- |
| 未見の人工道路画像 | 約90%で正解曲率から2 output units以内 | 1200 snapshotsで40 epochs学習後。厳密な曲率一致率や実車の成功率ではない |
| NAVLAB実車 | 約0.5m/sで400mの道を追従 | CMUキャンパスの林の中、晴れた秋の条件。推論は車載Sun computer |
| 従来手法との比較 | 類似の条件・同じコースで、従来手法は約1m/sかつ同程度の運転精度 | 従来手法はWarp上で実行。計算機条件が異なるため、ネットワークの優劣をこの速度差だけでは判断できない |

以上は[Training and Performance、pp.308–309](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)に基づく。実車試行回数、介入回数、統計的な成功率はこの記述では報告されていない。著者自身も、他手法との確定的な性能比較には天候・照明条件を広げた検証が必要だと述べる。[出典：Discussion and Extensions・Conclusion、p.312](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## 学習データによって変わる内部表現

道路幅を固定した画像で学ぶと、隠れunitは1–3本の道路位置に対応するfilterのような表現を得る。一方、道路幅を大きく変えると、片側の道路境界を検出するような表現が現れる。これは著者による接続重みの解釈であり、汎用的な視覚能力を実証したという意味ではない。[出典：Network Representation・Figs.4–5、pp.309–311](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

range finderの重みはカメラに比べて小さいが、道路と見なす場所の外側に障害物があると隠れunitを活性化し、内側にあると抑制する傾向が示される。ただし、本論文の道路追従条件では、range finder入力を障害物のない一定画像に置き換えても目立つ性能低下はなかった。これはoff-roadでの障害物回避にも不要という結果ではない。[出典：Discussion and Extensions、pp.311–312](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

## 限界と未実施の拡張

- 実車評価は限定的な天候・照明・コースであり、広い環境条件への一般化は未確認。
- 分岐では離れた二つの旋回方向を出力し、選択が振動して道路追従が不正確になる場合がある。停止・障害物迂回・地図を使う大域的経路計画は拡張項目として挙げられている。
- 人間が運転中の実画像を用いて適応的に学習する構想は、将来の拡張として述べられる。隠れactivationのfeedback、隠れ層追加、局所接続、Warpでの推論高速化もこの論文の実証結果とは区別する。

以上は[Discussion and Extensions・Conclusion、pp.311–312](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)に基づく。

## BC・分布シフトとの関係

本論文は、人間の運転中の画像を使う学習へ進む際、正確に走った例だけでなく、**間違えた後に道路中央へ戻る例**も必要だと指摘している。また、運転を引き継いだ際に遭遇する状況を学習データが十分に覆わなければ、頑健な表現を得られないと述べる。[出典：Discussion and Extensions、p.311](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)

**Wiki上の整理**：この指摘は、BCにおける実行時のdistribution shiftと関連付けて読むことができる。ただし、ALVINNの本実験は人工画像を用いた教師あり学習であり、デモからのBCの実験やDAggerの実装・評価として扱わない。DAggerは後年、学習者が訪れる状態へexpertのラベルを追加してデータを集約する方法を示した。[関連付けの根拠：ALVINN p.311](../../raw/papers/NIPS-1988-alvinn-an-autonomous-land-vehicle-in-a-neural-network-Paper.pdf)、[DAgger §1–3](../../raw/temp/ross_2011_dagger.pdf)

## 関連ページ

- [Behavior Cloning：学習方法と分布シフト](../concepts/behavior_cloning.md)
- [ロボットの模倣学習と強化学習](../concepts/imitation_and_reinforcement_learning.md)
- [ACTの論文要約](zhao_2023_act.md)
