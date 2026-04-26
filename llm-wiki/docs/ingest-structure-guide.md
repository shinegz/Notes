# Wiki 成稿结构指南（Ingest Structure Guide）

> llm-wiki 成稿的**结构层**指南：定义页面类型、认知功能、结构模型与原子化约束。
> 与 `ingest-style-guide.md`（风格层）配合使用：先确定"写什么类型、按什么结构"，再润色"怎么写得好"。

---

## 1. 核心原则

### P1: 类型由认知功能决定，不是由主题领域决定

不按"技术/算法/历史"分类，按"读者想用这个页面做什么"分类。

### P2: 一个页面，一个认知任务（原子化）

- `concepts/` 页只解释**一个**概念
- `syntheses/` 页只综合**一个**框架、问题或过程
- `comparisons/` 页只比较**一组**替代方案

### P3: 结构服从功能

页面的信息组织顺序由其认知目的推导，不是由惯例或模板推导。

### P4: 认知加载顺序（Epitome → Boundary → Detail → Connection）

读者需要先获得心智模型（schema），才能挂载细节。每种类型的页面必须以 epitome（一句话概括）开头。

---

## 2. 类型系统

### 2.1 页面类型总览

| 目录 | 读者的问题 | 认知功能 | 命名规范 | 必需 frontmatter |
|------|-----------|---------|---------|-----------------|
| `sources/` | "这篇 source 说了什么？" | **参考** | kebab-case.md | `type: source`, `source_file` |
| `entities/` | "这个实体是什么？" | **参考**（事实性） | TitleCase.md | `type: entity` |
| `concepts/` | "这个概念是什么？怎么工作？" | **解释** | TitleCase.md | `type: concept` |
| `syntheses/` | — 见 2.2 — | **综合** | kebab-case.md | `type: synthesis` |
| `comparisons/` | "X 和 Y 有什么区别？怎么选？" | **比较** | kebab-case.md | `type: comparison` |
| `index.md` | "有哪些页面？" | **目录** | — | 无 frontmatter |
| `overview.md` | "这个门类有什么？从哪开始？" | **导航** | — | `type: overview` |

### 2.2 综合页（syntheses/）的三种体裁

所有综合页都写在 `syntheses/`，但写作前必须先确定**主体裁**：

| 体裁 | 读者的问题 | 示例 |
|------|-----------|------|
| **框架综合** | "这些概念怎么关联？" | `ai-core-concepts.md`（认知框架） |
| **证据综合** | "关于这个问题，sources 怎么说？" | `harness-engineering-deep-dive.md` |
| **叙事综合** | "这个过程是怎么发生的？" | `token-lifecycle.md` |

**混合体裁规则**：允许在主体裁中嵌入其他体裁的元素（如证据综合开头用一个叙事钩子），但必须先确定主体裁，混合才有意图。

---

## 3. 类型决策流程

```
页面是关于单个外部 source 的摘要？
  YES → sources/

页面是关于一个事实实体（组织、人物、产品）？
  YES → entities/

页面是深入解释**一个**概念？
  YES → concepts/

页面是中性地比较多个替代方案？
  YES → comparisons/

页面是综合多个 sources/concepts？
  YES → syntheses/（再选体裁）：
    ├─ 展示概念之间的关系？     → 框架综合
    ├─ 用证据回答一个问题？     → 证据综合
    └─ 带读者走一遍过程？       → 叙事综合

页面是列出 shelf 中所有页面？
  YES → index.md

页面是提供 shelf 级别的认知地图？
  YES → overview.md
```

---

## 4. 结构模型

以下不是"固定段落模板"，而是**认知加载顺序**——信息应该按这个顺序呈现，以最小化外在认知负荷、最大化 schema 建构。

### 4.1 `concepts/` — 解释型

**认知功能**：帮读者建立对单一概念的正确心智模型。

**结构序列**：

