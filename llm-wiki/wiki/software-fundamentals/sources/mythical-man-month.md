---
title: "The Mythical Man-Month"
type: source
tags: [software-engineering, project-management, team-dynamics, Brooks-law]
last_updated: "2026-04-30"
source_file: raw/software-fundamentals/refs/frederick-brooks-official-site.md
source_url: https://www.cs.unc.edu/~brooks/
---

## Summary

《人月神话》是软件工程领域的里程碑著作，提出"增加人手到延误的软件项目只会让它更加延误"这一经典论断。Brooks 通过 IBM System/360 和 OS/360 的项目管理经验，论证了**软件项目的复杂性源于人的因素而非技术因素**，指出进度与人数的等价假设（人月）是一个危险的隐喻。

## Key Claims

- **Brooks 法则** — "Adding manpower to a late software project makes it later." 增加人力只在任务可完全分解时有效，否则只会增加沟通成本和协调开销。
- **妊娠期不可压缩** — 砍掉进度的唯一方式是减少范围，而不是增加人手。系统构建有其固有的"妊娠期"。
- **沟通成本呈二次方增长** — n 个人的团队有 n(n-1)/2 条沟通路径，人数增加导致指数级复杂度。
- **外科手术团队模式** — 高效团队像一个外科手术团队，主刀负责核心决策，其他成员执行特定任务。
- **第二系统效应** — 设计师的第二个系统往往是过度设计的——他们有太多想法和太少约束。
- **没有银弹**（No Silver Bullet）—— 软件工程不存在能十倍提升生产力的单一技术突破，因为软件复杂性的本质属性（essential complexity）来自问题本身。

## Key Quotes

> "The bearing of a child takes nine months, no matter how many women are assigned." — Frederick P. Brooks, Jr.

> "The management question is not how to add manpower, but how to sequence and link the tasks so that the critical chain is shortened as much as possible by adding resources." — Frederick P. Brooks, Jr.

## Connections

- [[software-fundamentals/sources/domain-driven-design|Domain-Driven Design]] — DDD 的战略设计思想与 Brooks 强调的"先设计架构再分配人力"理念一致
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — Thomas & Hunt 在团队协作章节多处引用 Brooks 的观点

> **注意**：《人月神话》20 周年版完整 PDF 未在本次收集范围内，本页基于 Brooks 教授 UNC 主页的出版物列表编写。