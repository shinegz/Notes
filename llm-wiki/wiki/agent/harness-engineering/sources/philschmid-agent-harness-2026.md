---
title: "The importance of Agent Harness in 2026"
type: source
tags: [harness-engineering, agent, benchmarks]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/philschmid-agent-harness-2026.md
source_url: https://www.philschmid.de/agent-harness-2026
---

## Summary

Phil Schmid 从 **长程可靠性** 与评测角度论证：静态榜上的微小差距不足以描述「几十上百步工具调用后是否漂移」；**Agent harness** 被比作操作系统（模型如 CPU、上下文如 RAM），在框架之上提供带默认能力的运行时。文章讨论 benchmark 从单轮输出转向系统评测后的缺口，并提出 harness 在 **对齐真实用户验证**、**释放模型潜力**、以及用可记录轨迹做 **hill-climbing** 三方面的作用；最后以「Bitter Lesson」提醒 harness 需要保持轻量、可替换，避免把控制流写死。

## Key claims

- leaderboard 差距缩小可能是错觉：长任务里 **耐久性 / instruction following** 才放大差异。
- harness 高于「框架积木」：带预设提示、工具习惯用法、hooks、规划/文件系统/子智能体等「batteries included」能力。
- 新 benchmark 需要测量 **第 50、100 次工具调用后** 的行为；否则与真实多天长任务脱节。
- 验证不对称性：系统越容易验证，迭代越快；harness 把模糊流程变成可记录、可评分的结构化数据。
- 面向未来：训练与推理环境收敛；**轨迹数据**（失败发生在第几步）本身就是下一代改进燃料。

## Key quotes

> The Agent Harness is the Operating System: It curates the context, handles the "boot" sequence (prompts, hooks), and provides standard drivers (tool handling).

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]] — 对 harness 组分的工程化展开
- [[agent/harness-engineering/sources/anthropic-building-c-compiler|Anthropic — C compiler]] — 长程并行与评测/验证压力测试

## Contradictions

- 「Start Simple / Build to Delete」与「企业需要重流程护栏」之间存在张力：本文偏向 **轻量可演进**，但具体团队可能短期更需要重护栏（取决于风险与阶段）。
