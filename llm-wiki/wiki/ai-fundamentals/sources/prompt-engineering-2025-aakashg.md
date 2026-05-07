---
title: "Prompt Engineering in 2025 (Aakash Gupta × OpenAI PM)"
type: source
tags: [prompt-engineering, context-engineering, product, economics]
last_updated: 2026-05-06
source_file: raw/ai-fundamentals/articles/prompt-engineering-2025-aakashg.md
source_url: https://www.news.aakashg.com/p/prompt-engineering
---

## Summary

对产品而言，Prompt Engineering 不是可选项而是决定成败的关键。Bolt（$50M ARR/5 月）和 Cluely（$6M ARR/2 月）的系统提示是其核心竞争壁垒。Prompt Engineering 是 Context Engineering 的一部分，通常承担 85% 的工作量。

## Key Claims

- **个人用 vs 产品化的差距**：日常对话中 Prompt 几乎不需要工程化，但产品级 AI 应用的质量差距往往就来自 Prompt 的差异。
- **系统提示 = 核心竞争壁垒**：Bolt 和 Cluely 的系统提示展示出共同模式——代码化结构（方括号）、Always/Never 列表、显示指令、If/then 边界处理。这些不是锦上添花，而是产品能否成功的关键因素。
- **Prompt 是 Context Engineering 的子集**：Context Engineering 是更大的框架，但 Prompt Engineering 通常承担 85% 的工作量。
- **成本经济学**：详细 Prompt（如 Bolt，2500 tokens）日均成本 $3000；精简结构化 Prompt（如 Cluely，212 tokens + few-shot）日均成本 $706——76% 的成本削减。更短的 Prompt 还意味着更低的输出方差和更低的延迟。
- **先爬质量山丘，再降成本**：业界最佳实践是先用详细 Prompt 把质量做到位，再逐步压缩成本。
- **PM 必须掌握 Prompt Engineering**：PM 最理解用户意图、能更快迭代、Prompt 中的每条指令都是产品决策、能识别出「用户投诉其实是 Prompt 优化的机会」。

## Connections

- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — 互补视角：Anthropic 从工程原理出发，本文从产品实践出发
- [[ai-fundamentals/sources/prompt-engineering-frameworks-parloa|Prompt Engineering Frameworks]] — 框架化方法论
- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 核心概念
