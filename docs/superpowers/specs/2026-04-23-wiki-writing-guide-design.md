# llm-wiki Ingest Writing Guide Redesign

## Overview

Redesign `llm-wiki/docs/ingest-writing-guide.md` to fix three fundamental flaws:

1. **Type confusion**: The guide mixes `concepts/`, `syntheses/`, `sources/` guidance without distinguishing their cognitive functions
2. **Pseudo-templates**: Claims to be "principles not templates" but provides fixed structural patterns by topic domain (technical/algorithmic, conceptual/framework, historical/evolutionary)
3. **No atomicity constraint**: Lacks the "one page, one cognitive task" principle, leading to scope violations like `ai-core-concepts.md` (414 lines covering 18 concepts)

The new guide is based on cognitive science (Schema Theory, Cognitive Load Theory, Diátaxis documentation framework) and splits into two focused documents:
- `docs/ingest-structure-guide.md` — type system and structural models
- `docs/ingest-style-guide.md` — writing style and expression quality

---

## Problem Evidence

### Current `ingest-writing-guide.md` (excerpt)

```
> 不是固定段落模版，而是 Agent 在写 concepts/、syntheses/、实质性修订 overview.md 时的原则

## 2. 文章结构模式

### 2.1 技术/算法类
1. 问题是什么
2. 核心思想
3. 逐步拆解
4. 内部实现
5. 实际应用
6. 常见误区

### 2.2 概念/框架类
1. 30 秒心智模型
2. 不是什么 vs 是什么
3. 核心概念逐个解析
4. 概念间关系图
5. 何时使用/何时不用
```

**Flaw**: "Not fixed templates" is immediately contradicted by exactly that — fixed templates organized by topic domain, not reader cognitive task.

### `ai-core-concepts.md` — Scope Violation

Intended as a cognitive framework showing how AI core concepts relate. Actual content:
- 30-second mental model (correct, framework-level)
- **18 individual concept explanations** (scope violation — these belong in `concepts/`)
- Relationship table (correct, framework-level)
- Source index (belongs in `index.md`)
- Extended reading (navigation noise)

**Root cause**: The guide never defined what a "framework synthesis" should and should NOT contain. Without atomicity constraints, writers default to "explain everything here."

### `syntheses/` Type Confusion

Three articles, all labeled `type: synthesis`, serving completely different reader needs:

| Article | Actual Genre | Reader's Question |
|---------|-------------|-------------------|
| `ai-core-concepts.md` | Attempted **framework** | "How do these concepts relate?" |
| `token-lifecycle.md` | **Narrative** | "How does this process work?" |
| `harness-engineering-deep-dive.md` | **Evidence** | "What do sources say about harness engineering?" |

---

## Design Principles

### P1: Type by Cognitive Function, Not Topic Domain

Do not classify by "technical/algorithmic vs conceptual/framework vs historical." Classify by what the reader is trying to do.

### P2: One Page, One Cognitive Task (Atomicity)

From Andy Matuschak's Evergreen Notes: atomic notes permit incremental progress. Applied to wiki pages:
- A `concepts/` page explains **one** concept
- A `syntheses/` page synthesizes **one** framework, question, or process
- A `comparisons/` page compares **one** set of alternatives

### P3: Structure Follows Function

From Diátaxis: the structure of a page should be derived from its cognitive purpose, not from convention. A concept page builds schemas; a synthesis page argues or maps; a source page references.

### P4: Cognitive Loading Sequence

From Schema Theory (Piaget/Anderson) and Elaboration Theory (Reigeluth): readers need a schema (mental model) before details can be attached. Every page type must start with an epitome that provides this schema.

---

## Type System

| Directory | Reader's Question | Cognitive Function | Naming |
|-----------|-------------------|-------------------|--------|
| `sources/` | "What did this source say?" | **Reference** | kebab-case.md |
| `entities/` | "What is this entity?" | **Reference** (factual) | TitleCase.md |
| `concepts/` | "What is this concept and how does it work?" | **Explanation** | TitleCase.md |
| `syntheses/` | — see three genres below — | **Synthesis** | kebab-case.md |
| `comparisons/` | "How do X and Y differ? Which fits when?" | **Comparison** | kebab-case.md |
| `index.md` | "What pages exist in this shelf?" | **Catalog** | — |
| `overview.md` | "What's in this shelf and where do I start?" | **Navigation** | — |

### Synthesis Genres

All three live in `syntheses/`. The writer must decide the primary genre before writing.

| Genre | Reader's Question | Example |
|-------|-------------------|---------|
| **Framework** | "How do these concepts relate?" | Intended `ai-core-concepts.md` |
| **Evidence** | "What do sources say about Q?" | `harness-engineering-deep-dive.md` |
| **Narrative** | "How does this process work?" | `token-lifecycle.md` |

