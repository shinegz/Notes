---
title: "95% 的 Vibe Coding 项目活不过两周——Spec-Driven Development 能拯救它吗？"
type: source
tags: [sdd, vibe-coding, framework-comparison, spec-kit, openspec, superpowers, kiro, tessl]
last_updated: 2026-04-29
source_file: raw/sdd/articles/zhihu-sdd-framework-landscape.md
source_url: https://zhuanlan.zhihu.com/p/2009360235362526486
---

## Summary

Vibe Coding 在原型阶段效率惊人，但 90-95% 的企业 AI 项目死于"规模化陷阱"。SDD 是 2025-2026 年最重要的工程化趋势，但当前五大框架（Spec Kit、OpenSpec、Superpowers、Kiro、Tessl）集体存在"过度设计"风险。正确的策略是"渐进式 Spec"——按项目规模选择工具，而非一刀切。

## Key Claims

- **90-95% 的企业 AI 项目未能从试点进入生产** — Rand Group 2026 调研数据，问题根源是"没人告诉 AI 为什么要写这段代码"。
- **五大框架的设计哲学差异巨大** — Spec Kit（标准化流水线）、OpenSpec（Brownfield-First 轻量）、Superpowers（TDD + Skills 强制约束）、Kiro（IDE 原生最轻量）、Tessl（Spec-as-Source 激进实验）。
- **渐进式 Spec 是正确的引入策略** — 原型阶段（<1000 行）用 Vibe Coding；功能迭代（1000-10000 行）用 OpenSpec 或 Superpowers；系统构建（>10000 行）用 Spec Kit 或 Kiro。
- **正面数据存在样本偏差** — 生产 Bug 减少 40-60%、重构时间降低 50% 等数据多来自 SDD 工具厂商，独立第三方评价更保守。
- **SDD 效果取决于三个变量交叉** — 项目规模 × 团队经验 × AI 工具成熟度。
- **Martin Fowler 的 Verschlimmbesserung 警告值得重视** — 现有工具假设每个任务需要完整 SDD 流水线，但现实中大多数编码任务不需要。

## 数据支撑

| 指标 | 改善幅度 | 来源 |
|------|---------|------|
| 生产 Bug 数量 | 减少 40-60% | Hoko Blog 2026 |
| 重构时间 | 降低 50% | Hoko Blog 2026 |
| 交付速度 | 提升 30% | Hoko Blog 2026 |
| 编程时间 | 减少 56% | Augment Code 2026 |
| 上市时间 | 缩短 30-40% | Augment Code 2026 |
| 开发成本（2年内） | 降低 20-30% | Cortex 2026 |

## Connections

- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — 核心引用来源
- [[sdd/sources/github-blog-spec-kit|GitHub Blog: Spec Kit 介绍]] — Spec Kit 官方阐述
- [[sdd/entities/Spec-Kit]] — GitHub 官方工具包
- [[sdd/entities/OpenSpec]] — Brownfield-First 轻量框架
- [[sdd/entities/Superpowers]] — TDD + Skills 框架
- [[sdd/entities/Kiro]] — AWS IDE 集成方案
- [[sdd/entities/Tessl]] — Spec-as-Source 实验平台
- [[sdd/comparisons/framework-comparison|五大框架对比]] — 更详细的维度比较
