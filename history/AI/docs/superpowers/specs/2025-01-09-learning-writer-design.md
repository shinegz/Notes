# learning-writer Skill Design Document

**Date:** 2025-01-09  
**Status:** Approved for Implementation  
**Replaces:** `learning-assistant`, `learn-and-visualize`

---

## 1. Overview

### 1.1 Core Positioning

`learning-writer` is a premium knowledge synthesis skill that creates beautifully written, visually rich Markdown learning notes. Unlike traditional learning assistants that produce rigid summaries, this skill acts as an experienced knowledge writer—studying materials deeply, identifying core concepts and their relationships, and crafting articles that are simple, precise, and visually compelling.

### 1.2 Design Principles

- **One Picture, Thousand Words**: Visualize complex concepts with elegant diagrams
- **Adaptive Structure**: Automatically select the best organization based on topic type
- **Human Voice**: Process all text through `humanizer-zh` to remove AI tone
- **Creative Freedom**: High-level principles only, no rigid case-by-case requirements
- **Visual Excellence**: Multiple style options with user preview/selection

---

## 2. Trigger Conditions

**Primary trigger:** All learning, research, and knowledge synthesis requests.

**Trigger phrases include:**
- "Help me learn X" / "I want to understand X"
- "Research X and write about it"
- "Study this and create notes"
- "Summarize these materials"
- "Explain X to me"
- "Digest this documentation"
- "帮我学习 X" / "我想了解 X" / "研究一下 X"

**This skill replaces both `learning-assistant` and `learn-and-visualize`.** When this skill is available, it takes precedence for all learning requests.

---

## 3. Learning Methodology

The agent automatically applies these human learning strategies:

### 3.1 Feynman Technique
- Explain concepts in simple language
- Identify knowledge gaps and fill them through research
- Ensure every concept can be explained in one sentence

### 3.2 Concept Mapping
- Build knowledge relationship networks
- Identify core vs. supporting concepts
- Establish hierarchical relationships

### 3.3 Analogical Learning
- Map new concepts to familiar domains
- Build consistent metaphor systems
- Avoid mixing metaphors randomly

### 3.4 Visual Thinking
- Use diagrams for complex relationships
- Choose appropriate visualization for each concept type
- Maintain visual consistency within each article

### 3.5 Problem-Driven Approach
- Start from core questions
- Work backwards to find knowledge
- Use questions to connect content

---

## 4. Material Gathering Strategy

### 4.1 Gathering Process

```
User Input
    │
    ├─→ User provides materials? ──→ Collect and read
    │
    └─→ Identify knowledge gaps
            │
            ├─→ Proactive search to fill gaps
            │
            └─→ Cross-verify information
```

### 4.2 Layered Parallel Search

**Layer 1 - Concept Definition:**
- Core terminology and basic concepts
- Both English and Chinese sources when relevant

**Layer 2 - Multi-Angle Search (parallel):**
- Official documentation / platform tutorials
- Video tutorials (YouTube, Bilibili)
- Courses and academies
- Chinese articles and tutorials

**Layer 3 - Gap Filling:**
- Targeted searches for specific weak points
- Deep dives into critical concepts

### 4.3 Information Verification

- Prioritize official docs and authoritative sources
- Cross-reference multiple sources
- Mark uncertain information clearly

---

## 5. Output Specifications

### 5.1 File Format

- **Format:** Markdown (.md)
- **Diagrams:** Mixed (Mermaid, SVG, ASCII based on content type)
- **Images:** Embedded or referenced
- **Dependencies:** None (self-contained)

### 5.2 Visual Style Options

Present 2-3 style options for user preview:

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| **Minimal Tech** | Clean lines, neutral colors, professional | Technical topics, algorithms |
| **Warm Sketch** | Hand-drawn feel, approachable | Creative topics, concepts |
| **Modern Editorial** | Magazine-quality, bold typography | Deep analysis, features |

### 5.3 Diagram Type Selection

| Content Type | Recommended Format | Example |
|--------------|-------------------|---------|
| Flow / Sequence | Mermaid | Algorithm steps, system flow |
| Relationship Network | Mermaid or SVG | Concept maps, dependencies |
| Simple Illustration | ASCII or Mermaid | Quick diagrams, hierarchies |
| Complex Visualization | SVG | Detailed architecture, data viz |

### 5.4 Content Organization (Adaptive)

The agent automatically selects structure based on topic type:

| Topic Type | Structure Pattern |
|------------|-------------------|
| **Technical / Algorithm** | Problem → Core Idea → Step-by-Step → Visualization → Applications |
| **Conceptual / Framework** | 30-sec Model → What It Is/Isn't → Core Concepts → Relationships → When to Use |
| **Historical / Evolution** | Timeline → Key Figures → Turning Points → Modern Impact |
| **Comparative / Decision** | Options Overview → Deep Dive Each → Trade-offs → Recommendation |
| **Process / How-To** | Goal → Prerequisites → Steps → Common Pitfalls → Checklist |

### 5.5 Writing Principles (High-Level)

