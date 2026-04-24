---
title: "The Illustrated Transformer"
type: source
tags: [transformer, attention, tutorial, visualization]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/articles/the-illustrated-transformer.md
source_url: https://jalammar.github.io/illustrated-transformer/
author: Jay Alammar
---

## Summary

Jay Alammar provides an accessible visual walkthrough of the Transformer architecture, building intuition from self-attention to the full encoder-decoder stack. The tutorial explains Q/K/V vectors, multi-head attention, positional encoding, and training dynamics with clear diagrams.

## Key Claims

- **Self-attention** allows each word to "attend to" all other words in the sequence
- **Q/K/V vectors**: Query (what am I looking for?), Key (what do I contain?), Value (what information do I hold?)
- **Multi-head attention** enables attending to different representation subspaces simultaneously
- **Positional encoding** injects sequence order information via sinusoidal signals
- **Residual connections + Layer Norm** stabilize training
- Decoder includes **masked attention** to prevent looking at future tokens

## Architecture Overview

```
Encoder Stack (×6):
  Input → Self-Attention → Add & Norm → Feed-Forward → Add & Norm → Output

Decoder Stack (×6):
  Output Embedding → Masked Self-Attention → Add & Norm
                   → Cross-Attention (attends to encoder) → Add & Norm
                   → Feed-Forward → Add & Norm → Output
```

## Connections

- [[ai-fundamentals/sources/attention-is-all-you-need|Attention Is All You Need]] — Original paper
- [[ai-fundamentals/concepts/transformer|Transformer]] — Concept page
- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — Concept page
