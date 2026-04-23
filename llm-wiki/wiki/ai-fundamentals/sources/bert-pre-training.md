---
title: "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
type: source
tags: [bert, transformer, nlp, pre-training]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/bert-pre-training.pdf
---

# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

**Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova**  
*Google AI Language*

## Abstract

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer for state-of-the-art performance on a wide range of NLP tasks.

## Key Contributions

- **Bidirectional pre-training**: First system to pre-train a deep bidirectional Transformer encoder
- **Masked Language Model (MLM)**: Randomly masks some tokens and predicts them based on context
- **Next Sentence Prediction (NSP)**: Pre-training task to understand sentence relationships
- **State-of-the-art**: Achieves new results on 11 NLP benchmarks

## Architecture

| Component | Description |
|-----------|-------------|
| Encoder | Bidirectional Transformer encoder (12 or 24 layers) |
| Pre-training | Masked LM + Next Sentence Prediction |
| Fine-tuning | Add task-specific output layer |

## Results

| Task | Model | Score |
|------|-------|-------|
| SQuAD 1.1 | BERT (ensemble) | **93.2 F1** |
| SQuAD 2.0 | BERT (ensemble) | **83.1 F1** |
| MultiNLI | BERT | **86.6%** |
| SST-2 | BERT | **93.5%** |

## Connections

- [[attention-is-all-you-need]] — BERT uses Transformer encoder architecture
