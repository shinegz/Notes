---
title: "OpenAI Prompt Engineering Best Practices (Help Center)"
type: source
tags: [prompt-engineering, openai, best-practices]
last_updated: 2026-05-06
source_file: raw/ai-fundamentals/articles/openai-prompt-guidance.md
source_url: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
---

## Summary

OpenAI Help Center 版 Prompt Engineering 实操指南，核心主张：用最新模型、指令放开头、分隔指令与上下文、具体描述期望输出、从 zero-shot 渐进到 few-shot 再到 fine-tune。

## Key Claims

- **使用最新模型**：新模型通常更容易做好 Prompt Engineering，推理模型与 GPT 模型的 Prompt 策略有差异。
- **指令放开头 + 分隔符**：用 `###` 或 `"""` 分隔指令和上下文，避免模型混淆指令与数据。
- **具体描述输出**：对上下文、结果、长度、格式、风格给出明确要求。模糊描述（"fairly short"）不如精确描述（"3 to 5 sentence paragraph"）。
- **用示例展示格式**：比纯文字描述格式更有效，也便于程序化解析输出。Show and tell > just tell。
- **渐进策略**：Zero-shot → Few-shot → Fine-tune。先不加示例尝试，不行则加 2-3 个示例，仍不行则考虑 fine-tune。
- **说「要做什么」而非「不要做什么」**：反面指令（"DO NOT ASK USERNAME"）不如正面引导（"refer the user to help article"）。
- **代码生成用前导词**：`import` 引导 Python，`SELECT` 引导 SQL，利用模型的续写倾向。
- **参数调优**：temperature=0 适合事实性任务；max_completion_tokens 是硬截断而非长度控制；stop sequences 可提前终止生成。

## Connections

- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — 更详细的官方指南（platform.openai.com 版本）
- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 核心概念页
- [[ai-fundamentals/sources/anthropic-context-engineering|Anthropic Context Engineering]] — 从单次 Prompt 写法到系统级上下文编排的演进
