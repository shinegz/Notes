---
title: "Spec-Anchored"
type: concept
tags: [sdd, spec-anchored, specification, maintenance]
sources:
  - sdd/sources/martin-fowler-sdd-3-tools
  - sdd/sources/obra-superpowers
last_updated: 2026-04-29
---

## 一句话理解

Spec-Anchored 是在 Spec-First 的基础上，将规范保留为功能的长期"锚点"，后续所有变更（维护、演进、Bug 修复）都回到规范进行修改，而非直接修改代码。

## 背景

Spec-First 的问题在于规范是一次性的——任务完成后规范被丢弃，当功能需要演进时，需要重新编写新规范。这导致知识流失和重复工作。Spec-Anchored 试图让规范成为功能的"活文档"，随功能一起演进。

## 核心机制

Spec-Anchored 的核心是**规范即契约**——规范不是一次性的前置步骤，而是功能的长期治理工具。

1. **规范持久化** — 功能完成后，规范文件保留在代码库中，与代码并存
2. **变更回溯** — 当功能需要修改时，先修改规范，再由 AI 根据更新后的规范生成新代码
3. **双向同步** — 理想状态下，规范与代码保持同步，规范变更自动驱动代码变更
4. **版本治理** — 规范随功能版本一起演进，成为功能历史的可信记录

### 与 Spec-First 的关键区别

| 维度 | Spec-First | Spec-Anchored |
|------|-----------|---------------|
| 规范生命周期 | 任务级，可丢弃 | 功能级，长期维护 |
| 变更入口 | 直接修改代码 | 先修改规范 |
| 知识保留 | 低（规范丢弃） | 高（规范即文档） |
| 实施复杂度 | 低 | 中 |

## 现实挑战

- **规范与代码的同步成本** — 当人类直接修改代码时，规范容易过时
- **AI 非确定性** — 同一规范多次生成可能产生不同代码，破坏一致性
- **规范维护意愿** — 开发者倾向于直接改代码，而非先更新规范

## 关联概念

- [[sdd/concepts/Spec-First|Spec-First]] — Spec-Anchored 的基础层级
- [[sdd/concepts/Spec-as-Source|Spec-as-Source]] — 更激进的层级，规范是唯一源文件
- [[sdd/concepts/Agentic-Skills|Agentic Skills]] — Superpowers 的 Skills 体系接近 Spec-Anchored

## 来源

- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — 定义 Spec-Anchored 为 SDD 第二层级
- [[sdd/sources/obra-superpowers|Superpowers README]] — Skills 体系使规范在多次会话中持续生效
