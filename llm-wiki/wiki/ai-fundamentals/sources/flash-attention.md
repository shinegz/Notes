---
title: "Flash Attention: Fast and Memory-Efficient Attention"
type: source
tags: [flash-attention, efficiency, attention, io-aware]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/flash-attention.pdf
source_url: https://arxiv.org/abs/2205.14135
---

## Summary

Dao et al. introduce **Flash Attention**—an IO-aware exact attention algorithm that computes attention faster by exploiting GPU memory hierarchy (SRAM vs HBM). Reduces memory complexity from O(N²) to O(N) and significantly speeds up training.

## Key Claims

- **IO-aware**: Minimizes HBM (high-bandwidth memory) reads/writes
- **Exact attention**: Algorithmically identical to standard attention
- **Memory efficient**: O(N) instead of O(N²) memory
- 2-4x speedup on standard attention implementations
- Enables training with longer sequences

## Key Insight

Standard attention materializes the N×N attention matrix to HBM, then reads it back. Flash Attention keeps attention in SRAM, computing in tiles to avoid the expensive HBM round-trips.

## Connections

- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — Improves attention efficiency
- [[ai-fundamentals/sources/gqa|Grouped Query Attention]] — Often combined with Flash Attention
