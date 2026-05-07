---
title: "Context Dilution: When More Tokens Hurt AI"
type: source
tags: [context-dilution, attention, long-context, rag]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/articles/context-dilution.md
source_url: https://diffray.ai/blog/context-dilution/
---

# Context Dilution: When More Tokens Hurt AI

## Summary

综合多篇研究论文（Stanford/Meta、MIT/Meta、Google、NVIDIA 等），揭示 LLM 在长上下文下的系统性性能退化：注意力零和、Attention Sinks、位置偏差和无关信息干扰共同导致"context dilution"。即使 100% 完美检索，性能仍随上下文长度退化 13.9%-85%。

## Key Claims

- **Context dilution 是架构约束** — Softmax 归一化使注意力零和，每个额外 token 都在争夺注意力份额
- **Attention Sinks** — 初始 token 接收不成比例的高注意力分数，成为"倾倒场"
- **有效上下文远小于声称** — GPT-4 声称 128K 但有效约 64K；Mistral 7B 声称 32K 但有效仅 16K
- **无关信息主动损害性能** — Google ICML 2023：数学问题中加入主题相关但无关的信息，准确率显著下降
- **上下文长度本身就有认知税** — 即使无关 token 替换为空白，退化仍然存在
- **策展上下文优于堆量** — Anthropic 的 Contextual Retrieval：50-100 token 上下文元数据减少 49% 检索失败；加 reranking 减少 67%

## Connections

- [[ai-fundamentals/sources/lost-in-the-middle|Lost in the Middle]] — 位置偏差的原始论文
- [[ai-fundamentals/sources/longllmlingua|LongLLMLingua]] — 压缩方案
- [[ai-fundamentals/concepts/context-engineering|Context Engineering]] — 策展上下文的核心实践
