---
title: "Machine Learning"
type: concept
tags: [machine-learning, ml, foundation]
sources: []
last_updated: 2026-04-26
---

# Machine Learning

**Machine Learning = 让模型从数据中自动学习规律，而非人工编码规则。**

## 一句话理解

传统编程是人写规则 + 数据得答案；Machine Learning 是数据 + 答案让模型自动推导规则。

## 核心类型

| 类型 | 训练方式 | 示例 |
|------|----------|------|
| **监督学习** | 有标签数据，学习 (输入 → 正确答案) | 分类、回归 |
| **无监督学习** | 无标签，发现数据结构 | 聚类、降维 |
| **强化学习** | 无标签，通过奖励信号学习 | 游戏、决策 |
| **半监督学习** | 少量标签 + 大量无标签 | 少样本场景 |

## 与 LLM 的关系

- **LLM 预训练**：自监督学习，在海量文本上预测 next token
- **LLM Fine-tuning**：监督学习，用标注数据微调
- **RLHF**：强化学习，用人类反馈信号优化

## 关键概念链路

```
Machine Learning
  ├── 监督学习 → Fine-tuning (SFT)
  ├── 强化学习 → RLHF, DPO
  └── 自监督学习 → LLM 预训练
```

## 来源

待补充。