```
1. Epitome（一句话心智模型）
   → 给读者挂细节的"钩子"
   → 例："Attention = Query × Key^T × Value，衡量「我应该关注什么」"

2. Boundary Clarification（不是什么 vs 是什么）
   → 防止挂错钩子
   → 例："LLM 不是搜索引擎，不是知识库——它只是预测下一个 token 的分布"

3. Mechanism / Principle（机制/原理）
   → 往钩子上挂核心细节
   → 可用公式、代码、图示辅助

4. Types / Variants / Applications（可选）
   → 扩展 schema 的边界

5. Connections
   → [[wikilink]] 到相关概念和来源

6. Sources
   → 验证 schema 来源
```

**原子化约束**：
- 只能解释**一个**概念
- 如果写到一半需要解释另一个概念，停止，用 `[[wikilink]]` 指向其 concept 页
- 目标长度：50-150 行

**好例子**：`wiki/ai-fundamentals/concepts/attention-mechanism.md` — 63 行，只讲 Attention，机制 → 类型 → 来源，不溢出。

---

### 4.2 `syntheses/` 框架综合

**认知功能**：展示多个概念如何构成一个系统或认知地图。

**结构序列**：

```
1. Epitome（关系的一句话概括）
   → 地图总览
   → 例："AI 核心概念分为 LLM 系统和 Agent 系统，通过推理引擎集成"

2. Concept Map / Diagram
   → 可视化关系
   → 用 SVG/Mermaid，不是文字堆砌

3. Relationship Table（推荐）
   → 系统性地展示概念间关系
   → 例：概念 × 来源定义 × 关联概念 × 关键关联

4. Boundary Clarifications（框架级误区）
   → 防止读者从框架层面理解偏
   → 例："LLM '理解'语言 = 只是统计关系，不是真正的理解"

5. Practical Integration（可选）
   → 框架在实践中的体现
   → 例：Agent 调用链路时序图

6. Navigation Pointers
   → "详情见 [[concepts/X]]"
   → 明确告诉读者哪里找细节
```

**铁律：只讲关系，不讲概念本身**。框架综合是**地图**，不是**百科全书**。如果某个概念需要解释，它应该有独立的 `concepts/` 页面。

**反例**：`ai-core-concepts.md` 原稿 — 414 行，其中 18 个"核心概念逐个解析"是严重的 scope violation，把 concept 页的内容重复了一遍。

**目标长度**：80-150 行（纯框架内容，不含导航）。

---

### 4.3 `syntheses/` 证据综合

**认知功能**：通过多源交叉，回答一个明确的问题。

**结构序列**（基于 Toulmin 论证模型）：

```
1. Framing Question（综合问题）
   → 本文要回答什么？
   → 例："Harness Engineering 的核心构件有哪些？"

2. Source Landscape（证据版图）
   → 有哪些 sources 涉及这个问题？
   → 简要说明每个 source 的立场/贡献

3. Convergence（共识点）
   → sources 在哪里一致？
   → 例："多文共识：Agent = Model + Harness"

4. Divergence / Contradictions（分歧点）
   → sources 在哪里不一致？
   → 使用 [[Contradictions]] 块标注

5. Synthesis（结论）
   → 基于证据，我们能回答这个问题吗？
   → 如果证据不足，明确说"目前无定论"

6. Implications（可选）
   → 这个结论意味着什么？

7. Sources
   → 完整来源列表，带 [[wikilink]]
```

**约束**：
- 每个实质性主张必须有 source 支撑
- 内联引用格式：`Anthropic 发现...（[[sources/anthropic-long-running|source]]）`
- 不允许无 source 的泛化判断

**好例子**：`harness-engineering-deep-dive.md` — 每个构件都有明确的 source 归属，用表格呈现多源共识。

---

### 4.4 `syntheses/` 叙事综合

**认知功能**：通过具体旅程让读者理解一个过程。

**结构序列**：

