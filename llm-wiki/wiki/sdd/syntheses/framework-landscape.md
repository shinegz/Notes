---
title: "SDD 框架全景分析"
type: synthesis
tags: [sdd, framework, landscape, synthesis]
last_updated: 2026-04-29
---

## Epitome

2025-2026 年的 SDD 框架生态呈现"金字塔"结构：底层是大量未命名的 Vibe Coding + 简单 Spec 实践，中层是五大主流框架（Spec Kit、OpenSpec、Superpowers、Kiro、Tessl）的差异化竞争，顶层是 Spec-as-Source 的激进实验。框架之间的核心分歧不是"要不要规范"，而是"规范应该活多久"和"谁来维护规范"。

## 概念地图

```
                    Spec-as-Source
                         |
            Tessl ───────┼─────── 规范即代码
                         |
                   Spec-Anchored
                         |
       Superpowers ──────┼─────── 规范长期维护
       Compound Eng. ────┤
                         |
                    Spec-First
                         |
    Spec Kit ────────────┼─────── 规范用完即弃
    OpenSpec ────────────┤
    Kiro ────────────────┤
                         |
              Vibe Coding ─────── 无规范
```

## 关系表

| 框架 | SDD 层级 | 核心机制 | 技术栈 | 适用场景 |
|------|---------|---------|--------|---------|
| Spec Kit | Spec-First | 四阶段流水线（Specify→Plan→Tasks→Implement） | Markdown + Bash 模板 | 大型企业标准化 |
| OpenSpec | Spec-First | Brownfield-First，Spec 与代码同仓 | Markdown | 已有代码库演进 |
| Superpowers | Spec-Anchored | Agentic Skills + 强制 TDD + 双阶段审查 | Markdown (SKILL.md) | 质量优先的个人/小团队 |
| gstack | Spec-Anchored | 23 专家角色 + 浏览器 Daemon + 并行 Sprint | Bun/TS + Markdown | 高吞吐量 solo builder |
| Compound Engineering | Spec-Anchored | Skills + Agents + 知识复利 + 跨平台转换 | Bun/TS + Markdown | 多平台团队 |
| Kiro | Spec-First | IDE 集成三文件工作流（Req→Design→Tasks） | VS Code 扩展 | AWS 生态用户 |
| Tessl | Spec-as-Source | 规范即代码，单向生成 | 专有平台 | 前沿实验者 |

## 框架级误区

- **"用 Spec Kit 做所有项目"** — Martin Fowler 团队指出 Spec Kit 对 3-5 点故事是"用大锤敲坚果"，过度流程是创造力的敌人
- **"规范越详细 AI 越听话"** — 规范详细程度与 AI 遵从度无线性关系，冗长规范反而增加审查负担
- **"SDD 只适用于新项目"** — OpenSpec、Compound Engineering、gstack 都强调 Brownfield-First，已有代码库才是主战场
- **"所有框架做的事情一样"** — 从 Spec-First 到 Spec-as-Source，从 Skills 框架到 IDE 集成，设计哲学差异巨大

## 实践集成

### 渐进式 Spec 策略

| 项目阶段 | 代码规模 | 推荐策略 | 工具 |
|---------|---------|---------|------|
| 原型验证 | < 1000 行 | Vibe Coding，别折腾 | Claude Code / Cursor 裸用 |
| 功能迭代 | 1000-10000 行 | 轻量 Spec + TDD | OpenSpec / Superpowers |
| 系统构建 | > 10000 行 | 完整 SDD 流水线 | Spec Kit / Kiro |
| 已有代码库改造 | 任意 | Brownfield-First | OpenSpec / Compound Engineering |

### 技能框架的选择

| 需求 | 推荐框架 | 原因 |
|------|---------|------|
| 强制 TDD | Superpowers | RED-GREEN-REFACTOR 是核心哲学 |
| 并行多 Sprint | gstack | Conductor + 10-15 并行 |
| 跨平台一致性 | Compound Engineering | 转换器确保各平台行为一致 |
| 浏览器自动化 | gstack | Chromium Daemon + Ref 系统 |
| 零依赖轻量 | Superpowers | 不引入任何第三方依赖 |
| 知识复利 | Compound Engineering | /ce-compound 自动记录 |

## Navigation Pointers

- 详情见 [[sdd/concepts/Spec-First|Spec-First 概念页]]
- 详情见 [[sdd/concepts/Spec-Anchored|Spec-Anchored 概念页]]
- 详情见 [[sdd/concepts/Spec-as-Source|Spec-as-Source 概念页]]
- 详情见 [[sdd/comparisons/framework-comparison|五大框架详细对比]]
- 源码分析见 [[sdd/entities/Superpowers|Superpowers 实体页]]
- 源码分析见 [[sdd/entities/Gstack|Gstack 实体页]]
- 源码分析见 [[sdd/entities/Compound-Engineering|Compound Engineering 实体页]]
