---
title: "Mixtral 8x7B (Mistral AI)"
type: source
tags: [moe, mixture-of-experts, mistral, sparse-moe]
sources: []
last_updated: 2026-04-26
source_file: raw/ai-fundamentals/pdfs/mixtral.pdf
source_url: https://arxiv.org/abs/2401.04088
---

## Summary

Mistral AI 提出 **Mixtral 8x7B**，一个稀疏混合专家（MoE）语言模型，每层有 8 个专家路由器选 2 个。相比同参数稠密模型，推理速度快 2 倍以上。

## Key Claims

- **稀疏 MoE**：每 token 只激活 2 个专家（总共 8 个），而不是全激活
- **高性能**：在 MT-Bench、HellaSwag 等基准上与 Llama 2 70B 相当
- **快速推理**：每 token 只需要 2x expert computation，而不是 8x
- **Expert Routing**：一个可学习的路由层选择 top-k 专家

## 架构对比

| 模型 | 参数量 | 每 Token 激活参数 | 推理成本 |
|------|--------|------------------|----------|
| Mistral 7B | 7B | 7B | 1x |
| **Mixtral 8x7B** | **46.7B** | **12.9B** | **~2x** |
| Llama 2 70B | 70B | 70B | ~10x |

## MoE 的核心思想

混合专家的核心思想是**分而治之**：
- 不同的专家擅长处理不同类型的输入
- 路由层（Router）学习选择最合适的专家
- 每个专家只处理部分任务，参数量可以被更多任务共享

## 与稠密模型的对比

| 对比维度 | 稠密模型 | MoE |
|----------|----------|-----|
| 参数量 | 全量激活 | 稀疏激活 |
| 计算量 | O(d) per token | O(k·d/r) per token |
| 通信开销 | 无 | All-to-All 通信 |
| 训练稳定性 | 高 | 需要负载均衡 |

## Connections

- [[ai-fundamentals/concepts/scaling-laws|Scaling Laws]] — MoE 是 Scaling 的一种架构方向
- [[ai-fundamentals/concepts/mixture-of-experts|MoE]] — 相关概念
