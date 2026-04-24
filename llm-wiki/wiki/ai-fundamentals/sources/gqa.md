---
title: "GQA: Grouped Query Attention"
type: source
tags: [gqa, efficiency, attention, inference]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/gqa.pdf
source_url: https://arxiv.org/abs/2305.13245
---

## Summary

Ainslie et al. propose **Grouped Query Attention (GQA)**—a variant of multi-head attention with fewer key/value heads than query heads. GQA reduces memory bandwidth during inference while maintaining quality close to MHA.

## Key Claims

- **Fewer KV heads**: GQA uses N_kv < N_q key/value heads
- **Quality close to MHA**: Better than MQA with similar inference speed
- **Faster inference**: Reduces memory bandwidth requirements
- Used in LLaMA 2 and many modern LLMs

## Attention Variants

| Variant | Query Heads | Key Heads | Value Heads |
|---------|-------------|-----------|-------------|
| MHA | N | N | N |
| MQA | N | 1 | 1 |
| GQA | N | G (1 < G < N) | G |

## Connections

- [[ai-fundamentals/sources/rope|RoPE]] — Often combined with GQA
- [[ai-fundamentals/sources/flash-attention|Flash Attention]] — Often combined with GQA
- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — Variant of attention
