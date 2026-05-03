---
title: "A2A (Agent-to-Agent Protocol)"
type: concept
tags: [protocol, multi-agent, interoperability, wire-format]
sources:
  - agent/core-architecture/sources/aws-bedrock-agentcore-best-practices
last_updated: 2026-05-03
---

## 一句话理解

A2A（Agent-to-Agent）是 Anthropic 提出的开放协议，定义 Agent 之间的通信格式和 API 契约，与 MCP（工具发现）和 HTTP（传输）同属协议层，与 Supervisor/Hierarchical/P2P 等协调模式是正交关系。

## 背景

随着 Multi-Agent 系统规模扩大，Agent 之间如何可靠地传递任务、结果和状态成为关键问题。A2A 填补了"工具调用标准化（MCP）"之后的"Agent 间通信标准化"缺口。

## 核心定位

| | A2A | MCP | HTTP |
|--|-----|-----|------|
| **定位** | Agent ↔ Agent | Agent ↔ 工具/数据/服务 | 底层传输 |
| **解决的问题** | Agent 间任务交接和状态同步 | 工具发现和调用标准化 | 数据传输 |
| **发起方** | Anthropic | Anthropic | — |
| **与模式的关系** | 协议层（正交于模式） | 协议层（正交于模式） | 传输层 |

**关键洞见**（AWS）：协议和模式是**正交**的——可以在 A2A 上跑 Sequential 模式，也可以在 MCP 上跑 Hierarchical 模式。混淆协议和模式是 Multi-Agent 系统设计失败的第一原因。

## 与 MCP 的关系

| 维度 | MCP | A2A |
|------|-----|-----|
| **连接方向** | Agent → 工具/数据源 | Agent → Agent |
| **核心抽象** | Tool（可调用函数） | Task/Agent（可交接的工作单元） |
| **发现机制** | 工具清单（tool manifest） | Agent 能力描述（agent card） |
| **典型场景** | Agent 调用外部 API、数据库 | Agent 之间委派子任务、同步状态 |

两者互补：一个 Agent 可以同时使用 MCP 连接外部工具，用 A2A 与其他 Agent 协作。

## 局限性

- **协议碎片化**：截至 2026 年初，A2A 仍是早期标准，生产环境多数仍用私有协议
- **状态一致性**：多 Agent 之间的分布式状态管理超出 A2A 协议范围
- **性能开销**：相比直接函数调用，Agent 间通信的延迟和 token 成本显著更高

## 来源

- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — A2A/MCP/HTTP 协议层与 Sequential/Hierarchical/P2P 模式层正交的核心论述
- [[agent/core-architecture/sources/multi-agent-system-architecture-guide|Multi-Agent Architecture Guide]] — 协调模式作为架构层与协议层的关系
- [[agent/core-architecture/sources/llm-enabled-multi-agent-systems|LLM-Enabled Multi-Agent Systems]] — MCP 作为互操作标准
