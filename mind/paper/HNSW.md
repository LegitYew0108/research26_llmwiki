HNSW=knn search with navigable small world graphs with controllable hierarchy
	- 要するに、制御可能な階層を使った小さな探索可能グラフによるK近傍検索
- 完全グラフベース手法で、他手法で主に用いられる追加探索0

## 何がしたいのか
ANNS=Approximate Nearest Neighbor Search　の一つ。
大量のデータから類似したものを高速に見つけだす手法。
### ユースケース
- 画像認識
- 自然言語処理
- レコメンデーションシステム
	- SNSやYoutubeなどにおける好みに応じた推薦システム
	- Amazon等のECだと売上に直結

### 何が問題なのか
ANNSは一般的にデータが増えると検索速度が落ちる
高次元データではこれが顕著。

