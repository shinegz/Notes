---
title: "Building a C compiler with a team of parallel Claudes"
type: source
tags: [harness-engineering, agent, multi-agent, testing]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/anthropic-building-c-compiler.md
source_url: https://www.anthropic.com/engineering/building-c-compiler
---

## Summary

Nicholas Carlini 记录用 **并行 Claude agent 团队**在长时间跨度内构建可编译 Linux 内核的 C 编译器实验，重点不是编译器本身，而是 **长程自主团队的 harness 设计**：用简单循环持续拉起会话、用文件锁在共享仓库上分配任务、把大部分精力投入测试/反馈/环境，让模型在人类不在场时仍能判断进度。文中强调 **验证器必须高质量**（否则模型会优化错目标）、测试输出要 **对模型友好**（避免上下文污染、提供可 grep 的错误行）、并行要匹配任务结构（Linux 内核单巨任务需要 GCC oracle 才能拆分并行）。

## Key claims

- 「Agent teams」通过并行与分工扩展自主开发上限，但依赖 **可执行的进度信号**而不是人类随时在线。
- 无限循环 +明确提示可以把「继续推进直到满足条件」外化为运行约束（也有实操风险：模型可能误杀循环进程）。
- **任务锁文件 + git同步** 是朴素的并行协调机制；合并冲突频繁但可被模型处理。
- 测试与 harness 设计要 **站在模型视角**：日志摘要、ERROR 行规范、时间盲导致的抽样测试（`--fast`）等。
- 多角色 agent（去重、性能、文档、结构 critique）可把「人类团队的分工」部分外化。

## Key quotes

> Most of my effort went into designing the environment around Claude—the tests, the environment, the feedback—so that it could orient itself without me.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] — 另一个长程 harness 方向（initializer / incremental）
- [[agent/harness-engineering/sources/philschmid-agent-harness-2026|Phil Schmid 2026]] —评测与长程耐久性动机

## Contradictions

- 与「完全无人监督即可安全上线」的想象相反：作者明确表达 **自主系统风险**（测试绿了也不等于真完成），与真实渗透测试经验带来的不安。
