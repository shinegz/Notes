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
last_updated: 2026-04-14
---

# Harness Engineering

**工作定义（行业常用说法）**：在编码智能体场景下，**Agent = Model + Harness**——harness 是模型之外、使其在真实仓库里可靠干活的整套运行时与环境（提示与入口文档、工具/MCP/Skills、钩子与 CI、测试与观测、并行与 handoff 等）。

## 落地要点（多文交叉）

- **入口短、深链到仓库**：`AGENTS.md` 类文件当「地图」，细节进结构化 `docs/` 或等价记录系统，避免单文件百科全书挤占上下文（OpenAI 中文、Ignorance playbook）。
- **把约束做成可执行信号**：分层架构、linter、结构测试、hooks；错误信息尽量带「怎么改」（OpenAI、Fowler的 feedback / sensors）。
- **长程要有交接工件**：initializer搭脚手架 +特性清单/进度日志 + 增量提交；必要时用更结构化的格式降低被模型误改概率（Anthropic long-running）。
- **上下文要会隔离与卸载**：子智能体、技能渐进披露、工具输出外置/compaction；警惕 MCP 工具描述膨胀（HumanLayer、LangChain）。
- **验证要省 tokens**：成功安静、失败才展开；能端到端就用浏览器/可观测性把「真完成」做实（Anthropic、OpenAI 中文）。
- **并行要匹配任务形状**：任务锁、共享文件系统、以及把大单体拆成可对齐的外部 oracle（Anthropic C compiler）。

## 在本 wiki 中的来源

| 来源 | 说明 |
|------|------|
| [[agent/harness-engineering/sources/深度解析-Harness-Engineering|深度解析（公众号）]] | 综合解读：四年演进史、六大构件、意图系统范式迁移、从 Chatbot 到 AgentOS |
| [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy of an Agent Harness]] | 组件拆解：文件系统、bash、沙箱、上下文与长程执行 |
| [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]] | 引导/反馈、计算式 vs 推断式控制、三类 harness |
| [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI（中文）]] | 仓库作记录系统、架构约束、反馈与控制回路 |
| [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] | initializer / coding agent、特性清单与增量交付 |
| [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic — C compiler]] | 并行 agent 团队、测试与 harness 设计教训 |
| [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]] | AGENTS.md、MCP、Skills、子智能体、hooks、背压 |
| [[agent/harness-engineering/sources/ignorance-emerging-harness-engineering|Ignorance.ai]] | 行业 playbook 收敛：架构、工具、文档即记录 |
| [[agent/harness-engineering/sources/parallel-what-is-an-agent-harness|Parallel]] | 术语与 harness 工作流程科普 |
| [[agent/harness-engineering/sources/philschmid-agent-harness-2026|Phil Schmid]] | harness 与长程可靠性、评测 |
| [[agent/harness-engineering/sources/mitchellh-ai-adoption-journey-step-5-harness|Mitchell Hashimoto]] | 「Step 5」：AGENTS.md + 可编程工具 |

## 参见

- [[agent/harness-engineering/index|harness-engineering 子主题索引]]
- [[overview|Living overview]]
- [[index|Wiki index]]

## Contradictions

- （各文侧重点不同：有的强调「上下文工程」与 harness 的包含关系，有的强调「仓库/CI」；精读时在对应 source 页记录即可。）
