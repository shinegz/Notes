---
title: "Software Architecture"
type: concept
sources:
  - software-fundamentals/sources/mythical-man-month
last_updated: "2026-04-30"
---

## 一句话理解

软件架构是系统早期做出的**高层设计决策**，决定了组件边界、交互方式和质量属性的优先级。

## 边界

- 软件架构不是画图。图只是表达手段，不是架构本身。
- 软件架构不是框架选型。框架是工具，不是架构。
- 软件架构是决策的集合。"架构 = 那些早期做出的、改变代价高昂的决策"。
- 软件架构是质量属性的权衡。没有"最好的架构"，只有"最适合当前场景的架构"。

## 核心机制

### 质量属性（Quality Attributes）

| 属性 | 衡量指标 | 典型场景 |
|------|----------|----------|
| **Performance** | 延迟 / 吞吐量 | 高并发 API |
| **Scalability** | 水平扩展能力 | 云原生系统 |
| **Availability** | 可用时间百分比 | 关键业务系统 |
| **Security** | 机密性 / 完整性 | 金融 / 医疗 |
| **Maintainability** | 修改成本 | 长期演进系统 |

### 经典架构风格

- **分层架构**（Layered）—— UI / Service / Domain / Infrastructure
- **微服务架构**（Microservices）—— 按业务边界拆分，独立部署
- **事件驱动架构**（Event-Driven）—— 松耦合，异步通信，最终一致性
- **六边形架构**（Hexagonal / Ports & Adapters）—— 核心业务与外部依赖解耦

## 类型

### 架构决策的层级

1. **企业级** — 系统边界、数据所有权
2. **应用级** — 模块划分、接口契约
3. **代码级** — 类结构、设计模式

### 架构演进

- **Evolutionary Architecture** — 架构不是一步到位，是渐进演进的
- **Architecture Decision Records (ADR)** — 用文档记录决策上下文

## 关联概念

- [[software-fundamentals/concepts/DesignPatterns|Design Patterns]] — 架构中的模式应用
- [[software-fundamentals/concepts/DomainDrivenDesign|Domain-Driven Design]] — Bounded Context 是架构边界的设计工具

## 来源

- [[software-fundamentals/sources/mythical-man-month|The Mythical Man-Month]] — "The design should precede coding"
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — "Thinking about design"