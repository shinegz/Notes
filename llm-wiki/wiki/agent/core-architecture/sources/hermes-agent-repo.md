---
title: "NousResearch/hermes-agent: The Agent That Grows With You"
type: source
tags: [agent, self-improving, skills, memory, cross-session, hermes, nousresearch]
last_updated: 2026-05-03
source_file: raw/agent/core-architecture/refs/hermes-agent-repo.md
source_url: https://github.com/nousresearch/hermes-agent
---

## Summary

Hermes Agent（Nous Research）是目前唯一内置**自改进学习 loop**的开源 Agent：能从经验中创建 skills、在使用中自我改进、定期 nudge 自己持久化知识、跨 session 搜索历史对话、用 Honcho 做用户建模。架构支持 6 种终端后端（local/Docker/SSH/Daytona/Singularity/Modal），可运行在 $5 VPS 或 serverless 环境。

## Key Claims

- **内置自改进学习 loop**：
  - Agent-curated memory + periodic nudges
  - 复杂任务后自动创建 skills
  - Skills 在使用中自我改进
  - FTS5 session search + LLM summarization 跨 session 记忆
- **Provider-agnostic**：OpenRouter（200+ 模型）、OpenAI、Anthropic、NVIDIA NIM、Hugging Face、自定义 endpoint；`hermes model` 切换无需改代码
- **多 channel 接入**：Telegram、Discord、Slack、WhatsApp、Signal、Email + CLI，统一 gateway 进程
- **Subagent 并行化**：spawn 隔离 subagent 并行工作流，Python RPC 调用工具
- **Atropos RL 集成**：批量轨迹生成、RL 环境、轨迹压缩用于训练下一代 tool-calling 模型
- **Skills 系统兼容**：`agentskills.io` 开放标准，Skills Hub 共享

## Architecture Features

| Feature | Implementation |
|---------|---------------|
| Self-improving loop | Memory nudges + autonomous skill creation |
| Cross-session memory | FTS5 + LLM summarization |
| User modeling | Honcho dialectic approach |
| Multi-backend | Local, Docker, SSH, Daytona, Singularity, Modal |
| Scheduling | Built-in cron → any platform |
| RL integration | Atropos RL, trajectory compression |

## Connections

- [[agent/core-architecture/sources/core-agentic-ai-architectural-patterns|Core Architectural Patterns]] — True Autonomy 三大支柱：Persistent Memory、Adaptive Planning 在 Hermes 中的具体实现
- [[agent/core-architecture/sources/agent-memory-architectures|Agent Memory Architectures]] — FTS5 session search 对应 Pattern 2/3 的检索机制
- [[agent/core-architecture/sources/ultimate-guide-ai-agent-architectures-2025|Ultimate Guide 2025]] — Subagent 并行化对应 Orchestrator-Worker 模式