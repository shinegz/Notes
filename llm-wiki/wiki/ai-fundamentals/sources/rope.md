---
title: "RoPE: Rotary Position Embedding"
type: source
tags: [rope, position-encoding, attention, rotary]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/rope.pdf
source_url: https://arxiv.org/abs/2104.09864
---

## Summary

Su et al. introduce **Rotary Position Embedding (RoPE)**—a position encoding method that encodes position information through rotation matrices. RoPE naturally captures relative position and has become dominant in modern LLMs (LLaMA, PaLM, etc.).

## Key Claims

- **Rotary encoding**: Uses rotation matrices to encode position
- **Relative position**: Naturally captures relative position dependencies
- **Decay-free**: No attention decay over distance (unlike some linear biases)
- **Widely adopted**: Standard in LLaMA, PaLM, Falcon, and many others

## Connections

- [[ai-fundamentals/sources/gqa|GQA]] — Often combined with RoPE
- [[ai-fundamentals/concepts/transformer|Transformer]] — Position encoding variant
