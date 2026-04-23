---
title: "Deep Residual Learning for Image Recognition (ResNet)"
type: source
tags: [deep-learning, cnn, residual-learning, computer-vision]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/resnet.pdf
---

# Deep Residual Learning for Image Recognition (ResNet)

**Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun**  
*Microsoft Research*

## Abstract

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth.

## Key Contributions

- **Residual connections (skip connections)** — F(x) + x formulation enables gradient to flow directly
- **ResNet-152** — 8× deeper than VGG nets, yet lower complexity; won ImageNet 2015 with 3.57% top-5 error
- **Addresses vanishing gradient problem** that prevented training networks deeper than ~20 layers
- **Residual blocks with identity mapping** — when dimensions match, skip connection is simple identity
- **Became foundational** for both computer vision (CNNs) and NLP (transformer residual connections)

## Connections

- [[alexnet]] — ResNet builds on CNN foundations, solving the depth limitation AlexNet faced
- [[attention-is-all-you-need]] — Transformer uses residual connections inspired by ResNet
- [[rope]] — Modern LLM architecture combines RoPE with residual Transformer blocks

## Key Facts

- Published at CVPR 2016 (Best Paper)
- Introduces **residual connections** (skip connections) enabling training of very deep networks
- ResNet-152 won ImageNet 2015 with 3.57% top-5 error
- Addressed the vanishing gradient problem that prevented training networks deeper than ~20 layers
- Residual block: output = F(x) + x
- Became foundational architecture for computer vision and later adapted for NLP (e.g., transformer residuals)
