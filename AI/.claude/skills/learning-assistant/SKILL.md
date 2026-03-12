---
name: learning-assistant
description: Autonomous learning agent that studies materials on behalf of the user and outputs distilled knowledge. Use when user wants to learn a new topic, understand complex materials, or needs a comprehensive summary of learning resources. Trigger when user says things like "help me learn", "study this for me", "summarize these materials", "I want to understand X", "research this topic", or provides multiple learning resources asking for synthesis. The agent reads and digests the provided materials (they are input for the agent), fills knowledge gaps through research, and produces a learning summary containing what it learned—so the user can learn by reading the summary, not by being directed to use the materials.
---

# Learning Assistant

This skill enables Claude to act as an autonomous learning agent that **studies the provided materials on its own**, fills knowledge gaps through research, and **outputs distilled knowledge** in a learning summary. The user learns by **reading the summary**; the provided materials are **input for the agent to learn from**, not a curriculum to direct the user to. The summary should contain what you learned and synthesized—not a guide on "how to use these learning resources" (e.g., "if you want X, take course A").

## Core Workflow

### Phase 1: Material Intake

When user provides learning materials, systematically process all inputs:

**Supported input types:**
- Files (PDF, DOCX, TXT, MD, code files, etc.)
- URLs/links to articles, documentation, papers
- Pasted text or code snippets
- Images with diagrams or text
- References to topics or concepts
- **Video content (e.g. YouTube)**：当用户提供 **YouTube 视频链接** 时，优先运行本技能下的 `scripts/get_youtube_transcript.py <url>` 获取字幕/文稿，将输出作为学习材料进入 Phase 1；若获取失败（无字幕、私密视频等），提示用户可改为粘贴视频文稿再继续。用户也可直接粘贴**视频字幕/文稿**，按「粘贴文本」处理。脚本依赖：`pip install youtube-transcript-api`，且需网络访问。

**Processing steps:**
1. Read all provided materials thoroughly
2. Create an internal knowledge map of key concepts
3. Identify the main topic and subtopics
4. Note terminology, definitions, and relationships between concepts
5. If the material has a clear section structure, preserve it; otherwise organize the summary by applying the 可借鉴之处 in Phase 5

**Initial assessment questions (ask only if context is unclear):**
- What is the learning goal? (general understanding, practical application, exam prep, etc.)
- What's the desired depth? (overview, intermediate, deep dive)
- Any specific aspects to focus on?
- What's the user's current knowledge level on this topic?

If user doesn't specify, default to:
- Goal: comprehensive understanding
- Depth: intermediate with deep dives where needed
- Focus: all major aspects
- Level: assume minimal prior knowledge

### Phase 2: Knowledge Gap Analysis

After processing initial materials, identify gaps:

**Gap detection criteria:**
- Undefined terms or jargon used without explanation
- Referenced concepts not fully explained
- Missing prerequisites needed to understand the material
- Contradictions or inconsistencies requiring clarification
- Practical applications mentioned but not demonstrated
- Historical context or motivation missing
- Edge cases or limitations not addressed

**For each identified gap:**
1. Assess importance (critical/helpful/optional)
2. Estimate effort to fill (quick search vs. deep research)
3. Prioritize based on learning goals

### Phase 3: Autonomous Research

Fill knowledge gaps through active research. When a topic or gap requires web search, use a **layered, parallel search strategy** (adapted from research-gathering) so results are broad and relevant.

**Layered search (run layers in order; parallelize within each layer):**

1. **Layer 1 – Concept**: One or two WebSearch calls for definition and key terms (English and 中文 if the topic is used in both communities). Get: 1–2 sentence summary, official/product names, key people or platforms. Use this to refine later queries.

2. **Layer 2 – By type**: Run **multiple WebSearch queries in parallel** for different angles:
   - Official docs / platform tutorials (e.g. "X official documentation", "Microsoft Learn X", "GitHub X tutorial")
   - Video: "X YouTube tutorial", "X video 教程", or "<key person> X" if a figure emerged in Layer 1
   - Courses / academies: "X course", "X academy", "Coursera/Codecademy X"
   - Chinese articles/tutorials (if relevant): "X 教程 中文", "X 工具 入门"

