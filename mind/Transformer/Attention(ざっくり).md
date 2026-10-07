ざっくりとしたAttentionの説明を書く。

# Transformerで何がしたい？
本質は「独立した複数のデータを周りの情報から文脈を関連付けたデータ表現に変える」ということ。



# 計算
Transformerの核となる部分。
$$Attention(Q,K,V)=softmax(QK^T/\sqrt d_k ) V$$

Q: Query 求めている情報
K: Key 持っているデータ
V: Value 渡す情報



