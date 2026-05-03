---
title: "Agent Memory Architectures: 5 Patterns and Trade-offs"
type: source
tags: [memory, architecture, vector-db, knowledge-graph, rag, enterprise, governance]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/articles/agent-memory-architectures.md
source_url: https://atlan.com/know/agent-memory-architectures/
---

## Summary

本文（Atlan, 2026-04）将 Agent 记忆架构分为 5 种模式（In-process → Flat Vector → Relational → Graph → Enterprise Context Layer），指出记忆类型（Episodic/Semantic/Procedural/Working）与记忆架构（存储基座+检索机制+Agent控制模型）是两个独立维度，混淆是实践者最常见的错误。Mem0 LOCOMO benchmark 量化了"准确率 vs 延迟"的 trade-off：full-context 72.9% @ 17.12s vs selective retrieval 66.9% @ 1.44s，token 成本降低 90%。

## Key Claims

- **记忆架构三要素**：存储基座（context window/Vector DB/Relational DB/Knowledge Graph/Governed Metadata Catalog）、检索机制（full-context injection/top-k similarity/graph traversal/function call）、Agent 控制模型（被动接收 vs 主动管理）
- **CoALA 框架**（Sumers et al., arXiv:2309.02427）正式化了"记忆类型 vs 记忆架构"的区分
- **Governance 与 Freshness 轴独立于 Accuracy 与 Latency 轴**：扩展 context window（如 2M token）解决了延迟问题，但无法解决治理问题
- **Pattern 3（Relational）**：支持 text-to-SQL，企业场景准确率提升 3x（vs bare schema）
- **Pattern 4（Graph）**：2026 年初已有 13 个框架支持图记忆生产，多跳关系查询必须用图结构
- **Pattern 5（Enterprise Context Layer）**：将企业已有治理元数据图直接作为 Agent 记忆，实现Governed Organizational Memory

## Five Memory Architecture Patterns

| Pattern | Storage | Retrieval | Latency | Accuracy | Governance |
|---------|---------|----------|---------|----------|------------|
| 1: In-process | Context window | None (full injection) | 17.12s p95 | 72.9% | None |
| 2: Flat Vector | Vector DB | Top-k similarity | 1.44s p95 | 66.9% | None |
| 3: Relational | Relational DB | Text-to-SQL | Medium | High (+3x with live metadata) | Partial |
| 4: Graph | Knowledge Graph | Graph traversal | Medium | High (multi-hop) | Partial |
| 5: Enterprise Context | Governed metadata catalog | Metadata catalog API | Low | High | Full |

## Key Data

- Full-context token cost: ~26,031 tokens/conversation
- Selective retrieval token cost: ~1,764 tokens/conversation（90% reduction）
- LOCOMO benchmark source: arXiv:2504.19413

## Connections

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns]] — Persistent Memory 作为 True Autonomy 三大支柱之一
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业 Agent 的工具定义与可观测性
- [[agent/core-architecture/sources/ai-agent-architecture-components-types|AI Agent Components & Types]] — PuppyGraph 指出图记忆适合企业级多跳查询