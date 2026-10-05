ざっくりとしたAttentionの説明を書く。

Transformerの核となる部分。
$$Attention(Q,K,V)=softmax(QK^T/\sqrt d_k ) V$$

Q: Query 求めている情報
K: Key 持っているデータ
V: Value 渡す情報

Attentionはこれを学習することによって、