3. **Layer 3 – Fill gaps**: If a category is thin or the user cares about a specific platform/language, add 1–2 targeted searches. Optionally use `mcp_web_fetch` on 1–2 key URLs to verify accessibility and relevance (no need to parse full content).

**Principles:**
- **Parallelize**: Use multiple WebSearch calls in one turn for different angles (concept, docs, video, courses, 中文) instead of one generic query.
- **Bilingual when relevant**: For topics used in both English and Chinese communities, include both "X tutorial" and "X 教程/概念" in the search plan.
- Prioritize official documentation, academic papers, reputable tutorials; cross-reference multiple sources for accuracy; track all sources for citation.

**Search triggers (no user confirmation needed):**
- Critical gaps that block understanding of core concepts
- Technical terms needing precise definitions
- Best practices and common patterns
- Recent updates or changes to the topic

**When researching:**
- Inform user briefly: "Researching [topic] to fill knowledge gap..."
- Keep searches focused and efficient
- Synthesize findings with original materials
- Note any conflicting information found

**Reference:** For more specific query patterns and classification dimensions, see `references/gathering-strategy.md` (optional).

### Phase 4: Synthesis and Organization

Organize learned knowledge into a coherent structure:

**Structure the knowledge by:**
1. Identifying the logical flow of concepts (what depends on what)
2. Grouping related concepts together
3. Creating a progression from basic to advanced
4. Highlighting connections and relationships
5. **Building a metaphor system**: Choose 1–2 analogy domains from the reader's daily life (company, kitchen, hospital, traffic, etc.), assign each core concept a fixed role in that domain, and use it consistently across the summary (see Writing guidelines: Metaphor & analogy system)

**Knowledge organization patterns:**
- Hierarchical: main concepts → subconcepts → details
- Sequential: prerequisites → core concepts → applications
- Comparative: concept A vs concept B, pros/cons
- Problem-solution: challenge → approach → implementation

### Phase 5: Summary Document Generation

Produce a **learning summary document that contains the knowledge you extracted and synthesized**—not a guide for the user on how to use the learning materials they provided.

**Output = distilled knowledge:**
- The **provided materials are for you (the agent) to learn from**. You read them, fill gaps with research, then write what you learned.
- The **user learns by reading your summary**. The summary should stand alone: someone who has not seen the original materials can read your document and come away with correct, well-organized knowledge of the topic.
- **Do not** turn the summary into a "how to use these learning resources" guide (e.g., "for quick start, do tutorial A"; "for depth, read document B"; "see 学习资料汇总 for links"). You may include a short **Sources consulted / 参考资料** section for citation and verification, but the main body is **the knowledge you distilled**, not pointers to where the user should go to learn.

Organize content by applying the **可借鉴之处** below; section order and depth can follow the source material or adapt to the topic—no need to rigidly match a fixed outline.

---

**可借鉴之处**（写总结时灵活运用）：

