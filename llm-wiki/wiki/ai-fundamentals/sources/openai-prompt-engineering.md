---
title: "Prompt Engineering (OpenAI Guide)"
type: source
tags: [prompt-engineering, openai, best-practices]
sources: []
last_updated: 2026-04-26
source_file: raw/ai-fundamentals/articles/openai-prompt-engineering.md
source_url: https://platform.openai.com/docs/guides/prompt-engineering
---

## Summary

OpenAI 官方 Prompt Engineering 指南，总结了在 API 中使用 LLM 获取更好结果的核心策略：写清楚指令、给参考文本、拆解复杂任务、给模型「思考」时间。

## Key Strategies

### 1. Write Clear Instructions（写清楚指令）

| 策略 | 示例 |
|------|------|
| 在查询中包含详细信息 | "Explain why the sky is blue" 而非 "Explain sky" |
| 使用分隔符 | 使用分隔符（如 `---`）分隔不同部分 |
| 指定输出格式 | "Respond in JSON format with fields: name, age" |
| 举例子 | "Classify the sentiment as positive/neutral/negative. Example: 'I love it' → positive" |

### 2. Give Reference Text（给参考文本）

让模型在回答时参考提供的文本，减少幻觉：
- "Based on the following passage, answer the question..."
- 适用于：总结、问答、信息提取

### 3. Split Complex Tasks（拆解复杂任务）

把复杂任务拆成简单步骤，而不是让模型一次完成：
- 管道式处理：先提取实体，再分类，再生成
- 适用于：多步骤分析、内容生成管道

### 4. Give Model Time to "Think"（给模型思考时间）

让模型在给出答案前先推理：
- 链式思考（Chain-of-Thought）："Think step by step before answering"
- 先列出步骤，再给出结论

### 5. Other Tactics（其他技巧）

| 策略 | 说明 |
|------|------|
| Use specific descriptors | "Write a 2-paragraph summary" 而非 "Write a summary" |
| Minimize "filler" language | 避免 "Certainly! Here's..." 直接给结论 |
| Order of inputs matters | 开头和结尾的信息权重更高 |
| Pre-commit to an output schema | 用 JSON schema 约束输出结构 |

## Connections

- [[ai-fundamentals/concepts/chain-of-thought-react|Chain-of-Thought]] — "给模型思考时间" 的具体实现
- [[ai-fundamentals/concepts/llm-agents|LLM Agents]] — Agent 使用 Prompt Engineering 驱动 Tool Use