### Type Decision Flowchart

```
Is the page about a single external source?
  YES → sources/

Is the page about a factual entity (org, person, product)?
  YES → entities/

Is the page explaining exactly ONE concept in depth?
  YES → concepts/

Is the page comparing alternatives neutrally?
  YES → comparisons/

Is the page synthesizing multiple sources/concepts?
  YES → syntheses/ (then choose genre):
    ├─ Showing how concepts relate? → Framework
    ├─ Answering a question with evidence? → Evidence
    └─ Walking through a process? → Narrative

Is the page listing all pages in a shelf?
  YES → index.md

Is the page providing a shelf-level cognitive map?
  YES → overview.md
```

---

## Structural Models

These are **not templates**. They are cognitive loading sequences — the order in which information should be presented to minimize extraneous cognitive load and maximize schema construction.

### `concepts/` — Explanation Type

**Purpose**: Build a correct mental schema for one concept.

**Structure**:
```
1. Epitome (one-sentence mental model)
   → Provides the schema hook

2. Boundary Clarification (what it's NOT vs what it IS)
   → Prevents incorrect schema attachment

3. Mechanism / Principle
   → Attaches details to the schema

4. Types / Variants / Applications (optional)
   → Extends the schema

5. Connections
   → Links to related schemas (wikilinks)

6. Sources
   → Verifies schema provenance
```

**Constraint**: Explain exactly one concept. If you find yourself explaining other concepts in depth, stop and link to their concept pages instead.

**Good example**: `wiki/ai-fundamentals/concepts/attention-mechanism.md` (63 lines, one concept, clear mechanism → types → sources)

---

### `syntheses/` Framework Genre

**Purpose**: Show how multiple concepts fit together as a coherent system or mental map.

**Structure**:
```
1. Epitome (the relationship in one sentence)
   → Provides the map overview

2. Concept Map / Diagram
   → Visualizes relationships

3. Relationship Table (optional but recommended)
   → Systematic connections

4. Boundary Clarifications (framework-level misconceptions)
   → Prevents misreading the map

5. Practical Integration (optional)
   → How the framework applies in practice

6. Navigation Pointers
   → "For details on X, see [[concepts/X]]"
```

**Critical Constraint**: Do NOT explain individual concepts. A framework synthesis is a **map**, not an **encyclopedia**. If a concept needs explanation, it should have its own `concepts/` page, and the framework should link to it.

**Corrected example** (`ai-core-concepts.md` should become):
- KEEP: 30-second mental model + concept-network.svg
- KEEP: Concept relationship table
- KEEP: Framework-level "what it's NOT vs what it IS"
- KEEP: Agent call sequence (practical integration)
- DELETE: 18 individual concept explanations (duplicates `concepts/`)
- DELETE: Source index (belongs in `index.md`)
- DELETE: Extended reading (navigation noise)
- **Target**: ~80-120 lines (down from 414)

---

### `syntheses/` Evidence Genre

**Purpose**: Answer a specific question by synthesizing evidence from multiple sources.

**Structure** (based on Toulmin argumentation model):
```
1. Framing Question
   → What exactly are we trying to answer?

2. Source Landscape
   → What sources exist and what do they claim?

3. Convergence
   → Where do sources agree?

4. Divergence / Contradictions
   → Where do sources disagree? (Use [[Contradictions]] block)

5. Synthesis
   → What conclusion can we draw from the evidence?

6. Implications (optional)
   → So what? What follows?

7. Sources
   → Full attribution with wikilinks
```

**Constraint**: Every substantive claim must be traceable to a source. Inline citations are required: "Anthropic found that... ([[sources/anthropic-long-running|source]])"

**Good example**: `wiki/agent/harness-engineering/syntheses/harness-engineering-deep-dive.md` — has a clear argument structure with inline source attribution.

---

### `syntheses/` Narrative Genre

**Purpose**: Explain a process or mechanism by letting the reader follow a concrete journey.

**Structure**:
```
1. Hook / Scenario
   → Why should the reader care? Establish motivation.

2. Step-by-Step Journey
   → Walk through the process concretely
   → Use examples, not abstractions

3. Why It Works
   → After the journey, explain the underlying principles
   → Now the reader has concrete experience to attach theory to

4. Connections
   → Link to related concepts and sources
```

**Constraint**: The journey must be concrete. Abstract explanations belong in `concepts/`. The narrative's power comes from the reader "experiencing" the process.

**Good example**: `wiki/ai-fundamentals/syntheses/token-lifecycle.md` — follows one token from input to output with concrete examples at each step.

---

### `comparisons/` — Comparison Type

**Purpose**: Present a neutral, systematic comparison of alternatives.

