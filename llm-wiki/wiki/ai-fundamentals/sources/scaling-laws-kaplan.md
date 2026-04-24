---
title: "Scaling Laws for Neural Language Models"
type: source
tags: [scaling-laws, kaplan, compute-optimal, training-dynamics]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/scaling-laws-kaplan.pdf
source_url: https://arxiv.org/abs/2001.08361
---

## Summary

Kaplan et al. establish empirical **scaling laws** for language model performance: loss scales as a power-law with model size (N), dataset size (D), and compute (C). Larger models are more compute-efficient than smaller models trained longer. Critical insight: for every 10x increase in compute, model size should increase ~5x.

## Key Claims

- **Power-law scaling**: `L(N) ∝ N^(-0.076)`, `L(D) ∝ D^(-0.095)`, `L(C) ∝ C^(-0.050)`
- **Compute-optimal allocation**: Larger models are more sample-efficient
- For 10x compute: model size ↑5x, dataset size ↑2x
- Optimal batch size scales with learning rate and compute
- Performance improves predictably over 7+ orders of magnitude

## Scaling Exponents

| Resource | Exponent |
|---------|----------|
| Model size (N) | α = 0.076 |
| Dataset size (D) | α = 0.095 |
| Compute (C) | α = 0.050 |

## Connections

- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — Follows these scaling laws
- [[ai-fundamentals/sources/chinchilla|Chinchilla]] — Challenges Kaplan's allocation; suggests equal scaling
- [[ai-fundamentals/concepts/scaling-laws|Scaling Laws]] — Concept page
