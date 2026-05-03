---
title: "General-Purpose Modules are Deeper"
type: concept
tags: [software-design, module-design, abstraction, information-hiding]
sources:
  - software-fundamentals/sources/posd-2nd-edition
last_updated: "2026-05-02"
---

## 一句话理解

通用目的模块比特殊目的模块接口更简洁、深层，能更好地隐藏信息（information hiding），即使当前只用一种方式使用它，建设通用目的是更少的工作量。

## 背景

在软件设计中，开发者常面临"通用目的"还是"特殊目的"实现的抉择。特殊目的实现看似更直接，但会导致接口膨胀和耦合加深。

## 核心机制

### 通用 vs 特殊

| 维度 | 通用目的模块 | 特殊目的模块 |
|------|------------|------------|
| 接口数量 | 少而深 | 多而浅 |
| 信息隐藏 | 好 | 差 |
| 可复用性 | 高 | 低 |
| 维护成本 | 低 | 高 |
| 实现工作量 | 初期较多 | 长期累积更多 |

### "Somewhat General-Purpose"原则

模块的功能应反映当前需求，但接口应足够通用以支持多种用途，而非绑定到特定用途。

```python
# 特殊目的接口（应避免）
text.backspace(cursor)
text.delete(cursor)
text.deleteSelection(selection)

# 通用目的接口（推荐）
text.insert(position, content)
text.deleteRange(range)
```

## 关联概念

- [[software-fundamentals/concepts/Orthogonality|Orthogonality]] — 正交组件独立运作，通用接口促进正交
- [[software-fundamentals/concepts/SoftwareArchitecture|Software Architecture]] — 模块深度是架构质量的核心指标
- [[software-fundamentals/concepts/InformationHiding|Information Hiding]] — 通用目的接口是信息隐藏的实现手段

## 来源

- [[software-fundamentals/sources/posd-2nd-edition|A Philosophy of Software Design]] — Ch 6
