---
title: "Transformer Taxonomy: A Literature Survey"
type: source
tags: [transformer, taxonomy, survey, architecture]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/articles/transformer-taxonomy-the-last-lit-review.md
source_url: https://arxiv.org/abs/2304.13712
---

## Summary

A survey paper categorizing the Transformer architecture and its variants across encoding-only (BERT), decoding-only (GPT), encoder-decoder (T5), and prefix LM variants. Reviews efficiency improvements, attention variants, and application-specific adaptations.

## Key Claims

- **Taxonomy of Transformers**: BERT (enc), GPT (dec), T5 (enc-dec), Prefix LM
- **Efficiency categories**: Quantization, pruning, knowledge distillation, efficient architectures
- **Attention variants**: Sparse, linear, Flash, Grouped Query
- **Application adaptations**: Vision, speech, multimodal

## Transformer Variants

| Type | Examples | Architecture |
|------|----------|--------------|
| Encoder-only | BERT, RoBERTa | Bidirectional attention |
| Decoder-only | GPT, PaLM | Causal/masked attention |
| Encoder-Decoder | T5, BART | Full attention |
| Prefix LM | UniLM | Flexible masking |

## Connections

- [[ai-fundamentals/concepts/transformer|Transformer]] — Concept page
- [[ai-fundamentals/sources/bert-pre-training|BERT]] — Encoder-only example
- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — Decoder-only example