1. **结论先行 + 30 秒心智模型**：前几节就把核心结论讲清楚。推荐在文章最前面（阅读路径之后、正文之前）用一个生动的类比建立**30 秒心智锚点**——选自读者熟悉的日常事物（如"管家""公司""机场"），用表格映射每个核心概念到类比中的角色。效果：读者即使只看这 30 秒，也能对别人说出"这东西大概是什么"。
2. **区分阅读路径**：若读者可能有两种目标（如「想快速用」vs「想搞懂原理」），在开篇给出两条路径并链到对应章节（如：想快速落地 → 优先看 A → B → 案例 → 总结；想补齐概念 → 先看概念入门 → 为什么需要）。
3. **语境与术语前置**：在进入正文前用「阅读指南」或等价小节交代：本文讨论范围（本文语境）、建议前置知识、术语表（最好含「在本文中的落点」）、约定或路径。避免后文频繁「读不懂」。
4. **先问题再方案（故事驱动）**：有痛点/背景时，先说清问题再给方案。推荐**用角色故事呈现痛点**（如"小明是个全栈开发者，他的日常是这样的……"），让读者从旁观者变成当事人；故事末尾再用简表做结构化汇总（现状 → 痛点 → 根因），兼顾感性认同和理性梳理。问题清晰，解法才容易记住。
5. **可选深入 + 密度控制**：非必读的概念/理论部分标为可选或折叠。每个概念主线用 **"类比 → 一句话 → 示例/表格"** 格式呈现；设计决策、原理深入等放进可折叠块（`> [!question]-` 或 `> [!info]-`）。大段散文优先转化为表格（对比、分类）、列表（步骤、枚举）、折叠 QA（为什么、怎么权衡）。效果：主线阅读通畅，好奇的读者可展开深入。
6. **概念讲清「在本文中的落点」**：关键名词配定义 + 小例子 + 在本文/本场景下的用法；图或表之后用 1～3 条「读图结论」点明要点。
7. **落地可循 + 每节嵌入启发**：若有实践/案例，写清「落点」「关键落地点」「什么时候值得用」；有 Before/After 对比更好。**不只在文末总结处给落地建议**，而是在每个概念讲完后紧跟 `> **对你的启发**：...`，让读者边学边收获可迁移的经验。总结部分给决策流程或核心原则，方便读者自判和落地。
8. **实践要具体、可剖析**：实践相关的内容不能只给「思路和说明」，要有**具体的最佳实践案例剖析**。根据主题选择与读者落地相关的形式：例如 Before/After 对比（模糊 vs 可验收、错误 vs 正确）、填好的模板或清单示例（与主题相关的 1～2 个）、真实场景下的「问题 → 证据/输入 → 解决」拆解。形式随主题变（可以是需求/设计/代码/流程/配置等），目标是让读者看到「好的做法长什么样」，而不是只记住原则和清单。
9. **回应质疑 + 清除误解**：若主题容易被误解，在介绍「是什么」之前先用 **"不是什么 vs 是什么"** 对比表格划清边界（❌ 不是 / ✅ 是），瞬间扫清认知障碍；若主题常被质疑（如「会不会过度设计」），用折叠式「常见质疑 Q&A」+ 每题「一句话结论」，减少读者犹豫。
10. **一致的隐喻体系**：为全文选定一到两个类比域（如快速路径用"管家"、深入路径用"公司"），而不是每处随机换比喻。同一概念在不同小节沿用同一隐喻角色，让读者形成连贯心智模型。**章节标题附加类比副标题**（如 `### 两级队列 — "银行叫号 + 限流窗口"`），让读者扫目录就能建立初步理解。

---

**Suggested document outline**（按需取舍、合并或调序，不必全用）：

- 开篇：本文定位、适用读者、阅读建议（含两条路径，若适用）
- **30 秒心智模型**（强烈建议）：用一个类比表格让读者 30 秒内建立核心认知锚点（见 #1）
- 阅读指南：本文语境、前置知识、术语表（含本文落点）、约定/路径
- **X 是什么**（若主题容易被误解）：先用"不是什么 vs 是什么"表格划清边界（见 #9），再给正式定义
- 背景与痛点（若适用）：用**故事场景**呈现痛点（见 #4），再用简表结构化汇总
- 方案总览 / 核心结论（建议靠前）：快速概览、要解决的问题、约束或形态对比
- 概念入门（可选）：快速扫读版、一句话版、关键名词+小例子+对比表。每个概念用 **"类比→一句话→示例/表格"** 格式，深入解释放折叠块
- 为什么需要 / 价值：图或对比 + 读图结论、Before/After、常见质疑 Q&A（折叠）、综上所述
- 落地实践：选型、结构/依赖、**最佳实践案例剖析**（与主题相关的具体案例：Before/After、填好的模板或清单、真实场景拆解）、落地要点。每小节末尾嵌入 `> **对你的启发**：...`
- 总结与落地建议：决策流程、核心原则、**一页速查**（从本主题带走的 N 条经验，用 callout 包裹）
- 参考资料/附录（可选）：**仅作引用与溯源**（你学习时参考了哪些来源），不是「教读者怎么选、怎么用这些学习资料」；正文主体 = 你提炼出的知识。

