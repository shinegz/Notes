---
title: "Backpropagation"
type: concept
tags: [backpropagation, backprop, training, gradient]
sources: []
last_updated: 2026-04-26
---

# Backpropagation

**Backpropagation = 通过链式法则，从输出层向输入层逐层计算梯度，用于训练神经网络。**

## 一句话理解

神经网络的参数成千上万，手动计算梯度不可能。Backprop 通过链式法则，把 Loss 对输出层的梯度，一层一层传回去，自动算出每个参数该往哪个方向调整。

## 工作原理

```
1. Forward Pass：输入 → 逐层计算 → 输出 → 计算 Loss

2. Backward Pass：
   Loss 对输出层的梯度
        ↓ 链式法则
   Loss 对中间层的梯度
        ↓ 链式法则
   ...
        ↓ 链式法则
   Loss 对每个参数的梯度 ∂L/∂Wᵢⱼ

3. 参数更新：
   W_new = W_old - η · ∂L/∂W
   （η = 学习率）
```

## 链式法则示意

```
∂L/∂W = ∂L/∂y · ∂y/∂z · ∂z/∂W
```

三层嵌套，每层一个偏导数，连乘即为梯度。

## 关键问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **梯度消失** | 链式法则导致梯度逐层指数减小 | ReLU、残差连接、BatchNorm |
| **梯度爆炸** | 链式法则导致梯度逐层指数增大 | 梯度裁剪 (gradient clipping) |

## 与 LLM 的关系

- LLM 的训练依赖 Backpropagation 计算梯度
- 预训练阶段：在海量文本上通过 Backprop + Gradient Descent 优化数十亿参数
- Fine-tuning 阶段：同样通过 Backprop 更新少量参数

见 [[ai-fundamentals/concepts/gradient-descent|Gradient Descent]]。

## 来源

待补充。
