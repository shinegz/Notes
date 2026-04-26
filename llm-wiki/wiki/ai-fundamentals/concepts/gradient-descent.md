---
title: "Gradient Descent"
type: concept
tags: [gradient-descent, optimization, training]
sources: []
last_updated: 2026-04-26
---

# Gradient Descent

**Gradient Descent = 沿着损失函数梯度的反方向，逐步更新参数以最小化损失。**

## 一句话理解

参数的更新方向：Loss 增大的方向 → 参数往反方向走 → Loss 减小。走多少步，由学习率控制。

## 更新公式

```
W_new = W_old - η · ∇L(W_old)

其中：
  W = 参数（权重矩阵）
  η = 学习率 (learning rate)
  ∇L = Loss 对 W 的梯度
```

## 三种变体

| 类型 | 每次样本数 | 优点 | 缺点 |
|------|-----------|------|------|
| **SGD** | 1 个 | 收敛快，能逃出局部最优 | 震荡，不稳定 |
| **Mini-batch GD** | N 个 (batch) | 平衡稳定性和速度 | 需要调 batch size |
| **Full GD** | 全部样本 | 稳定，方向准确 | 慢，无法处理大数据 |

## 学习率的影响

| 学习率 | 表现 |
|--------|------|
| **太大** | 震荡，无法收敛 |
| **太小** | 收敛慢，容易陷入局部最优 |
| **动态调整** | Adam、RMSprop 等自适应学习率优化器 |

## Adam 优化器

现代 LLM 训练默认使用 **Adam**（Adaptive Moment Estimation）：
- 动量：累积历史梯度方向，平滑更新
- 自适应学习率：每个参数有自己的学习率

## 与 LLM 的关系

- **预训练**：使用 AdamW 在海量文本上优化数十亿参数
- **Fine-tuning**：通常用更小的学习率和更小的 batch size
- **LoRA** 等高效微调：冻结大部分参数，只用 Adam 优化低秩矩阵

见 [[ai-fundamentals/concepts/backpropagation|Backpropagation]] 和 [[ai-fundamentals/concepts/lora|LoRA]]。

## 来源

待补充。
