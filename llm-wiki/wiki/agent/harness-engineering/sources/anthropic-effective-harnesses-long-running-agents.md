---
title: "Effective harnesses for long-running agents"
type: source
tags: [harness-engineering, agent, long-running]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/anthropic-effective-harnesses-long-running-agents.md
source_url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
---

## Summary

Anthropic 描述长程编码智能体的核心难题：**每个新会话没有上一会话记忆**，像轮班工程师永不交接。文章提出 **initializer agent + coding agent** 的双提示策略：首次会话生成可运行脚手架、进度日志与（示例中）大量细粒度功能条目；后续会话每次只做增量推进并留下 git/commit 与进度说明。**JSON 功能清单** 比 Markdown 更不易被模型误改；同时强调浏览器自动化做端到端验证，否则模型容易「以为做完」。

## Key claims

- 仅有 compaction 不足以支撑生产级长程交付；需要外部工件承担 **交接**功能。
- 两大失败模式：一次做太多导致半拉子状态；或中后期 **过早宣布完成**。
- initializer 产出 `init.sh`、进度文件、初始提交与结构化 feature 列表（带步骤与 `passes` 字段）。
- coding agent 每次应先 **校准现场**（目录、日志、feature列表、git），再启动服务做基础冒烟，最后才开发新功能。
- 工具链限制会形成「锯齿边界」（例如 Puppeteer 看不到原生 `alert`），需要 harness 侧规避或改写 UI。

## Key quotes

> The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic — C compiler]] — 另一类长程并行 harness
- [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]] — feedforward/feedback 控制视角可映射到 feature列表 + 测试

## Contradictions

- 与「多智能体专职 QA一定更好」的直觉相反：文中引用社区经验提示 **盲目加 QA agent可能适得其反**（更关键的是主循环内的验证与工具设计）。
