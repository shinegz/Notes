---
name: research-gathering
description: Systematic workflow for gathering learning materials on a topic. Use when the user asks to collect, curate, or summarize learning resources (e.g. "搜集关于 X 的学习资料", "find learning materials for X", "整理 X 的教程/视频/文档") in any format—docs, videos, courses, articles—and output a structured, link-rich summary (tables by type, with brief descriptions and URLs).
---

# Research Gathering (搜集资料)

Systematic workflow for gathering and organizing learning materials on a given topic into a structured, link-rich document (e.g. markdown with tables by resource type).

## When to Use

- User asks to **collect** or **curate** learning resources on a topic (e.g. "搜集关于 X 的学习资料", "整理 X 的教程").
- User explicitly allows **any format**: docs, videos, courses, articles, etc.
- Deliverable is a **summary document** with clear categories, brief descriptions, and working links—not just a list of raw search results.

## Workflow

### 1. Clarify scope and output

- **Topic**: What exactly is the subject (e.g. "vibe coding", "React hooks")?
- **Formats**: Confirm "不限文档、视频链接等形式" or note any constraints (e.g. "only free", "Chinese only").
- **Output**: Where to write (e.g. new file under `topic/学习资料汇总.md`) and whether to align with existing notes (e.g. `学习总结.md`).

### 2. Search in layers (parallel when possible)

- **Layer 1 – Concept**: WebSearch for definition + key terms (English and 中文 if relevant). Use results to get: 1–2 sentence summary, official/product names, key people/platforms.
- **Layer 2 – By type**: Run **multiple WebSearch queries in parallel**:
  - Official docs / platform tutorials (e.g. "X official documentation", "Microsoft Learn X", "GitHub X tutorial").
  - Video: "X YouTube tutorial", "X video 教程", or "&lt;key person&gt; X" if a figure emerged in Layer 1.
  - Courses / academies: "X course", "X academy", "Coursera/Codecademy X".
  - Chinese articles/tutorials: "X 教程 中文", "X 工具 入门".
- **Layer 3 – Fill gaps**: If a category is thin or user cares about a specific platform/language, add 1–2 targeted searches. Optionally use `mcp_web_fetch` on 1–2 key URLs to verify accessibility and relevance (no need to parse full content).

### 3. Organize and write output

- **Structure**: Use sections by resource type (e.g. 官方/平台文档 → 视频 → 在线课程 → 中文文章). One table per section.
- **Table columns**: At least **name, type/form, short description, link**. Optional: duration, level, language.
- **Opening**: Start with a 1–2 sentence concept summary so the doc stands alone.
- **Closing**: Optional "速查/按人群推荐" (e.g. 零基础推荐 X，系统学习推荐 Y) or "与现有笔记的配合" if user has a 学习总结 or similar.

### 4. Optional: link to existing notes

If the user already has a summary/checklist for the same topic (e.g. `学习总结.md`), add a short subsection at the end: this doc = **sources and links**; the other = **workflow and checklists**; suggest reading the summary first, then picking 1–2 items from this doc to go deeper.

## Resources

### references/gathering-strategy.md

Detailed strategy: query patterns by layer, classification dimensions, and output structure. Read when you need more specific search phrasing, categories, or template ideas than above.

## Principles

- **Parallelize**: Use multiple WebSearch calls in one turn for different angles (concept, docs, video, courses, 中文) instead of one generic query.
- **Bilingual when relevant**: For topics used in both English and Chinese communities, include both "X tutorial" and "X 教程/概念" (or "X 是什么") in the search plan.
- **Structured over raw**: Prefer tables with type + description + link over long unstructured lists.
- **Verify sparingly**: Use fetch only for a few critical URLs when you need to confirm the page exists and matches the topic; do not fetch every link.
