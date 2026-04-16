# llm-wiki

Karpathy-style **persistent Markdown wiki**: compile sources into cross-linked `wiki/` pages instead of re-deriving from raw chunks on every question.

This tree is **self-contained**: docs and `tools/` assume only this directory as the wiki root (`WIKI_ROOT`); no sibling folders (e.g. parent-repo `.agents/`) are required. Pair it with any agent that can read `CLAUDE.md` and follow file workflows.

## Features

- **Shelves**: `raw/<shelf>/…` and `wiki/<shelf>/…` — path is the library category.
- **Collect → approve → ingest**: agent proposes `sessions/.../candidates.md`; you confirm before anything is written to `raw/`.
- **Taxonomy gate**: structural changes to shelves require explicit human approval (`taxonomy.md`).
- **Tools (no API key)**: `tools/source_registry_cli.py` (validate / match-url / match-file / layout), `tools/lint_wiki.py`, `tools/build_graph.py` (wikilink-only edges + optional Louvain via [networkx](https://networkx.org/)).

## Quick start

```bash
export WIKI_ROOT="$PWD"   # or path to this directory
pip install -r requirements.txt
bash tools/check_all.sh "$WIKI_ROOT"
python3 tools/build_graph.py --wiki-root "$WIKI_ROOT"
```

Read **`CLAUDE.md`** for ingest / query / lint / graph steps and page templates.  
For prose quality and de-AI-ing, see **`skills/wiki-writing/SKILL.md`** and **`skills/humanizer-zh/SKILL.md`**. For URL/material collection, start with **`skills/collect/SKILL.md`** and **`tools/source_registry.tsv`** (bundled adapter skills under **`skills/`**).

## Inspiration & credits

Design ideas are drawn from (this directory is **not** a fork of any of them):

- [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) — wiki 分层与 **ingest / lint 步骤清单**（如 `.claude/commands/wiki-ingest.md`）；其自带的 `tools/ingest.py` 走 API自动写 wiki，**本目录主流程由 Agent 按 `CLAUDE.md` 执行 + 本地 `tools/` 做结构校验**，不绑同一套脚本。
- [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) — source-type registry mindset (`tools/source_registry.tsv`).
- [safishamsi/graphify](https://github.com/safishamsi/graphify) — treating the corpus as a graph.

Core pattern: [Andrej Karpathy — llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## License

MIT — see [LICENSE](LICENSE).
