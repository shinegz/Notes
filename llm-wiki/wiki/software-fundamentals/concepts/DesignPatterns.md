---
title: "Design Patterns"
type: concept
last_updated: "2026-04-30"
---

## Epitome

设计模式是**可重用的解决方案**，针对软件设计中反复出现的问题提供经过验证的抽象结构，让开发者不必从零思考。

## Boundary Clarification

- 设计模式不是可直接套用的代码模板。模式是思维框架，不是代码片段。
- 设计模式不是银弹。滥用模式比不用模式更危险。
- 设计模式是经验的提炼。GoF 1994 年总结了 23 种经典模式。
- 设计模式是沟通的词汇表。说出"单例模式"团队成员就懂上下文。

## Mechanism

### 模式的价值

1. **避免重复踩坑** — 模式是前人踩过的坑，总结了何时用、优缺点
2. **促进团队沟通** — 用模式名而非实现细节描述设计
3. **揭示设计意图** — 代码中的模式名暴露了设计者的思考

### 反模式（Anti-Patterns）

- **God Object** — 一个类做太多事，违反 SRP
- **Spaghetti Code** — 缺乏结构的代码，逻辑纠缠
- **Golden Hammer** — 对熟悉模式的盲目依赖

## Types

### 按目的分类

| 类别 | 意图 | 代表模式 |
|------|------|----------|
| **创建型** | 对象创建逻辑解耦 | Singleton、Factory、Builder |
| **结构型** | 类/对象组合成更大结构 | Adapter、Decorator、Proxy |
| **行为型** | 对象间的责任分配 | Observer、Strategy、Command |

### 按复杂度分类

- **简单模式** — 单个类即可实现（Singleton）
- **复合模式** — 多个模式组合（Model-View-Controller）

## Applications

| 场景 | 推荐模式 |
|------|----------|
| 全局唯一资源 | Singleton |
| 复杂对象构造 | Builder |
| 跨 API 适配 | Adapter |
| 功能动态增强 | Decorator |
| 状态流转 | State |
| 异步任务管理 | Command |

## Connections

- [[software-fundamentals/concepts/ObjectOrientedDesign|Object-Oriented Design]] — 设计模式是 OOD 原则的具体化
- [[software-fundamentals/concepts/DomainDrivenDesign|Domain-Driven Design]] — DDD 的 Repository/Aggregate/Factory 等概念源自 GoF 模式
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — TPP 强调"选择工具"而非"记住模式"

## Sources

- 《设计模式：可复用面向对象软件的基础》（Gang of Four, 1994）
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — "与你熟知的模式和习惯做斗争"