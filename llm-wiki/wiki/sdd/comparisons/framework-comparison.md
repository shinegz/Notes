---
title: "五大 SDD 框架对比"
type: comparison
tags: [sdd, comparison, spec-kit, openspec, superpowers, kiro, tessl]
last_updated: 2026-04-29
---

## Framing

本文从 **SDD 层级、工具兼容、学习成本、适用项目、强制约束、社区活跃度、核心哲学** 七个维度，比较当前五大主流 SDD 框架。

## 维度对比

### SDD 层级

| 框架 | 层级 | 说明 |
|------|------|------|
| Spec Kit | Spec-First | 规范随分支生命周期，不长期维护 |
| OpenSpec | Spec-First | 规范归档合并，可回溯但非活文档 |
| Superpowers | Spec-Anchored | Skills 体系使规范在多次会话中持续生效 |
| Kiro | Spec-First | 三文件工作流，任务完成即结束 |
| Tessl | Spec-as-Source | 规范是唯一源文件，代码为生成物 |

### 工具兼容

| 框架 | 兼容数量 | 限制 |
|------|---------|------|
| Spec Kit | 17+ | 无特别限制 |
| OpenSpec | 20+ | 无特别限制 |
| Superpowers | 5+ | 深度绑定 Claude Code，其他平台支持较浅 |
| Kiro | 1 | 仅 VS Code IDE |
| Tessl | 1 | 专有平台 |

### 学习成本

| 框架 | 成本 | 原因 |
|------|------|------|
| Spec Kit | 中 | 四阶段流程有明确文档 |
| OpenSpec | 低 | 轻量灵活，不强制完整流水线 |
| Superpowers | 中高 | TDD + 双阶段审查需要理解其哲学 |
| Kiro | 低 | IDE 原生，学习曲线最平缓 |
| Tessl | 高 | Spec-as-Source 需要全新心智模型 |

### 适用项目

| 框架 | 最佳场景 | 不适合 |
|------|---------|--------|
| Spec Kit | 大型团队新项目 | 小修小改、已有代码库 |
| OpenSpec | 已有代码库持续演进 | 从零开始的全新架构 |
| Superpowers | 中型项目、质量优先 | 快速原型、非 Claude Code 用户 |
| Kiro | 各规模（但 IDE 内） | 非 VS Code 用户、需要灵活调整 |
| Tessl | 前沿实验 | 生产环境、团队协 |

### 强制约束

| 框架 | 约束强度 | 机制 |
|------|---------|------|
| Spec Kit | 强 | 检查清单 + Constitution |
| OpenSpec | 弱 | 可选规范，依赖团队纪律 |
| Superpowers | 强 | 强制 TDD + 双阶段审查 |
| Kiro | 中 | 三阶段流程，但可跳过 |
| Tessl | 极强 | 人类不触碰代码 |

### 社区活跃度

| 框架 | Stars | 活跃度 |
|------|-------|--------|
| Spec Kit | 50,000+ | 高，但已有维护质疑 |
| OpenSpec | 未披露 | 中 |
| Superpowers | 未披露 | 中高，Discord 活跃 |
| Kiro | 未披露 | 中（AWS 背书） |
| Tessl | 未披露 | 低（Private Beta） |

### 核心哲学

| 框架 | 一句话 |
|------|--------|
| Spec Kit | "意图是真相" |
| OpenSpec | "Brownfield-First" |
| Superpowers | "TDD + Skills = 质量" |
| Kiro | "Spec 即 super-prompt" |
| Tessl | "规范即代码" |

## Decision Context

### 如果你是...

- **Claude Code 重度用户，追求代码质量** → **Superpowers**（TDD 强制约束 + Skills 可组合）
- **Solo builder，需要虚拟团队** → **gstack**（23 专家角色 + 浏览器 + 并行 Sprint）
- **多工具混用团队** → **OpenSpec**（轻量、兼容性好、Brownfield-First）
- **大型企业，需要标准化** → **Spec Kit**（GitHub 官方背书、完整流水线）
- **已有代码库，需要知识复利** → **Compound Engineering**（80/20 规划 + 跨平台）
- **愿意押注前沿** → **Tessl**（Spec-as-Source 实验）

### 项目规模匹配

| 规模 | 推荐 |
|------|------|
| < 1000 行原型 | Vibe Coding（无框架） |
| 1000-10000 行 | OpenSpec / Superpowers |
| > 10000 行新系统 | Spec Kit / Kiro |
| 任意 Brownfield | OpenSpec / Compound Engineering |

## Sources

- [[sdd/sources/zhihu-sdd-landscape|知乎：SDD 框架全景]] — 五大框架横评的核心数据来源
- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — Kiro、Spec Kit、Tessl 的深度评测
- [[sdd/entities/Superpowers|Superpowers 实体页]] — 源码级分析
- [[sdd/entities/Gstack|Gstack 实体页]] — 源码级分析
- [[sdd/entities/Compound-Engineering|Compound Engineering 实体页]] — 源码级分析
