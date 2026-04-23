---
title: "Training Compute-Optimal Large Language Models (Chinchilla)"
type: source
tags: [scaling-laws, llm, training, compute-optimal]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/chinchilla.pdf
---

# Training Compute-Optimal Large Language Models (Chinchilla)

**Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, Laurent Sifre**  
*DeepMind*

## Abstract

We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget. We find that current large language models are significantly under-trained, a consequence of the recent focus on scaling language models whilst keeping the amount of training data constant. By training over 400 language models ranging from 70 million to over 16 billion parameters on 5 to 500 billion tokens, we find that for compute-optimal training, the model size and the number of training tokens should be scaled equally: for every doubling of model size the number of training tokens should also be doubled.

## Key Contributions

- **Compute-optimal scaling laws** — model size and training tokens should scale equally
- **Current LLMs are under-trained** — they use too few tokens relative to their size
- **Chinchilla (70B params, 1.5T tokens)** — trained with same compute as Gopher (280B) but outperforms it
- **Optimal ratio: ~20 tokens per parameter** — vs. previous practice of ~1-2 tokens per parameter
- **400+ models trained** to empirically validate the scaling relationship across a wide range

## Connections

- [[scaling-laws-kaplan|Scaling Laws (Kaplan)]] — Chinchilla updates these with new optimal ratios
- [[gpt3-language-models-few-shot|GPT-3]] — GPT-3 was trained with far fewer tokens than Chinchilla-optimal
- [[transformer-taxonomy]] — Chinchilla is catalogued as a key model in the taxonomy
