---
title: "LoRA: Low-Rank Adaptation of Large Language Models"
type: source
tags: [lora, fine-tuning, efficiency, parameter-efficient]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/lora.pdf
source_url: https://arxiv.org/abs/2106.09685
---

## Summary

Hu et al. propose **LoRA**—a parameter-efficient fine-tuning method that adds low-rank update matrices to frozen pre-trained weights. LoRA reduces trainable parameters by 10,000x with comparable performance to full fine-tuning.

## Key Claims

- **Low-rank updates**: Only train A and B matrices, not full weights
- **10,000x fewer parameters**: Trainable: 0.1% of original
- **No inference latency**: Merge weights after training
- **Works with frozen pre-trained weights**: Only updates residual

## LoRA Formula

```
W = W₀ + BA
where:
  W₀ = frozen pre-trained weights
  B = trainable (d × r)
  A = trainable (r × k)
  r = rank (typically 4-64)
```

## Connections

- [[ai-fundamentals/concepts/fine-tuning|Fine-tuning]] — Parameter-efficient variant
