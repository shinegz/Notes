---
title: "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl"
type: source
tags: [sdd, spec-first, spec-anchored, spec-as-source, kiro, spec-kit, tessl]
last_updated: 2026-04-29
source_file: raw/sdd/articles/martin-fowler-sdd-3-tools.md
source_url: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
---

## Summary

SDD（Spec-Driven Development）目前仍是一个语义扩散中的术语，但核心可归纳为三个递进层级：Spec-First（先写规范再编码）、Spec-Anchored（规范长期维护用于演进）、Spec-as-Source（规范即唯一源文件，人类不触碰代码）。Birgitta Böckeler 通过深度实测 Kiro、Spec Kit、Tessl 三个工具后发现，大多数框架停留在 Spec-First 层级，且存在工作流与问题规模不匹配、审查负担过重、AI 可控性有限等现实挑战。

## Key Claims

- **SDD 有三个递进层级，但多数工具仅实现第一层** — Spec-First（规范可丢弃）→ Spec-Anchored（规范长期维护）→ Spec-as-Source（规范即代码）。目前 Kiro、Spec Kit 主要停留在 Spec-First，仅 Tessl 明确探索 Spec-as-Source。
- **Spec 应定义为行为导向的结构化自然语言制品** — 最接近 PRD（产品需求文档），区别于通用的 Memory Bank（项目上下文、规则文件）。
- **现有工具的"一刀切"工作流难以适应不同问题规模** — 用 Kiro 修小 Bug 会产生 16 条 acceptance criteria，用 Spec Kit 做 3-5 点故事会生成大量 Markdown 文件，"用大锤敲坚果"。
- **审查 Markdown 可能比审查代码更耗时** — Spec Kit 生成了大量重复、冗长的 Markdown 文件，"I'd rather review code than all these markdown files"。
- **规范详细程度与 AI 遵从度无线性关系** — AI 仍会忽略指令或过度执行，更大的上下文窗口不等于更好的指令遵循。
- **Spec-as-Source 与 MDD 有历史平行** — 2000 年代的模型驱动开发（MDD）曾承诺"画 UML 生成代码"，最终失败于抽象层级笨重和约束过多。LLM 消除了 MDD 的部分约束，但引入了非确定性风险，可能"兼具两者的缺点：不灵活 + 非确定性"。
- **SDD 可能是 "Verschlimmbesserung"** — 德语"越改越坏的改进"，在试图用更多流程解决流程问题时，可能放大现有挑战。

## Key Quotes

> "The past has shown that the best way for us to stay in control of what we're building are small, iterative steps, so I'm very skeptical that lots of up-front spec design is a good idea." — 对前期大量规范设计的怀疑

> "Are we making something worse in the attempt of making it better?" — 对 SDD 工具现状的核心质疑

## Connections

- [[sdd/sources/github-blog-spec-kit|GitHub Blog: Spec Kit 介绍]] — GitHub 官方对 Spec Kit 的阐述，本文对其做了独立实测验证
- [[sdd/sources/zhihu-sdd-landscape|知乎：SDD 框架全景]] — 本文是该知乎文章的核心引用来源之一
- [[sdd/concepts/Spec-First]] — 本文定义的 SDD 第一层级
- [[sdd/concepts/Spec-Anchored]] — 本文定义的 SDD 第二层级
- [[sdd/concepts/Spec-as-Source]] — 本文定义的 SDD 第三层级
- [[sdd/entities/Kiro]] — AWS 推出的轻量级 SDD IDE
- [[sdd/entities/Spec-Kit]] — GitHub 官方 SDD 工具包
- [[sdd/entities/Tessl]] — 探索 Spec-as-Source 路线的商业化平台
