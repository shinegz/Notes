---
title: "Fine-tuning"
type: concept
tags: [fine-tuning, sft, pre-training, adaptation]
sources:
  - ai-fundamentals/sources/instructgpt
  - ai-fundamentals/sources/scaling-laws-kaplan
  - ai-fundamentals/sources/gpt3-language-models-few-shot
last_updated: 2026-04-24
---

# Fine-tuning

**Fine-tuning = 在预训练好的模型基础上，用特定任务的数据继续训练，让模型学会特定技能。**

## 一句话理解

预训练让 LLM"会说人话"，Fine-tuning 让它"说好特定场景的话"——比如遵循指令、写代码、做客服。

## 预训练 vs Fine-tuning

| 阶段 | 数据 | 目标 | 成本 |
|------|------|------|------|
| **预训练** | 海量无标注文本（TB 级）| 学会语言规律 | 极高（百万美元级）|
| **Fine-tuning** | 少量标注数据（MB~GB 级）| 适配特定任务 | 低（几千美元级）|

[[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] 证明了 few-shot prompting 可以在不 fine-tuning 的情况下完成任务，但 fine-tuning 能更稳定、更可靠地控制模型行为。

## 主要 Fine-tuning 方法

### 1. SFT（Supervised Fine-Tuning）

- **数据**：人工标注的 (prompt, response) 对
- **目标**：让模型学会期望的输出格式和内容
- **应用**：InstructGPT 的第一步就是 SFT，让 GPT-3 学会遵循指令

### 2. RLHF（Reinforcement Learning from Human Feedback）

- **流程**：SFT → 训练 Reward Model → 用 PPO 算法优化策略
- **目标**：让模型输出符合人类偏好（有用、无害、诚实）
- **应用**：ChatGPT、InstructGPT 的核心技术
- 详见概念页 [[ai-fundamentals/concepts/alignment|Alignment]]

### 3. Parameter-Efficient Fine-Tuning（PEFT）

- **LoRA**（见 source [[ai-fundamentals/sources/lora|LoRA]]）：只训练低秩适配矩阵，大幅减少可训练参数
- **Prefix-tuning / Prompt-tuning**：冻结模型权重，只优化输入前缀

## Fine-tuning 的边界

[[ai-fundamentals/sources/scaling-laws-kaplan|Scaling Laws]] 的研究表明：
- 模型基础能力主要来自预训练
- Fine-tuning 不能教给模型预训练中没有的"新知识"
- 对于需要实时信息或专有数据的场景，Fine-tuning 不如 [[ai-fundamentals/concepts/rag|RAG]]

## 来源

- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — RLHF 与 SFT 的完整流程
- [[ai-fundamentals/sources/scaling-laws-kaplan|Scaling Laws — Kaplan]] — 预训练 vs 微调的能力边界
- [[ai-fundamentals/sources/gpt3-language-models-few-shot|GPT-3]] — Few-shot 作为 fine-tuning 的替代方案
