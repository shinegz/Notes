---
title: "工程技术：在智能体优先的世界中利用 Codex"
type: source
tags: [harness-engineering, agent, codex]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/openai-harness-engineering-zh.md
source_url: https://openai.com/zh-Hans-CN/index/harness-engineering/
---

## Summary

OpenAI 团队记录一次刻意约束的实验：**仓库内几乎不出现人类手写代码**，由 Codex 生成从业务代码到测试、CI、文档与可观测性的全栈；人类职责转向 **设计环境、明确意图、建立反馈回路**。文章强调把仓库做成 **记录系统**：短 `AGENTS.md` 当「地图」，结构化 `docs/` 渐进披露；用自定义 linter/结构测试机械执行分层架构；让 UI/日志/指标对 agent **可读可查询**；并通过「doc-gardening」与 **垃圾回收式**后台任务抑制长期漂移。

## Key claims

- 瓶颈经常不是模型写不出来，而是 **环境规范不足**（缺工具、缺抽象、缺可验证约束）。
- PR 推进可以高度依赖 **agent-on-agent review** 的循环（文中以 Ralph loop 类比），人类更多在做仲裁与产品判断。
- 「地图而非百科全书」：`AGENTS.md` 过长会挤占上下文、难维护、难机械验证；应用渐进披露把深内容放 `docs/`。
- **严格分层 + 机械 enforcement** 在 agent 场景是加速器；linter 错误信息可直接承载「如何修复」的教学。
- 吞吐提高后，合并哲学可能改变：**等待人类注意力的成本**高于自动纠错成本时需要不同门控策略（作者也提示这在低吞吐团队不适用）。
- 漂移与「垃圾回收」任务：用周期性扫描/重构 PR 抑制长期不一致，把已达成共识的规则持续灌回仓库。

## Key quotes

> 人类掌舵。智能体执行。

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/ignorance-emerging-harness-engineering|Ignorance.ai playbook]] — 引用该案例做行业收敛
- [[agent/harness-engineering/sources/martin-fowler-harness-engineering|Martin Fowler]] — feedforward/feedback 与 linter 作为传感器的框架化表述

## Contradictions

- 与「合并必须传统严格门控」流程可能冲突：文中有意描述一种 **高吞吐、低等待** 的权衡；是否可复制取决于组织风险承受度与验证强度。
