---
title: "Attention Is All You Need"
type: source
tags: [transformer, attention, nlp, deep-learning]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/attention-is-all-you-need.pdf
source_url: https://arxiv.org/abs/1706.03762
---

## Summary

Vaswani et al. propose the **Transformer**—a network architecture based entirely on attention mechanisms, dispensing with recurrence and convolution. The model achieves state-of-the-art results on WMT 2014 translation benchmarks while being significantly more parallelizable and requiring less training time.

## Key Claims

- **First fully attention-based sequence transduction model** — no recurrence or convolution
- Achieves 28.4 BLEU on WMT 2014 English-to-German and 41.8 BLEU on English-to-French
- Training time: 3.5 days on 8 GPUs (vs. weeks for competing models)
- Scaled dot-product attention: `Attention(Q, K, V) = softmax(QK^T / √d_k) × V`
- Multi-head attention allows the model to jointly attend to information from different representation subspaces

## Architecture

| Component | Description |
|-----------|-------------|
| Encoder | 6 layers, each with multi-head self-attention + feed-forward |
| Decoder | 6 layers, each with masked self-attention + encoder-decoder attention + feed-forward |
| Positional Encoding | Sinusoidal encoding added to input embeddings |
| Layer Norm | Applied after each sub-layer with residual connection |

## Key Quotes

> "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks... We propose a new simple network architecture, the Transformer, based entirely on attention mechanisms."

## Connections

- [[ai-fundamentals/sources/bert-pre-training|BERT]] — Uses Transformer encoder architecture
- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — Uses Transformer decoder architecture
- [[ai-fundamentals/sources/the-illustrated-transformer|The Illustrated Transformer]] — Jay Alammar's visual tutorial
