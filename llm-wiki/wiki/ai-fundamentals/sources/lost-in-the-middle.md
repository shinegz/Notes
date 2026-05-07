---
title: "Lost in the Middle"
type: source
tags: [attention, long-context, position-bias, rag]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/pdfs/lost-in-the-middle.pdf
source_url: https://arxiv.org/abs/2307.03172
---

# Lost in the Middle

## Summary

LLM 对上下文中信息的使用存在显著的 U 形位置偏差：开头和结尾的信息召回率高，中间位置的信息召回率显著降低。GPT-3.5-Turbo 在信息位于中间时准确率甚至低于无上下文的闭卷基线，表明增加上下文可能反而损害性能。

## Key Claims

- **U 形性能曲线** — 在多文档 QA 和键值检索任务中，LLM 对开头（primacy bias）和结尾（recency bias）的信息处理最好，中间信息性能显著下降（20+ 百分点）
- **扩展上下文模型未必更好** — 扩展上下文版本（如 gpt-3.5-turbo-16k）在长上下文使用上与标准版本表现相近
- **编码器-解码器架构更鲁棒** — encoder-decoder 模型对信息位置变化更不敏感，但超出训练长度后仍出现 U 形曲线
- **Query-aware contextualization 有效** — 将查询放在文档前后（而非仅放在前面）可显著提升中间位置的检索性能
- **指令微调加剧位置偏差** — 非指令微调模型倾向关注近端 token（recency bias），指令微调后模型增加了对远端 token 的关注但出现 primacy bias

## Key Quotes

> "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts" — 核心发现

## Connections

- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — U 形偏差是注意力权重分布的宏观表现
- [[ai-fundamentals/concepts/context-window|Context Window]] — 有效上下文远小于声称上下文的实证支撑
- [[ai-fundamentals/concepts/context-engineering|Context Engineering]] — 位置偏差是上下文编排的核心约束
