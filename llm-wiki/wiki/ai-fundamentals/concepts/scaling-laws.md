---
title: "Scaling Laws"
type: concept
tags: [scaling-laws, compute, training]
sources:
  - ai-fundamentals/sources/scaling-laws-kaplan
  - ai-fundamentals/sources/chinchilla
  - ai-fundamentals/sources/gpt3-language-models-few-shot
last_updated: 2026-04-23
---

# Scaling Laws

**Scaling Laws = 模型性能随算力、参数量、数据量可预测增长的规律。**

## 一句话理解

当计算预算增加时，模型该变大还是该加数据？Scaling Laws 给出了定量答案。

## Kaplan (2020) 的发现

[Scaling Laws](../sources/scaling-laws-kaplan.md) 在 OpenAI 的研究中提出：

### 核心公式

```
Loss ∝ C^(-α)
```

其中 C 是 compute（FLOPs），α ≈ 0.05。意味着算力翻一倍，loss 下降一个固定比例。

### 三个发现

| 维度 | 规律 | 含义 |
|------|------|------|
| **模型大小 (N)** | Loss ∝ N^(-0.076) | 参数量越大越好 |
| **数据量 (D)** | Loss ∝ D^(-0.095) | 数据量越大越好 |
| **计算量 (C)** | Loss ∝ C^(-0.050) | 三者中最强的预测因子 |

Kaplan 的结论是：在固定算力下，模型应该尽量做大，数据可以相对少（Chinchilla 后来推翻了这一点）。

## Chinchilla (2022) 的修正

[Chinchilla](../sources/chinchilla.md) 训练了 400+ 个模型（70M ~ 16B params，5B ~ 500B tokens），发现：

### 核心结论

> **模型大小和数据量应该等比例增长**

对于计算最优训练，每翻倍模型大小，训练 token 数也应该翻倍。

### Chinchilla vs Gopher

| | Gopher | Chinchilla |
|--|--------|------------|
| 参数量 | 280B | 70B |
| 训练 token | 300B | 1.5T |
| 算力预算 | **相同** | **相同** |
| 效果 | 基线 | **显著优于 Gopher** |

### 最优比例

- **Chinchilla 最优比**：~20 tokens per parameter
- 此前实践：~1-2 tokens per parameter（严重 under-trained）
- [GPT-3](../sources/gpt3-language-models-few-shot.md) 175B params / 300B tokens ≈ 1.7:1（远低于最优）

## 实际影响

| 方面 | Kaplan 时代 | Chinchilla 时代 |
|------|-------------|-----------------|
| 模型趋势 | 越大越好 | 更小的模型 + 更多数据 |
| 训练成本 | 高（大模型） | 中等（小模型但长训练） |
| 推理成本 | 高 | 低（小模型推理更快） |
| 代表 | GPT-3, Gopher | Chinchilla, LLaMA |

## 来源

- [Scaling Laws](../sources/scaling-laws-kaplan.md) — Kaplan et al., OpenAI, 2020
- [Chinchilla](../sources/chinchilla.md) — Hoffmann et al., DeepMind, 2022
- [GPT-3](../sources/gpt3-language-models-few-shot.md) — Brown et al., OpenAI, 2020（案例对比）
