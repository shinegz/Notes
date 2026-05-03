---
title: "AI Agent Architecture: Components & Types"
type: source
tags: [agent, components, architecture, memory, planning, tools, harness, security]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/articles/ai-agent-architecture-components-types.md
source_url: https://www.puppygraph.com/blog/ai-agent-architecture
---

## Summary

本文（PuppyGraph, 2026-04）指出生产级 AI Agent 失败的根因几乎都在"架构"而非"模型"本身，提出 Agent 架构需回答四个问题：上下文从哪来（Perception/Memory）、下一步如何决策（Reasoning/Planning）、能做什么（Tools）、如何防止跑偏（Guardrails/Observability）。文章还指出向量存储作为默认记忆方案的局限性——多跳、关系型问题需要知识图谱，并给出 5 类架构模式的适用场景对比表。

## Key Claims

- **Agent 架构四问**：Context 来源、Decision 机制、Action 能力、Safety 保证
- **Agent Loop**：Observe → Reason → Act → Update State → Loop；Harness（即运行时/编排层）负责工具调度、context 组装、重试、超时、结构化输出解析
- **Workflow vs Agent**：Anthropic 定义差异在于"LLM 是否动态决定执行顺序"
- **单 Agent 架构类型**：Single-loop ReAct、Plan-and-Execute、Orchestrator-Worker、Hierarchical/Role-based、Reflexive/Self-Critique
- **向量记忆的局限**：无法处理多跳关系查询（"谁拥有这张表，自审计以来所有权是否变更？"），知识图谱更适合企业级关系密集型问题
- **OWASP Excessive Agency**：生产 Agent 安全失败的主要类别，提示架构层面的权限控制设计必要性

## Architecture Types Comparison

| Architecture | Description | Best Fit |
|-------------|-------------|----------|
| Single-loop ReAct | One model, one loop, flat tool list | Narrow tool surface, well-defined task |
| Plan-and-Execute | Planner decomposes; Executor runs each step | Long-horizon, mid-task drift risk |
| Orchestrator-Worker | Lead delegates subtasks to parallel specialists | Open-ended research, parallel exploration |
| Hierarchical/Role-based | Planner/Researcher/Critic/Writer small org | Complex deliverables, multiple personas |
| Reflexive/Self-Critique | Primary generates; Critic evaluates & revises | Quality-sensitive: code, legal, analytics |

## Key Quotes

> "The gap, between a model that can talk and an autonomous agent that can actually do work, is what this architecture is for."

> "Most production failures trace back to one of four: context source, decision mechanism, action capability, safety保证."

## Connections

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns]] — Planning Engine 作为 True Autonomy 支柱之一
- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]] — Graph Memory (Pattern 4) 与向量记忆的对比
- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]] — 5 类架构模式的不同选型依据
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — Harness 层的具体实现（重试、超时、观测）