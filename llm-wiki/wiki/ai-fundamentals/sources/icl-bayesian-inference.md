---
title: "In-Context Learning as Implicit Bayesian Inference"
type: source
tags: [icl, bayesian-inference, pretraining, few-shot]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/pdfs/icl-bayesian-inference.pdf
source_url: https://arxiv.org/abs/2111.02080
---

# In-Context Learning as Implicit Bayesian Inference

## Summary

ICL 的本质是隐含的贝叶斯推断：模型从 Prompt 示例中推断共享的隐含概念（latent concept），然后基于该概念条件化输出分布。模型不是在"学习新知识"，而是在推断"用户想要哪种模式"。

## Key Claims

- **ICL = 隐含贝叶斯推断** — 预训练中，模型学会推断文档级隐含概念以生成连贯续写；ICL 发生在模型从 Prompt 示例中推断共享概念并用于预测
- **分布不匹配下仍可推断** — Prompt 是独立示例的拼接，与自然语言分布不同，但模型仍能在信号强度超过分布不匹配带来的误差时正确推断隐含概念
- **后验预测分布的边际化** — p(output|prompt) = ∫ p(output|concept, prompt) p(concept|prompt) d(concept)，更多示例使 p(concept|prompt) 集中于正确概念
- **模型缩放改善 ICL** — 在合成数据集 GINC 上，更大的模型 ICL 性能更好，即使预训练损失相同
- **示例顺序敏感** — ICL 性能受示例顺序影响，这是隐含推断的自然结果

## Connections

- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — Few-shot 有效的理论解释
- [[ai-fundamentals/concepts/attention-mechanism|Attention Mechanism]] — Transformer 如何实现隐含推断的底层机制
- [[ai-fundamentals/sources/openai-prompt-engineering|OpenAI Prompt Engineering Guide]] — ICL 的实践指南
