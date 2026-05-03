---
title: "ReAct"
type: concept
tags: [agent, reasoning, tool-use, reasoning-action-loop]
sources:
  - agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025
  - agent/core-architecture/sources/memory-autonomous-llm-agents
last_updated: 2026-05-03
---

## 一句话理解

ReAct（Reason + Act）是用 LLM 交替做推理和动作执行的循环，工具调用结果作为 observation 反馈进推理链，直到任务完成。

## 背景

ReAct 由 Yao et al. (2022) 提出，在 ALFWorld benchmark 上比单用推理或单用动作的方法提升 34% 绝对准确率。ReAct 的关键洞见是：推理（reasoning）和动作（acting）交替比单独使用效果更好——推理帮助模型感知状态、规划下一步，动作让模型获得真实环境反馈。

## 核心机制

```
Loop:
  1. Reasoning: LLM 基于当前状态决定下一步
  2. Action: 执行工具调用
  3. Observation: 结果作为 context 反馈
  4. 重复直到目标达成
```

## 关键特征

- **Short-horizon working memory**：推理轨迹本身就是 working memory，不需要额外的外部存储
- **34% 绝对提升**（ALFWorld vs baseline）
- **简单有效**：成本比 Reflexion/LDB 低约 50%，但准确率相当

## 局限性

- 无持久记忆，session 结束即丢失
- "lost in the middle" 问题——长 context 中间信息被忽略
- 推理步骤是 myopic 的，不是真正的规划

## 在记忆架构中的位置

ReAct 属于 **Context-resident memory** 机制家族——推理轨迹作为短时 working memory，没有外部存储。

## 来源

- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]]
- [[agent/core-architecture/sources/memory-autonomous-llm-agents|Memory for Autonomous LLM Agents]]