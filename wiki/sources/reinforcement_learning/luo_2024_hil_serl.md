---
title: "HIL-SERL: Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning"
type: source
tags: [robotics, reinforcement-learning, HIL-SERL, SERL, RLPD, human-in-the-loop, demonstrations, bimanual-manipulation]
sources:
  - ../../../raw/papers/luo_2024_hil_serl.pdf
updated: 2026-10-31
---

# HIL-SERL: Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning

## 書誌情報と要点

- 著者：Jianlan Luo、Charles Xu、Jeffrey Wu、Sergey Levine（UC Berkeley）。
- 対象版：arXiv:2410.21845v3、2025年3月20日、54ページ。表紙の「Oct 2024」と取り込んだ版の更新日は区別する。
- 一次資料：[保存済みPDF・表紙](../../../raw/papers/luo_2024_hil_serl.pdf)。原本はtempからpapersへ移動し、内容は変更していない。

**初期デモと、学習中の人による修正介入を使って、精密・動的・双腕の操作を実機で学ぶ視覚ベースRLシステム**。SERLのRLPDベースの構成を発展させ、必要な場面で人が制御を引き継ぎ、その経験からも報酬に基づいて方策を改善する。人の修正を正解行動として教師あり学習するHG-DAggerとは、介入の形式が似ていても学習目的が異なる。[出典：§1–3](../../../raw/papers/luo_2024_hil_serl.pdf)

## SERLから何が変わるか

著者らは、SERLが初期デモを使うのに対し、HIL-SERLでは**オンラインの修正も継続的に学習データへ取り込む**点を区別する。また、双腕の協調、gripperの離散制御、動的操作を含む幅広い実験へ拡張している。SERLそのものの構成と実験は[既存要約](luo_2024_serl.md)を参照。[出典：HIL-SERL §2–3](../../../raw/papers/luo_2024_hil_serl.pdf)

## 学習データの流れ

1. カメラ画像から成功判定を行うbinary reward classifierを用意する。
2. 通常20–30本の成功デモをdemo bufferへ入れる。
3. actorが実機で方策を動かす。人はSpaceMouseで必要なときに操作を引き継ぎ、方策の出力を人の行動へ置き換える。
4. 人の介入中の遷移は**demo bufferとRL bufferの両方**へ入れる。方策自身が実行した遷移はRL bufferだけへ入れる。
5. learnerは両bufferから半分ずつsamplingし、RLPDでQ-functionと方策を更新する。更新した方策をactorへ送る。

出典：[§3.1–3.5・Figs. 2–3](../../../raw/papers/luo_2024_hil_serl.pdf)。1本のepisodeの中で複数回介入できる。demo bufferは初期デモだけを保持する固定集合ではない。近傍検索によるデモ選択も、この学習手順には含まれない。

RLPDはoff-policy actor-criticであり、過去のデモ・介入・自律試行を報酬に基づく更新に利用できる。人の行動へ直接合わせるBCの損失を中核とする方法ではない。人の修正は、失敗状態から回復する経験や、探索だけでは到達しにくい成功への経路を与える役割を持つ。[出典：§3.1・3.4・4.5](../../../raw/papers/luo_2024_hil_serl.pdf)

## 実機システムと準備

### 観測・報酬・制御

- 観測はカメラ画像とproprioception。画像をcropして128×128へ縮小し、ImageNet事前学習済みResNet-10で特徴化する。
- 報酬はタスク別binary classifierによるsparse rewardで、完了時に正、未完了時に0を与える。通常はpositive約200点・negative約1000点を収集し、誤判定があれば追加する。classifierの評価精度は一般に95%超と報告するが、実行中の誤判定が起きない保証ではない。
- 精密操作では、episode開始時基準のproprioceptionと現在の手先座標系での行動を使う。多くのタスクで方策10 Hz、impedance controller 1 kHzとし、実時間側でreferenceを制限する。
- Jenga whippingとobject flippingでは3 DoF feedforward wrenchを低レベルcontrollerへ渡す。すべてのタスクで同じ6D twistを使うわけではない。

出典：[§3.3・3.5、Appendices A・B・D](../../../raw/papers/luo_2024_hil_serl.pdf)。画像classifier用データと、RLの初期デモは役割が異なる。

### Gripperの連続・離散制御を分ける

