---
title: "Memory"
type: concept
tags: [memory, agent, vector-db, context]
sources:
  - ai-fundamentals/sources/llm-powered-autonomous-agents
last_updated: 2026-04-23
---

# Memory

**Memory = Agent 存储和检索信息的能力，分为短期记忆（上下文窗口）和长期记忆（外部存储）。**

## 一句话理解

Agent 需要记忆来完成复杂任务——短期记忆像便签纸（随时看但容量小），长期记忆像图书馆（容量大但需要检索）。

## 两类记忆

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 明确区分了两种记忆：

| 类型 | 实现 | 容量 | 持久性 |
|------|------|------|--------|
| **短期记忆** | In-context learning / Prompt | 有限（受 context window 限制）| 会话级别 |
| **长期记忆** | 外部 Vector DB / Graph DB | 理论上无限 | 持久存储 |

### 短期记忆

- **载体**：当前对话的上下文（Context Window）
- **限制**：受限于模型的 context length（如 GPT-3 的 2048 tokens）
- **作用**：传递当前对话的历史信息
- **问题**：超出窗口后信息丢失；长上下文导致注意力分散（"Lost in the Middle"）

### 长期记忆

- **写入**：将历史信息、知识、经验通过 Embedding 转化为向量，存入外部数据库
- **检索**：需要时通过相似度搜索（MIPS/ANN）召回最相关的信息，注入 Prompt
- **载体**：Vector DB（FAISS, Milvus, Pinecone 等）或 Graph DB
- **优势**：容量不受模型限制；信息可持久保存；跨会话可用

## Agent 中的记忆工作流程

```
用户输入 → Agent 判断需要什么记忆 → 
  ├─ 需要当前对话上下文 → 从短期记忆读取
  └─ 需要历史知识/经验 → 从长期记忆检索 → 注入 Prompt → LLM 生成回复
```

## 记忆设计的挑战

[LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) 指出的关键问题：

1. **检索精度**：如何从海量记忆中找到真正相关的片段
2. **记忆冲突**：新旧信息矛盾时如何处理
3. **写入策略**：什么值得记住？何时写入？
4. **上下文压缩**：长期记忆检索结果可能很长，需要压缩到 context window 内

## 来源

- [LLM Powered Autonomous Agents](../sources/llm-powered-autonomous-agents.md) — Agent 记忆系统综述（短期 vs 长期，MIPS 检索）
