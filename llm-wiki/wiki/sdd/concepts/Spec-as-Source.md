---
title: "Spec-as-Source"
type: concept
tags: [sdd, spec-as-source, mdd, code-generation]
sources:
  - sdd/sources/martin-fowler-sdd-3-tools
last_updated: 2026-04-29
---

## 一句话理解

Spec-as-Source 是将规范作为唯一源文件，人类只编辑规范，代码完全由 AI 从规范自动生成，实现"意图即代码"的终极形态。

## 背景

Spec-as-Source 是 SDD 的最激进层级，也是争议最大的层级。它试图回答一个问题：如果 AI 足够可靠，为什么人类还需要直接编辑代码？Tessl 是目前唯一明确探索这一层级的商业化平台。

## 核心机制

Spec-as-Source 的运行模式是**单向生成**：

1. **人类只写规范** — 使用结构化自然语言描述功能、接口和行为
2. **AI 生成代码** — 运行构建命令（如 `tessl build`），AI 将规范翻译为代码
3. **代码标记为生成物** — 代码文件顶部标记 `// GENERATED FROM SPEC - DO NOT EDIT`
4. **变更循环** — 需要修改时，人类编辑规范，重新生成代码

### Tessl 的 Spec 结构示例

Tessl 的规范使用 `@generate`、`@test` 等标签指示 AI 生成内容，API 部分定义对外暴露的接口以确保关键部分受控。

## 与 MDD 的历史平行

Spec-as-Source 与 2000 年代的 **Model-Driven Development（MDD）** 有惊人相似：

| 维度 | MDD（2000s） | Spec-as-Source（2020s） |
|------|-------------|------------------------|
| 抽象层 | UML / 自定义 DSL | 结构化自然语言 |
| 代码生成 | 自定义代码生成器 | LLM |
| 约束 | 预定义、可解析的语言 | 自然语言的灵活性 |
| 工具支持 | 丰富的 IDE 辅助（验证、补全） | 有限（LLM 非确定性） |
| 失败原因 | 抽象层级笨重、约束过多 | 待观察 |

Martin Fowler 的评价是：Spec-as-Source 可能**兼具 MDD 和 LLM 的缺点——不灵活性 + 非确定性**。

## 现实挑战

- **非确定性** — 同一规范多次生成可能产生不同代码
- **低抽象层级的 overhead** — Tessl 目前按文件级生成规范，规范粒度很细
- **调试困难** — Bug 在代码中，但修复入口在规范中，心智模型需要转换
- **工具支持缺失** — MDD 时代有 UML 工具辅助写规范，自然语言规范缺乏同等工具支持

## 关联概念

- [[sdd/concepts/Spec-First|Spec-First]] — 最基础层级
- [[sdd/concepts/Spec-Anchored|Spec-Anchored]] — 中间层级，规范与代码并存

## 来源

- [[sdd/sources/martin-fowler-sdd-3-tools|Martin Fowler: SDD 三工具评测]] — 定义 Spec-as-Source 并对比 MDD 历史
- [[sdd/sources/zhihu-sdd-landscape|知乎：SDD 框架全景]] — 对 Tessl 路线的谨慎观望态度
