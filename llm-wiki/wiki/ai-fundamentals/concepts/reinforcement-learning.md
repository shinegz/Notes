---
title: "Reinforcement Learning"
type: concept
tags: [reinforcement-learning, rl, foundation]
sources: []
last_updated: 2026-04-26
---

# Reinforcement Learning

**Reinforcement Learning = 通过与环境交互，根据奖励信号学习最优策略的机器学习范式。**

## 一句话理解

RL 的核心循环：Agent 观察状态 → 选择动作 → 获得奖励 → 更新策略。不断试错，学会在不确定环境中做最优决策。

## RL 基本框架

```
Agent（智能体）
  ├── 观察 State (s)
  ├── 选择 Action (a)
  └── 获得 Reward (r) + 下一状态 s'

Environment（环境）
  ├── 接收 Action
  ├── 返回 Reward + 下一状态
  └── 状态转移概率 P(s'|s, a)
```

## 核心概念

| 概念 | 说明 |
|------|------|
| **Policy π** | 状态 → 动作的映射，Agent 的决策函数 |
| **Value Function V** | 状态的长期价值期望 |
| **Q-Function Q(s, a)** | 在状态 s 采取动作 a 的长期价值 |
| **Reward Signal** | 即时反馈信号，指导学习方向 |

## 与 LLM 的关系

| LLM 技术 | RL 应用 |
|----------|---------|
| **RLHF** | 用人类反馈作为 reward 优化策略 |
| **PPO** | RLHF 中常用的策略优化算法 |
| **Reward Model** | 学习预测人类偏好的奖励模型 |
| **DPO** | 绕过显式 reward model 的 RL 替代方案 |

见 [[ai-fundamentals/concepts/alignment|Alignment]]。

## 来源

待补充。
