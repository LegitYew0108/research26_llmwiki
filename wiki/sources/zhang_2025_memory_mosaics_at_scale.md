---
title: "Memory Mosaics at scale"
type: source
tags: [memory-mosaics, associative-memory, language-model, in-context-learning, kernel-regression]
sources:
  - ../../raw/papers/2507.03285v3.pdf
updated: 2026-10-09
---

# Memory Mosaics at scale

## 書誌情報と要点

著者はJianyu Zhang、Léon Bottou。NeurIPS 2025の論文で、本ページの対象はarXiv:2507.03285v3（2026年1月14日）。一次資料は[保存したPDF](../../raw/papers/2507.03285v3.pdf)。以下の結果はこの版に基づく。[出典：表紙](../../raw/papers/2507.03285v3.pdf)

Memory Mosaicsを約10B parameters・1T tokensの言語モデルへ拡大し、**Memory Mosaics v2**として評価する。通常の言語ベンチマークでは比較Transformerと近い性能を保ち、文脈内の新情報の検索と、例示から分類規則を使うin-context learning（ICL）では優位を報告する。主な変更はadaptive bandwidth、入力依存のgateを持つkey extractor、3種類のmemoryである。[出典：§1・3–5](../../raw/papers/2507.03285v3.pdf)

## 連想記憶としてのモデル

[Associative MemoryとKernel Regression](../concepts/associative_memory_and_kernel_regression.md)では、key-value集合からqueryに似たkeyのvalueを重み付き平均して取り出す。keyは最近の過去を、valueはその近傍の未来を表す特徴で、同じkey抽出方法をqueryにも使う。明示的なposition encodingを使わないが、key抽出の再帰計算とvalueの隣接時刻の混合を通じて順序を扱う。[出典：§2・3、式(3)–(9)](../../raw/papers/2507.03285v3.pdf)

v2の変更は次の通り。[出典：§3](../../raw/papers/2507.03285v3.pdf)

- **Adaptive bandwidth**：key-value数を $n$ として、softmaxの鋭さを $\beta=\beta_1 n^\alpha+\beta_0$ で調整する。$\beta$ が大きいほど、似たkeyへ重みが集中する。各係数は学習する。
- **Gated key extractor**：$\bar k_t=g_t W_\phi x_t+\lambda_t\bar k_{t-1}$ をL2正規化してkeyにする。$g_t=\exp(W_gx_t)$、$\lambda_t=\exp(-|W_\lambda x_t|)$ は入力に依存し、過去の保持と現在入力の寄与を調整する。
- **3-level memory**：短期と長期の文脈記憶を別のパラメータで構成し、学習済み知識を担うpersistent memoryと組み合わせる。

| 種類 | 保存する情報・実装 |
| --- | --- |
| Short-term memory | 最近のtokenのkey-value。window設定は $h=256$。 |
| Long-term memory | 現在からdelay $m$ 以上前のtokenのkey-value。短期との重なりを許す。 |
| Persistent memory | 訓練で重みに蓄積する情報。SwiGLUのdense 2-layer networkで実装する。 |

学習時は $m$ を[64, 256]からサンプリングし、推論時は64に固定する。「long-term」は入力文脈の古いtokenを指し、会話を越えた永続データベースを意味しない。本文の短期範囲は $t-h+1$ から $t-1$、付録Fig. 11は $t-h$ から $t-1$ と記しており、境界には1 tokenの表記差がある。再現時の実装確認事項として残す。[出典：§3.3・4、Appendix C・Fig. 11](../../raw/papers/2507.03285v3.pdf)

## 学習・比較条件

smallは24層・hidden dimension 2048・16 heads、200B tokensで学習。largeは32層・4096・32 heads、1T tokensで学習する。文脈長4096で事前学習し、32768へfine-tuningする。比較TransformerはLlama系のmulti-head attentionで、対応する設定・datamixを使う。ただしlargeのparametersはTransformer 8.8Bに対しv2 9.9Bで、完全に同じモデルサイズではない。[出典：§4、Table 2](../../raw/papers/2507.03285v3.pdf)

共通のbatch sizeは1024、optimizerはAdamW。論文のGPUは80GB H100。ハイパーパラメータはTransformer向けに探索したものをv2へ転用したとされる。[出典：Appendix C・J](../../raw/papers/2507.03285v3.pdf)

## 結果：何が改善したか

### 1. 訓練で得た知識

