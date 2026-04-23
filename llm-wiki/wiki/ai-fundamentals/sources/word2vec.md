---
title: "Efficient Estimation of Word Representations in Vector Space (word2vec)"
type: source
tags: [word-embeddings, nlp, representation-learning, word2vec]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/word2vec.pdf
---

# Efficient Estimation of Word Representations in Vector Space (word2vec)

**Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean**  
*Google Inc.*

## Abstract

We propose two novel model architectures for computing continuous vector representations of words from very large data sets. The quality of these representations is measured in a word similarity task, and the results are compared to the previously best performing techniques based on different types of neural networks. We observe large improvements in accuracy at much lower computational cost — it takes less than a day to learn high quality word vectors from a 1.6 billion words data set. Furthermore, we show that these vectors provide state-of-the-art performance on measuring syntactic and semantic word similarities.

## Key Contributions

- **Two architectures**: Continuous Bag-of-Words (CBOW) and Skip-gram
- **Scalable to massive datasets** — trains on 1.6B words in less than a day
- **Vector arithmetic captures semantics** — famous example: "king - man + woman ≈ queen"
- **Outperforms previous neural network approaches** on word similarity benchmarks
- **Foundation for modern NLP** — embeddings became standard for downstream tasks and retrieval

## Connections

- [[attention-is-all-you-need]] — Word embeddings are the input to the Transformer embedding layer
- [[llm-powered-autonomous-agents]] — Long-term memory in agents uses vector embeddings (descendants of word2vec)
- [[gan]] — Both represent early 2013-2014 deep learning breakthroughs from Google/U de Montreal
