---
title: "Tracer Bullets"
type: concept
sources:
  - software-fundamentals/sources/pragmatic-programmer-20th-anniversary
last_updated: "2026-05-01"
---

## 一句话理解

曳光弹（Tracer Bullets）是一种**快速端到端反馈**的开发方式——用最小可见功能快速穿越整个技术栈，持续验证而非追求完美设计。

## 边界

- 曳光弹不是"原型"。原型是废弃的，曳光弹是生产代码的起点。
- 曳光弹不是"增量开发"。增量可能是胡乱堆积，曳光弹有明确的技术验证目标。
- 曳光弹是**有方向的探索**。目标是找到路，而不是走完路。
- 曳光弹是**风险早期暴露**。用可见成果验证技术可行性，而非最后才发现踩坑。

## 核心机制

### 曳光弹 vs Big Design Up Front

| 维度 | Big Design Up Front | Tracer Bullets |
|------|---------------------|----------------|
| 设计时机 | 开发前完成所有设计 | 开发中持续设计 |
| 反馈来源 | 假设、模型 | 真实运行结果 |
| 风险暴露 | 后期集中暴露 | 早期持续暴露 |
| 变更成本 | 高（后期修改代价大） | 低（早期迭代） |

### 曳光弹的开发流程

1. **确定目标** — 明确要验证的技术风险点
2. **构建骨架** — 建立完整的最小系统（数据库 → API → UI）
3. **射击验证** — 实现一个可见功能，观察各层是否衔接
4. **迭代修正** — 根据弹道调整方向，直到命中目标
5. **扩展填充** — 在稳固骨架上填充细节功能

### 曳光弹的适用场景

- 新技术栈的可行性验证
- 架构决策的技术验证
- 跨团队接口契约的确认
- 不确定需求的技术风险探测

## 关联概念

- [[software-fundamentals/concepts/Orthogonality|Orthogonality]] — 正交架构让曳光弹更容易穿越各层
- [[software-fundamentals/concepts/SoftwareArchitecture|Evolutionary Architecture]] — 曳光弹是渐进式架构的具体实践

## 来源

- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — Tracer Bullets 章节