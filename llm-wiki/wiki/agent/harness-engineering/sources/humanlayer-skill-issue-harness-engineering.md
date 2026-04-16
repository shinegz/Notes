---
title: "Skill Issue: Harness Engineering for Coding Agents"
type: source
tags: [harness-engineering, agent, context-engineering]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/humanlayer-skill-issue-harness-engineering.md
source_url: https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents
---

## Summary

HumanLayer 把多数编码智能体失败归因于 **harness 配置**，而不是模型本身：「coding agent = AI model(s) + harness」。**Harness engineering**（术语引用 Viv Trivedy）指系统性地使用入口文档、MCP、Skills、子智能体、hooks、背压与验证等手段，提高输出质量与可靠性；并被明确放在 **context engineering**（12-factor agents）之下，核心问题是管理好上下文窗口与「指令预算」。文中也讨论 post-training 与默认 harness 的耦合：换 harness 可能更好也可能更差。

## Key claims

- 非确定性系统会不断出现新的意外失效模式；应优先回答「如何把今天的模型用好」，而不是假设下一代模型会一劳永逸。
- 子智能体主要价值是 **上下文隔离**（context firewall），把中间工具噪声挡在父线程外；按「角色」划分子智能体效果通常不好。
- MCP 工具描述会进入 system prompt：**不可信 MCP 有 prompt injection 风险**；工具过多会快速把模型推入「dumb zone」，应渐进披露或用 CLI 替代臃肿 MCP。
- Skills 通过 **progressive disclosure** 缓解上下文膨胀；需像安装 npm 包一样审视来源（恶意 skill 注册表已有公开报道）。
- Hooks 把格式化、类型检查、构建失败等 **确定性信号** 接回循环；验证输出要 **context-efficient**（成功安静、失败才啰嗦）。

## Key quotes

> But over the course of dozens of projects and hundreds of agent sessions, we kept arriving at the same conclusion: it's not a model problem. It's a configuration problem.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]] — 概念枢纽
- [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]] — 对 harness 组分的另一种推导
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]] — 更偏仓库/反馈回路/背压的工程叙事（措辞焦点不同）

## Contradictions

- 与「尽量别改默认 harness（post-training 最优）」的推断相反：文引用 Terminal Bench 2.0，说明 **换 harness 可显著提升排名**；与默认 harness 的关系是双向的（耦合 vs 过拟合）。
