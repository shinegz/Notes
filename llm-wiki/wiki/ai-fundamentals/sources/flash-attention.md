---
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
type: source
tags: [flash-attention, attention, optimization, efficiency]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/flash-attention.pdf
---

# FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

**Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré**  
*Stanford University, UC Berkeley*

## Abstract

Attention is a core primitive in neural network architectures, but the standard attention mechanism has quadratic time and memory complexity in the sequence length. We propose FlashAttention, an exact attention algorithm that computes the attention output faster and with less memory by exploiting the memory hierarchy of modern hardware (GPU). Our algorithm achieves 2-4x speedup over standard attention implementations and up to 10-16x memory reduction.

## Key Contributions

- **IO-aware algorithm**: Exploits GPU memory hierarchy (SRAM vs HBM)
- **Exact attention**: Mathematically equivalent to standard attention
- **2-4x faster**: Significant speedup on standard benchmarks
- **10-16x less memory**: Enables attention on very long sequences

## Memory Hierarchy

| Level | Size | Bandwidth |
|-------|------|-----------|
| HBM (GPU memory) | ~40GB | ~1 TB/s |
| L2 cache | ~6MB | ~4 TB/s |
| SRAM (per thread block) | ~128KB | ~19 TB/s |

FlashAttention keeps data in fast SRAM and only writes to slow HBM when necessary.

## Algorithm Overview

```
1. Divide K, V into blocks
2. For each block of Q:
   - Load Q block to SRAM
   - Compute attention with K, V blocks (tiling)
   - Update output in HBM
3. Return final attention output
```

## Connections

- [[attention-is-all-you-need]] — Flash Attention implements exact Transformer attention
