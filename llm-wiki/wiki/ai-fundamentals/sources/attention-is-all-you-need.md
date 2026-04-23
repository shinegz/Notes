---
title: "Attention Is All You Need"
type: source
tags: [transformer, attention, nlp, deep-learning]
sources: []
last_updated: 2026-04-19
source_file: raw/ai-fundamentals/pdfs/attention-is-all-you-need.pdf
---

# Attention Is All You Need

**Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin**  
*Google Brain, Google Research, University of Toronto*

## Abstract

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based entirely on attention mechanisms, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.

## Key Contributions

- **First fully attention-based sequence transduction model** — no recurrence or convolution
- Achieves state-of-the-art results on WMT 2014 English-to-German (28.4 BLEU) and English-to-French (41.8 BLEU)
- Training time significantly reduced: 3.5 days on 8 GPUs (vs. weeks for other models)
- Highly parallelizable architecture enables scaling with more data and compute

## Scaled Dot-Product Attention

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

The two most commonly used attention functions are additive attention and dot-product (multiplicative) attention. Dot-product attention is identical to our algorithm, except for the scaling factor of 1/√d_k. The scaling factor prevents large dot products from pushing softmax into regions with extremely small gradients.

## Multi-Head Attention

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W^O
where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

Instead of performing a single attention function, we project the queries, keys and values h times in parallel with different learned linear projections to d_q, d_k and d_v dimensions respectively.

## Model Architecture

| Component | Description |
|-----------|-------------|
| Encoder | 6 identical layers, each with 2 sub-layers (multi-head self-attention + position-wise FFN) |
| Decoder | 6 identical layers, with 3 sub-layers (masked self-attention + encoder-decoder attention + FFN) |
| Positional Encoding | Sinusoidal encoding added to input embeddings |
| Layer Norm | Applied after each sub-layer with residual connection |

## Connections

- [[bert-pre-training]] — BERT uses Transformer encoder architecture
- [[gpt3-language-models-few-shot|GPT-3]] — GPT-3 uses Transformer decoder architecture

## Results

| Task | Model | BLEU |
|------|-------|------|
| WMT 2014 En-De | Transformer (base) | 25.8 |
| WMT 2014 En-De | Transformer (big) | **28.4** |
| WMT 2014 En-Fr | Transformer (big) | **41.8** |

