---
title: "Prompt Engineering From First Principles"
type: source
tags: [prompt-engineering, autoregressive, attention, first-principles]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/articles/prompt-from-first-principles-dev.md
source_url: https://dev.to/programmerraja/prompt-engineering-from-first-principles-the-mechanics-they-dont-teach-you-part-1-12nb
---

# Prompt Engineering From First Principles

## Summary

从 LLM 运行机制出发解释 Prompt Engineering：LLM 是概率引擎而非推理机器，Prompt 的作用是塑造概率分布。通过理解 Tokenization → Embedding → Transformer → 概率预测 → 采样的完整流程，推导出 Prompt 技巧有效的底层原因。

## Key Claims

- **LLM 是概率引擎** — LLM 只做一件事：预测下一个 token 的概率分布，不是在"思考"
- **Prompt 塑造概率分布** — 换几个词、重排指令、加示例，不同 token 变得更可能，不同 token 意味着不同输出
- **Temperature 控制分布尖锐度** — 低温度集中概率在 top 选择（确定性），高温度展平分布（创造性）
- **Top-P 截断低概率尾部** — 只考虑累积概率达到阈值的 token，防止选择极低概率的无意义 token
- **预训练 vs 后训练** — 预训练学会统计模式（续写），SFT+RLHF 学会助手行为（回答），后者塑造了"哪些预测有高概率"

## Connections

- [[ai-fundamentals/syntheses/token-lifecycle|一个 Token 的一生]] — 更详细的 LLM 运行流程
- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 核心策略与原则
- [[ai-fundamentals/concepts/alignment|Alignment]] — SFT + RLHF 的完整解释
