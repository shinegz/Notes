---
title: "Information Hiding"
type: concept
tags: [software-design, encapsulation, abstraction, module-design]
sources:
  - software-fundamentals/sources/posd-2nd-edition
last_updated: "2026-05-02"
---

## 一句话理解

Information Hiding（信息隐藏）主张将设计决策封装在模块内部，外部只能通过接口访问，隐藏实现细节和变化理由。

## 背景

软件复杂性来自变化。当一个模块的实现需要因为某个原因改变时，如果这个原因没有被隐藏，其他依赖模块也需要跟着改变。

## 核心机制

### 隐藏什么

- 算法的实现细节
- 数据结构和编码方式
- 资源分配策略
- 第三方依赖

### 信息隐藏 vs 封装

| 概念 | 关注点 |
|------|--------|
| Information Hiding | 隐藏变化的原因和时机 |
| Encapsulation（封装） | 隐藏数据的表示形式 |

信息隐藏是更广义的 principle，封装是其实现手段之一。

### 与抽象的关系

好的接口是抽象的——它只暴露必要行为，不暴露实现细节。抽象是信息隐藏的结果。

## 关联概念

- [[software-fundamentals/concepts/GeneralPurposeModules|General-Purpose Modules are Deeper]] — 通用目的模块是信息隐藏的最佳实践
- [[software-fundamentals/concepts/SoftwareArchitecture|Software Architecture]] — 信息隐藏是架构质量属性的基础
- [[software-fundamentals/concepts/ObjectOrientedDesign|Object Oriented Design]] — SOLID 的 SRP 和 ISP 直接来自信息隐藏原则

## 来源

- [[software-fundamentals/sources/posd-2nd-edition|A Philosophy of Software Design]] — Ch 6
