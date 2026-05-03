---
title: "Multi-Agent Coordination Patterns"
type: concept
tags: [multi-agent, architecture, coordination, supervisor, hierarchical, p2p]
sources:
  - agent/core-architecture/sources/multi-agent-system-architecture-guide
last_updated: 2026-05-03
---

## 一句话理解

多 Agent 协调模式解决"多个 Agent 如何通信和决策"的问题，五种核心模式（Supervisor/Hierarchical/P2P/Blackboard/Swarm）各有适用场景，选错是生产失败的第一原因。

## 五种协调模式

### 1. Supervisor（Orchestrator-Worker）

中心协调者做路由，子 Agent 不直接通信。

| 特点 | 说明 |
|------|------|
| 决策 | 中心化，单一协调者 |
| 扩展性 | 线性（新增 worker 不增加通信路径） |
| 优势 | 确定性强，易调试，集中可观测 |
| 劣势 | 协调者单点瓶颈 |

**适用**：顺序任务、清晰的任务边界、需要确定性执行顺序

### 2. Hierarchical

多层 Supervisor 叠加，适合复杂多层分解。

**适用**：大型企业工作流、层层拆解的任务

### 3. Peer-to-Peer（P2P）

Agent 间对等通信，协商决策。

| 特点 | 说明 |
|------|------|
| 通信 | 每对 Agent 间直接通信 |
| 扩展性 | O(n²) 通信开销 |
| 优势 | 适合协商场景 |
| 劣势 | 协调复杂，调试困难 |

### 4. Blackboard

共享黑板供多个 Agent 读写，专家系统风格。

**适用**：需要多个专家视角共同解决问题的场景

### 5. Swarm

高度去中心化，Agent 自主发现和协作。

**适用**：开放性探索任务，但输出不可预测

## 关键量化数据

- Supervisor 使并行任务提升 80%，但使顺序推理退化 70%
- 协调开销随 Agent 数量**平方增长**
- 论文量 2024→2025 从 820 篇增至 2500+ 篇，但生产落地严重滞后

## 选型决策树

```
任务是否并行可分？
  YES → Supervisor / Hierarchical
  NO → 任务是否需要协商？
        YES → P2P / Blackboard
        NO → 是否开放性探索？
              YES → Swarm
```

## 来源

- [[agent/core-architecture/sources/multi-agent-system-architecture-guide|Multi-Agent Architecture Guide]]