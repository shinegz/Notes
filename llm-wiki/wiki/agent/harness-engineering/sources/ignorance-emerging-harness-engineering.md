---
title: "The Emerging Harness Engineering Playbook"
type: source
tags: [harness-engineering, agent, playbook]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/ignorance-emerging-harness-engineering.md
source_url: https://www.ignorance.ai/p/the-emerging-harness-engineering
---

## Summary

Ignorance.ai 把 2026 年前后若干「规模化用 agent 写代码」的案例（OpenAI 内部 Codex 项目、Stripe Minions、OpenClaw 等）收敛成一份仍在演化的 **playbook**：工程师工作被拆成 **搭建环境**（结构、工具、反馈）与 **管理工作**（规划、品味、并行编排）两半，且二者交替迭代。文中用 Mitchell Hashimoto 的 **harness engineering** 命名这套约束/工具/文档/反馈回路，并归纳四条重复出现的实践：架构当护栏、工具既可扩展能力也可提供反馈、文档当记录系统（含 AGENTS.md 的持续更新）、以及把长程任务拆成 initializer / 计划 / 验收。

## Key claims

- 规模化信号来自真实生产系统：极高 commit/PR 吞吐、Slack 一键到 PR、以及「人类几乎不写实现代码但仍在掌舵」的组织方式。
- **严格架构与机械 enforcement** 在 agent场景里是乘数：自定义 linter/结构测试把错误信息写成「可执行的修复指导」，让工具在反馈阶段教学。
- **AGENTS.md** 要成为负载-bearing的基础设施：不是写一次，而是每次 agent 犯错就更新；OpenAI 团队用短入口 + `docs/` 深链与 doc-gardening agent 维护新鲜度。
- 「AI manager」侧：规划与执行分离、拒 **slop**（合并门槛不随速度下降）、以及 **attended vs unattended** 并行化需要不同的 harness 成熟度。
- 仍开放的问题包括：功能正确但难维护的代码累积（entropy）、规模化验证、brownfield 改造、以及文化/组织 adoption。

## Key quotes

> The first half is building the environment… The second half is managing the work… You do both at the same time, and each one informs the other.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]] — playbook 中多条引用来源
- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] — initializer / feature list / handoff

## Contradictions

- 与「仅靠更大上下文窗口」的直觉相反：多篇共识强调 **结构、工具与验证** 才是长程可靠性的杠杆（与 HumanLayer / LangChain 的上下文工程叙事一致，但本文更偏组织与流程层）。