**Writing guidelines:**
- Use clear, simple language
- Explain jargon when first introduced
- Provide concrete examples for abstract concepts
- Use analogies to connect new concepts to familiar ones
- Include code snippets for programming topics
- Use diagrams (ASCII or Mermaid) for complex relationships
- Highlight practical takeaways
- **Practice sections must be concrete, not only high-level.** When the topic has 实践/落地/最佳实践 content, include **best-practice case studies with breakdowns** in a form relevant to the topic: e.g. before/after examples (vague vs actionable), filled-in templates or checklists, real scenario breakdowns (problem → evidence/input → resolution). The format depends on the subject (requirements, design, code, workflow, config, etc.); the goal is that the reader sees what good looks like—not just principles and checklists.

**Metaphor & analogy system（类比体系构建）:**
- **选域**：在 Phase 4（组织知识）时，为整篇总结选定 1~2 个「类比域」——从读者日常生活中取材（公司、厨房、医院、交通、建筑……），让核心概念都能映射到该域中的角色或事物。
- **一致映射**：为每个核心概念分配一个固定的类比角色，全文复用。例如：Gateway = 总经理，Agent = 工程师，Queue = 银行叫号机。避免同一个概念在不同段落换不同比喻。
- **分层可选**：若总结有快速路径和深入路径，可为两条路径各选一个类比域（如快速路径用"管家"、深入路径用"公司"），但两个域之间应有内在对应关系。
- **落点**：类比出现在三个位置——① 30 秒心智模型（开篇锚点）；② 章节标题副标题（扫读辅助）；③ 概念首次出现时（理解桥梁）。

**Density control（信息密度控制）:**
- 每个概念的主线呈现使用 **"类比 → 一句话定义 → 表格或示例"** 格式，确保扫读即可获取要点。
- 设计决策、原理深入、边界条件等内容放进**可折叠块**（Obsidian 用 `> [!question]-` 或 `> [!info]-`），不打断主线阅读。
- 大段散文优先转化为：**表格**（对比、分类）、**列表**（步骤、枚举）、**折叠 QA**（为什么、怎么权衡）。
- 章节标题使用 `### 概念名 — "类比短语"` 格式（如 `### 两级队列 — "银行叫号 + 限流窗口"`），扫目录即建立初步认知。

**Mermaid diagram style**（提炼自《基于DDD的Smax前端架构设计与实践》，总结中若画图可统一采用）：
- **类型**：优先用 `flowchart TB`（自上而下）、`flowchart LR`（左右）或 `flowchart TD`；复杂分组用 `subgraph`。
- **节点**：节点内换行用 `<br/>`（如 `A["UI 层<br/>页面/组件"]`）；连线可加标签（如 `-->|抽象|`）。
- **配色**：为每个节点显式写 `style NODE fill:#HEX,stroke:#e2e8f0`，保持统一语义：
  - 中性/背景/UI：`#f1f5f9`
  - 应用/流程层：`#bae6fd`
  - 领域/核心：`#ddd6fe` 或 `#c4b5fd`
  - 基础设施/外部：`#cbd5e1`
  - 正向/成功/结论：`#a8e6cf`
  - 根因/错误/强调：`#fecaca`
  - 警告/次要强调：`#fef3c7` 或 `#fed7aa`
  - 子图背景：`subgraph` 内 `style sub fill:#f8fafc,stroke:#e2e8f0`
- **读图结论**：图下方用 1～3 条「读图结论」点明要点，便于扫读。

### Phase 6: Quality Verification

Before delivering the summary:

**Verify completeness:**
- All core concepts from original materials covered
- All identified gaps filled with researched content
- Logical flow from basics to advanced
- Practical applications included

