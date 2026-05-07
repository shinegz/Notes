---
title: "LongLLMLingua"
type: source
tags: [prompt-compression, long-context, position-bias, efficiency]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/pdfs/longllmlingua.pdf
source_url: https://aclanthology.org/2024.acl-long.91.pdf
---

# LongLLMLingua

## Summary

面向长上下文场景的 Prompt 压缩方法，通过问题感知的粗到细压缩提升关键信息密度，同时降低成本和延迟。在 NaturalQuestions 上用 GPT-3.5-Turbo 实现了 4x 压缩下性能提升 21.4%。

## Key Claims

- **问题感知压缩** — 利用小语言模型捕获问题相关的关键信息分布，压缩时保留与问题相关的高信息量 token
- **文档重排序** — 将压缩后的关键信息重新排列到上下文开头和结尾，缓解 Lost in the Middle 位置偏差
- **动态压缩比** — 根据文档与问题的相关性动态调整压缩比率，相关度高的文档压缩少
- **后压缩恢复策略** — 压缩后补充恢复指令，帮助 LLM 适应压缩后的输入格式
- **成本与性能双赢** — GPT-3.5-Turbo 上 4x 压缩 + 21.4% 性能提升；LooGLE 上 94% 成本降低；10k token 压缩 2x-6x 可加速 1.4x-2.6x

## Connections

- [[ai-fundamentals/sources/lost-in-the-middle|Lost in the Middle]] — LongLLMLingua 的文档重排序策略直接针对 U 形位置偏差
- [[ai-fundamentals/concepts/context-engineering|Context Engineering]] — 压缩是 Context Engineering 的核心技术
- [[ai-fundamentals/concepts/context-window|Context Window]] — 有效上下文利用的工程化方案
