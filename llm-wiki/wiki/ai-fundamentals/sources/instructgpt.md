---
title: "Training Language Models to Follow Instructions with Human Feedback (InstructGPT)"
type: source
tags: [instructgpt, rlhf, alignment, openai]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/instructgpt.pdf
source_url: https://arxiv.org/abs/2203.02155
---

## Summary

Ouyang et al. introduce **InstructGPT** (also known as GPT-3.5), which uses RLHF to align language models with human preferences. The three-step process—SFT, Reward Model, PPO—becomes the standard alignment pipeline for modern LLMs.

## Key Claims

- **RLHF pipeline**: SFT → Reward Model → PPO optimization
- Dramatically improves alignment on human preferences vs. pre-training alone
- Smaller models fine-tuned with RLHF outperform much larger pre-trained models
- Reduces hallucinations and harmful outputs
- Misaligned models can still be useful but not what users want

## RLHF Pipeline

| Step | Description |
|------|-------------|
| 1. SFT | Supervised fine-tuning on human demonstrations |
| 2. Reward Model | Train model to predict human preference |
| 3. PPO | Fine-tune SFT model with RL to maximize reward |

## Connections

- [[ai-fundamentals/sources/rlhf-from-feedback|RLHF from Human Feedback]] — Foundation paper
- [[ai-fundamentals/sources/dpo|Direct Preference Optimization]] — Simplifies RLHF
- [[ai-fundamentals/concepts/alignment|Alignment]] — Concept page
