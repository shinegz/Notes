---
title: "Memory Taxonomy（Agent 记忆架构）"
type: concept
tags: [memory, agent, taxonomy, episodic, semantic, procedural, working]
sources:
  - agent/core-architecture/sources/agent-memory-architectures
  - agent/core-architecture/sources/memory-autonomous-llm-agents
last_updated: 2026-05-03
---

## 一句话理解

Agent 记忆不是单一技术，而是**存储基座 × 检索机制 × 控制模型**的三维设计空间；Memory Type（记忆类型）和 Memory Architecture（记忆架构）是两个独立维度，混淆是实践者最常见的错误。

## 两个独立维度

### Memory Types（记忆类型）

描述**存储什么内容**，四类经典分法（CoALA 框架）：

| 类型 | 内容 | 示例 |
|------|------|------|
| **Episodic** | 具体事件和经历 | "用户上周问过报销流程" |
| **Semantic** | 抽象知识和事实 | "报销需在30天内提交" |
| **Procedural** | 如何做事的步骤 | "提交报销的步骤" |
| **Working** | 当前推理上下文 | 当前 session 的中间状态 |

### Memory Architecture（记忆架构）

描述**如何存储和检索**，三维空间：

1. **Temporal Scope**：瞬时 / Session / 长期 / 永久
2. **Representational Substrate**：Context压缩 / 向量检索 / 结构化 / 层级虚上下文 / 策略学习
3. **Control Policy**：被动注入 / 启发式 / 反思式 / RL 学习

## 五种架构模式（Atlan 分类）

| Pattern | Storage | Retrieval | Latency | Accuracy | Token Cost |
|---------|---------|----------|---------|----------|-----------|
| 1: In-process | Context window | None | 17.12s | 72.9% | ~26k/conv |
| 2: Flat Vector | Vector DB | Top-k similarity | 1.44s | 66.9% | ~1.7k/conv |
| 3: Relational | SQL DB | Text-to-SQL | Medium | High (+3x) | Low |
| 4: Graph | Knowledge Graph | Graph traversal | Medium | High (multi-hop) | Low |
| 5: Enterprise Context | Governed metadata | Catalog API | Low | High | Very Low |

## 关键量化数据（Mem0 LOCOMO Benchmark）

- Full-context (Pattern 1): 72.9% @ 17.12s p95, ~26k tokens/对话
- Selective retrieval (Pattern 2): 66.9% @ 1.44s p95, ~1.7k tokens/对话
- **90% token 成本降低，精度仅下降 6 个百分点**

## 核心洞见

> "The gap between 'has memory' and 'does not have memory' is often larger than the gap between different LLM backbones." — Memory for Autonomous LLM Agents

## 来源

- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]]
- [[agent/core-architecture/sources/memory-autonomous-llm-agents|Memory for Autonomous LLM Agents]]