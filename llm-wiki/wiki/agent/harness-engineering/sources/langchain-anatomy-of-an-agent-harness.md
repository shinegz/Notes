---
title: "The Anatomy of an Agent Harness"
type: source
tags: [harness-engineering, agent, langchain]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/langchain-anatomy-of-an-agent-harness.md
source_url: https://blog.langchain.com/the-anatomy-of-an-agent-harness/
---

## Summary

Vivek Trivedy 给出一句分界：**If you're not the model, you're the harness**，并把 harness engineering 描述为把模型从「会输出文本」变成「能持续工作」所需的工程。文章从模型原生做不到的事情反推组件：文件系统、bash/代码执行、沙箱与验证、记忆与检索、对抗 **context rot**（compaction、工具输出卸载、Skills 渐进披露）、以及长程自主（Ralph loop、计划与自验证）。最后讨论 **post-training 与 harness 共演化** 导致的工具过拟合，同时用 Terminal Bench 2.0 说明 **换 harness 仍能巨大提分**。

## Key claims

- harness 至少覆盖：system prompt、tools/skills/MCP、捆绑基础设施（fs/沙箱/浏览器）、编排（子智能体/handoff/路由）、以及 hooks/middleware（确定性步骤）。
- 文件系统是最底层 primitive之一：持久化、协作、以及跨会话恢复。
- bash/代码执行是通用工具策略：让模型在运行时用代码「自造工具」。
- harness 很大程度上是 **context engineering 的交付机制**；Skills 缓解「启动即加载过多工具描述」导致的性能衰减。
- 模型与 harness 共同进化会带来 **泛化/迁移** 问题，但不等于「别定制 harness」。

## Key quotes

> Agent = Model + Harness

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]] — 对 MCP/Skills/hooks 的落地补充
- [[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|Parallel]] — 术语与流程科普视角

## Contradictions

- 「未来模型更强，harness 重要性下降」与「仍需工程化环境」并存：作者认为会像 prompt engineering 一样 **长期仍有价值**（与短周期 hype 叙述不同）。
