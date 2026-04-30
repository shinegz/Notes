---
title: "Domain-Driven Design"
type: source
tags: [domain-driven-design, software-design, architecture, tactical-design, strategic-design]
last_updated: "2026-04-30"
source_file: raw/software-fundamentals/pdfs/ddd-fulldraft.pdf
source_url: https://www.domainlanguage.com/ddd/
---

## Summary

Domain-Driven Design (DDD) 是一套通过**深度理解业务领域**来指导软件设计的思想框架，核心理念是让**领域模型**与**代码实现**保持紧密绑定。DDD 将复杂系统拆分为**限界上下文**（Bounded Context），用**统一语言**（Ubiquitous Language）弥合领域专家与开发团队之间的沟通鸿沟，从而在系统核心部分建立清晰、富有表达力的模型。

## Key Claims

- **模型驱动设计**（Model-Driven Design）—— 代码结构必须反映领域模型，模型不是文档，是活的代码。
- **限界上下文**（Bounded Context）—— 每个模型有明确的适用范围，上下文之间通过**上下文地图**（Context Map）显式描述集成关系。
- **战术构建块**（Tactical Building Blocks）—— Entity、Value Object、Aggregate、Domain Event、Service、Repository、Factory 等模式提供了建模工具箱。
- **战略设计优先于战术设计** —— 在引入具体模式之前，必须先通过**子域划分**（Core Domain / Supporting Domain / Generic Domain）和上下文边界确定系统结构。
- **持续集成**（Continuous Integration）—— 防止上下文漂移，保持模型的内部一致性。

## Architecture Table

| Part | 主要内容 |
|------|----------|
| Part I. Putting the Domain Model to Work | Ubiquitous Language、Artifacts and Context、Isolating the Domain |
| Part II. The Building Blocks of Model-Driven Design | Entity、Value Object、Services、Modules、Aggregates、Factories、Repositories |
| Part III. Refactoring Toward Deeper Insight | Bringing Down the Heat、Distillation、Analysis Patterns |
| Part IV. Strategic Design | Bounded Contexts、Context Maps、Continuous Integration、Anticorruption Layer 等集成模式 |
| Part V. Conclusions | 总结与展望 |

## Key Quotes

> "The model is the glue. It is the place where the detail is captured and organized in a way that it can be effectively used in the construction of the software." — Eric Evans

> "A bounded context is a conceptual boundary in which a particular model is applicable and consistent." — Eric Evans

## Connections

- [[software-fundamentals/sources/mythical-man-month|The Mythical Man-Month]] — Brooks 的项目管理和"No Silver Bullet"观点与 DDD 的战略设计思想相互呼应
- [[software-fundamentals/sources/pragmatic-programmer-20th-anniversary|The Pragmatic Programmer]] — Thomas & Hunt 的务实编程哲学与 DDD 的代码模型绑定理念有交集

> **注意**：DDD 官网（domainlanguage.com）需要交互访问，本次为基于 PDF 摘要的 source 页。