---
title: "MCP (Model Context Protocol)"
type: concept
tags: [protocol, tool-integration, interoperability, standard]
sources:
  - agent/core-architecture/sources/aws-bedrock-agentcore-best-practices
  - agent/core-architecture/sources/llm-enabled-multi-agent-systems
last_updated: 2026-05-03
---

## 一句话理解

MCP（Model Context Protocol）是 Anthropic 提出的开放标准，让 LLM 能以统一方式连接外部工具、数据源和服务，避免每个 Agent 重复造轮子。

## 背景

随着 Agent 系统增长，工具集成成本成为瓶颈。AWS Bedrock AgentCore 指出：团队不应重复建设同一个数据库连接器。MCP 解决了工具发现和集成的标准化问题。

## 核心价值

| 价值 | 说明 |
|------|------|
| **统一协议** | 跨 Agent、跨 Provider 的工具发现和调用 |
| **减少重复** | 不用每个 Agent 重写 Slack/Google Drive 连接器 |
| **互操作** | 不同 Agent 框架之间的工具可互相调用 |

## MCP vs A2A

| | MCP | A2A |
|--|-----|-----|
| **定位** | Agent ↔ 工具/数据/服务 | Agent ↔ Agent |
| **解决的问题** | 工具发现和调用标准化 | Agent 间通信协议 |
| **发起方** | Anthropic | Anthropic |

AWS 强调：**协议（Protocol）和模式（Pattern）是正交的**。A2A/MCP 是协议，Sequential/Hierarchical/P2P 是模式。两者可以自由组合。

## 来源

- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]]
- [[agent/core-architecture/sources/llm-enabled-multi-agent-systems|LLM-Enabled Multi-Agent Systems]]