---
title: "Scaling Laws for Neural Language Models"
type: source
tags: [scaling-laws, kaplan, compute-optimal, training-dynamics]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/scaling-laws-kaplan.pdf
---

# Scaling Laws for Neural Language Models

**Jared Kaplan, Jeff McFee, Ben Mann, Henrik Milczarek, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei**  
*OpenAI*

## Abstract

We study empirical scaling laws for language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. We also describe the compute-optimal allocation of training compute across model size and dataset size.

## Key Contributions

- **Power-law scaling**: Model loss scales as L(N) ∝ N^(-α) where α ≈ 0.076
- **Compute-optimal training**: Larger models are more efficient than smaller models trained longer
- **Optimal batch size**: Scales roughly proportionally to learning rate with compute
- **Critical insight**: For every 10x increase in compute, model size should increase 5x

## Scaling Laws

| Resource | Scaling Exponent |
|----------|-----------------|
| Model size (N) | L(N) ∝ N^(-0.076) |
| Dataset size (D) | L(D) ∝ D^(-0.095) |
| Compute (C) | L(C) ∝ C^(-0.050) |

## Compute-Optimal Allocation

| Compute Budget | Optimal Model Size | Optimal Dataset Size |
|----------------|-------------------|---------------------|
| 10^18 FLOPs | 85M | 22B tokens |
| 10^20 FLOPs | 2.7B | 283B tokens |
| 10^22 FLOPs | 85B | 3.7T tokens |

## Connections

- [[gpt3-language-models-few-shot|GPT-3]] — GPT-3 follows scaling laws for model size selection
