---
title: "Context Engineering"
type: concept
tags: [context-engineering, agent, prompt-engineering, llm]
sources:
  - ai-fundamentals/sources/anthropic-context-engineering
  - ai-fundamentals/sources/prompt-engineering-2025-aakashg
  - ai-fundamentals/sources/lost-in-the-middle
  - ai-fundamentals/sources/context-dilution
  - ai-fundamentals/sources/longllmlingua
last_updated: 2026-05-07
---

# Context Engineering

**Context Engineering = 在有限的注意力预算内，为 LLM 每次推理筛选最优 token 集合的工程实践。**

## 一句话理解

Context Engineering 是 Prompt Engineering 的自然演进：从「写好单次指令」升级为「持续编排推理时整个上下文状态」——系统指令、工具、外部数据、消息历史都在管理范围内。

## 背景

LLM 的注意力机制产生 n² 对关系（n = token 数）。随着上下文增长，每对关系的权重被稀释，出现 context rot 现象：上下文越长，信息召回精度越低。这使得上下文成为有限资源，必须像内存一样工程化管理。

Agent 在循环中运行，每轮产生更多可能相关的数据，上下文编排从一次性动作变为持续迭代。

## 核心机制

### Prompt Engineering vs Context Engineering

| 维度 | Prompt Engineering | Context Engineering |
|------|-------------------|-------------------|
| 范围 | 系统指令的写法 | 推理时所有 token 的编排 |
| 时间性 | 一次性设计 | 每次推理前迭代筛选 |
| 关注点 | 指令文本 | 指令 + 工具 + MCP + 数据 + 历史 |
| 适用场景 | 单次/短交互 | Agent 长时程循环 |

### 最小高信噪比原则

好的 Context Engineering = 找到最小的高信噪比 token 集合，使期望输出的概率最大化。Minimal ≠ short，但每个 token 都应有存在的理由。

### 系统提示的「正确海拔」

- 太具体 → 脆弱难维护（if-else 硬编码）
- 太抽象 → 模型缺乏行为锚点
- 正确海拔 = 具体到能引导行为，灵活到提供强启发式

### 长时程任务三策略

| 策略 | 机制 | 适用场景 |
|------|------|----------|
| Compaction | 压缩上下文继续 | 需要大量来回交互 |
| Structured Note-taking | 持久化笔记到上下文外 | 迭代开发，有清晰里程碑 |
| Sub-agent | 子 Agent 隔离上下文后只返回摘要 | 复杂研究，并行探索 |

### 上下文检索策略

| 策略 | 特点 | 示例 |
|------|------|------|
| 预计算检索 | 速度快，提前加载 | RAG、嵌入向量检索 |
| Just-in-Time | 深度好，按需加载 | Claude Code 的 glob/grep |
| Hybrid | 两者结合 | CLAUDE.md 预加载 + 实时检索 |

## 关联概念

- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — Context Engineering 的子集，承担约 85% 工作量
- [[ai-fundamentals/concepts/llm-agents|LLM Agents]] — Agent 的循环运行模式是 Context Engineering 的核心驱动
- [[ai-fundamentals/concepts/context-window|Context Window]] — 物理限制是 Context Engineering 的根本约束
- [[ai-fundamentals/concepts/memory|Memory]] — Structured Note-taking 是 Memory 的工程化实现

## 来源

- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — 核心理论来源
- [[ai-fundamentals/sources/prompt-engineering-2025-aakashg|Prompt Engineering in 2025]] — 产品实践视角
