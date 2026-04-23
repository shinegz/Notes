---
title: "LoRA: Low-Rank Adaptation of Large Language Models"
type: source
tags: [fine-tuning, parameter-efficient, lora, llm]
sources: []
last_updated: 2026-04-23
source_file: raw/ai-fundamentals/pdfs/lora.pdf
---

# LoRA: Low-Rank Adaptation of Large Language Models

**Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen**  
*Microsoft Corporation*

## Abstract

As we pre-train larger models, full fine-tuning becomes less feasible. Using GPT-3 175B as an example — deploying independent instances of fine-tuned models is prohibitively expensive. We propose Low-Rank Adaptation (LoRA), which freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks.

## Key Contributions

- **10,000x reduction in trainable parameters** compared to full fine-tuning of GPT-3 175B
- **3x reduction in GPU memory requirement** during training
- **No additional inference latency** — weights can be merged at deployment
- **Performs on-par or better than fine-tuning** on RoBERTa, DeBERTa, GPT-2, and GPT-3
- **Empirical investigation into rank-deficiency** — optimal rank is surprisingly low (r=4 or r=8)

## Connections

- [[gpt3-language-models-few-shot|GPT-3]] — Primary motivation for parameter-efficient adaptation
- [[instructgpt]] — InstructGPT fine-tuning could benefit from LoRA efficiency
- [[attention-is-all-you-need|Transformer]] — LoRA injects into each Transformer layer

## Key Facts

- Published at ICLR 2022
- **LoRA** freezes pre-trained model weights and injects trainable rank decomposition matrices into each layer
- Reduces trainable parameters by 10,000x while matching or exceeding full fine-tuning quality
- No additional inference latency (merged weights at deployment)
- Became the de facto standard for parameter-efficient fine-tuning of LLMs
