---
title: "True Autonomy"
type: concept
tags: [agent, architecture, autonomy, cognitive-architecture, world-model]
sources:
  - agent/core-architecture/sources/core-agentic-ai-architectural-patterns
last_updated: 2026-05-03
---

## 一句话理解

True Autonomy 是将 LLM 作为规划引擎之一，配合 World Model、Persistent Memory 和 Adaptive Planning 三大支柱构成模块化认知架构，使系统具备跨 session 学习、环境建模和动态策略调整能力。

## 背景

Ken Mendoza（Oregoncoast.ai）指出，Simulated Agency 只能做"following a map"，而 True Autonomy 能"drawing one"。这不仅是功能差异，而是根本性的架构差异。

## 三大支柱

### 1. World Model

对环境内部建模，支持预测和规划。不是简单的状态存储，而是对"如果做 X，世界会怎样变化"的模拟。

**与 Simulated Agency 的区别**：后者没有 World Model，只有 context window 中的表面信息。

### 2. Persistent Memory

跨 session 持久化的记忆系统，能积累知识、更新信念、避免重复犯错。

**关键特征**：记忆内容不只来自当前 session，而是来自与环境的多次交互。

### 3. Adaptive Planning Engine

根据反馈动态调整策略，不是执行固定目标，而是能生成和修改子目标。

**与 Simulated Agency 的区别**：后者目标固定，只在 prompt 范围内做反应式决策。

## 架构特点

| 特点 | 说明 |
|------|------|
| 模块化 | LLM 是工具，不是唯一的"大脑" |
| 感知-反思-预测-适应循环 | 区别于单纯的 ReAct 循环 |
| 跨 session 进化 | 系统随使用变得更值钱 |

## 来源

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns 2025]]