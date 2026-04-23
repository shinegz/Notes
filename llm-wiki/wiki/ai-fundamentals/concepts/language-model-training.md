---
title: "Language Model Training"
type: concept
tags: [llm, pre-training, scaling-laws]
sources:
  - ai-fundamentals/sources/scaling-laws-kaplan
  - ai-fundamentals/sources/gpt3
last_updated: 2026-04-19
---

# Language Model Training

**预训练 = Next Token Prediction + Scaling，让模型学会语言规律。**

## 一句话理解

LLM 通过「预测下一个词」在大规模文本上学习语言规律，模型越大、数据越多、能力越强。

## 训练范式

```mermaid
graph LR
    A[文本] --> B[Tokenize]
    B --> C[Transformer]
    C --> D[预测下一个词]
    D --> E[计算损失]
    E --> F[反向传播]
```

### 预训练目标

```python
loss = -sum(log P(token_i | token_0, ..., token_i-1))
```

最大化下一个 token 的概率。

## Scaling Laws

### Kaplan (2020)

发现性能与规模存在幂律关系：

```python
L(N) ∝ N^(-0.076)  # N = 参数量
L(D) ∝ D^(-0.095)  # D = 数据量
L(C) ∝ C^(-0.054)  # C = 计算量
```

### Chinchilla (2022) 修正

**新结论**：模型参数量和训练数据量应该**等比例 scaling**。

| 模型大小 | Kaplan 建议数据 | Chinchilla 建议数据 |
|----------|-----------------|---------------------|
| 1B | 20B | 20B |
| 70B | 1.4T | 1.4T |
| 280B | 7T | 5.6T |

## 涌现能力

> 大模型能「涌现」出小模型没有的能力。

| 能力 | 出现规模 |
|------|----------|
| In-Context Learning | ~10B |
| Chain-of-Thought | ~100B |
| 复杂推理 | >100B |

## 来源

- [[../sources/scaling-laws-kaplan|Scaling Laws]]
- [[../sources/gpt3-language-models-few-shot|GPT-3]]
