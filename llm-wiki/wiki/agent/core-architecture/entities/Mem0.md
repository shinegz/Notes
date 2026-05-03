---
title: "Mem0"
type: entity
tags: [organization, memory, llm-agent, vector-db]
sources:
  - agent/core-architecture/sources/agent-memory-architectures
last_updated: 2026-05-03
---

## 一句话定义

Mem0 是专注于 LLM Agent 记忆层的开源组织，开发了 Memory Agents 框架和 LOCOMO benchmark，是向量检索类记忆架构的主要推动者。

## 关键贡献

### LOCOMO Benchmark

长时记忆 benchmark：
- 支持最多 35 个 session、300+ 轮对话、9k–16k tokens/对话
- 人类表现仍然显著领先当前所有系统
- 量化了 In-context（72.9% @ 17.12s）vs Selective retrieval（66.9% @ 1.44s）的 trade-off

### Memory Agents

支持向量检索为基础的记忆架构，提供 flat namespace 的 semantic search 记忆系统。

## 来源

- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]]