---
title: "Training Compute-Optimal Large Language Models (Chinchilla)"
type: source
tags: [chinchilla, scaling-laws, compute-optimal, deepmind]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/chinchilla.pdf
source_url: https://arxiv.org/abs/2203.15556
---

## Summary

Hoffmann et al. challenge Kaplan's scaling recommendations with **Chinchilla**—a model trained with compute-optimal token scaling. While Kaplan suggested 10x compute → 5x model size, Chinchilla finds that model and data should scale **equally**: for 10x compute, use 10x more of both.

## Key Claims

- **Equal scaling**: Model size and training tokens should scale together
- **Kaplan's error**: Underestimated dataset scaling needs
- Chinchilla 70B outperforms Gopher 280B with same compute
- Revised optimal allocation: ~20 tokens per parameter

## Kaplan vs Chinchilla

| Compute Budget | Kaplan Model | Chinchilla Model | Kaplan Tokens | Chinchilla Tokens |
|---------------|-------------|-----------------|--------------|-------------------|
| 10^20 FLOPs | 2.7B | 1.4B | 283B | 14B |
| 10^22 FLOPs | 85B | 70B | 3.7T | 1.4T |

## Connections

- [[ai-fundamentals/sources/scaling-laws-kaplan|Kaplan Scaling Laws]] — Original paper that Chinchilla refines
- [[ai-fundamentals/concepts/scaling-laws|Scaling Laws]] — Concept page
