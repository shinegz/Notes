---
title: "Embedding"
type: concept
tags: [embedding, word2vec, representation-learning]
sources:
  - ai-fundamentals/sources/word2vec
  - ai-fundamentals/sources/attention-is-all-you-need
last_updated: 2026-04-24
---

# Embedding

**Embedding = 将离散符号映射为连续向量，让语义相近的词在向量空间中距离相近。**

## 一句话理解

Embedding 是把"词"变成"数字向量"的过程。语义相似的词（如"king"和"queen"）在向量空间中距离相近。

## 核心思想

### 从 one-hot 到 dense vector

```
One-hot:     king = [1, 0, 0, 0, ...]  # 50000 维，只有一个 1
Embedding:   king = [0.2, -0.5, 0.8, ...]  # 512 维，每个维度都有语义含义
```

Embedding 解决了 one-hot 的两个问题：
- **维度灾难**：vocab size 越大，one-hot 向量越长
- **无语义关系**：one-hot 中任意两个词的向量正交，无法表达相似性

### 著名示例：Vector Arithmetic

[[ai-fundamentals/sources/word2vec|word2vec]] 的经典发现：

```
king - man + woman ≈ queen
paris - france + italy ≈ rome
```

这表明 embedding 向量编码了语义关系（性别、首都-国家等）。

## word2vec 的两种架构

| 架构 | 预测方向 | 特点 |
|------|----------|------|
| **CBOW** | 用上下文词预测中心词 | 训练更快，对高频词效果好 |
| **Skip-gram** | 用中心词预测上下文词 | 对低频词和罕见词效果好 |

[[ai-fundamentals/sources/word2vec|word2vec]] 训练了 1.6B 词的语料，一天内完成训练。

## 从 Word Embedding 到 Contextual Embedding

| 阶段 | 代表 | 特点 |
|------|------|------|
| Word Embedding | word2vec, GloVe | 每个词一个固定向量，忽略上下文 |
| Contextual Embedding | ELMo | 基于双向 LSTM，词向量随上下文变化 |
| Transformer Embedding | BERT, GPT | 基于 Self-Attention，每个 token 的表示取决于整句话 |

在 [[ai-fundamentals/sources/attention-is-all-you-need|Transformer]] 中，Input Embedding 和 Positional Encoding 相加后进入 Encoder，Embedding 维度为 512。

## 现代应用

- **LLM 输入层**：所有现代 LLM 的第一层都是 Embedding 层
- **Vector DB**：文档/查询先 embedding 再存储/检索（见 [[ai-fundamentals/concepts/vector-database|Vector Database]]）
- **类比推理**：Vector arithmetic 成为评估 embedding 质量的标准测试

## 来源

- [[ai-fundamentals/sources/word2vec|word2vec]] — 词嵌入奠基论文（Google）
- [[ai-fundamentals/sources/attention-is-all-you-need|Attention Is All You Need]] — Transformer 中的 Embedding + Positional Encoding
