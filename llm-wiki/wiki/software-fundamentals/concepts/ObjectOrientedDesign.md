---
title: "Object-Oriented Design"
type: concept
last_updated: "2026-04-30"
---

## Epitome

面向对象设计（OOD）通过**封装状态与行为**来建模现实世界。核心是让对象成为**数据+逻辑的自治单元**。

## Boundary Clarification

- OOD 不是关于"用 class 写代码"。class 只是组织手段，不是目的。
- OOD 不是关于"继承层级"。现代 OOD 更强调组合优于继承。
- OOD 是关于**消息传递**（Smalltalk 原始定义）。对象之间通过发送消息协作。
- OOD 是关于**封装**（信息隐藏）。内部实现对外部不可见。

## Mechanism

### SOLID 原则

| 首字母 | 原则 | 违反后果 |
|--------|------|----------|
| **S** Single Responsibility | 每个类只有一个改变理由 | God Object |
| **O** Open/Closed | 对扩展开放，对修改关闭 | 修改影响范围不可控 |
| **L** Liskov Substitution | 子类必须可替代父类 | 继承滥用 |
| **I** Interface Segregation | 客户端不依赖不需要的接口 | 接口污染 |
| **D** Dependency Inversion | 依赖抽象而非具体 | 硬耦合 |

### 设计原则的本质

- **DRY** — 知识单一表达。重复导致维护噩梦。
- **正交性** — 改变一个维度不影响其他维度。
- **信息隐藏** — 封装隔离复杂度。

## Types

### Gang of Four（GoF）模式分类

**创建型**：Singleton、Factory Method、Abstract Factory、Builder、Prototype
**结构型**：Adapter、Bridge、Composite、Decorator、Facade、Flyweight、Proxy
**行为型**：Command、Observer、Strategy、Template Method、Iterator、Chain of Responsibility...

### 现代设计原则

- **Composition over Inheritance** — 用组合替代深层继承。
- **Tell, Don't Ask** — 不要查询状态后再决策，直接发消息。
- **Law of Demeter** — 只与直接邻居通信。

## Connections

- [[software-fundamentals/concepts/DesignPatterns|Design Patterns]] — GoF 模式是 OOD 经验的结晶。
- [[software-fundamentals/concepts/DomainDrivenDesign|Domain-Driven Design]] — DDD 在战术层面使用 OOD 模式。
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — TPP 的 DRY 和正交性是 OOD 的具体实践。

## Sources

- [[software-fundamentals/sources/domain-driven-design|Domain-Driven Design]] — 第 4 章战术建模深入讨论 OOD。