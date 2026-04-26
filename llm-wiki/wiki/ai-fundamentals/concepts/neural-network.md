---
title: "Neural Network"
type: concept
tags: [neural-network, nn, foundation]
sources: []
last_updated: 2026-04-26
---

# Neural Network

**Neural Network = 由可调参数组成的人工神经元组成的网络，通过学习参数实现从输入到输出的映射。**

## 一句话理解

一个神经元：输入 → 加权求和 → 激活函数 → 输出。 billions of 神经元互联形成网络，学习从海量数据中发现模式。

## 单个神经元

```
输入 x₁, x₂, ..., xₙ
    ↓
权重 w₁, w₂, ..., wₙ
    ↓
加权和： Σ(wᵢ · xᵢ) + b
    ↓
激活函数：σ(Σ)
    ↓
输出 y
```

## 与 LLM 的关系

| 组件 | 在 LLM 中的角色 |
|------|----------------|
| **Embedding 层** | 输入 token 的可学习表示 |
| **Self-Attention** | Query/Key/Value 的交互计算 |
| **前馈网络 (FFN)** | 每个 Transformer block 的 MLP 层 |
| **输出层** | 预测下一个 token 的概率分布 |

## 关键概念

- **参数 (Parameters)**：模型的可学习权重 W 和偏置 b
- **前向传播 (Forward Pass)**：输入 → 输出，计算损失
- **反向传播 (Backpropagation)**：从输出向输入计算梯度
- **梯度下降 (Gradient Descent)**：用梯度更新参数

见 [[ai-fundamentals/concepts/backpropagation|Backpropagation]] 和 [[ai-fundamentals/concepts/gradient-descent|Gradient Descent]]。

## 来源

待补充。
