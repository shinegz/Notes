---
title: "深度解析：Harness Engineering"
type: source
tags: [harness-engineering, chinese, wechat, comprehensive]
sources: []
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/wechat/深度解析-Harness-Engineering.md
source_url: https://mp.weixin.qq.com/s/-mgf8K7XZrTKoD0pMOIn3w
---

## Summary

浮之静（公众号）2026-04-03 发布的 Harness Engineering 深度解析，约 2 万字。从 AI 工程四年演进史出发，推导 Harness 的必要性，系统阐述六大工程构件、意图系统范式迁移、从 Chatbot 到 AgentOS 的演化路径，以及五个典型症状与未来判断。配 9 张图，覆盖 Anthropic/OpenAI 实践细节。

## Key claims

- **Agent = Model + Harness**：评估 agent 效果时，评估的是组合而非模型单独能力
- **Harness 五大挑战**：状态持久性、目标一致性、行动可验证性、熵增抑制、人机边界——均无法靠更聪明的模型单独解决
- **六大构件**：Durable State Surfaces、Decomposition & Plans、Feedback Loops（Guides/Sensors 2×2）、Legibility、Tool Mediation、Entropy Control
- **三层抽象**：Prompt → Context → Harness；Context Engineering 是 Harness Engineering 子集
- **Harnessability**：强类型、测试完备、边界清晰、文档版本化的系统天然更高 harnessability
- **范式迁移**：从指令驱动到意图驱动；人机交互经历 CLI → GUI → App → Agent 四次断裂

## Key quotes

> 模型不是瓶颈，系统才是。当 AI Agent 从"能跑"走向"能治"，一门新的基础学科正在成形。

> Harness = 让模型能够作为 Agent 行动起来的外循环系统。它包含计划分解、持久状态、工具编排、验证门控、反馈回路、回退机制、人机交接点和审计日志。

> 凡是不在 agent 运行时可见范围内的知识，就等于不存在。

> 状态 ≠ "保存聊天记录"。真正的 durable state 是 agent 可以在冷启动后、没有任何上下文历史的情况下读取、理解、续航的结构化工件。

> Harness 不只负责"让 agent 跑起来"，还负责持续抑制 agent 放大的系统噪声。

## Connections

- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] — Anthropic 官方实践，planner/generator/evaluator 三角色系统
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]] — OpenAI 五个月百万行代码实验
- [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]] — 2×2 控制矩阵（Guides/Sensors + Computational/Inferential）
- [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]] — LangChain Terminal Bench 2.0 实验结果
- [[agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness|Mitchell Hashimoto]] — "Engineer the Harness" 术语来源之一
- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]] — 概念页

## Timeline

| 时间 | 事件 |
|------|------|
| 2022-11 | ChatGPT 上线，Prompt Engineering 时代 |
| 2023-03 | GPT-4 + Plugins，模型"能连" |
| 2024-09 | OpenAI o1 推理模型 |
| 2024-12 | Anthropic MCP 协议 + Building Effective Agents |
| 2025 | Agent 年：Claude Code、Cursor、Manus、Operator |
| 2026-02 | Mitchell Hashimoto "Engineer the Harness"；OpenAI 官方文章 |
| 2026-03 | Anthropic planner/generator/evaluator 三角色 |
| 2026-04 | Martin Fowler 2×2 控制矩阵 |

## Contradictions

暂无与其他 source 的直接矛盾。本文为综合性解读，与各官方 source 互补。
