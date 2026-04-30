---
title: "Domain-Driven Design"
type: concept
abbreviation: "DDD"
last_updated: "2026-04-30"
---

## Epitome

Domain-Driven Design 是一套**通过深度理解业务领域来指导软件设计**的方法论。核心理念是让**领域模型**与**代码实现**保持紧密绑定，用**统一语言**（Ubiquitous Language）弥合业务与技术的鸿沟。

## Boundary Clarification

- DDD 不是关于 ORM 或 Entity 框架。战术工具只是实现手段。
- DDD 不是微服务。Bounded Context 可以是 monolith 的内部划分，也可以是微服务的边界。
- DDD 是关于业务认知的。模型是对业务知识的深刻提炼，不是数据结构。
- DDD 是关于战略优先于战术的。先确定边界和子域，再谈具体模式。

## Mechanism

### 战略设计（Strategic Design）

| 概念 | 定义 |
|------|------|
| **Bounded Context** | 模型的明确适用范围，超出边界则模型失效 |
| **Context Map** | 上下文之间的集成关系图 |
| **Subdomain** | 子域划分：Core（核心竞争力）/ Supporting（支撑）/ Generic（通用） |

### 战术设计（Tactical Design）

| 概念 | 作用 |
|------|------|
| **Entity** | 有生命周期标识的领域对象 |
| **Value Object** | 无标识、不可变、用于描述特征 |
| **Aggregate** | 一组内聚对象的边界，外部只能通过根访问 |
| **Domain Event** | 业务发生的记录，用于解耦和审计 |
| **Service** | 无状态的操作，跨越多个 Entity |
| **Repository** | 持久化抽象，不暴露存储细节 |
| **Factory** | 复杂对象的创建逻辑 |

### 集成模式

- **Anticorruption Layer** — 防腐层，隔离外部模型的侵入
- **Open Host Service** — 开放主机服务，定义协议供外部调用
- **Published Language** — 发布的语言（如 XML Schema、JSON Schema）

## Connections

- [[software-fundamentals/concepts/ObjectOrientedDesign|Object-Oriented Design]] — DDD 战术层大量使用 OOD 模式
- [[software-fundamentals/concepts/DesignPatterns|Design Patterns]] — Repository/Aggregate/Factory 源自 GoF
- [[software-fundamentals/sources/domain-driven-design|Domain-Driven Design]] — Eric Evans 原著（359 pages）

## Sources

- [[software-fundamentals/sources/domain-driven-design|Domain-Driven Design]] — Eric Evans, 2003