---
title: "RAG"
type: concept
tags: [rag, retrieval, vector-db, llm]
sources:
  - ai-fundamentals/sources/llm-powered-autonomous-agents
  - ai-fundamentals/sources/word2vec
last_updated: 2026-04-23
---

# RAG（Retrieval-Augmented Generation）

**RAG = 先检索相关文档，再将检索结果注入 Prompt，让 LLM 基于外部知识生成回答。**

## 一句话理解

LLM 的知识截止于训练数据。RAG 让它在回答前先去"查资料"，解决知识时效性和专有数据访问问题。

## 核心流程

```
用户问题 → Embedding → Vector DB 相似度检索 → Top-K 相关文档 → 
拼接进 Prompt（[检索结果] + [用户问题]）→ LLM 生成基于检索结果的回答
```

## 为什么需要 RAG

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 指出 LLM 的两大固有限制：

1. **知识截止**：模型权重中的知识只到训练数据的时间点
2. **幻觉倾向**：对未知问题会自信地编造答案

RAG 通过引入外部检索步骤解决这两个问题：
- **时效性**：检索最新文档，不受训练数据时间限制
- **准确性**：基于检索到的真实文档生成，减少幻觉
- **专有数据**：可以访问企业内部知识库、个人笔记等私有数据

## RAG vs Fine-tuning

| | RAG | Fine-tuning |
|--|-----|-------------|
| **数据更新** | 实时更新（改 Vector DB 即可）| 需要重新训练 |
| **成本** | 低（检索 + 推理）| 高（训练）|
| **适用场景** | 知识库问答、客服、文档查询 | 风格迁移、特定任务优化 |
| **知识来源** | 外部文档 | 训练数据 |

## 关键组件

| 组件 | 作用 | 相关概念 |
|------|------|----------|
| **Embedding 模型** | 将查询和文档转化为向量 | [Embedding](../concepts/embedding.md) |
| **Vector DB** | 存储文档向量并快速检索 | [Vector Database](../concepts/vector-database.md) |
| **LLM** | 基于检索结果生成回答 | [LLM](../concepts/language-model-training.md) |
| **重排序（Rerank）** | 对初步检索结果精排，提升相关性 | — |

## 来源

- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — Agent 长期记忆与检索机制
- [word2vec](../sources/word2vec.md) — Embedding 向量表示的基础
