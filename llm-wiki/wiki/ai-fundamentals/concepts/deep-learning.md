---
title: "Deep Learning"
type: concept
tags: [deep-learning, neural-network, foundation]
sources: []
last_updated: 2026-04-26
---

# Deep Learning

**Deep Learning = 用多层神经网络自动学习数据的层次化表示。**

## 一句话理解

浅层网络只能学简单模式，深层网络通过逐层抽象，从像素到边缘到物体到场景，逐层提取越来越抽象的特征。

## 为什么叫「深度」

| 层数 | 能力 |
|------|------|
| 1-2 层 | 线性分类 |
| 3-5 层 | 简单非线性模式 |
| 10+ 层 | 复杂抽象表示 |
| 100+ 层 | 极深网络，特征层次丰富 |

## 核心技术

| 技术 | 作用 |
|------|------|
| **ReLU 激活** | 引入非线性，避免梯度消失 |
| **BatchNorm** | 稳定训练，加速收敛 |
| **Dropout** | 防止过拟合 |
| **残差连接** | 解决深层网络的梯度消失问题 |

## 与 LLM 的关系

- **Transformer** = Deep Learning 的集大成者
- **Attention Mechanism** = 让深层网络高效学习长距离依赖
- **预训练 + Fine-tuning** = Deep Learning 的标准范式在 NLP 的应用

## 来源

待补充。
