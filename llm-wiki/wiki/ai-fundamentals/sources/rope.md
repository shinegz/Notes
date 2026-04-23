---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
type: source
tags: [positional-encoding, transformer, rope, rotation]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/rope.pdf
---

# RoFormer: Enhanced Transformer with Rotary Position Embedding

**Jianlin Su, Yu Lu, Shengfeng Pan, Ahmed Murtadha, Bo Wen, Yunfeng Liu**  
*Zhuiyi Technology, Sun Yat-sen University*

## Abstract

Position encoding has shown effective in the transformer architecture, enabling valuable supervision for dependency modeling between elements at different positions. This paper investigates various methods to integrate positional information and proposes Rotary Position Embedding (RoPE), which encodes absolute position with a rotation matrix while simultaneously incorporating explicit relative position dependency in self-attention formulation.

## Key Contributions

- **Rotary Position Embedding (RoPE)** — encodes position by rotating query/key vectors in 2D subspaces
- **Combines absolute and relative position** — uses rotation matrix for absolute, naturally derives relative
- **Extrapolates to longer sequences** than seen during training
- **Adopted by major models** — PaLM, LLaMA, GPT-NeoX, and many modern LLMs
- **Theoretically elegant** — decays inter-token dependency with relative distance via rotation angles

## Connections

- [[attention-is-all-you-need]] — Original sinusoidal positional encoding that RoPE improves upon
- [[transformer-taxonomy]] — Lists RoPE as a key architectural change in the taxonomy
- [[gpt3-language-models-few-shot|GPT-3]] — GPT-3 uses learned position embeddings; later models switched to RoPE

## Key Facts

- Published 2021
- Proposes **Rotary Position Embedding (RoPE)** as an alternative to absolute and relative positional encodings
- Encodes position by rotating query/key vectors in 2D subspaces
- Naturally extends to longer sequences than seen during training
- Adopted by PaLM, LLaMA, and many modern LLMs
