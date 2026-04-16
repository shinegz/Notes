---
title: "What is an agent harness?"
type: source
tags: [harness-engineering, agent, glossary]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/parallel-what-is-an-agent-harness.md
source_url: https://parallel.ai/articles/what-is-an-agent-harness
---

## Summary

Parallel 的长文把 **agent harness** 定义为包在 LLM 之外的软件基础设施：负责意图捕获、规格化、执行、验证与持久化等「生命周期」能力，让模型能调用工具、跨越会话保持状态，并把多步工作做成可审计的流程。文章解释 harness 为何在长程、工具型任务中成为刚需，并给出典型工作流（编排、工具执行、上下文编译、验证迭代、会话交接），同时区分 **framework / orchestrator / harness** 与软件工程里「test harness」等易混术语。

## Key claims

- 真实效果往往更多来自 **编排 + harness** 而非模型尺寸的边际提升。
- 典型缺口包括：上下文与记忆、工具执行、结构化规划与验收、以及长程状态与 handoff。
- 成熟 harness 常见模块：工具集成、记忆与状态、上下文工程、规划分解、验证与护栏、可插拔扩展。
- harness 与模型解耦：可通过更换模型保留工具/记忆/流程，从而在不重训的前提下扩展能力。

## Key quotes

> In simple terms, an agent harness is the software infrastructure that wraps around a large language model (LLM) or AI agent, handling everything except the model itself.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/langchain-anatomy-of-an-agent-harness|LangChain — Anatomy]] — 更偏实现者视角的组件清单
- [[agent/harness-engineering/sources/anthropic-effective-harnesses-long-running-agents|Anthropic — Long-running]] — harness 在长程任务中的落点示例

## Contradictions

- （暂无强矛盾；本文偏科普与术语梳理，与行业文在 emphasis 上互补。）
