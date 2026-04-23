---
title: "Transformer Taxonomy (the last lit review)"
type: source
tags: [transformer, llm, survey, architecture, taxonomy]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/articles/transformer-taxonomy-the-last-lit-review.md
---

# Transformer Taxonomy (the last lit review)

**kipply**

## Abstract

A running literature review covering 22 models, 11 architectural changes, 7 post-pre-training techniques, and 3 training techniques in the Transformer era. The document provides concise one-paragraph summaries of each paper with key hyperparameters and architectural details, ordered by importance and uniqueness. Excludes systems/performance and alignment research.

## Key Contributions

- **22 model summaries** with hyperparameters, training data, and architectural specifics
- **11 architectural changes** catalogued with implementation details
- **7 post-pre-training techniques** documented
- **Curated selection** based on author's domain knowledge rather than exhaustive coverage

## Notable Models Surveyed

| Model | Params | Organization | Date | Key Detail |
|-------|--------|-------------|------|------------|
| GPT-3 | 175B | OpenAI | May 2020 | Seminal LLM; 300B tokens; established standard recipe |
| GPT-4 | Unknown | OpenAI | Mar 2023 | Multi-modal; evals extrapolated from smaller models |
| Gopher | 280B | DeepMind | Dec 2021 | RMSNorm; relative positional encoding; 300B tokens |
| Chinchilla | 70B | DeepMind | Mar 2022 | **Compute-optimal scaling**: 20:1 token-to-param ratio |
| PaLM | 540B | Google | Apr 2022 | Largest known dense LM; SwiGLU; parallel attention |
| LLaMA | 65B | Meta | Feb 2023 | Chinchilla replication; open weights |
| BLOOM | 176B | HuggingFace | Jul 2022 | Largest open-source model; 366B tokens; ALiBi |

## Architectural Changes Catalogued

| Change | Description | Key Papers |
|--------|-------------|------------|
| **Multi-Query Attention** | Share K/V across heads; reduces inference memory | Shazeer 2019 |
| **Sparse Attention** | Attend to subsets of tokens, not all previous | Sparse Transformer 2019 |
| **Mixture-of-Experts** | Sparsely activate parameters per token | GLaM, Switch |
| **FlashAttention** | Tiled attention with O(√n) memory; 1.7x training speedup | Dao et al. 2022 |
| **Parallel Attention** | Run attention and MLP layers in parallel | PaLM, GPT-J |
| **Activation Functions** | GeGLU, SwiGLU, SoLU as ReLU alternatives | Shazeer 2020, Anthropic 2022 |
| **LayerNorm Variants** | DeepNorm, RMSNorm as alternatives to standard LayerNorm | Various |
| **RoPE** | Rotary Position Embedding | Su et al. 2021 |
| **ALiBi** | Attention with Linear Biases for extrapolation | Press et al. 2021 |
| **Encoder+Decoder** | Original transformer architecture for seq2seq | Vaswani et al. 2017 |
| **Tokenizer Choices** | BPE vs SentencePiece trade-offs | Various |

## Connections

- [[attention-is-all-you-need]] — Foundation paper for all models in this taxonomy
- [[scaling-laws-kaplan|Scaling Laws]] — GPT-3 follows these; Chinchilla updates them
- [[flash-attention]] — Detailed coverage of FlashAttention architectural change
- [[gpt3-language-models-few-shot|GPT-3]] — First model in the taxonomy
- [[bert-pre-training|BERT]] — Pre-dates most models here but established encoder paradigm