19個の一般的な言語ベンチマークの平均はlargeで両者52.2。長期記憶を学習後に除くと、13タスク平均は56.8から56.6へほぼ変わらない一方、残る6タスク平均は42.1から34.9へ下がる。著者は前者をpersistent knowledge中心の評価として扱うが、これは除去実験に基づく解釈であり、各タスクの能力を完全に切り分けた証明ではない。[出典：§5.1、Tables 1–2・9](../../raw/papers/2507.03285v3.pdf)

### 2. 文脈内の新情報の保存と検索

RULERの複数の無関係な文書を連結し、**文書の後に質問を置く**QAを評価する。32kへfine-tuningしたモデルの結果は次の通り。数値は論文のaccuracy（%）である。[出典：§5.2、Table 4](../../raw/papers/2507.03285v3.pdf)

| モデル | 4k | 8k | 16k | 32k | 64k |
| --- | ---: | ---: | ---: | ---: | ---: |
| Transformer small | 37.0 | 29.3 | 29.0 | 22.1 | × |
| Memory Mosaics v2 small | 44.3 | 39.3 | 39.4 | 36.9 | 25.3 |
| Transformer large | 51.2 | 48.8 | 44.7 | 41.1 | × |
| Memory Mosaics v2 large | 58.9 | 55.5 | 54.9 | 53.4 | 46.4 |

32kでの差はsmallが14.8、largeが12.3 **percentage points**。×は原表の失敗表記で、0%という測定値には置き換えない。4k学習のみでもv2は32kでsmall 31.7、large 26.5を報告するが、学習時の4k精度（45.0、59.3）から低下しており、無劣化の外挿ではない。[出典：Tables 3–4](../../raw/papers/2507.03285v3.pdf)

長期記憶を除くとlargeの32k精度は53.4から20.2へ低下。delayをランダム化する学習ではsmallの4k学習→32k評価が15.9から31.7へ改善する。典型的な単一needle検索では両モデルがほぼ満点となり、同じ差は現れない。[出典：Tables 10・12–13](../../raw/papers/2507.03285v3.pdf)

### 3. In-context learning

Banking77（77クラス）、Tacred（41クラス）、Goemotion（28クラス）で、意味のあるラベルと匿名ラベルの分類を評価する。**1 shotは全クラスから1例ずつ**なので、例えばBanking77の2 shotsは154例となる。各shot数でdelimiterと例の順序を変え、最も良いprompt設定を採用する。[出典：§5.3・脚注13、Appendix I](../../raw/papers/2507.03285v3.pdf)

v2は例示数の増加に伴って改善し、比較Transformerは頭打ちや低下を示す。差は課題・shot数に依存するため、「全タスクで一律10%改善」とは読まない。匿名ラベルは既知のラベル意味への依存を減らす設計だが、未知分布への適応能力すべてを測定するものではない。[出典：§5.3、Figs. 3–4・13–14](../../raw/papers/2507.03285v3.pdf)

## 追加実験

- **データを8倍にしたTransformer**：32k QAは46.9で、1T tokensのv2の53.4を下回る。一方、意味ラベルのICLはv2に近づくが、匿名ラベルでは依然差が残る。8TモデルはGQA・8k事前学習を使っており、訓練token数だけを変えた比較ではない。[出典：§6、Table 5・Figs. 6–7](../../raw/papers/2507.03285v3.pdf)
- **長文へのfine-tuning**：4k事前学習から32kへ適応する実験では、v2は1 minibatch（1 optimization step）で約22 percentage points改善し、2 minibatchesで最良水準に達すると報告する。これは32k RULER QAでの結果で、「どの新タスクも1例で学べる」という意味ではない。[出典：§7・Fig. 8](../../raw/papers/2507.03285v3.pdf)

## 限界と研究テーマとの関係

本手法は全key-valueを保持して重み付き検索する。key extractorが再帰的でも、記憶全体を固定長stateへ圧縮する方式やlinear attentionではない。超長文脈の計算費用削減は今後の課題で、fuzzy hashingやhierarchical memoryが将来方向として挙げられる。ANN・グラフ探索による高速化を本論文で実証したわけではない。[出典：§3.2脚注6、§8、Appendix E](../../raw/papers/2507.03285v3.pdf)

言語モデルの情報検索とICLの実験であり、ロボットの制御・強化学習の性能は評価していない。記憶圧縮方式についての強い限界の主張も著者の議論として扱い、Appendix Dの既存モデル・既存研究から引用した結果を全方式の不可能性へ一般化しない。[出典：§5・Appendix D](../../raw/papers/2507.03285v3.pdf)

## 関連ページ

- [Associative MemoryとKernel Regression](../concepts/associative_memory_and_kernel_regression.md)
- [角度判定と参照角度](../concepts/angle_testing.md)：別の一次資料を扱う検索関連ページ。本論文との手法統合は未検証。
