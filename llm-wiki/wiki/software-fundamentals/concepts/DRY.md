---
title: "DRY Principle"
type: concept
sources:
  - software-fundamentals/sources/pragmatic-programmer-20th-anniversary
last_updated: "2026-05-01"
---

## 一句话理解

DRY（Don't Repeat Yourself）原则要求**每份知识必须在系统中具有单一、无歧义的表达**，避免同一知识在多处重复导致维护噩梦。

## 边界

- DRY 不是"不要复制代码"。有时候复制是合理的（如数据不变性约束）。
- DRY 不是"消除所有重复"。只有**真正的知识**重复才需要消除，偶然的代码相似不算。
- DRY 是关于**意图**的。相同的代码可能表达不同的意图，不算重复；不同的代码可能表达相同的意图，必须合并。
- DRY 是**正交性**的基础。消除重复知识才能让组件正交。

## 核心机制

### 知识重复的类型

| 类型 | 例子 | 风险 |
|------|------|------|
| **数据重复** | 数据库和缓存同时存储相同数据 | 数据不一致 |
| **逻辑重复** | 两处代码做相同的判断逻辑 | 修改遗漏 |
| **文档重复** | 代码和注释描述同一件事 | 注释过期 |
| **命名重复** | 同一个概念用多个名称 | 沟通歧义 |

### 实现手段

- **抽象层** — 将公共知识提取到函数、类、模块中
- **单一数据源** — 数据只在一处定义，其他地方引用
- **代码生成** — 从单一源头生成重复代码（如 schema → code）
- **正交化** — 分离关注点，让变更的影响范围明确

### DRY vs WET

- **DRY** — "Don't Repeat Yourself"
- **WET** — "Write Everything Twice"、"We Enjoy Typing"、"Waste Everyone's Time"

## 关联概念

- [[software-fundamentals/concepts/Orthogonality|Orthogonality]] — 正交组件改变一个不影响另一个，DRY 让知识单一表达才能实现正交
- [[software-fundamentals/concepts/ObjectOrientedDesign|SOLID 原则]] — SRP 要求每个类只有一个改变理由，天然促进 DRY

## 来源

- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — DRY 原则的完整阐述