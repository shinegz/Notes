---
title: "Vector Database"
type: concept
tags: [vector-db, retrieval, memory, embedding]
sources:
  - ai-fundamentals/sources/llm-powered-autonomous-agents
  - ai-fundamentals/sources/word2vec
last_updated: 2026-04-23
---

# Vector Database

**Vector Database = 存储和检索高维向量的数据库，核心操作是「找最相似的向量」。**

## 一句话理解

把文本/图片/代码变成向量（embedding）存起来，查询时用"语义相似度"而不是"关键词匹配"来检索。

## 为什么 LLM 需要 Vector DB

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 明确指出 LLM 的两大限制：

1. **有限的上下文长度** — 模型一次只能看有限的 token
2. **知识截止于训练数据** — 无法访问新信息

Vector DB 作为**长期记忆**（long-term memory）解决这两个问题：

```
用户问题 → Embedding → Vector DB 相似度搜索 → Top-K 相关文档 → 注入 Prompt → LLM 回答
```

## 核心机制：Approximate Nearest Neighbor (ANN)

直接计算查询向量与所有存储向量的距离，时间复杂度 O(N)，太慢。

ANN 算法通过索引结构近似搜索，将复杂度降到 O(log N) 或更低：

| 算法 | 原理 | 代表实现 |
|------|------|----------|
| **HNSW** | 分层可导航小世界图 | FAISS, Milvus |
| **IVF** | 倒排文件 + 聚类 | FAISS |
| **LSH** | 局部敏感哈希 | Annoy |

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 将这一检索过程称为 MIPS（Maximum Inner Product Search）。

## Agent 中的 Memory 分层

| 记忆类型 | 实现 | 容量 | 来源 |
|----------|------|------|------|
| **短期记忆** | In-context learning / Prompt | 有限（context window）| [Agent Survey](../sources/llm-powered-autonomous-agents.md) |
| **长期记忆** | Vector DB + ANN 检索 | 理论上无限 | [Agent Survey](../sources/llm-powered-autonomous-agents.md) |

短期记忆和长期记忆的区别：
- 短期记忆：当前对话的上下文，受限于 context window
- 长期记忆：历史信息通过 embedding 存入 vector DB，需要时检索注入

## 工作流程

```
1. 写入：文档 → Tokenizer → Embedding 模型 → 向量 → Vector DB
2. 查询：用户问题 → Embedding 模型 → 向量 → ANN 搜索 → Top-K 结果
3. 使用：检索结果 → 拼接进 Prompt → LLM 生成回答
```

## 来源

- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — Agent 长期记忆与 MIPS 检索
- [word2vec](../sources/word2vec.md) — Embedding 向量表示的基础