1. **Start with Impact** - Hook the reader immediately
2. **One Picture, Thousand Words** - Visualize complex concepts
3. **Simple, Precise, Sharp** - Explain clearly without fluff
4. **Consistent Metaphors** - Build analogy systems, don't mix them
5. **Concept Hierarchy** - Show relationships between ideas
6. **No AI Taste** - Use humanizer-zh for final polish

### 5.6 File Naming Convention

Auto-generated based on topic type:

| Topic Type | Naming Pattern | Example |
|------------|----------------|---------|
| Technical deep dive | `{topic}-深度解析.md` | `react-fiber-深度解析.md` |
| Getting started | `{topic}-入门指南.md` | `rust-入门指南.md` |
| Concept explanation | `{topic}-核心概念.md` | `区块链-核心概念.md` |
| Comparative analysis | `{topic}-对比分析.md` | `微前端方案-对比分析.md` |
| Practical guide | `{topic}-实践指南.md` | `k8s-实践指南.md` |

---

## 6. Core Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Topic Analysis                                     │
│  - Understand topic nature and complexity                    │
│  - Determine appropriate structure type                      │
│  - Identify required materials                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Material Gathering                                 │
│  - Collect user-provided materials (if any)                  │
│  - Proactively search to fill knowledge gaps                 │
│  - Cross-verify information accuracy                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Knowledge Digestion                                │
│  - Apply learning methodologies deeply                       │
│  - Build concept maps                                        │
│  - Identify core questions and insights                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Content Restructuring                              │
│  - Reorganize with simple, precise, sharp language           │
│  - Design appropriate analogies and metaphors                │
│  - Plan visual elements                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: Visual Design                                      │
│  - Create style mockups (2-3 options)                        │
│  - Present to user for selection                             │
│  - Finalize diagram designs                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 6: Humanizer Processing                               │
│  - Apply humanizer-zh rules                                  │
│  - Make text sound human-written                             │
│  - Inject personality and opinions                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 7: Markdown Generation                                │
│  - Generate Markdown with embedded diagrams                  │
│  - Ensure proper formatting and structure                    │
│  - Add navigation and cross-references                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 8: Quality Verification                               │
│  - Check content accuracy and completeness                   │
│  - Verify all diagrams render correctly                      │
│  - Ask user for save location                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Technical Implementation

### 7.1 Markdown Template Structure

```markdown
# {Topic Name}

> {One-sentence hook}

## 30-Second Mental Model

{Quick analogy table}

## Table of Contents

{Auto-generated}

## {Section 1}

{Content with embedded diagrams}

## {Section 2}

{Content with embedded diagrams}

## Summary

{Key takeaways}

## Sources

{References consulted}
```

### 7.2 Diagram Tools

- **Mermaid**: Primary choice for flows, sequences, relationships
- **SVG**: Complex custom visualizations
- **ASCII**: Simple inline diagrams

### 7.3 Dependencies

- `humanizer-zh` skill (for text processing)
- Mermaid rendering support (in Markdown viewers)

---

## 8. Quality Standards

### 8.1 Content Quality

- [ ] Core concepts fully covered
- [ ] Knowledge gaps filled
- [ ] Logical flow from basic to advanced
- [ ] Practical examples included
- [ ] Key facts cross-verified

### 8.2 Visual Quality

- [ ] Complex concepts have visual explanations
- [ ] Diagrams help understanding (not decoration)
- [ ] Charts are clear and readable
- [ ] Color usage is meaningful
- [ ] Style is consistent throughout

### 8.3 Writing Quality

- [ ] Processed through humanizer-zh
- [ ] Simple, precise, sharp language
- [ ] Appropriate analogies (not overused)
- [ ] No AI taste
- [ ] Natural sentence variation

### 8.4 Technical Quality

- [ ] Markdown renders correctly
- [ ] Diagrams are viewable
- [ ] Structure is clear
- [ ] File is self-contained

---

## 9. Boundaries and Limitations

### 9.1 Scope

**Suitable for:**
- Technical concepts and algorithms
- System architecture
- Theoretical knowledge
- Process documentation
- Comparative analysis

**Not suitable for:**
- Real-time data
- Backend-dependent applications
- Massive-scale content (> 50 pages)

### 9.2 Technical Limits

- File size: Recommend < 2MB
- Diagram complexity: May need simplification
- Some advanced visualizations may not render in all Markdown viewers

### 9.3 Content Limits

- No login-required content
- No sensitive information
- Sources cited but content stands alone

---

## 10. References

- `humanizer-zh` SKILL.md - Text humanization rules
- `learning-assistant` references/mermaid-style.md - Diagram styling
- `learning-assistant` references/beautiful-mermaid-guide.md - Mermaid best practices

---

## 11. Example Topics

For testing the skill:

1. React Fiber Architecture
2. TCP Three-Way Handshake
3. Blockchain Consensus Mechanisms
4. Gradient Descent in Machine Learning
5. Browser Rendering Pipeline
6. Event Loop in JavaScript
7. Database Indexing Strategies
8. OAuth 2.0 Flow

---

**Document End**
