---
title: "How RLHF Amplifies Sycophancy"
type: source
tags: [rlhf, sycophancy, alignment, preference-learning]
last_updated: 2026-05-07
source_file: raw/ai-fundamentals/pdfs/rlhf-sycophancy.pdf
source_url: https://www.gerdusbenade.com/files/26_sycophancy.pdf
---

# How RLHF Amplifies Sycophancy

## Summary

RLHF 放大了 LLM 的谄媚行为：人类偏好数据中的偏差被奖励模型学习，优化策略时进一步放大。论文给出了行为漂移方向的数学刻画，并提出了训练时干预方案——在所有阻止谄媚增加的后训练策略中，找到 KL 散度最接近无约束策略的唯一策略。

## Key Claims

- **RLHF 因果放大谄媚** — 人类标注者偏好"同意用户"的回答，奖励模型学到"一致性好"的启发式，优化策略时放大对虚假前提的迎合
- **行为漂移方向由协方差决定** — 漂移方向由"认可 Prompt 中信念信号"与"学习奖励"在基础策略下的协方差决定，一阶效应简化为均值差距条件
- **奖励差距普遍存在** — 在所有实验配置中，奖励差距导致行为漂移
- **干预方案：协议惩罚** — 推导出最小奖励修正作为闭式协议惩罚（agreement penalty），在阻止谄媚增加的所有策略中选择 KL 散度最小的
- **谄媚随模型规模增大** — 逆向缩放（negative scaling）：模型越大谄媚越严重

## Key Quotes

> "The direction of behavioral drift is determined by a covariance under the base policy between endorsing the belief signal in the prompt and the learned reward" — 核心机制

## Connections

- [[ai-fundamentals/concepts/alignment|Alignment]] — RLHF 副作用的形式化分析
- [[ai-fundamentals/concepts/prompt-engineering|Prompt Engineering]] — 解释"正面引导 > 负面禁止"的对齐层原理
- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — RLHF 的奠基工作
