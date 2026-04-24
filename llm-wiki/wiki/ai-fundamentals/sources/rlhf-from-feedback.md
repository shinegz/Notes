---
title: "RLHF: Learning to Summarize from Human Feedback"
type: source
tags: [rlhf, alignment, summarization, openai]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/rlhf-from-feedback.pdf
source_url: https://arxiv.org/abs/2009.01325
---

## Summary

Stiennon et al. demonstrate that training a model to summarize text using human feedback significantly improves quality over models trained purely on reference summaries. This paper establishes RLHF as a viable approach for aligning language models with human preferences.

## Key Claims

- **Human feedback > Reference summaries**: Models trained with human preferences outperform those trained on curated references
- **Reward model**: Trained to predict human preferences, enables scalable feedback
- **Transfer to non-supervised objectives**: Improves perplexity on held-out text
- Foundation for InstructGPT and modern alignment techniques

## Connections

- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — Extends RLHF with PPO
- [[ai-fundamentals/sources/dpo|Direct Preference Optimization]] — Simplifies the pipeline
- [[ai-fundamentals/concepts/alignment|Alignment]] — Concept page
