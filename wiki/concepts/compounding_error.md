---
title: "Behavior CloningのCompounding Error：状態分布のずれと誤りの連鎖"
type: concept
tags: [imitation-learning, behavior-cloning, compounding-error, distribution-shift, dagger]
sources:
  - ../../raw/temp/ross_2011_dagger.pdf
updated: 2026-10-17
---

# Behavior CloningのCompounding Error

## 行動が次の入力を変える

BCの誤りの蓄積は、単に毎時刻の行動誤差を足すことではない。誤った行動が次の状態を変え、expertのデモに少ない状態へ移ると、そこでの行動予測が不正確になり、さらに状態がずれるという連鎖である。必ず発生するわけではない。[出典：DAgger §1–2](../../raw/temp/ross_2011_dagger.pdf)

状態を $s_t$、行動を $a_t$、環境の遷移を $P$ とすると、実行時には $a_t=\pi(s_t)$、$s_{t+1}\sim P(\cdot\mid s_t,a_t)$ となる。方策の出力が将来の入力に影響するため、expertの状態での予測精度だけでは実行時の精度を保証できない。[出典：DAgger §1–2](../../raw/temp/ross_2011_dagger.pdf)

## 学習する分布と実行時の分布

expertを $\pi^*$、方策 $\pi$ が訪れる状態の時間平均分布を $d_\pi$ とする。標準的なBCは $\mathbb{E}_{s\sim d_{\pi^*}}[\ell(\pi(s),\pi^*(s))]$ を小さくするが、実行時の模倣精度に対応する量は $\mathbb{E}_{s\sim d_\pi}[\ell(\pi(s),\pi^*(s))]$ である。入力分布そのものが方策に依存する点が重要である。有限データでの過学習とは別に、expert分布で十分に汎化していても、この分布の違いは残りうる。[出典：DAgger §2、式(1)–(2)](../../raw/temp/ross_2011_dagger.pdf)

説明用の仮想例として、道路中央を走るデモから操舵を学ぶ場合を考える。少し右へずれると、入力は「中央から見た道路」から「右端から見た道路」へ変わる。そこでは中央へ戻す操舵が必要だが、その状態での教師例が乏しければ、さらに右へ進む可能性がある。これは原論文の特定実験の再現ではなく、分布シフトの説明例である。[機構の根拠：DAgger §1](../../raw/temp/ross_2011_dagger.pdf)

## なぜ累積コストに二乗の依存が現れるのか

DAggerのTheorem 2.1では、expert分布での0–1模倣誤り率（またはその上界）を $\epsilon$、時刻数を $T$、各時刻のタスクコストを $[0,1]$ とすると、$J(\pi)\le J(\pi^*)+T^2\epsilon$ と評価する。この増加が実現する問題も存在するが、すべてのBCで必ず二乗増加するという意味ではない。連続行動のMSEをそのまま $\epsilon$ に代入することもできない。[出典：DAgger §2.1、Theorem 2.1](../../raw/temp/ross_2011_dagger.pdf)

直感を得るため、各時刻のexpert分布での誤り率が $\epsilon$ 以下で、一度誤ると残りの時刻すべてで追加コストを払う最悪ケースを考える。時刻 $t$ までに誤る確率はunion boundで高々 $t\epsilon$（厳密には1以下）なので、累積の追加コストは $\sum_{t=1}^T t\epsilon=\epsilon T(T+1)/2=O(T^2\epsilon)$ と見積もれる。この説明は一様な時刻別誤り率を置いた簡略化で、誤りの独立性は必要ない。単純に毎時刻 $\epsilon$ のコストを払う $T\epsilon$ との違いは、一度の誤りが後続の多数の時刻に影響する点である。[理論の根拠：DAgger §1・2.1](../../raw/temp/ross_2011_dagger.pdf)

これは物理的な位置誤差が $T^2$ に比例するという主張ではない。また、コストが有界なので累積コスト自体は高々 $T$ であり、大きな $T\epsilon$ では二乗の上界は緩くなる。[出典：DAgger §2のコスト定義・Theorem 2.1からの帰結](../../raw/temp/ross_2011_dagger.pdf)

## 回復とDAgger

ずれた状態で適切に修正できれば、最初の誤りが長期の損失につながるとは限らない。原論文は、expertが少数ステップで回復できる場合、一回の誤りが将来コストへ与える影響を小さく抑えられると説明する。[出典：DAgger §2.2、Theorem 2.2](../../raw/temp/ross_2011_dagger.pdf)

DAggerは学習者を実行し、実際に訪れた状態に対するexpertの行動を教師ラベルとして取得し、既存データに追加して再学習する。学習者が出した行動をそのまま正解として追加する方法ではない。学習対象の分布を実行時へ近づけることで連鎖に対処するが、一般のタスクコストの保証には回復可能性などの条件が関わり、任意の失敗を修復できる保証ではない。[出典：DAgger §3、Algorithm 3.1、Theorem 3.1–3.2](../../raw/temp/ross_2011_dagger.pdf)

## 関連ページ

- [Behavior Cloning：学習方法と分布シフト](behavior_cloning.md)
