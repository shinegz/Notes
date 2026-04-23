# [决策]: docs: redesign wiki writing guides and rewrite ai-core-concepts as framework synthesis

## 日期
2026-04-23

## 背景
- Add ingest-structure-guide.md: type system, cognitive loading order, atomicity rules
- Add ingest-style-guide.md: expression style, visual enhancement, de-AI-tone checklist
- Delete ingest-writing-guide.md (superseded by new guides)
- Update CLAUDE.md: add comparisons/ naming, reference new guides
- Rewrite ai-core-concepts.md: remove 18 concept explanations, keep relationship map + boundary clarifications + agent call sequence
  - Shrink from 414 lines to 91 lines (framework synthesis target: 80-150)

## 决策
docs: redesign wiki writing guides and rewrite ai-core-concepts as framework synthesis

## 影响范围
- ...23-docs-add-wiki-writing-guide-redesign-spec.md
- .promem/promem.log
- llm-wiki/CLAUDE.md
- llm-wiki/docs/ingest-structure-guide.md
- llm-wiki/docs/ingest-style-guide.md
- llm-wiki/docs/ingest-writing-guide.md
- .../wiki/ai-fundamentals/concepts/llm-agents.md
- .../ai-fundamentals/syntheses/ai-core-concepts.md
- .../ai-core-concepts-architecture.png
- .../ai-core-concepts-architecture.svg
- .../syntheses/ai-core-concepts/concept-network.svg
- .../ai-core-concepts/generate_concept_map.py
## 删除的函数/类
- `get_anchor`
- `draw_manhattan_edge`
- `get_connection`
- `return (fx + fw, fcy, tx, fcy)`
- `return (fx, fcy, tx + tw, fcy)`
- `return (fcx, fy + fh, fcx, ty)`
- `return (fcx, fy, fcx, ty + th)`
- `print(f"SVG generated: {out_path}")`
- `print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")`

## 相关注释
> # [决策]: docs: add wiki writing guide redesign spec
> # Wiki 成稿结构指南（Ingest Structure Guide）
> ### P1: 类型由认知功能决定，不是由主题领域决定
> ### P2: 一个页面，一个认知任务（原子化）
> ### P3: 结构服从功能


## 相关链接
- Commit: 3b9bede35dadcbc8bb30663446007f2cc7b82552
