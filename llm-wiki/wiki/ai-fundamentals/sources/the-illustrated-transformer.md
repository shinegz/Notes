---
title: "The Illustrated Transformer"
type: source
tags: [transformer, attention, self-attention, encoder-decoder, nlp]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/articles/the-illustrated-transformer.md
---

# The Illustrated Transformer

**Jay Alammar**

## Abstract

A visual, step-by-step walkthrough of the Transformer architecture introduced in "Attention Is All You Need." The article breaks down the model into its core components — encoder/decoder stacks, self-attention mechanism, multi-head attention, and positional encoding — using intuitive diagrams and toy examples. It explains how Query/Key/Value vectors work, why multi-head attention improves performance, and how positional encoding injects sequence order information.

## Key Contributions

- **Intuitive visual explanation** of the full Transformer architecture for non-experts
- **Step-by-step self-attention calculation** using word-level examples
- **Matrix-form implementation** bridging intuition to actual computation
- **Multi-head attention visualization** showing different attention heads focusing on different relationships
- **Positional encoding explained** with sine/cosine pattern visualization

## Architecture Overview

| Component | Structure |
|-----------|-----------|
| **Encoder Stack** | 6 identical encoders (each: self-attention → feed-forward) |
| **Decoder Stack** | 6 identical decoders (each: masked self-attention → encoder-decoder attention → feed-forward) |
| **Embeddings** | 512-dim vectors per word (bottom encoder only) |
| **Self-Attention** | Q/K/V vectors (64-dim each), scaled dot-product with softmax |
| **Multi-Head Attention** | 8 parallel attention heads, concatenated and projected |
| **Positional Encoding** | Sine/cosine vectors added to input embeddings |

## Self-Attention in Six Steps

1. **Create Q/K/V vectors** from each input embedding (multiply by learned weight matrices)
2. **Calculate score** — dot product of query with each key
3. **Scale** by √(d_k) for stable gradients
4. **Softmax** to normalize scores to probabilities
5. **Weight values** — multiply each value vector by its softmax score
6. **Sum** weighted values → self-attention output for this position

## Multi-Head Attention

- Expands the model's ability to focus on different positions simultaneously
- Provides multiple "representation subspaces" (8 sets of Q/K/V weight matrices)
- Different heads attend to different relationships (e.g., one head focuses on "animal" for "it", another on "tired")

## Positional Encoding

- Adds position-aware vectors to input embeddings
- Uses sine/cosine functions with different frequencies
- Advantage: can scale to sequence lengths longer than training data

## Connections

- [[attention-is-all-you-need]] — Original Transformer paper this article visualizes
- [[bert-pre-training|BERT]] — Uses Transformer encoder; this article explains the encoder mechanism
- [[gpt3-language-models-few-shot|GPT-3]] — Uses Transformer decoder; this article explains the decoder mechanism
