---
title: "ResNet: Deep Residual Learning for Image Recognition"
type: source
tags: [resnet, deep-learning, residual-connections, computer-vision]
last_updated: 2026-04-24
source_file: raw/ai-fundamentals/pdfs/resnet.pdf
source_url: https://arxiv.org/abs/1512.03385
---

## Summary

He et al. introduce **ResNet**—a residual learning framework with skip connections that enables training of very deep networks (152 layers). ResNet won CVPR 2016 Best Paper and became the backbone for many computer vision models.

## Key Claims

- **Skip connections**: Enable training of very deep networks (100+ layers)
- **Residual learning**: H(x) = F(x) + x instead of learning H(x) directly
- **152 layers**: 8x deeper than VGG nets
- **Foundation for modern architectures**: Preceded and influenced Transformers

## Connections

- [[ai-fundamentals/sources/alexnet|AlexNet]] — Earlier CNN architecture
- [[ai-fundamentals/concepts/transformer|Transformer]] — Residual connections inspired by ResNet
