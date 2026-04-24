---
title: "Language Models are Few-Shot Learners (GPT-3)"
type: source
tags: [gpt3, few-shot, in-context-learning, nlp]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/gpt3-language-models-few-shot.pdf
source_url: https://arxiv.org/abs/2005.14165
---

## Summary

Brown et al. present **GPT-3**, a 175-billion-parameter language model that achieves competitive few-shot performance across diverse NLP tasks without task-specific fine-tuning. The paper demonstrates that scaling up language models greatly improves task-agnostic, few-shot performance.

## Key Claims

- **175B parameters** — largest language model at publication time
- **Few-shot learning**: competitive results without fine-tuning
- **In-context learning**: learns from demonstrations in the prompt
- Broad capabilities: translation, Q&A, reasoning, domain adaptation
- Power-law scaling continues up to 175B

## Model Sizes

| Model | Parameters |
|-------|------------|
| GPT-3 Small | 125M |
| GPT-3 XL | 1.3B |
| GPT-3 175B | **175B** |

## Few-Shot Results

| Task | Fine-tuned SOTA | GPT-3 Few-shot |
|------|-----------------|----------------|
| SuperGLUE | 89.8 | **90.3** |
| TriviaQA | 68.9 | **71.2** |
| LAMBADA | 68.0 | **76.2** |

## Connections

- [[ai-fundamentals/sources/attention-is-all-you-need|Attention Is All You Need]] — Transformer decoder architecture
- [[ai-fundamentals/sources/scaling-laws-kaplan|Scaling Laws]] — Follows scaling laws
- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — Fine-tuned with RLHF