**Verify accuracy:**
- Cross-check key facts
- Ensure consistent terminology
- Verify examples work as described (for code)

**Verify usability:**
- Document can stand alone without original materials—**the reader learns from the summary itself**, not from being directed to the original materials
- Someone with stated prerequisites can follow it
- Key points are easy to find and reference
- The summary is **distilled knowledge**, not a "how to use the learning resources you gave me" guide

**Reader perspective check**（借鉴 doc-coauthoring）：  
从「无上下文的读者」角度验证总结是否成立：
1. **Predict reader questions**: 列出 5～10 个读者看完总结后可能提出的问题（如「X 是什么？」「什么时候该用 Y？」），自检总结是否已回答或能推断出答案。
2. **Ambiguity and assumptions**: 自问：有没有默认读者已具备但未写明的知识？有没有容易歧义或前后不一致的表述？若有，在总结中补一句说明或术语表条目。
3. **Every sentence carries weight**: 若某段连续几轮修改无实质变化，可问自己是否有多余可删的句子，使总结更精炼。

## Interaction Patterns

### Starting a learning session

When user provides materials:
1. Acknowledge receipt of materials
2. Briefly describe what was received
3. Ask clarifying questions if needed (max 3-5 questions)
4. Begin processing

Example:
```
收到了3份学习资料：
- Python异步编程教程.pdf
- asyncio官方文档链接  
- 一段示例代码

我将开始学习这些资料。请问：
1. 你的学习目标是什么？（理解原理/能够实际应用/两者都要）
2. 有没有特别想重点了解的方面？

如果没有特殊要求，我会全面学习并生成完整的学习总结。
```

### During learning

Keep user informed of progress:
- "正在阅读第1份资料..."
- "发现知识空白：[概念X]需要补充了解，正在搜索..."
- "资料学习完成，正在整理知识结构..."

### Handling user questions during learning

If user asks questions mid-process:
- Answer briefly if possible without disrupting flow
- Note the question as an area of interest for the summary
- If question requires significant deviation, ask if user wants to pause for a detailed answer

### Delivering results

1. Save the summary document to an appropriate location
2. Provide a brief overview of what was learned
3. Highlight 3-5 most important takeaways
4. Offer to clarify any part or dive deeper into specific areas

## Output Options

**Default output:** Markdown file saved to workspace

**Alternative outputs (ask user preference if unclear):**
- Markdown file (default)
- Obsidian-compatible note (if user uses Obsidian)
- DOCX document (use docx skill if available)
- Direct conversation summary (for quick topics)

## Handling Special Cases

### Conflicting information in sources
- Note the conflict explicitly in the summary
- Present both viewpoints
- Indicate which is more authoritative/recent if determinable

### Outdated materials
- Search for current information
- Note what has changed
- Present current best practices

### Incomplete initial materials
- Research to fill critical gaps
- Clearly mark what came from original materials vs. research

### Very broad topics
- Ask user to narrow focus, OR
- Provide overview summary with pointers to subtopics for deeper learning

### Very technical/specialized topics
- Ensure prerequisites are covered or noted
- Include glossary of specialized terms
- Provide references for further depth

## Preserving Source Structure

When the source material already has a clear, navigable structure, **preserve that structure** in the learning summary. Otherwise organize the summary by applying the **可借鉴之处** in Phase 5—section order and depth can follow the topic; the goal is clear reading paths, terminology up front, and actionable landing/decision guidance, not a fixed outline.

## Quality Standards

**A good learning summary should:**
- **Contain the knowledge you learned and distilled**—the user learns by reading it, not by being told which resource to use
- Be understandable without the original materials; the summary stands alone as the learning vehicle
- Save the user significant reading time (they get the essence without reading all sources)
- Organize knowledge better than the original materials
- Include practical, actionable information
- Serve as a useful reference for future recall
- Cite sources for verifiability (as "sources consulted," not as "go here to learn")
- Apply the 可借鉴之处 where relevant so the summary has clear reading paths, terminology up front, and landing/decision guidance
