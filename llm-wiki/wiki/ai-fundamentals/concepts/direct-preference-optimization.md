---
title: "Direct Preference Optimization (DPO)"
type: concept
tags: [dpo, alignment, fine-tuning, preference-learning]
sources:
  - ai-fundamentals/sources/dpo
last_updated: 2026-04-26
---

# Direct Preference Optimization (DPO)

**DPO = 直接在偏好数据上优化 LLM，无需奖励模型和强化学习。**

## 一句话理解

DPO 用一个巧妙的损失函数，把 RLHF 的「预测人类偏好 → 训练奖励模型 → PPO 优化」三步流程，变成一步端到端训练，稳定又省事。

## 背景

RLHF 的问题：
- 需要单独训练一个 Reward Model
- 需要 PPO 强化学习，优化不稳定
- 实现复杂，调参难度大

## 核心机制

DPO 直接在偏好对上优化，损失函数蕴含了「reward model + PPO」的效果：

```
loss = -log σ(r(x, y_w) - r(x, y_l) - β·log(π(y_l|x)/π_ref(y_l|x)))
其中：
  y_w = 偏好回答（chosen）
  y_l = 非偏好回答（rejected）
  r(x, y) = 隐式奖励
  π = 待优化的策略
  π_ref = 参考策略（SFT 后模型）
```

等价于同时完成 Reward Model 训练和策略优化。

## DPO vs RLHF

| 方面 | RLHF | DPO |
|------|------|-----|
| Reward Model | 需要单独训练 | 不需要 |
| 强化学习 | 需要 PPO | 不需要 |
| 实现复杂度 | 高 | 低 |
| 训练稳定性 | 敏感 | 更稳定 |
| 效果 | 相当 | 相当或更好 |

## 为什么有效

DPO 的关键洞察：偏好对数据的隐式梯度，同时完成了：
1. 隐式 Reward Model 的训练（通过 log 差分）
2. 策略优化（通过 REBAR/ReBar 类型的梯度估计）

## 关联概念

- [[ai-fundamentals/concepts/alignment|Alignment]] — Alignment 的三种主流方法之一
- [[ai-fundamentals/concepts/fine-tuning|Fine-tuning]] — DPO 是一种 Fine-tuning 方法
- [[ai-fundamentals/sources/instructgpt|InstructGPT]] — RLHF 的标准流程

## 来源

- [[ai-fundamentals/sources/dpo|DPO]] — 原始论文
