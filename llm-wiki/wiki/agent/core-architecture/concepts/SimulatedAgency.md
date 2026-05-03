---
title: "Simulated Agency"
type: concept
tags: [agent, architecture, react, prompt-chaining]
sources:
  - agent/core-architecture/sources/core-agentic-ai-architectural-patterns
last_updated: 2026-05-03
---

## 一句话理解

Simulated Agency 是用单一 LLM 的 ReAct 循环做"next-best-action"决策，依赖 context window 记忆，本质是 prompt chaining 的高级形式，不具备真正的规划和适应能力。

## 背景

以 AutoGPT、BabyAGI 为代表的系统展示了 LLM 做多步任务的能力，但它们的"智能"是 LLM 预训练知识的反射，不是真正的自主性。Ken Mendoza（Oregoncoast.ai）将这类系统定义为 Simulated Agency，与 True Autonomy 相对。

## 核心机制

**ReAct Loop（Reason + Act）**：

1. **Goal Ingestion**：接收高层目标
2. **Reasoning**：LLM 结合当前状态和可用工具决定下一步动作
3. **Action**：执行工具调用，返回结果
4. **Observation & Iteration**：结果加入 context，循环直到 LLM 认为目标达成

**LLM 的角色**：不是规划器，是"myopic 决策器"——每步只看眼前，不真正规划全局。

## 三大失败模式

| 失败模式 | 描述 |
|---------|------|
| **Hallucination Cascades** | 单个错误假设被反馈进 context，形成复合错误链 |
| **Anchor Problem** | Agent 执着于初始 plan，出现反证时无法 pivot |
| **Lost in the Middle** | context 中间位置信息回忆率低于边界位置 |

## 局限性

- **无 World Model**：对操作的概念没有底层理解
- **Context 记忆有限**：窗口填满后旧信息被稀释，且 token 成本线性增长
- **无持久学习**：session 结束后没有学到任何东西，相同失败会重复
- **Brittleness**：不适合任务关键或长时运行场景

## 与 True Autonomy 的对比

| 维度 | Simulated Agency | True Autonomy |
|------|------------------|---------------|
| Memory | Context window（临时） | Persistent external store |
| Planning | Reactive, myopic | Adaptive, forward-looking |
| World Model | None | Dedicated module |
| Learning | None | Cumulative across sessions |

## 来源

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns 2025]]