---
title: "Harness Engineering"
type: concept
tags: [harness-engineering, agent, coding-agents]
sources:
  - agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness
  - agent/harness-engineering/sources/martin-fowler-harness-engineering
  - agent/harness-engineering/sources/openai-harness-engineering-zh
  - agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents
  - agent/harness-engineering/sources/anthropic-building-c-compiler
  - agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering
  - agent/harness-engineering/sources/ignorance-emerging-harness-engineering
  - agent/harness-engineering/sources/parallel-what-is-an-agent-harness
  - agent/harness-engineering/sources/philschmid-agent-harness-2026
  - agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness
  - agent/harness-engineering/sources/深度解析-Harness-Engineering
last_updated: 2026-04-24
---

# Harness Engineering

**核心公式：Agent = Model + Harness**

Harness 是模型之外的整套运行时与环境，使模型能在真实仓库里可靠地完成任务——包括提示与入口文档、工具/MCP/Skills、钩子与 CI、测试与观测、并行与交接等[[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|1]]。

## 一句话理解

Harness 是让 LLM 从「能说」进化到「能把复杂的事在长时间跨度内做成」的工程化外循环系统。

## 落地要点（多文交叉）

| 原则 | 说明 | 来源 |
|------|------|------|
| **入口短、深链到仓库** | `AGENTS.md` 当「地图」，细节进结构化 `docs/`，避免单文件百科全书挤占上下文 | [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI]][[agent/harness-engineering/sources/ignorance-emerging-harness-engineering|Ignorance]] |
| **把约束做成可执行信号** | 分层架构、linter、结构测试、hooks；错误信息带「怎么改」 | [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Fowler]][[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI]] |
| **长程要有交接工件** | initializer 搭脚手架 + 特性清单/进度日志 + 增量提交；用结构化格式降低被模型误改概率 | [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic]] |
| **上下文要会隔离与卸载** | 子智能体、技能渐进披露、工具输出外置/compaction；警惕 MCP 工具描述膨胀 | [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]][[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain]] |
| **验证要省 tokens** | 成功安静、失败才展开；能用浏览器/可观测性把「真完成」做实 | [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic]][[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI]] |
| **并行要匹配任务形状** | 任务锁、共享文件系统、把大单体拆成可对齐的外部 oracle | [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic C]] |

## 来源导航

| 来源 | 核心贡献 |
|------|----------|
| [[agent/harness-engineering/sources/深度解析-Harness-Engineering|深度解析（公众号）]] | 综合解读：四年演进史、六大构件、意图系统范式迁移 |
| [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]] | 组件拆解：文件系统、bash、沙箱、上下文与长程执行 |
| [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]] | 引导/反馈、计算式 vs 推断式控制 |
| [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI]] | 仓库作记录系统、架构约束、反馈与控制回路 |
| [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] | initializer / coding agent、特性清单与增量交付 |
| [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic — C compiler]] | 并行 agent 团队、测试与 harness 设计 |
| [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]] | AGENTS.md、MCP、Skills、子智能体、hooks |
| [[agent/harness-engineering/sources/ignorance-emerging-harness-engineering|Ignorance.ai]] | 行业 playbook 收敛 |
| [[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|Parallel]] | 术语与 harness 工作流程 |
| [[agent/harness-engineering/sources/philschmid-agent-harness-2026|Phil Schmid]] | harness 与长程可靠性、评测 |
| [[agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness|Mitchell Hashimoto]] | Step 5：AGENTS.md + 可编程工具 |

## 参见

- [[agent/harness-engineering/syntheses/harness-engineering-deep-dive|深度解析]] — 基于 11 篇来源的综合分析
- [[agent/harness-engineering/index|harness-engineering 子主题索引]]
- [[overview|Living overview]]
- [[index|Wiki index]]
