---
title: "My AI Adoption Journey — Step 5: Engineer the Harness"
type: source
tags: [harness-engineering, agent]
last_updated: 2026-04-14
source_file: raw/agent/harness-engineering/articles/mitchellh-ai-adoption-journey-step-5-harness.md
source_url: https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness
---

## Summary

Mitchell Hashimoto 在个人 adoption 路径的 **Step 5** 里给出一句可操作的定义：**harness engineering** 是每次发现 agent 犯错，就工程化一层机制让它以后不再重复（或让它能自动验证「做对了」）。实现上主要是两条：**更新 AGENTS.md（或等价入口文档）**记录失败模式；以及补齐 **可编程工具**（截图、筛选测试等）把错误检测变成快速反馈。全文（见 canonical URL）还强调从 chatbot 转向 agent、用验证闭环提升效率等前置步骤。

## Key claims

- 让 agent 第一次就更接近正确，最稳的路径是给它 **高质量、快速的「你错了」信号**。
- 「.harness engineering」不必是行业统一术语；关键是行为模式：**失败 → 固化约束/工具**。
- Ghostty 的 `AGENTS.md` 被当作例子：**一行对应一次真实坏行为** 的修复记录。
- 与 Step 6「尽量总有 agent 在跑」并行：harness 质量决定后台委托是否划算。

## Key quotes

> It is the idea that anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

## Connections

- [[agent/harness-engineering/concepts/HarnessEngineering|Harness Engineering]]
- [[agent/harness-engineering/sources/humanlayer-skill-issue-harness-engineering|HumanLayer]] — 引用该定义并扩展到 MCP/Skills/hooks
- [[agent/harness-engineering/sources/openai-harness-engineering-zh|OpenAI 中文]] — 将「地图式 AGENTS.md + docs」推到仓库治理层面

## Contradictions

- （暂无；本文是定义级短文段落，细节以 canonical 全文为准。）
