---
title: "openclaw/openclaw: Your own personal AI assistant"
type: source
tags: [personal-assistant, multi-channel, open-source, gateway, sandbox]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/refs/openclaw-repo.md
source_url: https://github.com/openclaw/openclaw
---

## Summary

OpenClaw 是本地优先的个人 AI Assistant，支持 20+ 消息通道（WhatsApp/Telegram/Discord/Slack/iMessage 等），通过 Gateway 控制平面统一管理 session、channel、tools 和 events。核心差异化是本地优先（local-first）+ 多渠道接入（multi-channel）+ 沙箱安全模型，定位是"personal AI that stays on your own devices"。

## Key Claims

- **Local-first 架构**：Gateway 运行在本地设备，Agent 控制在本地，不强制依赖云端服务
- **20+ 消息通道**：统一接入 WhatsApp、Telegram、Discord、Slack、iMessage、Signal、WeChat、QQ 等，支持多 channel 同时在线
- **Multi-agent routing**：根据 inbound channel/account/peer 路由到隔离的 Agent workspace，每个 workspace 有独立 session
- **Sandbox 安全模型**：非 main session 默认运行在 Docker 沙箱中，可配置允许/拒绝的工具列表（默认 deny browser/canvas/cron/discord/gateway）
- **Skills 系统**：通过 ClawHub 共享和安装 skills，支持 browser/canvas/nodes/cron/sessions 等工具
- **Voice + Canvas**：支持 Voice Wake（macOS/iOS）和 Live Canvas（agent 驱动的视觉工作空间）

## Architecture Overview

| Component | Description |
|-----------|-------------|
| Gateway | 本地控制平面，管理 session、channel、tools、events |
| Workspace | 隔离的 Agent 工作空间，各有独立 session |
| Channel | 消息通道接入层（每个 channel 可单独配置 allowlist/dmPolicy） |
| Skills | 可共享的工具集，通过 ClawHub 分发 |

## Security Model

OpenClaw 连接到真实消息平台，**默认将所有入站 DM 视为不可信输入**。关键安全机制：

- **DM Pairing**：未知发送者收到配对码，管理员 `openclaw pairing approve` 后才加入 allowlist
- **Sandbox**：main session 默认在宿主机运行完整权限；非 main session 默认在 Docker 沙箱中，工具调用受限
- **dmPolicy 控制**：可设置为 `pairing`（需审批）或 `open`（公开），影响哪些发送者可与 Agent 交互

## Connections

- [[agent/core-architecture/sources/pi-mono-repo|pi-mono]] — 开源 Agent 工具链的另一实现路径
- [[agent/core-architecture/sources/hermes-agent-repo|Hermes Agent]] — 自改进 + 多 channel 接入的另一个案
- [[agent/core-architecture/sources/aws-bedrock-agentcore-best-practices|AWS Bedrock AgentCore]] — 企业级 Agent 的安全/可观测性设计参照
