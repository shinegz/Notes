---
title: "AlexNet: ImageNet Classification with Deep CNNs"
type: source
tags: [alexnet, deep-learning, computer-vision, imagenet]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/alexnet.pdf
source_url: https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks
---

## Summary

Krizhevsky et al. demonstrate that deep convolutional neural networks (CNNs) can dramatically outperform traditional methods on ImageNet. AlexNet's success sparked the deep learning revolution and introduced key techniques like ReLU, dropout, and GPU training.

## Key Claims

- **8-layer CNN** winning ImageNet 2012 with 15.3% top-5 error
- **ReLU activation**: Faster than tanh, enables deeper networks
- **GPU training**: Two GPUs used for parallel training
- **Dropout**: Regularization technique to prevent overfitting
- **Data augmentation**: Random crops, horizontal flips

## Connections

- [[ai-fundamentals/sources/resnet|ResNet]] — Deeper architecture with residual connections
- [[ai-fundamentals/concepts/transformer|Transformer]] — Inspired by deep learning scaling