**Structure**:
```
1. Framing
   → What is being compared and along what dimensions?

2. Dimension-by-Dimension Comparison
   → For each dimension, present both alternatives side-by-side
   → Use tables for scannability
   → No "winner/loser" framing

3. Decision Context
   → "If you need X, consider A; if you need Y, consider B"
   → Condition matching, not recommendation

4. Sources
   → Attribution for both sides
```

**Constraint**: Neutral presentation. Comparison pages do not argue for one alternative. If the goal is to argue that X is better, write an **evidence synthesis** instead.

---

### `sources/` — Reference Type

**Purpose**: Accurately summarize and index an external source.

**Structure** (already defined in `CLAUDE.md`, retained):
```
---
title: "Source Title"
type: source
tags: []
last_updated: YYYY-MM-DD
source_file: raw/<shelf>/...
---

## Summary
2-4 sentence summary.

## Key Claims
- Claim 1
- Claim 2

## Key Quotes
> "Quote" — context

## Connections
- [[EntityName]] — connection note
- [[ConceptName]] — connection note

## Contradictions
- Conflict with [[OtherPage]]: description
```

---

### `entities/` — Entity Reference Type

**Purpose**: Provide factual reference information about a specific entity (organization, person, product, project).

**Structure**:
```
1. Definition (what is this entity)
2. Key Attributes (factual properties)
3. Relationships (to other entities, concepts, sources)
4. Sources
```

---

### `index.md` — Catalog Type

**Purpose**: List and organize all pages in a shelf for navigation.

**Structure**:
```
1. Shelf description (one sentence)
2. Sources by topic
3. Concepts list
4. Syntheses list
5. Comparisons list (if any)
6. See also links
```

---

### `overview.md` — Navigation Type

**Purpose**: Provide a cognitive map of the entire shelf, guiding readers on where to start.

**Structure**:
```
1. One-sentence summary of the shelf
2. Knowledge map / diagram
3. Key entry points (recommended reading order)
4. Topic organization (how the shelf is structured)
5. Timeline (if relevant)
6. Next steps
```

**Distinction from framework synthesis**:
- `overview.md` = shelf-level map (breadth, navigation)
- Framework synthesis = topic-level deep map (specific domain, relationships between concepts)

---

## Guide Document Architecture

Split the current monolithic `ingest-writing-guide.md` into two focused documents:

### `docs/ingest-structure-guide.md`

**Scope**: Type system, structural models, atomicity constraints, migration examples.

**Sections**:
1. Type system overview (the table above)
2. Structural models for each type (the sequences above)
3. Atomicity constraints and scope rules
4. How to choose a type (decision flowchart)
5. Examples: good and bad (using actual wiki pages)
6. Migration notes for existing content

### `docs/ingest-style-guide.md`

**Scope**: Expression quality, visual design, tone, editing checklist.

**Source**: Reorganized from the existing `ingest-writing-guide.md` sections: 结论先行, 简单精准犀利, 视觉增强, 去AI味, 成稿前自检. Not written from scratch.

**Sections**:
1. Inverted pyramid / conclusion first
2. Simple, precise, sharp (delete redundancy)
3. Visual enhancement (when to diagram, when not)
4. De-AI-ing (humanizer-zh integration)
5. Self-checklist (pre-publish)

**Rationale**: Separating structure from style lets agents solve one problem at a time. First: "what type am I writing and what's the structure?" Second: "how do I make it read well?"

---

## Migration: `ai-core-concepts.md`

**Current state**: 414 lines, mixed genre (attempted framework + concept enumeration)

**Target genre**: Framework synthesis

**Actions**:
1. Remove 18 individual "核心概念逐个解析" sections
2. Remove Source索引 section (redundant with `index.md`)
3. Remove 延伸阅读 section (navigation noise)
4. Keep and strengthen:
   - 30-second mental model
   - Concept-network diagram
   - Concept relationship table
   - Framework-level boundary clarifications
   - Agent call sequence (practical integration)
5. Add navigation pointers to individual concept pages

**Target size**: ~80-120 lines.

---

## Files to Create / Modify

| File | Action |
|------|--------|
| `docs/ingest-structure-guide.md` | **Create** (new) |
| `docs/ingest-style-guide.md` | **Create** (new) |
| `docs/ingest-writing-guide.md` | **Delete** (replaced by the two above) |
| `CLAUDE.md` | **Update** (reference new guides, add `comparisons/` to naming conventions table and directory layout) |
| `wiki/ai-fundamentals/syntheses/ai-core-concepts.md` | **Rewrite** (apply framework synthesis model) |

---

## Success Criteria

1. An agent reading `ingest-structure-guide.md` can correctly classify any new page into a type and genre, and knows the structural sequence
2. An agent can identify scope violations (e.g., concept explanations in a framework synthesis)
3. The rewritten `ai-core-concepts.md` is under 150 lines and contains no duplicated concept explanations
4. The two guides contain zero contradictions with `CLAUDE.md`
