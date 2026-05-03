---
title: "anomalyco/opencode: The Open Source Coding Agent"
type: source
tags: [coding-agent, open-source, provider-agnostic, client-server, lsp, tui]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/refs/opencode-repo.md
source_url: https://github.com/anomalyco/opencode
---

## Summary

OpenCode 是 100% 开源的编码 Agent，与 Claude Code 能力相近但无 provider 绑定（可接 Claude/OpenAI/Google/本地模型）。内置 build/plan 双 Agent（Tab 切换），plan Agent 拒绝文件编辑、bash 执行需授权，适合代码探索；client/server 架构支持远程操控；内置 LSP 支持；由 neovim 用户开发，TUI 为核心交互界面。

## Key Claims

- **100% 开源 + Provider-agnostic**：不绑定任何模型 provider，通过 OpenCode Zen 提供服务但可自由切换
- **双 Agent 设计**：
  - `build` — 全权限开发 Agent
  - `plan` — 只读分析 Agent（默认拒绝编辑，bash 需授权）
  - `general` — 复杂搜索和多步骤任务的子 Agent
- **Client/Server 架构**：Agent 运行在远端，TUI 作为 client 之一，支持远程操控移动端 App
- **内置 LSP 支持**：对代码语义理解优于纯 prompt 方案
- **TUI 优先**：由 neovim 用户和 terminal.shop 创建者开发，追求终端交互极限
- **多平台桌面 App**：macOS/Windows/Linux 的 DMG/EXE/AppImage

## vs Claude Code Comparison

| Dimension | OpenCode | Claude Code |
|-----------|---------|------------|
| License | 100% Open Source | Proprietary |
| Provider | Provider-agnostic | Anthropic-only |
| Architecture | Client/Server | Local |
| LSP | Built-in opt-in | Not specified |
| Agents | build + plan (Tab switch) | Claude (main) |

## Connections

- [[agent/core-architecture/sources/pi-mono-repo|pi-mono]] — 开源编码 Agent 工具链的另一实现路径
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业级 Agent 的设计原则参照
- [[agent/core-architecture/sources/ai-agent-architecture-components-types|AI Agent Components & Types]] — Plan Agent 对应 Plan-and-Execute 架构模式