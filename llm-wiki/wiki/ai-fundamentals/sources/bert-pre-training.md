---
title: "BERT: Pre-training of Deep Bidirectional Transformers"
type: source
tags: [bert, pre-training, masked-lm, nlp]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/bert-pre-training.pdf
source_url: https://arxiv.org/abs/1810.04805
---

## Summary

Devlin et al. introduce **BERT**—a method for pre-training bidirectional language representations from unlabeled text. BERT uses Masked Language Modeling (MLM) and Next Sentence Prediction (NSP) to achieve state-of-the-art results on NLP benchmarks.

## Key Claims

- **Bidirectional pre-training**: Unlike GPT's unidirectional approach
- **Masked LM**: 15% tokens masked, predict from context
- **Next Sentence Prediction**: Understanding sentence relationships
- **Fine-tuning paradigm**: Pre-train once, fine-tune for any task

## Pre-training Tasks

| Task | Description |
|------|-------------|
| MLM | Mask 15% tokens, predict from both left and right context |
| NSP | Predict if sentence B follows sentence A |

## Connections

- [[ai-fundamentals/sources/attention-is-all-you-need|Attention Is All You Need]] — Transformer encoder architecture
- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — Decoder-only alternative