```
1. Hook / Scenario（为什么关心）
   → 建立动机和情境
   → 例："你输入'中国的首都是什么'，LLM 回复'北京'。这个过程是怎么发生的？"

2. Step-by-Step Journey（一步步发生什么）
   → 用具体例子带读者走过程
   → 每步配示意图或代码片段
   → 避免抽象描述

3. Why It Works（底层原理）
   → 走完旅程后，解释背后的机制
   → 此时读者有 concrete experience，能挂住理论

4. Connections
   → 指向相关 concept 页和 source 页
```

**约束**：
- 必须是**具体**的，不能是抽象的步骤罗列
- 一个例子贯穿始终，不要中途换例子
- 目标读者是"第一次了解这个过程的人"

**好例子**：`token-lifecycle.md` — 用"中国的首都是什么"这个单一例子，从 Tokenization 走到 Auto-Regressive，每步都有可视化。

---

### 4.5 `comparisons/` — 比较型

**认知功能**：中立呈现替代方案的差异，让读者自己判断。

**结构序列**：

```
1. Framing
   → 比较对象 + 比较维度
   → 例："本文从架构、性能、适用场景三个维度比较 RAG 与 Fine-tuning"

2. Dimension-by-Dimension Comparison
   → 每个维度下并排呈现
   → 用表格增强可扫描性
   → ❌ 禁用"更好/更差" framing
   → ✅ 用"A 在 X 上强，B 在 Y 上强"

3. Decision Context
   → "如果你需要 X，考虑 A；如果你需要 Y，考虑 B"
   → 条件匹配，不是推荐排序

4. Sources
```

**与证据综合的区别**：
- 证据综合可以得出结论（"sources 支持 X"）
- 比较页必须保持中立（"X 和 Y 各有适用场景"）

---

### 4.6 `sources/` — 参考型

**认知功能**：准确总结和索引一篇外部来源。

**结构**：完整规范见 **`docs/source-template.md`**。

**约束**：
- Summary 和 Claims 必须用作者自己的话，不是你的解读
- Claims 必须能在 source 中找到对应

---

### 4.7 `entities/` — 实体参考型

**认知功能**：提供关于一个实体的客观事实。

**结构序列**：

```
1. Definition（一句话定义）
2. Key Attributes（关键属性/事实）
3. Relationships（与其他实体、概念、来源的关系）
4. Sources
```

**约束**：
- 只陈述可验证的事实
- 不写评价、不写"重要意义"

---

### 4.8 `overview.md` — 导航型

**认知功能**：为整个 shelf 提供认知地图和阅读路径。

**结构序列**：

```
1. One-sentence Summary（shelf 的一句话概括）
2. Knowledge Map / Diagram
   → Mermaid 或 SVG，展示 shelf 内核心概念的关系
3. Key Entry Points（推荐阅读顺序）
   → "从 [[concepts/X]] 开始，然后..."
4. Topic Organization（shelf 的组织逻辑）
5. Timeline（可选，如果该领域有明确演进线）
6. Next Steps
```

**与框架综合的区别**：
- `overview.md` = **shelf 级别**的广度地图（导航功能）
- 框架综合 = **主题级别**的深度关系（某个具体话题的概念关联）

---

### 4.9 `index.md` — 目录型

**认知功能**：列出 shelf 中的所有页面，便于查找。

**结构**：

```
1. Shelf 一句话描述
2. Sources by topic（按主题分组列出 sources）
3. Concepts list
4. Syntheses list
5. Comparisons list（如有）
6. See also（指向 overview.md、上级 index.md）
```

**约束**：
- 只列链接，不加解释
- 不重复 source 的摘要内容

---

## 5. 原子化约束（Atomicity Rules）

### 5.1 通用规则

- **一个页面只处理一个认知单元**
- 如果写作者发现自己在同一页里处理两个独立的概念/问题/过程，拆页
- 短而聚焦的页面 > 长而杂糅的页面

### 5.2 各类型原子化检查

