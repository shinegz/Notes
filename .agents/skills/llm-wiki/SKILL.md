---
name: llm-wiki
description: Karpathy 式持久 wiki（llm-wiki/）— 按门类路径组织 raw/wiki，Collect 先清单后落盘，ingest/query/lint/graph；融合 llm-wiki-agent、llm-wiki-skill、graphify 的设计思路，工具无 API Key。知识库根目录为仓库内 llm-wiki/。
---

# LLM Wiki

## 知识库根目录

**`llm-wiki/`**（与仓库根相对路径；也可单独拷贝本目录对外开源）

## 会话开始必读

1. `llm-wiki/CLAUDE.md`
2. `llm-wiki/taxonomy.md`
3. `llm-wiki/wiki/index.md` 与 `wiki/overview.md`

**按任务追加**：Collect → `llm-wiki/skills/collect/SKILL.md` + `llm-wiki/tools/source_registry.tsv`；写成稿 → `llm-wiki/skills/wiki-writing/SKILL.md` + `llm-wiki/skills/humanizer-zh/SKILL.md`

## 环境变量

```bash
export WIKI_ROOT="$PWD/llm-wiki"
```

## 工具命令

```bash
pip install -r llm-wiki/requirements.txt
bash llm-wiki/tools/check_all.sh "$WIKI_ROOT"
python3 llm-wiki/tools/build_graph.py --wiki-root "$WIKI_ROOT"
```

## 上游理念来源

- [llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) — wiki 分层、ingest / query / lint / graph
- [llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) — 来源类型表 `tools/source_registry.tsv`
- [graphify](https://github.com/safishamsi/graphify) — 图与社区视角（本实现为轻量 deterministic 子集）

## 与用户约定的流程

- **Collect**：Agent 检索 → `sessions/.../candidates.md` → **用户确认** → 写入 `raw/<门类>/…` → **ingest**
- **Taxonomy**：新建/合并/重命名/删除门类目录前 **必须用户明确同意**
- **路径即分类**：`raw/<shelf>/…` 与 `wiki/<shelf>/…` 对齐
