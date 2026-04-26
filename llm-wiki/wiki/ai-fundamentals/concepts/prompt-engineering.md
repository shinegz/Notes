---
title: "Prompt Engineering"
type: concept
tags: [prompt-engineering, llm, instruction]
sources:
  - ai-fundamentals/sources/openai-prompt-engineering
last_updated: 2026-04-26
---

# Prompt Engineering

**Prompt Engineering = 用精心设计的输入文本（Prompt）引导 LLM 产生期望输出。**

## 一句话理解

Prompt 是给 LLM 的「编程语言」——同样的模型，好的 Prompt 可以激发强大能力，差的 Prompt 导致幻觉或无用输出。

## 核心策略

| 策略 | 说明 | 示例 |
|------|------|------|
| **写清楚指令** | 在 Prompt 中包含所有必要细节 | "Explain why the sky is blue in 2 sentences" |
| **给参考文本** | 让模型基于提供的内容回答 | "Based on this article, summarize..." |
| **拆解复杂任务** | 多步骤代替一步到位 | 先提取实体 → 再分类 → 再生成 |
| **给模型思考时间** | 链式思考，让模型先推理再回答 | "Think step by step" |
| **指定输出格式** | 用 JSON schema 约束结构 | "Respond in JSON with fields: name, age" |

## 一句话理解进阶：CLOPE 原则

| 首字母 | 原则 | 说明 |
|--------|------|------|
| **C**lear | 清晰 | 明确说明要什么，不要什么 |
| **L**everage | 借力 | 给参考文本、举例子 |
| **O**rder | 顺序 | 重要信息放开头或结尾 |
| **P**atience | 耐心 | 让模型先推理再回答 |
| **E**xample | 示例 | Few-shot examples 比描述更有效 |

## Prompt 的进化

| 阶段 | 特点 | 示例 |
|------|------|------|
| 1. Zero-shot | 直接提问 | "翻译：Hello" |
| 2. Few-shot | 给示例 | "猫→cat，狗→dog，鸟→" |
| 3. Chain-of-Thought | 加推理链 | "Think step by step. Then answer" |
| 4. Constitutional AI | 加约束 | "遵循以下原则回答..." |
| 5. Agentic | Tool + Loop | 自动拆解任务、调用工具 |

## 为什么重要

1. **无需训练**：Prompt 可以改变模型行为，无需重新训练
2. **成本低**：相比 Fine-tuning，Prompt 的成本接近零
3. **可控性强**：通过 Prompt 可以精确控制输出格式、风格、内容
4. **模型能力边界**：很多能力需要通过 Prompt 激发，而不是自动涌现

## 与其他概念的关系

- [[ai-fundamentals/concepts/chain-of-thought-react|CoT]] — 给模型「思考时间」的具体方法
- [[ai-fundamentals/concepts/llm-agents|Agent]] — Agent 的核心能力之一是动态生成 Prompt
- [[ai-fundamentals/concepts/fine-tuning|Fine-tuning]] — 当 Prompt 无法满足需求时的替代方案

## 来源

- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — 官方最佳实践
