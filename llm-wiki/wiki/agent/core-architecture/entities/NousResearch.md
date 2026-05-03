---
title: "Nous Research"
type: entity
tags: [organization, llm, agent, open-source]
sources:
  - agent/core-architecture/sources/hermes-agent-repo
last_updated: 2026-05-03
---

## 一句话定义

Nous Research 是 AI 研究组织，开发了 Hermes Agent——唯一内置自改进学习 loop 的开源 Agent，也是首个将 Atropos RL 轨迹压缩技术用于 tool-calling 模型训练的开源项目。

## 关键产品

### Hermes Agent

自改进 Agent，核心特性：
- 内置学习 loop：自动创建 skills、从使用中改进、定期 nudge 持久化知识
- FTS5 session search + LLM summarization 跨 session 记忆
- Honcho dialectic 用户建模
- 6 种终端后端支持（local/Docker/SSH/Daytona/Singularity/Modal）
- 兼容 `agentskills.io` 开放标准
- 支持 Atropos RL 轨迹压缩

### 社区资源

- [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/)
- [Discord 社区](https://discord.gg/NousResearch)

## 来源

- [[agent/core-architecture/sources/hermes-agent-repo|Hermes Agent Repo]]