---
title: "LoRA: Low-Rank Adaptation"
type: concept
tags: [lora, fine-tuning, efficiency, parameter-efficient]
sources:
  - ai-fundamentals/sources/lora
last_updated: 2026-04-26
---

# LoRA: Low-Rank Adaptation

**LoRA = 在冻结的预训练权重旁添加低秩矩阵，大幅减少可训练参数。**

## 一句话理解

LoRA 的核心思想是：模型的权重更新是低秩的，不需要更新整个矩阵，只需要训练两个小的低秩矩阵相乘，可训练参数减少 10000 倍。

## 背景

Full Fine-tuning 的问题：
- 175B 参数的模型，全量更新需要全部参数
- 训练成本高，硬件要求高
- 每个任务一个模型，无法共享

## 核心机制

```
W = W₀ + BA
其中：
  W₀ = 冻结的预训练权重
  B = 可训练矩阵 (d × r)
  A = 可训练矩阵 (r × k)
  r = rank（通常 4-64），远小于 d 或 k
```

只有 A 和 B 是可训练的，W₀ 保持冻结。推理时，可以把 BA 的结果合并到 W₀ 中，不引入额外推理延迟。

## 关键参数

| 参数 | 作用 | 典型值 |
|------|------|--------|
| rank r | 低秩矩阵的秩 | 4-64 |
| α | 缩放因子 | 通常 r 的倍数 |
| 可训练参数量 | 原模型的 | 0.1%（减少 10000×） |

## LoRA 的优势

| 优势 | 说明 |
|------|------|
| 参数效率 | 可训练参数只有原模型的 0.1% |
| 无推理延迟 | 训练后合并权重，推理同原模型 |
| 多任务共享 | 不同任务可训练不同的 A、B，共享 W₀ |
| 训练稳定 | 只优化低秩矩阵，收敛更快 |

## 应用场景

- 大模型 Fine-tuning（GPT、Llama、Stable Diffusion）
- 多任务学习（不同任务用不同的 A、B）
- 领域适配（冻结基座，训练适配层）

## 关联概念

- [[ai-fundamentals/concepts/fine-tuning|Fine-tuning]] — LoRA 是 Fine-tuning 的一种高效变体
- [[ai-fundamentals/concepts/alignment|Alignment]] — LoRA 可用于 RLHF/DPO 的高效训练

## 来源

- [[ai-fundamentals/sources/lora|LoRA]] — 原始论文
