---
title: "Generative Adversarial Networks"
type: source
tags: [gan, generative-model, deep-learning, adversarial-training]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/gan.pdf
---

# Generative Adversarial Networks

**Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, Yoshua Bengio**  
*Université de Montréal*

## Abstract

We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data rather than G. The training procedure for G is to maximize the probability of D making a mistake. This framework corresponds to a minimax two-player game.

## Key Contributions

- **Adversarial training framework** — Generator vs. Discriminator trained simultaneously
- **No Markov chains or unrolled inference** — direct backpropagation through both networks
- **Theoretical guarantee** — unique solution exists where G recovers training data distribution
- **Demonstrated on images** — MNIST, TFD, CIFAR-10 with compelling qualitative results
- **Sparked entire field** of generative adversarial networks and applications across domains

## Connections

- [[word2vec]] — Both represent early deep learning breakthroughs from 2013-2014
- [[alexnet]] — Contemporary deep learning breakthrough, but discriminative rather than generative

## Key Facts

- Published at NeurIPS 2014
- Introduces the adversarial training framework: Generator vs. Discriminator
- Generator learns to produce realistic data; Discriminator learns to distinguish real from fake
- Minimax game formulation
- Sparked a major line of research in generative modeling
