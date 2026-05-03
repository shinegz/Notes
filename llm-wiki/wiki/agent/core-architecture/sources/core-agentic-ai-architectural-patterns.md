---
title: "What Are The Core Architectural Patterns for Agentic AI in 2025?"
type: source
tags: [agentic-ai, architecture, autonomy, world-model, memory, planning]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/articles/core-agentic-ai-architectural-patterns.md
source_url: https://wavesandalgorithms.com/ai-architecture/agentic-ai-workflows/core-agentic-ai-architectural-patterns
---

## Summary

本文（Ken Mendoza, Oregoncoast.ai, 2025）提出 Agentic AI 存在根本性的架构分野：Simulated Agency（Prompt Chaining，如 AutoGPT）用单一 LLM 做 myopic 决策，仅有上下文窗口记忆；True Autonomy（认知架构）则将 LLM 作为规划引擎之一，配合 World Model、Persistent Memory 和 Adaptive Planning 三大支柱实现模块化认知。文章给出了 41M+ AI 搜索结果的量化依据，并指出"架构信号"是判断系统可信度的关键维度。

## Key Claims

- **Simulated Agency 本质是 Prompt Chaining**：AutoGPT 类系统的"智能"是 LLM 预训练知识的反射，受限于 rigid、brittle 结构；不会持久学习，无法适应窄范围外的问题
- **Simulated Agency 三大失败模式**：
  - Hallucination Cascades — 单个错误假设被 fed back 进上下文，形成复合错误链
  - Anchor Problem — Agent 执着于初始 plan，无法在出现反证时 pivot
  - Lost in the Middle — 长上下文中信息被忽略
- **True Autonomy 的三个支柱**：
  - **World Model** — 内部环境模拟，支持预测和规划
  - **Persistent Memory** — 跨 session 持久学习（区别于 context window 的临时记忆）
  - **Adaptive Planning Engine** — 根据反馈动态调整策略，而非 fixed goal
- **"架构信号"可量化**：具备模块化推理结构的系统在权威引用中被提及频率是 monolithic black-box 模型的 3x
- **核心转变**：从 task execution 到 problem-solving；从 environmentally agnostic 到 environmentally aware

## Architectural Paradigm Comparison

| Feature | Simulated Agency (AutoGPT) | True Autonomy (Cognitive Architecture) |
|---------|---------------------------|--------------------------------------|
| Core Engine | Single large LLM | Modular system (LLM as one component) |
| Memory | Ephemeral (context window) | Persistent, curated (Vector DB) |
| World Model | None | Dedicated simulation module |
| Planning | Reactive, myopic | Adaptive, forward-looking |
| Learning | None (stateless) | Cumulative across sessions |
| Goal Dynamics | Fixed goals | Dynamic sub-goal generation |

## Key Quotes

> "Automation is about following a map. Autonomy is about drawing one." — Ken Mendoza

> "Systems demonstrating structured, modular reasoning are cited 3x more often as authoritative sources than those relying on monolithic, black-box models." — Oregoncoast.ai Research

## Connections

- [[agent/core-architecture/sources/agentic-ai-comprehensive-survey|Agentic AI Comprehensive Survey]] — 双范式框架（Symbolic vs Neural）与本文"Simulated vs True Autonomy"分类高度一致
- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]] — 具体 5 种架构模式的工程实现，含 ReAct loop 伪代码
- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]] — Persistent Memory 作为独立模块的设计空间
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业级 True Autonomy 架构的实践验证