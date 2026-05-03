---
title: "AI Agents in Enterprises: Best Practices with Amazon Bedrock AgentCore"
type: source
tags: [agent, enterprise, aws, observability, tooling, mcp, production]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/articles/aws-bedrock-agentcore-best-practices.md
source_url: https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/
---

## Summary

本文（AWS, 2026-02）提出企业级 AI Agent 开发的 9 条最佳实践，核心观点是：从狭义场景出发（而非泛化）、从第一天就埋设可观测性、工具定义要精确而非简洁。强调了 Agent 的产出质量取决于"约束的质量而非模型的大小"，并给出企业 Agent 的规划文档模板和观测架构图。

## Key Claims

- **从狭义场景出发**：先定义 Agent 不做什么（scope exclusion），再从高频小任务开始迭代；泛化 Agent 必然平庸
- **四个规划交付物**：Agent 定义（功能边界）、Tone & Personality、Tools 定义（含参数格式和错误处理）、Ground Truth 数据集（50+ query 含 expected/edge cases）
- **可观测性三层**：Trace-level debugging（开发阶段）→ CloudWatch dashboards（生产监控）→ Token/Latency/Error 追踪（治理）
- **工具定义原则**：`清晰描述 > 简洁描述`，需包含输入格式、输出单位、错误行为、retry/fallback 策略
- **MCP 协议**：Model Context Protocol 作为跨工具和跨 Agent 的统一发现协议，避免重复造轮子
- **协议 vs 模式之别**：A2A/MCP/HTTP 是协议（wire format），Sequential/Hierarchical/P2P 是模式（workflow design）；两者正交，不应耦合
- **AgentCore Observability**：OpenTelemetry 原生集成，自动捕获 model invocations、tool calls、reasoning steps

## Agent Definition Template

| Dimension | Example: Financial Analytics Agent |
|-----------|----------------------------------|
| Function | Retrieve quarterly revenue, calculate growth, generate summaries |
| Exclusion | No investment advice, no trade execution, no comp data |
| Tools | `getQuarterlyRevenue(region, quarter)` → millions USD |
| Ground Truth | 50 queries including edge cases ("CEO bonus?" → decline) |

## Connections

- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]] — 企业场景下的架构选型参考
- [[agent/core-architecture/sources/multi-agent-system-architecture-guide|Multi-Agent Architecture Guide]] — Supervisor 模式下协议与模式正交设计的印证
- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]] — 企业 Agent 的可观测性与记忆架构关联