腕の連続行動はRLPDの方策で出し、gripperは別のcriticをDQNに基づいて学習する。単腕ならopen / close / stayの3択、双腕ならその組合せ9択を評価し、argmaxで行動を選ぶ。両者の行動を組み合わせて実行する。[出典：§3.3 Gripper Control・Fig. 2](../../../raw/papers/luo_2024_hil_serl.pdf)

### 人の負担とリセットは残る

各試行のリセットはscripted motionまたは人手。SERLにあるforward/backward方策によるreset-free学習を全タスクに採用した構成ではない。人は初期デモの収集だけでなく、報酬ラベル、オンライン介入、必要なリセットにも関わる。[出典：§3.5・Appendix A](../../../raw/papers/luo_2024_hil_serl.pdf)

著者らは、必要な箇所で具体的に修正し、それ以外では自律探索させることを勧める。一方で、成功まで長く操作し続ける疎な介入を繰り返すと、特に学習初期に価値の過大評価と不安定さを招くと注意している。これは論文の運用上の指摘であり、最適な介入規則を一般に証明したものではない。[出典：§3.4–3.5](../../../raw/papers/luo_2024_hil_serl.pdf)

## 主実験：タスク別結果

Table 1(a)の「BC」列は、多くのタスクでは**初期BC＋HG-DAggerによる追加修正**のbaseline。HIL-SERLとepisode数・介入数を揃えるようにする。例外としてJenga whippingは50本、object flippingは200本のデモを使う固定データのBCであり、比較条件は一律ではない。[出典：§4.3・Table 1(a)](../../../raw/papers/luo_2024_hil_serl.pdf)

| タスク | 学習時間 | baseline成功率 | HIL-SERL成功率 | cycle time baseline / HIL-SERL |
| --- | ---: | ---: | ---: | ---: |
| RAM Insertion | 1.5時間 | 29% | 100% | 8.3 / 4.8秒 |
| SSD Assembly | 1時間 | 79% | 100% | 6.7 / 3.3秒 |
| USB Grasp-Insertion | 2.5時間 | 26% | 100% | 13.4 / 6.7秒 |
| Cable Clipping | 1.25時間 | 95% | 100% | 7.2 / 4.2秒 |
| IKEA Side Panel 1 | 2時間 | 77% | 100% | 6.5 / 2.7秒 |
| IKEA Side Panel 2 | 1.75時間 | 79% | 100% | 5.0 / 2.4秒 |
| IKEA Top Panel | 1時間 | 35% | 100% | 8.9 / 2.4秒 |
| IKEA Whole Assembly | 記載なし | 1/10 | 10/10 | 記載なし |
| Car Dashboard Assembly | 2時間 | 41% | 100% | 20.3 / 8.8秒 |
| Object Handover | 2.5時間 | 79% | 100% | 16.1 / 13.6秒 |
| Timing Belt Assembly | **6時間** | 2% | 100% | 9.1 / 7.2秒 |
| Jenga Whipping | 1.25時間 | 8% | 100% | 記載なし |
| Object Flipping | 1時間 | 46% | 100% | 3.9 / 3.8秒 |

出典：[Table 1(a)・§4.3](../../../raw/papers/luo_2024_hil_serl.pdf)。通常は各100評価試行、IKEA全体組立のみ10試行で、学習済みの部分方策をつないで評価する。学習はRTX 4090 1枚。報告の学習時間はscripted motion、rollout、意図した停止、計算を含むが、初期準備・デモ収集等を含む総作業時間と同一視しない。

表の平均成功率はbaseline 49.7%、HIL-SERL 100%。「+101%」は相対改善であり、100 percentage pointsの向上ではない。cycle timeの平均は9.6秒から5.4秒へ短縮、約1.8倍の速度に相当する。平均値は論文の集計値として扱い、試行数の異なる行を含めた全試行の合算成功率とは区別する。[出典：Table 1(a)](../../../raw/papers/luo_2024_hil_serl.pdf)

## Ablation：初期デモとオンライン介入の役割

| 条件 | RAM Insertion | Dashboard Assembly | Object Flipping |
| --- | ---: | ---: | ---: |
| デモ・介入ともになし | 0% | 0% | 0% |
| 初期デモあり・介入なし | 48% | 0% | 100% |
| HIL-SERL | 100% | 100% | 100% |

