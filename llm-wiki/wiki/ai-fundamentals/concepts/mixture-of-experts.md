---
title: "Mixture of Experts (MoE)"
type: concept
tags: [moe, mixture-of-experts, scaling, architecture]
sources:
  - ai-fundamentals/sources/mixtral
last_updated: 2026-04-26
---

# Mixture of Experts (MoE)

**MoE = 稀疏激活的专家混合模型，用更少计算实现更大参数量的模型。**

## 一句话理解

MoE 的核心思想是把模型「分包」给不同专家，每次只激活相关的专家（而不是全激活），实现「大参数、低计算」。

## 与稠密模型的对比

| 对比维度 | 稠密模型 | MoE |
|----------|----------|-----|
| 参数分布 | 所有参数参与每个 token | 只有被选中专家参与 |
| 激活参数 | 全部参与 | 只激活 Top-K（如 2/8）|
| 推理成本 | 与参数量成正比 | 与激活参数量成正比 |
| 训练效率 | 高 | 需要负载均衡 |

## 核心组件

```
输入 → Router → 选择 Top-K 专家 → Expert 1 / Expert 2 / ... / Expert N
                         ↓
                    只激活被选中的专家
```

| 组件 | 作用 |
|------|------|
| **Router** | 学习选择最合适的专家 |
| **Expert** | 每个专家擅长不同类型输入 |
| **Top-K** | 只激活 K 个专家，减少计算 |

## 为什么 MoE 有效

1. **专家专业化**：不同专家学习不同类型的 pattern
2. **稀疏激活**：大幅降低计算量，同时保持高参数总量
3. **可扩展性**：可以大幅增加参数量而不增加推理成本
4. **负载均衡**：需要辅助 loss 防止只有少数专家被选中

## 代表模型

| 模型 | 参数量 | 激活参数 | 专家数 |
|------|--------|---------|--------|
| Switch Transformer | 1.6T | 1.6B | 2048 |
| Mixtral 8x7B | 46.7B | 12.9B | 8 (激活2) |
| DBRX | 132B | 36B | 4 (激活2) |

## 与 Scaling Laws 的关系

MoE 是 **Scaling 的架构方向**之一：

- **参数Scaling**：增加专家数量和参数量
- **计算Scaling**：增加激活专家数
- **效率Scaling**：在同等计算量下实现更大参数量

## 关联概念

- [[ai-fundamentals/concepts/scaling-laws|Scaling Laws]] — MoE 是 Scaling 的一种路径
- [[ai-fundamentals/concepts/transformer|Transformer]] — MoE 通常基于 Transformer 架构
- [[ai-fundamentals/sources/mixtral|Mixtral]] — 开源 MoE 代表作

## 来源

- [[ai-fundamentals/sources/mixtral|Mixtral]] — Mixtral 8x7B 论文
