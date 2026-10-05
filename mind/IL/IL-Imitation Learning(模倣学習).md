# 解く問題
基本的には、強化学習などの機械学習と同じ。
観測`Observation`から、いかにして次の行動`Action`を導出するかの方策`Policy`を学習する手法。

# 学習方法
お手本となる`demonstration` のデータを基に、それに近づくように学習していく。
完全な正解データがあるというよりは、多数の状況の違い(ボールが転がったり)に対応した行動を学び、

# 代表的手法
- Behavior Cloning(BC)
- Dataset Aggregation(DAgger)
- Generative Adversarial Imitation Learning(GAIL)
- Adversarial Inverse Reinforcement Learning(AIRL)