出典：[§4.5・Table 1(b)](../../../raw/papers/luo_2024_hil_serl.pdf)。介入なし比較では、本文は初期デモを通常20本から200本へ増やしたと説明する。したがって、デモを増やすだけではRAM挿入やdashboard組立の結果に届かない一方、**object flippingでは介入なしでも成功**しており、すべてのタスクで介入が必要とはいえない。Jenga whippingも実時間修正が不適切なため30本の初期デモから学ぶ（§4.2）。

同じ3タスクに対するDiffusion Policyの成功率は27 / 18 / 56%、IBRLは75 / 0 / 95%、Residual RLは0 / 0 / 97%、DAPGは8 / 18 / 72%。これらは当該実装・調整・タスク条件での比較であり、模倣学習や各RL手法一般に対する優劣の証明ではない。[出典：§4.5・Table 1(b)](../../../raw/papers/luo_2024_hil_serl.pdf)

## 学習された挙動と分析

- 動く対象への追従、gripperを強制的に開かれた後の再把持などを定性的に示す。これを未知環境での定量的な汎化評価と混同しない。
- RAM挿入では、手先の状態訪問分布が目標へ集まるfunnel状になる様子を分析する。Q-value varianceは、**同じ状態で行動にnoiseを加えた場合のQ値の分散**であり、critic ensemble間の不確実性ではない。正規化行動に±0.2の一様noiseを加え、100 samplesで推定する。
- Jenga whippingでは方策の標準偏差が小さく、RAM挿入では接近から精密調整へ標準偏差が変わることを示し、predictive / reactiveな挙動として解釈する。別途のモデルベースplannerを導入したという意味ではない。

出典：[§4.4・5、Figs. 6–8](../../../raw/papers/luo_2024_hil_serl.pdf)。funnelと挙動の説明は著者らの経験的分析・解釈であり、全タスクの成功保証ではない。

## 限界と記述上の注意

- 各タスクの方策は個別に学習する。大幅に長いhorizonへの拡張は未解決で、広範なrandomizationや非構造環境での汎化は検証していない。[出典：§6](../../../raw/papers/luo_2024_hil_serl.pdf)
- 概要の「1–2.5時間」にはtiming belt組立6時間という例外がある。特定の評価条件での100/100は、将来の失敗率0や人間の監視が一切不要であることを意味しない。[出典：Table 1・§6](../../../raw/papers/luo_2024_hil_serl.pdf)
- Diffusion Policyのdashboard成功率はTable 1(b)で18%、§4.5本文で28%と不一致。本ページは表の18%を採用する。再現には実装・評価記録の追加確認が必要。[出典：Table 1(b)・§4.5](../../../raw/papers/luo_2024_hil_serl.pdf)
- Fig. 5の学習曲線は介入を含む実行の移動平均であり、人が助けた成功を含む場合がある。Table 1の最終評価と区別する。介入率はepisode内の介入step数 / 全step数で、20 episodesの移動平均。[出典：Fig. 5 caption・§4.3](../../../raw/papers/luo_2024_hil_serl.pdf)
- 本論文はグラフベース近傍検索を評価していない。検索によるデータ選択への適用効果は、この結果だけから主張できない。[出典：§3–4](../../../raw/papers/luo_2024_hil_serl.pdf)

## 再現時に参照する付録

Appendix Aはタスク別の観測・行動・初期デモ・リセット・randomization等を列挙する。例えばRAMは初期デモ20本、最大100 steps、scripted reset、timing beltは20本、最大200 steps、human reset。両者とも環境10 Hz、discount factor 0.97、MLP 256×256、Adam・learning rate 3e-4を記す。これらを全タスク共通と決めつけない。[出典：Appendix A、Tables 2・10](../../../raw/papers/luo_2024_hil_serl.pdf)

Appendix Bは報酬classifier、CはDiffusion Policy baseline、Dは座標表現とcontroller、Eは追加の学習曲線を扱う。本ingestは保存PDFの整理であり、コード実行や実機再現は行っていない。[出典：Appendices B–E](../../../raw/papers/luo_2024_hil_serl.pdf)

## 関連ページ

- [SERL：元となる実機RLのソフトウェア基盤](luo_2024_serl.md)
- [デモを併用する実機RL：SERLとHIL-SERLのデータの流れ](../../concepts/reinforcement_learning/demonstration_augmented_robot_rl.md)
- [模倣学習と強化学習の基本](../../concepts/imitation_learning/imitation_and_reinforcement_learning.md)
