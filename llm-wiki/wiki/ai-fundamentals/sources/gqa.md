---
title: "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"
type: source
tags: [attention, multi-query, inference, transformer]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/gqa.pdf
---

# GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints

**Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón, Sumit Sanghai**  
*Google Research*

## Abstract

Multi-query attention (MQA), which only uses a single key-value head, drastically speeds up decoder inference. However, MQA can lead to quality degradation, and it may not be desirable to train a separate model just for faster inference. We (1) propose a recipe for uptraining existing multi-head language model checkpoints into models with MQA using 5% of original pre-training compute, and (2) introduce grouped-query attention (GQA), a generalization of multi-query attention which uses an intermediate number of key-value heads.

## Key Contributions

- **Grouped-Query Attention (GQA)** — intermediate number of key-value heads between MHA (all) and MQA (one)
- **Uptraining recipe** — convert existing multi-head checkpoints to MQA with only 5% of original compute
- **Quality close to MHA** with inference speed comparable to MQA
- **Addresses memory bandwidth bottleneck** in autoregressive decoder inference
- **Practical** — enables faster inference without training separate models from scratch

## Connections

- [[attention-is-all-you-need]] — Original multi-head attention mechanism
- [[transformer-taxonomy]] — Catalogues MQA and GQA as architectural changes
- [[flash-attention]] — Complementary optimization for attention memory efficiency

## Key Facts

- Published 2023
- Proposes **Grouped-Query Attention (GQA)** as a middle ground between Multi-Head Attention and Multi-Query Attention
- Groups attention heads to share key/value projections, reducing memory bandwidth at inference
- Interpolates between MHA (high quality, high memory) and MQA (lower quality, low memory)
