---
title: "Attention Mechanism"
type: concept
tags: [attention, deep-learning, transformer]
sources:
  - ai-fundamentals/sources/attention-is-all-you-need
last_updated: 2026-04-19
---

# Attention Mechanism

**Attention = Query × Key^T × Value，衡量「我应该关注什么」。**

## 一句话理解

Attention 让模型能够「有选择地」关注输入的不同部分，而不是把所有信息同等对待。

## 数学原理

### 1. 核心公式

```python
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

三个步骤：
1. **Query × Key**：计算相关性
2. **Scale + Softmax**：归一化权重
3. **Weight × Value**：加权求和

### 2. 图解

```
Token:        我    爱    深    度    学    习
Query:        q1    q2    q3    q4    q5    q6
              ↓     ↓     ↓     ↓     ↓     ↓
注意力权重:   0.1   0.05  0.3   0.3   0.2   0.05
              ↓     ↓     ↓     ↓     ↓     ↓
输出:         加权融合了「深度」和「学习」的语义
```

### 3. 为什么除以 √d_k

防止点积结果过大，导致 softmax 梯度消失。

```python
# d_k = 64 时
scores = q @ k.T  # 值可能很大
scores = scores / sqrt(64)  # 归一化
```

## Attention 的类型

| 类型 | 描述 | 应用 |
|------|------|------|
| Self-Attention | Q, K, V 来自同一序列 | Transformer |
| Cross-Attention | Q 来自 A，K, V 来自 B | Encoder-Decoder |
| Multi-Head | 多个 Attention 并行 | Transformer |

## 来源

- [[../sources/attention-is-all-you-need|Attention Is All You Need]]
