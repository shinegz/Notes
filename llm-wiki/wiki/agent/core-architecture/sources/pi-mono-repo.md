---
title: "badlogic/pi-mono: AI Agent Toolkit"
type: source
tags: [agent, toolkit, coding-agent, cli, tui, multi-provider-llm]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/refs/pi-mono-repo.md
source_url: https://github.com/badlogic/pi-mono
---

## Summary

pi-mono 是 Mario Zechner 的 AI Agent 工具箱 monorepo，核心包包括：`@mariozechner/pi-ai`（统一多 LLM API）、`@mariozechner/pi-agent-core`（Agent 运行时+工具调用+状态管理）、`@mariozechner/pi-coding-agent`（交互式编码 CLI）。项目强调公共 OSS session 数据对改进编码 Agent 的价值，倡导通过 `pi-share-hf` 共享工作 session。

## Key Components

| Package | Description |
|--------|-------------|
| `@mariozechner/pi-ai` | 统一多 LLM API（OpenAI, Anthropic, Google 等） |
| `@mariozechner/pi-agent-core` | Agent 运行时，含工具调用和状态管理 |
| `@mariozechner/pi-coding-agent` | 交互式编码 Agent CLI |
| `@mariozechner/pi-tui` | Terminal UI 库（差分渲染） |
| `@mariozechner/pi-web-ui` | AI 聊天界面 Web 组件 |

## Key Claims

- **统一 LLM API**：`pi-ai` 提供多 provider 统一接口，降低 provider 切换成本
- **Agent 运行时分离**：`pi-agent-core` 将工具调用和状态管理与具体 LLM 解耦
- **Session 数据共享**：通过 Hugging Face 共享 OSS session（真实任务、工具调用、失败案例），而非 toy benchmarks
- **开发友好**：`./pi-test.sh` 可从源码运行，`npm run check` 包含 lint + format + type check

## Connections

- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业级 Agent 运行时设计的参照
- [[agent/core-architecture/sources/ai-agent-architecture-components-types|AI Agent Components & Types]] — pi-agent-core 对应 harness/运行时层