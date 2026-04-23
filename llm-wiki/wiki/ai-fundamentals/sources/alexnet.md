---
title: "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)"
type: source
tags: [deep-learning, cnn, computer-vision, imagenet]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/alexnet.pdf
---

# ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)

**Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton**  
*University of Toronto*

## Abstract

We trained a large, deep convolutional neural network to classify the 1.2 million high-resolution images in the ImageNet LSVRC-2010 contest into 1000 classes. The network achieved top-1 and top-5 error rates of 37.5% and 17.0%, substantially better than previous state-of-the-art methods.

## Key Contributions

- **Deep CNN architecture** with 8 layers (5 convolutional + 3 fully-connected), 60M parameters
- **ReLU activation** — first to demonstrate non-saturating nonlinearity enables faster training in deep networks
- **GPU training** — used two GTX 580 GPUs with cross-GPU parallelization
- **Dropout regularization** — applied to fully-connected layers to reduce overfitting
- **Local response normalization** — inspired by biological lateral inhibition
- **Won ImageNet 2012** with top-5 error of 15.3% (vs. 26.2% second place)

## Connections

- [[resnet]] — Built upon CNN foundations established by AlexNet, adding residual connections for even deeper networks
- [[attention-is-all-you-need|Transformer]] — Alternative architecture that later surpassed CNNs in many vision tasks

## Key Facts

- Published at NeurIPS 2012
- Won ImageNet LSVRC-2012 with top-5 error of 15.3% (vs. 26.2% second place)
- 8 layers: 5 convolutional + 3 fully connected
- 60M parameters
- Used ReLU activation, dropout regularization, and GPU training
- Widely credited with sparking the deep learning revolution
