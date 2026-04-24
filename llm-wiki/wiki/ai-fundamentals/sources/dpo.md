---
title: "Direct Preference Optimization (DPO)"
type: source
tags: [dpo, alignment, fine-tuning, preference-learning]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/dpo.pdf
source_url: https://arxiv.org/abs/2305.18290
---

## Summary

Rafailov et al. propose **DPO**—a simpler alternative to RLHF that directly fine-tunes language models on preference data without training a separate reward model or running reinforcement learning. DPO achieves comparable or better results with simpler training.

## Key Claims

- **No reward model needed**: Directly optimizes against preference data
- **No RL**: Eliminates PPO, simplifying training
- Equivalent to or better than RLHF on sentiment, summarization, and dialogue
- More stable and easier to implement

## DPO vs RLHF

| Aspect | RLHF | DPO |
|--------|------|-----|
| Reward Model | Required | Not needed |
| RL Training | PPO | Implicit in loss |
| Complexity | High | Low |
| Stability | Sensitive | More stable |

## Connections

- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — Standard RLHF pipeline
- [[ai-fundamentals/sources/rlhf-from-feedback|RLHF]] — Foundation paper
- [[ai-fundamentals/concepts/alignment|Alignment]] — Concept page