| 类型 | 检查问题 |
|------|---------|
| `concepts/` | 我是否在解释**一个**概念？如果出现了"首先介绍 A，然后介绍 B"，拆成两页 |
| `syntheses/` 框架 | 我是否在重新解释单个概念？如果是，删掉，改链接到 `concepts/` |
| `syntheses/` 证据 | 我是否只回答**一个**综合问题？如果问题超过一个，拆页或收窄 |
| `syntheses/` 叙事 | 我是否只跟踪**一个**过程/例子？如果中途换例子，选一个贯穿始终 |
| `comparisons/` | 我是否在比较**一组**明确的替代方案？如果超过 4 个，考虑拆成多个比较或改用框架综合 |

### 5.3 范围失控的典型症状

如果你发现自己在写：
- "首先我们需要了解 X 的概念..." → 你在写 concept 解释，不该出现在 synthesis/comparison 中
- 一个页面超过 300 行 → 大概率包含了多个认知单元
- 页面中有"延伸阅读"或"Source 索引" → 这些是导航功能，属于 `index.md`

---

## 6. 正反例

### ✅ 好例子

**`concepts/attention-mechanism.md`** — 解释型典范
- 63 行，只讲 Attention
- Epitome → 公式 → 图解 → 类型对比表 → 来源
- 没有溢出到 Transformer 或 Embedding 的细节

**`syntheses/harness-engineering-deep-dive.md`** — 证据型典范
- 289 行，回答一个明确问题："Harness Engineering 是什么、为什么需要、怎么实现"
- 每个构件都有 inline source 引用
- 用表格呈现多源共识（Convergence）
- 用 2×2 矩阵展示分类框架

**`syntheses/token-lifecycle.md`** — 叙事型典范
- 210 行，跟踪一个 Token 的完整生命周期
- 用同一个例子（"中国的首都是什么"）贯穿始终
- 每步配 ASCII 图示或代码
- 最后才解释"为什么 LLM 能'理解'"

### ❌ 反例

**`syntheses/ai-core-concepts.md`（原稿）** — 范围失控
- 414 行，标为 `type: synthesis`，实际写成了 18 个 concept 解释的拼盘
- 18 个"核心概念逐个解析"每个都重复了 `concepts/` 页的内容
- Source 索引和延伸阅读属于导航功能，不该在 synthesis 中

**正确做法**：保留 30 秒心智模型、概念关系图、关系表、框架级误区，删掉所有单个概念的解释，用 `[[wikilink]]` 指向 concept 页。目标 80-120 行。

---

## 7. 迁移说明

### 7.1 旧指南 → 新指南

| 旧 `ingest-writing-guide.md` 内容 | 去向 |
|----------------------------------|------|
| 第 1 节"核心原则"（结论先行等） | → `ingest-style-guide.md` |
| 第 2 节"文章结构模式"（技术/算法/历史模板） | → **删除**，替换为本指南的类型系统 |
| 第 3 节"视觉增强" | → `ingest-style-guide.md` |
| 第 4 节"去 AI 味" | → `ingest-style-guide.md` |
| 第 5 节"成稿前自检" | → `ingest-style-guide.md` |

### 7.2 现有文章检查清单

当你修改或重写现有文章时，用这个清单判断是否需要调整类型或结构：

- [ ] 这个页面的 `type:` frontmatter 是否匹配其实际认知功能？
- [ ] 如果是 `syntheses/`，它的主体裁是什么？（框架/证据/叙事）
- [ ] 是否存在概念解释溢出？（ concept 解释出现在非 concept 页中）
- [ ] 页面是否超过 300 行？如果是，检查是否违反了原子化约束
- [ ] 是否包含导航内容（source 索引、延伸阅读）？如果是，移到 `index.md`

---

## 8. 与相关文档的关系

| 文档 | 职责 |
|------|------|
| `CLAUDE.md` | Schema：目录结构、命名规范、操作总览 |
| `ingest-structure-guide.md`（本文） | **结构层**：类型系统、认知加载顺序、原子化约束 |
| `ingest-style-guide.md` | **风格层**：表达质量、视觉增强、去 AI 味、自检清单 |
| `collect-workflow.md` | Collect 阶段工作流 |
| `tools/source_registry.tsv` | Source adapter 清单 |
