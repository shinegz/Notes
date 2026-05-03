---
title: "Orthogonality"
type: concept
sources:
  - software-fundamentals/sources/pragmatic-programmer-20th-anniversary
last_updated: "2026-05-01"
---

## 一句话理解

正交性（Orthogonality）要求**改变一个组件不影响其他组件**——组件之间相互独立，各司其职。

## 边界

- 正交不是"分离关注点"。分离是手段，正交是效果。
- 正交不是"模块化"。模块化可能产生高内聚但非正交的耦合。
- 正交是**系统属性**。组件自身无法判断是否正交，只有在系统中与其他组件的关系才能判断。
- 正交与 DRY 互为因果。正交组件不重复知识，知识不重复的组件更可能正交。

## 核心机制

### 正交性的三个层级

| 层级 | 描述 | 违反后果 |
|------|------|----------|
| **架构层** | 子系统边界清晰，依赖单向 | 循环依赖、级联修改 |
| **模块层** | 类/函数职责单一 | God Object、频繁修改 |
| **接口层** | API 契约稳定 | 破坏性变更、版本撕裂 |

### 正交与非正交的对比

| 场景 | 非正交 | 正交 |
|------|--------|------|
| 改动数据库 | 需改业务逻辑 | 只需改 Repository 层 |
| 改动 UI | 需改后端逻辑 | 前后端通过 API 解耦 |
| 改动配置 | 需重新编译 | 配置与代码分离 |
| 增加功能 | 需修改核心代码 | 插件式扩展 |

### 检验方法

- **独立测试** — 每个组件可以不依赖其他组件独立测试
- **独立部署** — 每个组件可以独立发布，不影响其他组件
- **独立修改** — 改变一个组件不需要了解其他组件的内部

## 关联概念

- [[software-fundamentals/concepts/DRY|DRY]] — 知识单一表达是正交的基础
- [[software-fundamentals/concepts/SoftwareArchitecture|Software Architecture]] — 架构决策决定了系统的正交性基线

## 来源

- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — "Orthogonality" 章节系统阐述